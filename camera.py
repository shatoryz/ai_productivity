import cv2
import math
import time
import threading
import numpy as np
from PyQt6.QtCore import pyqtSignal, QObject, QThread
import mediapipe as mp


class CamSignals(QObject):
    frame_ready = pyqtSignal(object)
    status_ready = pyqtSignal(float, str, dict, float)


class CamThread(QThread):
    def __init__(self, camera_index=0):
        super().__init__()
        self.running = True
        self._lock = threading.Lock()
        self._sleepiness = 0.0
        self._energy = 1.0
        self._emotion = 'neutral'
        self._emotion_probs = {'neutral': 1.0}
        self._blink_count = 0
        self._head_angle = 0.0
        self.camera_index = camera_index
        self.cap = None
        self.signals = CamSignals()
        self.face_mesh = mp.solutions.face_mesh.FaceMesh(refine_landmarks=True)
        self.mp_draw = mp.solutions.drawing_utils
        self.left_eye_idx = [263, 385, 387, 362, 373, 380]
        self.right_eye_idx = [133, 160, 158, 33, 153, 144]
        self.ear_threshold = 0.10
        self.max_closed_duration = 2.0
        self.closed_eyes_start_time = None
        self._ear_history = []
        self._ear_history_max = 30
        self._init_emotion_model()

    def _init_emotion_model(self):
        self.compiled_model = None
        self.emotion_labels = ['neutral', 'happy', 'sad', 'surprise', 'anger']
        try:
            from openvino.runtime import Core
            ie = Core()
            model_path = "models/emotions-recognition-retail-0003.xml"
            import os
            if os.path.exists(model_path):
                model = ie.read_model(model_path)
                self.compiled_model = ie.compile_model(model, "CPU")
        except Exception as e:
            print(f'OpenVINO init error: {e}')
        self.face_cascade = cv2.CascadeClassifier(
            cv2.data.haarcascades + 'haarcascade_frontalface_default.xml'
        )

    def _detect_emotion(self, frame, faces):
        emotion_probs = {'neutral': 1.0}
        emotion = 'neutral'
        if self.compiled_model is None or len(faces) == 0:
            return emotion, emotion_probs
        try:
            x, y, w, h = faces[0]
            face = cv2.resize(frame[y:y + h, x:x + w], (64, 64))
            blob = np.transpose(face, (2, 0, 1)).reshape(1, 3, 64, 64).astype(np.float32)
            output_layer = self.compiled_model.output(0)
            emotion_res = self.compiled_model(blob)[output_layer]
            emotion_idx = int(np.argmax(emotion_res))
            emotion = self.emotion_labels[emotion_idx] if emotion_idx < len(self.emotion_labels) else 'neutral'
            emotion_probs = {label: 0.0 for label in self.emotion_labels}
            for i, prob in enumerate(emotion_res[0]):
                if i < len(self.emotion_labels):
                    emotion_probs[self.emotion_labels[i]] = float(prob)
            total = sum(emotion_probs.values())
            if total > 0:
                emotion_probs = {k: v / total for k, v in emotion_probs.items()}
        except Exception as e:
            print(f'Emotion detection error: {e}')
        return emotion, emotion_probs

    def _distance(self, p1, p2):
        return math.hypot(p1[0] - p2[0], p1[1] - p2[1])

    def _compute_ear(self, eye_points):
        if len(eye_points) < 6:
            return 0.0
        p1, p2, p3, p4, p5, p6 = eye_points
        return (self._distance(p2, p6) + self._distance(p3, p5)) / (2.0 * self._distance(p1, p4))

    def _calculate_energy(self, avg_ear):
        self._ear_history.append(avg_ear)
        if len(self._ear_history) > self._ear_history_max:
            self._ear_history.pop(0)
        smoothed_ear = sum(self._ear_history) / len(self._ear_history)
        ear_min = 0.15
        ear_max = 0.35
        energy = (smoothed_ear - ear_min) / (ear_max - ear_min)
        energy = max(0.0, min(1.0, energy))
        energy = 0.7 * energy + 0.3 * self._energy
        return energy

    def get_sleepiness(self):
        with self._lock:
            return self._sleepiness if self._sleepiness is not None else 0.0

    def get_energy(self):
        with self._lock:
            return self._energy if self._energy is not None else 1.0

    def get_emotion(self):
        with self._lock:
            return self._emotion if self._emotion is not None else 'neutral'

    def get_emotion_probs(self):
        with self._lock:
            return self._emotion_probs.copy() if self._emotion_probs else {'neutral': 1.0}

    def get_blink_count(self):
        with self._lock:
            return self._blink_count if self._blink_count is not None else 0

    def get_head_angle(self):
        with self._lock:
            return self._head_angle if self._head_angle is not None else 0.0

    def _init_camera(self):
        self.cap = cv2.VideoCapture(self.camera_index)
        self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
        self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)
        time.sleep(0.5)

    def _cleanup(self):
        if self.cap:
            self.cap.release()
            self.cap = None
        if self.face_mesh:
            self.face_mesh.close()

    def run(self):
        self._init_camera()
        while self.running:
            if self.cap is None or not self.cap.isOpened():
                time.sleep(0.1)
                continue
            ret, frame = self.cap.read()
            if not ret:
                time.sleep(0.01)
                continue
            rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            sleepiness = 0.0
            energy = 1.0
            emotion = 'neutral'
            emotion_probs = {'neutral': 1.0}

            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            faces = self.face_cascade.detectMultiScale(gray, 1.1, 5) if self.face_cascade is not None else []
            if len(faces) > 0:
                emotion, emotion_probs = self._detect_emotion(frame, faces)

            results = self.face_mesh.process(rgb)
            if results.multi_face_landmarks:
                for face_landmarks in results.multi_face_landmarks:
                    h, w, _ = frame.shape
                    left_eye_points = [
                        (int(face_landmarks.landmark[idx].x * w),
                         int(face_landmarks.landmark[idx].y * h))
                        for idx in self.left_eye_idx
                    ]
                    left_eye_ear = self._compute_ear(left_eye_points)
                    right_eye_points = [
                        (int(face_landmarks.landmark[idx].x * w),
                         int(face_landmarks.landmark[idx].y * h))
                        for idx in self.right_eye_idx
                    ]
                    right_eye_ear = self._compute_ear(right_eye_points)

                    if left_eye_ear <= self.ear_threshold and right_eye_ear <= self.ear_threshold:
                        if self.closed_eyes_start_time is None:
                            self.closed_eyes_start_time = time.time()
                        closed_duration = time.time() - self.closed_eyes_start_time
                        if closed_duration >= self.max_closed_duration:
                            with self._lock:
                                self._blink_count += 1
                            self.closed_eyes_start_time = None
                    else:
                        self.closed_eyes_start_time = None

                    avg_ear = (left_eye_ear + right_eye_ear) / 2.0
                    sleepiness = max(0.0, min(1.0, 1.0 - (avg_ear / 0.3)))
                    energy = self._calculate_energy(avg_ear)

            with self._lock:
                self._sleepiness = sleepiness
                self._energy = energy
                self._emotion = emotion
                self._emotion_probs = emotion_probs

            frame_copy = rgb.copy()
            self.signals.frame_ready.emit(frame_copy)
            self.signals.status_ready.emit(sleepiness, emotion, emotion_probs, energy)
            time.sleep(0.03)
        self._cleanup()