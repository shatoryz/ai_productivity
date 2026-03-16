import datetime
from PyQt6.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QFormLayout, QGroupBox,
    QLabel, QLineEdit, QComboBox, QTimeEdit, QSlider, QPushButton,
    QTableWidget, QTableWidgetItem, QHeaderView, QSpinBox, QDialogButtonBox,
    QWidget, QMessageBox
)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QIcon, QFont
from styles import get_current_theme
from utils import validate_time_interval


class AddActivityDialog(QDialog):
    def __init__(self, parent=None, selected_date=None):
        super().__init__(parent)
        self.selected_date = selected_date
        self.setWindowTitle('Add Activity')
        self.setMinimumSize(500, 650)
        self.setStyleSheet(get_current_theme())
        layout = QVBoxLayout(self)
        layout.setSpacing(15)
        title = QLabel('Create New Activity')
        title.setStyleSheet('font-size: 20px; font-weight: bold; color: #58a6ff;')
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(title)
        form_layout = QFormLayout()
        form_layout.setSpacing(12)
        self.name_inp = QLineEdit()
        self.name_inp.setPlaceholderText('e.g., Deep Work Session')
        form_layout.addRow('Activity Name:', self.name_inp)
        self.cat_box = QComboBox()
        self.cat_box.addItems(['Mental', 'Physical', 'Creative', 'Break', 'Learning'])
        form_layout.addRow('Category:', self.cat_box)
        self.start_time = QTimeEdit()
        self.start_time.setTime(datetime.datetime.now().time())
        self.start_time.setDisplayFormat('HH:mm')
        form_layout.addRow('Start Time:', self.start_time)
        self.end_time = QTimeEdit()
        end_time = datetime.datetime.now() + datetime.timedelta(minutes=60)
        self.end_time.setTime(end_time.time())
        self.end_time.setDisplayFormat('HH:mm')
        form_layout.addRow('End Time:', self.end_time)
        self.dur_lbl = QLabel('Duration: 60 minutes')
        form_layout.addRow(self.dur_lbl)
        layout.addLayout(form_layout)
        self.start_time.timeChanged.connect(self.update_duration)
        self.end_time.timeChanged.connect(self.update_duration)
        coeff_group = QGroupBox('Task Coefficients')
        coeff_group.setObjectName('settingsCard')
        coeff_layout = QVBoxLayout(coeff_group)
        self.diff_slider = QSlider(Qt.Orientation.Horizontal)
        self.diff_slider.setRange(1, 10)
        self.diff_slider.setValue(5)
        self.diff_lbl = QLabel('Difficulty: Medium (5/10)')
        self.diff_slider.valueChanged.connect(
            lambda v: self.diff_lbl.setText(f'Difficulty: {self._diff_label(v)} ({v}/10)')
        )
        coeff_layout.addWidget(self.diff_slider)
        coeff_layout.addWidget(self.diff_lbl)
        self.prio_slider = QSlider(Qt.Orientation.Horizontal)
        self.prio_slider.setRange(1, 10)
        self.prio_slider.setValue(7)
        self.prio_lbl = QLabel('Priority: High (7/10)')
        self.prio_slider.valueChanged.connect(
            lambda v: self.prio_lbl.setText(f'Priority: {self._prio_label(v)} ({v}/10)')
        )
        coeff_layout.addWidget(self.prio_slider)
        coeff_layout.addWidget(self.prio_lbl)
        layout.addWidget(coeff_group)
        button_layout = QHBoxLayout()
        self.cancel_btn = QPushButton('Cancel')
        self.cancel_btn.setObjectName('secondaryButton')
        self.cancel_btn.setMinimumWidth(140)
        self.cancel_btn.setMinimumHeight(48)
        self.cancel_btn.clicked.connect(self.reject)
        button_layout.addWidget(self.cancel_btn)
        self.add_btn = QPushButton('Add Activity')
        self.add_btn.setObjectName('addButton')
        self.add_btn.setMinimumWidth(180)
        self.add_btn.setMinimumHeight(48)
        self.add_btn.clicked.connect(self.validate_and_accept)
        button_layout.addWidget(self.add_btn)
        layout.addLayout(button_layout)

    def _diff_label(self, v):
        labels = {1: 'Very Easy', 5: 'Medium', 10: 'Extreme'}
        return labels.get(v, 'Medium')

    def _prio_label(self, v):
        labels = {1: 'Lowest', 5: 'Medium', 10: 'Critical'}
        return labels.get(v, 'High')

    def update_duration(self):
        start = self.start_time.time()
        end = self.end_time.time()
        start_mins = start.hour() * 60 + start.minute()
        end_mins = end.hour() * 60 + end.minute()
        if end_mins < start_mins:
            end_mins += 24 * 60
        duration = end_mins - start_mins
        self.dur_lbl.setText(f'Duration: {duration} minutes')

    def validate_and_accept(self):
        start_time = self.start_time.time().toString('HH:mm')
        end_time = self.end_time.time().toString('HH:mm')
        is_valid, message = validate_time_interval(start_time, end_time)
        if not is_valid:
            QMessageBox.warning(self, 'Invalid Time', message)
            return
        if not self.name_inp.text().strip():
            QMessageBox.warning(self, 'Error', 'Activity name is required')
            return
        self.accept()

    def get_data(self):
        category_map = {'Mental': 'mental', 'Physical': 'physical', 'Creative': 'creative',
                        'Break': 'break', 'Learning': 'learning'}
        start = self.start_time.time()
        end = self.end_time.time()
        date = self.selected_date if self.selected_date else datetime.datetime.now().strftime('%Y-%m-%d')
        start_mins = start.hour() * 60 + start.minute()
        end_mins = end.hour() * 60 + end.minute()
        if end_mins < start_mins:
            end_mins += 24 * 60
        return {
            'activity': self.name_inp.text().strip(),
            'category': category_map.get(self.cat_box.currentText(), 'mental'),
            'scheduled_date': date,
            'start_time': start.toString('HH:mm'),
            'end_time': end.toString('HH:mm'),
            'difficulty': self.diff_slider.value() / 10.0,
            'priority': self.prio_slider.value() / 10.0,
            'estimated_duration': end_mins - start_mins
        }


class CoefficientsDialog(QDialog):
    def __init__(self, parent=None, coefficients=None):
        super().__init__(parent)
        self.coefficients = coefficients or self._default_coeffs()
        self.setWindowTitle('Recommendation Coefficients')
        self.setMinimumSize(500, 600)
        self.setStyleSheet(get_current_theme())
        layout = QVBoxLayout(self)
        layout.setSpacing(15)
        title = QLabel('Customize Recommendation Weights')
        title.setStyleSheet('font-size: 20px; font-weight: bold; color: #58a6ff;')
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(title)
        form_layout = QFormLayout()
        form_layout.setSpacing(15)
        self.s_slider = QSlider(Qt.Orientation.Horizontal)
        self.s_slider.setRange(0, 100)
        self.s_slider.setValue(int(self.coefficients['w_S'] * 100))
        self.s_lbl = QLabel(f'Energy (S): {self.coefficients["w_S"]:.2f}')
        self.s_slider.valueChanged.connect(lambda v: self.s_lbl.setText(f'Energy (S): {v / 100:.2f}'))
        form_layout.addRow(self.s_slider, self.s_lbl)
        self.e_slider = QSlider(Qt.Orientation.Horizontal)
        self.e_slider.setRange(0, 100)
        self.e_slider.setValue(int(self.coefficients['w_E'] * 100))
        self.e_lbl = QLabel(f'Emotion (E): {self.coefficients["w_E"]:.2f}')
        self.e_slider.valueChanged.connect(lambda v: self.e_lbl.setText(f'Emotion (E): {v / 100:.2f}'))
        form_layout.addRow(self.e_slider, self.e_lbl)
        self.p_slider = QSlider(Qt.Orientation.Horizontal)
        self.p_slider.setRange(0, 100)
        self.p_slider.setValue(int(self.coefficients['w_P'] * 100))
        self.p_lbl = QLabel(f'Time (P): {self.coefficients["w_P"]:.2f}')
        self.p_slider.valueChanged.connect(lambda v: self.p_lbl.setText(f'Time (P): {v / 100:.2f}'))
        form_layout.addRow(self.p_slider, self.p_lbl)
        self.c_slider = QSlider(Qt.Orientation.Horizontal)
        self.c_slider.setRange(0, 100)
        self.c_slider.setValue(int(self.coefficients['w_C'] * 100))
        self.c_lbl = QLabel(f'Capacity (C): {self.coefficients["w_C"]:.2f}')
        self.c_slider.valueChanged.connect(lambda v: self.c_lbl.setText(f'Capacity (C): {v / 100:.2f}'))
        form_layout.addRow(self.c_slider, self.c_lbl)
        layout.addLayout(form_layout)
        self.total_lbl = QLabel('Total: 1.00')
        self.total_lbl.setStyleSheet('font-size: 16px; font-weight: bold; color: #58a6ff;')
        self.total_lbl.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.total_lbl)
        self.s_slider.valueChanged.connect(self.update_total)
        self.e_slider.valueChanged.connect(self.update_total)
        self.p_slider.valueChanged.connect(self.update_total)
        self.c_slider.valueChanged.connect(self.update_total)
        button_layout = QHBoxLayout()
        self.reset_btn = QPushButton('Reset')
        self.reset_btn.setObjectName('secondaryButton')
        self.reset_btn.setMinimumWidth(140)
        self.reset_btn.setMinimumHeight(48)
        self.reset_btn.clicked.connect(self.reset_defaults)
        button_layout.addWidget(self.reset_btn)
        self.save_btn = QPushButton('Save')
        self.save_btn.setObjectName('saveButton')
        self.save_btn.setMinimumWidth(140)
        self.save_btn.setMinimumHeight(48)
        self.save_btn.clicked.connect(self.accept)
        button_layout.addWidget(self.save_btn)
        layout.addLayout(button_layout)
        self.update_total()

    def _default_coeffs(self):
        return {'w_S': 0.40, 'w_E': 0.30, 'w_P': 0.20, 'w_C': 0.10}

    def update_total(self):
        total = (self.s_slider.value() + self.e_slider.value() +
                 self.p_slider.value() + self.c_slider.value()) / 100.0
        self.total_lbl.setText(f'Total: {total:.2f}')
        if abs(total - 1.0) > 0.01:
            self.total_lbl.setStyleSheet('font-size: 16px; font-weight: bold; color: #f85149;')
        else:
            self.total_lbl.setStyleSheet('font-size: 16px; font-weight: bold; color: #3fb950;')

    def reset_defaults(self):
        defaults = self._default_coeffs()
        self.s_slider.setValue(int(defaults['w_S'] * 100))
        self.e_slider.setValue(int(defaults['w_E'] * 100))
        self.p_slider.setValue(int(defaults['w_P'] * 100))
        self.c_slider.setValue(int(defaults['w_C'] * 100))
        self.update_total()

    def get_coefficients(self):
        return {
            'w_S': self.s_slider.value() / 100.0,
            'w_E': self.e_slider.value() / 100.0,
            'w_P': self.p_slider.value() / 100.0,
            'w_C': self.c_slider.value() / 100.0
        }


class TimeInputDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.planned_time = 30
        self.setWindowTitle('Plan Your Session')
        self.setMinimumSize(400, 250)
        self.setStyleSheet(get_current_theme())
        layout = QVBoxLayout(self)
        layout.setSpacing(15)
        title = QLabel('How much time do you want to spend?')
        title.setStyleSheet('font-size: 18px; font-weight: bold; color: #58a6ff;')
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(title)
        layout.addSpacing(10)
        time_layout = QHBoxLayout()
        time_layout.addWidget(QLabel('Time (minutes):'))
        self.time_spin = QSpinBox()
        self.time_spin.setRange(5, 180)
        self.time_spin.setValue(30)
        self.time_spin.setStyleSheet('font-size: 16px; padding: 8px;')
        time_layout.addWidget(self.time_spin)
        layout.addSpacing(20)
        button_box = QDialogButtonBox(
            QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel
        )
        button_box.button(QDialogButtonBox.StandardButton.Ok).setObjectName('loginButton')
        button_box.button(QDialogButtonBox.StandardButton.Ok).setMinimumWidth(120)
        button_box.button(QDialogButtonBox.StandardButton.Ok).setMinimumHeight(48)
        button_box.button(QDialogButtonBox.StandardButton.Cancel).setObjectName('secondaryButton')
        button_box.button(QDialogButtonBox.StandardButton.Cancel).setMinimumWidth(120)
        button_box.button(QDialogButtonBox.StandardButton.Cancel).setMinimumHeight(48)
        button_box.accepted.connect(self.accept)
        button_box.rejected.connect(self.reject)
        layout.addWidget(button_box)

    def get_time(self):
        if self.exec() == QDialog.DialogCode.Accepted:
            self.planned_time = self.time_spin.value()
            return self.planned_time
        return None


class ActivitySelectDialog(QDialog):
    def __init__(self, parent=None, activities=None):
        super().__init__(parent)
        self.activities = activities or []
        self.selected_activity = None
        self.setWindowTitle('Select Activity')
        self.setMinimumSize(600, 500)
        self.setStyleSheet(get_current_theme())
        layout = QVBoxLayout(self)
        layout.setSpacing(15)
        title = QLabel('Choose an Activity from Your Schedule')
        title.setStyleSheet('font-size: 20px; font-weight: bold; color: #58a6ff;')
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(title)
        self.activity_table = QTableWidget()
        self.activity_table.setColumnCount(5)
        self.activity_table.setHorizontalHeaderLabels(['Activity', 'Category', 'Start', 'End', ''])
        header = self.activity_table.horizontalHeader()
        header.setSectionResizeMode(0, QHeaderView.ResizeMode.Stretch)
        header.setSectionResizeMode(4, QHeaderView.ResizeMode.Fixed)
        header.resizeSection(4, 100)  # Ширина колонки для галочки
        self.activity_table.setAlternatingRowColors(True)
        for i, act in enumerate(self.activities):
            r = self.activity_table.rowCount()
            self.activity_table.insertRow(r)
            self.activity_table.setItem(r, 0, QTableWidgetItem(act.get('activity', 'Unknown')))
            self.activity_table.setItem(r, 1, QTableWidgetItem(act.get('category', 'mental')))
            self.activity_table.setItem(r, 2, QTableWidgetItem(act.get('start_time', '00:00')))
            self.activity_table.setItem(r, 3, QTableWidgetItem(act.get('end_time', '00:00')))

            select_btn = QPushButton('✓')
            select_btn.setObjectName('selectButton')
            select_btn.setFixedSize(60, 40)
            select_btn.setCursor(Qt.CursorShape.PointingHandCursor)
            select_btn.setToolTip('Select this activity')
            select_btn.setStyleSheet('''
                QPushButton#selectButton {
                    background: qlineargradient(x1:0, y1:0, x2:0, y2:1, stop:0 #1f6feb, stop:1 #388bfd);
                    color: #ffffff;
                    border: none;
                    border-radius: 8px;
                    font-size: 20px;
                    font-weight: bold;
                    padding: 0px;
                }
                QPushButton#selectButton:hover {
                    background: qlineargradient(x1:0, y1:0, x2:0, y2:1, stop:0 #388bfd, stop:1 #58a6ff);
                }
            ''')
            select_btn.clicked.connect(lambda checked, a=act: self.select_activity(a))

            cell_widget = QWidget()
            cell_layout = QHBoxLayout(cell_widget)
            cell_layout.setContentsMargins(0, 0, 0, 0)
            cell_layout.setSpacing(0)
            cell_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
            cell_layout.addWidget(select_btn)
            cell_widget.setLayout(cell_layout)
            self.activity_table.setCellWidget(r, 4, cell_widget)
            self.activity_table.setRowHeight(r, 55)
        layout.addWidget(self.activity_table)
        cancel_btn = QPushButton('Cancel')
        cancel_btn.setObjectName('secondaryButton')
        cancel_btn.setMinimumWidth(140)
        cancel_btn.setMinimumHeight(48)
        cancel_btn.clicked.connect(self.reject)
        layout.addWidget(cancel_btn)

    def select_activity(self, activity):
        self.selected_activity = activity
        self.accept()

    def get_selected_activity(self):
        return self.selected_activity


class FeedbackDialog(QDialog):
    def __init__(self, parent=None, activity_name=''):
        super().__init__(parent)
        self.activity_name = activity_name
        self.feedback = 0
        self.setWindowTitle('Feedback')
        self.setMinimumSize(400, 300)
        self.setStyleSheet(get_current_theme())
        layout = QVBoxLayout(self)
        layout.setSpacing(15)
        title = QLabel(f'How did it go: {activity_name}?')
        title.setStyleSheet('font-size: 18px; font-weight: bold; color: #58a6ff;')
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(title)
        layout.addSpacing(20)
        btn_layout = QHBoxLayout()
        btn_layout.setSpacing(20)
        self.good_btn = QPushButton('😊 Great')
        self.good_btn.setObjectName('startButton')
        self.good_btn.setMinimumWidth(100)
        self.good_btn.setMinimumHeight(60)
        self.good_btn.setStyleSheet('font-size: 16px;')
        self.good_btn.clicked.connect(lambda: self.finish(1))
        btn_layout.addWidget(self.good_btn)
        self.ok_btn = QPushButton('😐 OK')
        self.ok_btn.setObjectName('secondaryButton')
        self.ok_btn.setMinimumWidth(100)
        self.ok_btn.setMinimumHeight(60)
        self.ok_btn.setStyleSheet('font-size: 16px;')
        self.ok_btn.clicked.connect(lambda: self.finish(0))
        btn_layout.addWidget(self.ok_btn)
        self.bad_btn = QPushButton('😞 Poor')
        self.bad_btn.setObjectName('stopButton')
        self.bad_btn.setMinimumWidth(100)
        self.bad_btn.setMinimumHeight(60)
        self.bad_btn.setStyleSheet('font-size: 16px;')
        self.bad_btn.clicked.connect(lambda: self.finish(-1))
        btn_layout.addWidget(self.bad_btn)
        layout.addLayout(btn_layout)
        self.comment_inp = QLineEdit()
        self.comment_inp.setPlaceholderText('Optional comment...')
        self.comment_inp.setMinimumHeight(48)
        layout.addWidget(self.comment_inp)
        layout.addStretch()

    def finish(self, value):
        self.feedback = value
        self.accept()

    def exec(self):
        super().exec()
        return self.feedback

    def get_feedback(self):
        return self.feedback
