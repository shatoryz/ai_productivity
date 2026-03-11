import datetime
import time
from PyQt6.QtWidgets import (
    QWidget, QMainWindow, QVBoxLayout, QHBoxLayout, QLabel,
    QLineEdit, QPushButton, QFrame, QTableWidget, QTableWidgetItem,
    QHeaderView, QTabWidget, QCalendarWidget, QProgressBar,
    QMessageBox, QComboBox, QDialog, QSizePolicy, QScrollArea
)
from PyQt6.QtCore import QTimer, Qt, QObject, pyqtSignal, QSize
from PyQt6.QtGui import QImage, QPixmap, QIcon
from styles import get_current_theme, toggle_theme, get_theme_colors, is_dark
from database import db
from camera import CamThread
from engine import Engine
from charts import Chart
from dialogs import AddActivityDialog, CoefficientsDialog, TimeInputDialog, ActivitySelectDialog, FeedbackDialog
from utils import format_time, safe_format, safe_get, get_available_cameras


class ActivityTimer(QObject):
    tick = pyqtSignal(int)

    def __init__(self):
        super().__init__()
        self.running = False
        self.start_time = 0
        self.elapsed = 0
        self.timer = QTimer()
        self.timer.timeout.connect(self._update)

    def start(self, activity, category):
        self.start_time = time.time()
        self.elapsed = 0
        self.running = True
        self.timer.start(1000)

    def stop(self):
        self.running = False
        self.timer.stop()
        return self.elapsed

    def _update(self):
        if self.running:
            self.elapsed = time.time() - self.start_time
            self.tick.emit(int(self.elapsed))


class RegisterWindow(QWidget):
    def __init__(self, login_callback=None):
        super().__init__()
        self.login_callback = login_callback
        self.setWindowTitle('Register')
        self.setMinimumSize(550, 750)
        self.setStyleSheet(get_current_theme())
        main_layout = QVBoxLayout(self)
        main_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        auth_card = QFrame()
        auth_card.setObjectName('authCard')
        card_layout = QVBoxLayout(auth_card)
        card_layout.setSpacing(16)
        title = QLabel('Create Account')
        title.setObjectName('authTitle')
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        card_layout.addWidget(title)
        subtitle = QLabel('Join our productivity community')
        subtitle.setObjectName('authSubtitle')
        subtitle.setAlignment(Qt.AlignmentFlag.AlignCenter)
        card_layout.addWidget(subtitle)
        card_layout.addSpacing(15)
        self.username_inp = QLineEdit()
        self.username_inp.setPlaceholderText('Username')
        card_layout.addWidget(self.username_inp)
        pass_layout = QHBoxLayout()
        self.password_inp = QLineEdit()
        self.password_inp.setPlaceholderText('Password')
        self.password_inp.setEchoMode(QLineEdit.EchoMode.Password)
        pass_layout.addWidget(self.password_inp)
        self.eye_btn1 = QPushButton('')
        self.eye_btn1.setObjectName('eyeButton')
        self.eye_btn1.setCheckable(True)
        self.eye_btn1.setFixedSize(45, 45)
        icon_open = QIcon('images/pug.png')
        self.eye_btn1.setIcon(icon_open)
        self.eye_btn1.setIconSize(QSize(45, 45))
        self.eye_btn1.clicked.connect(lambda: self.toggle_password(self.password_inp, self.eye_btn1))
        pass_layout.addWidget(self.eye_btn1)
        card_layout.addLayout(pass_layout)
        confirm_layout = QHBoxLayout()
        self.confirm_password_inp = QLineEdit()
        self.confirm_password_inp.setPlaceholderText('Confirm Password')
        self.confirm_password_inp.setEchoMode(QLineEdit.EchoMode.Password)
        confirm_layout.addWidget(self.confirm_password_inp)
        self.eye_btn2 = QPushButton('')
        self.eye_btn2.setObjectName('eyeButton')
        self.eye_btn2.setCheckable(True)
        self.eye_btn2.setFixedSize(45, 45)
        icon_open2 = QIcon('images/pug.png')
        self.eye_btn2.setIcon(icon_open2)
        self.eye_btn2.setIconSize(QSize(45, 45))
        self.eye_btn2.clicked.connect(lambda: self.toggle_password(self.confirm_password_inp, self.eye_btn2))
        confirm_layout.addWidget(self.eye_btn2)
        card_layout.addLayout(confirm_layout)
        self.strength_bar = QProgressBar()
        self.strength_bar.setRange(0, 100)
        self.strength_bar.setValue(0)
        card_layout.addWidget(self.strength_bar)
        self.strength_lbl = QLabel('Password Strength: None')
        self.strength_lbl.setObjectName('passwordStrength')
        self.strength_lbl.setAlignment(Qt.AlignmentFlag.AlignCenter)
        card_layout.addWidget(self.strength_lbl)
        self.password_inp.textChanged.connect(self.update_password_strength)
        card_layout.addSpacing(10)
        self.register_btn = QPushButton('Register')
        self.register_btn.setObjectName('registerButton')
        self.register_btn.clicked.connect(self.register_user)
        card_layout.addWidget(self.register_btn)
        self.back_btn = QPushButton('Back to Login')
        self.back_btn.setObjectName('secondaryButton')
        self.back_btn.clicked.connect(self.go_back)
        # Исправление размеров кнопки Back to Login
        self.back_btn.setMinimumWidth(280)
        self.back_btn.setMinimumHeight(52)
        self.back_btn.setStyleSheet('font-size: 16px; padding: 14px 24px;')
        card_layout.addWidget(self.back_btn)
        main_layout.addWidget(auth_card)

    def toggle_password(self, line_edit, button):
        if button.isChecked():
            line_edit.setEchoMode(QLineEdit.EchoMode.Normal)
            button.setIcon(QIcon('images/pug_closed_eyes.png'))
        else:
            line_edit.setEchoMode(QLineEdit.EchoMode.Password)
            button.setIcon(QIcon('images/pug.png'))

    def update_password_strength(self):
        from utils import get_password_strength
        password = self.password_inp.text()
        strength, color = get_password_strength(password)
        if strength == 'weak':
            self.strength_bar.setValue(33)
            self.strength_lbl.setText('Password Strength: Weak')
        elif strength == 'medium':
            self.strength_bar.setValue(66)
            self.strength_lbl.setText('Password Strength: Medium')
        else:
            self.strength_bar.setValue(100)
            self.strength_lbl.setText('Password Strength: Strong')
        self.strength_lbl.setStyleSheet(f'color: {color}; font-size: 12px; font-weight: 600;')
        colors = get_theme_colors()
        self.strength_bar.setStyleSheet(f'''
            QProgressBar {{
                background-color: {colors['bg_tertiary']};
                border-radius: 4px;
                height: 8px;
                border: none;
            }}
            QProgressBar::chunk {{
                background-color: {color};
                border-radius: 4px;
            }}
        ''')

    def register_user(self):
        username = self.username_inp.text().strip()
        password = self.password_inp.text()
        confirm = self.confirm_password_inp.text()
        if not username or len(username) < 3:
            QMessageBox.warning(self, 'Error', 'Username must be at least 3 characters')
            return
        if password != confirm:
            QMessageBox.warning(self, 'Error', 'Passwords do not match')
            return
        from utils import validate_password
        errors = validate_password(password)
        if errors:
            QMessageBox.warning(self, 'Weak Password', '\n'.join(errors))
            return
        conn = db.get_connection()
        cur = conn.cursor()
        cur.execute('INSERT INTO users(username, password) VALUES(?,?)', (username, password))
        conn.commit()
        conn.close()
        QMessageBox.information(self, 'Success', 'Registration successful!\nYou can now login.')
        self.go_back()

    def go_back(self):
        if self.login_callback:
            self.login_callback()
        self.close()


class LoginWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Login')
        self.setMinimumSize(500, 650)
        self.setStyleSheet(get_current_theme())
        main_layout = QVBoxLayout(self)
        main_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        auth_card = QFrame()
        auth_card.setObjectName('authCard')
        card_layout = QVBoxLayout(auth_card)
        card_layout.setSpacing(20)
        title = QLabel('PugRitm')
        title.setObjectName('authTitle')
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        card_layout.addWidget(title)
        subtitle = QLabel('Sign in to continue your journey')
        subtitle.setObjectName('authSubtitle')
        subtitle.setAlignment(Qt.AlignmentFlag.AlignCenter)
        card_layout.addWidget(subtitle)
        card_layout.addSpacing(15)
        camera_container = QHBoxLayout()
        camera_container.addWidget(QLabel('Camera:'))
        self.cam_box = QComboBox()
        for cam in get_available_cameras():
            self.cam_box.addItem(f'Camera {cam}', cam)
        camera_container.addWidget(self.cam_box)
        card_layout.addLayout(camera_container)
        self.username_inp = QLineEdit()
        self.username_inp.setPlaceholderText('Username')
        card_layout.addWidget(self.username_inp)
        pass_layout = QHBoxLayout()
        self.password_inp = QLineEdit()
        self.password_inp.setPlaceholderText('Password')
        self.password_inp.setEchoMode(QLineEdit.EchoMode.Password)
        pass_layout.addWidget(self.password_inp)
        self.eye_btn = QPushButton('')
        self.eye_btn.setObjectName('eyeButton')
        self.eye_btn.setCheckable(True)
        self.eye_btn.setFixedSize(45, 45)
        icon_open = QIcon('images/pug.png')
        self.eye_btn.setIcon(icon_open)
        self.eye_btn.setIconSize(QSize(45, 45))
        self.eye_btn.clicked.connect(self.toggle_password)
        pass_layout.addWidget(self.eye_btn)
        card_layout.addLayout(pass_layout)
        card_layout.addSpacing(10)
        self.login_btn = QPushButton('Sign In')
        self.login_btn.setObjectName('loginButton')
        self.login_btn.clicked.connect(self.login)
        card_layout.addWidget(self.login_btn)
        self.reg_btn = QPushButton('Create Account')
        self.reg_btn.setObjectName('secondaryButton')
        self.reg_btn.clicked.connect(self.open_register)
        # Исправление размеров кнопки Create Account
        self.reg_btn.setMinimumWidth(280)
        self.reg_btn.setMinimumHeight(52)
        self.reg_btn.setStyleSheet('font-size: 16px; padding: 14px 24px;')
        card_layout.addWidget(self.reg_btn)
        main_layout.addWidget(auth_card)

    def toggle_password(self):
        if self.eye_btn.isChecked():
            self.password_inp.setEchoMode(QLineEdit.EchoMode.Normal)
            self.eye_btn.setIcon(QIcon('images/pug_closed_eyes.png'))
        else:
            self.password_inp.setEchoMode(QLineEdit.EchoMode.Password)
            self.eye_btn.setIcon(QIcon('images/pug.png'))

    def login(self):
        username = self.username_inp.text().strip()
        password = self.password_inp.text()
        camera_index = self.cam_box.currentData() if self.cam_box else 0
        conn = db.get_connection()
        cur = conn.cursor()
        cur.execute('SELECT * FROM users WHERE username=? AND password=?', (username, password))
        user = cur.fetchone()
        conn.close()
        if user:
            self.main_win = MainWindow(user[0], username, camera_index)
            self.main_win.show()
            self.close()
        else:
            QMessageBox.warning(self, 'Error', 'Invalid credentials\nPlease check your username and password')

    def open_register(self):
        self.reg_window = RegisterWindow(login_callback=self.show)
        self.reg_window.show()
        self.hide()


class MainWindow(QMainWindow):
    def __init__(self, user_id, username, camera_index=0):
        super().__init__()
        self.user_id = user_id
        self.username = username
        self.camera_index = camera_index
        self.engine = Engine(self.user_id, db)
        self.recommendations = []
        self.timer = ActivityTimer()
        self.timer.tick.connect(self.update_timer_display)
        self.activity_name = None
        self.activity_category = None
        self.cam_thread = None
        self.selected_date = datetime.datetime.now().strftime('%Y-%m-%d')
        self._last_update = 0
        self._session_start_time = None
        self.chart_main = None
        self.chart_session = None
        self.chart_category = None
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout(central_widget)
        main_layout.setSpacing(0)
        main_layout.setContentsMargins(20, 20, 20, 20)
        top_bar = QHBoxLayout()
        top_bar.setContentsMargins(0, 0, 0, 10)
        user_info = QLabel(f'{username}')
        user_info.setStyleSheet('font-size: 14px; font-weight: 500;')
        top_bar.addWidget(user_info)
        top_bar.addStretch()
        self.theme_btn = QPushButton('🌙' if is_dark() else '☀️')
        self.theme_btn.setObjectName('themeButton')
        self.theme_btn.setFixedSize(55, 55)
        self.theme_btn.clicked.connect(self.toggle_theme)
        top_bar.addWidget(self.theme_btn)
        main_layout.addLayout(top_bar)
        self.tab_widget = QTabWidget()
        self.tab_widget.addTab(self._create_dashboard_tab(), 'Dashboard')
        self.tab_widget.addTab(self._create_calendar_tab(), 'Calendar')
        self.tab_widget.addTab(self._create_recommendations_tab(), 'Recommendations')
        self.tab_widget.addTab(self._create_productivity_overview_tab(), 'Overview')
        self.tab_widget.addTab(self._create_productivity_charts_tab(), 'Charts')
        self.tab_widget.addTab(self._create_settings_tab(), 'Settings')
        main_layout.addWidget(self.tab_widget)
        self.setWindowTitle(f'Dashboard - {username}')
        self.setMinimumSize(1400, 850)
        self.setStyleSheet(get_current_theme())
        self.cam_thread = CamThread(camera_index=camera_index)
        self.cam_thread.signals.frame_ready.connect(self.update_video_frame)
        self.cam_thread.signals.status_ready.connect(self.update_status)
        self.cam_thread.start()
        self.load_calendar_activities()
        self.timer_update = QTimer()
        self.timer_update.timeout.connect(self.update_productivity_charts)
        self.timer_update.start(60000)
        self.timer_session = QTimer()
        self.timer_session.timeout.connect(self.update_session_productivity)
        self.timer_session.start(10000)
        QTimer.singleShot(100, self._initialize_charts)

    def _get_chart_figure(self, chart):
        if not chart:
            return None
        if hasattr(chart, 'figure'):
            return chart.figure
        elif hasattr(chart, 'fig'):
            return chart.fig
        elif hasattr(chart, 'canvas') and hasattr(chart.canvas, 'figure'):
            return chart.canvas.figure
        elif hasattr(chart, 'get_figure'):
            return chart.get_figure()
        return None

    def _initialize_charts(self):
        colors = get_theme_colors()
        for chart in [self.chart_main, self.chart_session, self.chart_category]:
            if chart:
                chart.setStyleSheet(f'''
                    QWidget {{
                        background-color: {colors['bg_secondary']};
                        color: {colors['text_primary']};
                    }}
                ''')
                figure = self._get_chart_figure(chart)
                if figure:
                    figure.patch.set_facecolor(colors['bg_secondary'])
                if hasattr(chart, 'axes') and chart.axes:
                    chart.axes.set_facecolor(colors['bg_secondary'])
                if hasattr(chart, 'draw'):
                    chart.draw()
        self.update_productivity_charts(force=True)

    def toggle_theme(self):
        toggle_theme()
        self.setStyleSheet(get_current_theme())
        self.theme_btn.setText('🌙' if is_dark() else '☀️')
        colors = get_theme_colors()
        self._safe_update_chart(self.chart_main)
        self._safe_update_chart(self.chart_session)
        self._safe_update_chart(self.chart_category)
        if hasattr(self, 'calendar') and self.calendar:
            self._update_calendar_theme()
        if hasattr(self, 'energy_bar') and self.cam_thread:
            energy = self.cam_thread.get_energy() if self.cam_thread else 1.0
            self._update_energy_display(energy)
        if hasattr(self, 'video_lbl') and self.video_lbl:
            self.video_lbl.setStyleSheet(
                f'background-color: {colors["bg_secondary"]}; border-radius: 10px; color: {colors["text_secondary"]}; font-size: 16px;')
        QTimer.singleShot(100, lambda: self.update_productivity_charts(force=True))

    def _safe_update_chart(self, chart):
        if not chart:
            return
        colors = get_theme_colors()
        chart.setStyleSheet(f'''
            QWidget {{
                background-color: {colors['bg_secondary']};
                color: {colors['text_primary']};
            }}
        ''')
        if hasattr(chart, 'axes') and chart.axes:
            chart.axes.set_facecolor(colors['bg_secondary'])
        figure = self._get_chart_figure(chart)
        if figure:
            figure.patch.set_facecolor(colors['bg_secondary'])
        if hasattr(chart, 'draw'):
            chart.draw()

    def _update_calendar_theme(self):
        colors = get_theme_colors()
        self.calendar.setStyleSheet(f'''
            QCalendarWidget {{
                background-color: {colors['bg_secondary']};
                color: {colors['text_primary']};
                border-radius: 12px;
                border: 1px solid {colors['border']};
            }}
            QCalendarWidget QToolButton {{
                background-color: {colors['bg_tertiary']};
                color: {colors['text_primary']};
                border-radius: 8px;
                padding: 10px;
                min-height: 40px;
                font-weight: 600;
            }}
            QCalendarWidget QToolButton:hover {{
                background-color: {colors['border']};
            }}
            QCalendarWidget QMenu {{
                background-color: {colors['bg_secondary']};
                color: {colors['text_primary']};
                border: 1px solid {colors['border']};
                border-radius: 8px;
            }}
            QCalendarWidget QWidget#qt_calendar_navigationbar {{
                background-color: {colors['bg_tertiary']};
                border: 1px solid {colors['border']};
                border-radius: 8px;
            }}
            QCalendarWidget QSpinBox {{
                background-color: {colors['bg_primary']};
                color: {colors['text_primary']};
                border: 1px solid {colors['border']};
                border-radius: 6px;
            }}
            QCalendarWidget QLabel {{
                color: {colors['text_primary']};
            }}
        ''')

    def _create_dashboard_tab(self):
        tab = QWidget()
        layout = QVBoxLayout(tab)
        layout.setSpacing(20)
        layout.setContentsMargins(10, 10, 10, 10)
        video_layout = QHBoxLayout()
        video_layout.setSpacing(20)
        self.video_lbl = QLabel('Camera Feed')
        self.video_lbl.setMinimumSize(640, 480)
        self.video_lbl.setAlignment(Qt.AlignmentFlag.AlignCenter)
        colors = get_theme_colors()
        self.video_lbl.setStyleSheet(
            f'background-color: {colors["bg_secondary"]}; border-radius: 10px; color: {colors["text_secondary"]}; font-size: 16px;')
        video_layout.addWidget(self.video_lbl, stretch=2)
        side_panel = QVBoxLayout()
        side_panel.setSpacing(15)
        self.status_frame = QFrame()
        self.status_frame.setObjectName('statusCard')
        status_layout = QVBoxLayout(self.status_frame)
        status_layout.setSpacing(12)
        status_title = QLabel('Status')
        status_title.setStyleSheet(f'font-size: 16px; font-weight: 600; color: {colors["accent"]};')
        status_layout.addWidget(status_title)
        self.sleep_lbl = QLabel('Sleepiness: 0.00')
        self.sleep_lbl.setObjectName('sleepinessLabel')
        status_layout.addWidget(self.sleep_lbl)
        self.emotion_lbl = QLabel('Emotion: neutral')
        self.emotion_lbl.setObjectName('emotionLabel')
        status_layout.addWidget(self.emotion_lbl)
        side_panel.addWidget(self.status_frame)
        self.energy_frame = QFrame()
        self.energy_frame.setObjectName('energyCard')
        energy_layout = QVBoxLayout(self.energy_frame)
        energy_layout.setSpacing(10)
        energy_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        energy_title = QLabel('Energy Level')
        energy_title.setStyleSheet(f'color: {colors["energy_low"]}; font-size: 16px; font-weight: 600;')
        energy_title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        energy_layout.addWidget(energy_title)
        self.energy_value_lbl = QLabel('100%')
        self.energy_value_lbl.setObjectName('energyValue')
        self.energy_value_lbl.setAlignment(Qt.AlignmentFlag.AlignCenter)
        energy_layout.addWidget(self.energy_value_lbl)
        self.energy_bar = QProgressBar()
        self.energy_bar.setRange(0, 100)
        self.energy_bar.setValue(100)
        energy_layout.addWidget(self.energy_bar)
        side_panel.addWidget(self.energy_frame)
        self.timer_frame = QFrame()
        self.timer_frame.setObjectName('timerCard')
        timer_layout = QVBoxLayout(self.timer_frame)
        timer_layout.setSpacing(15)
        timer_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        timer_title = QLabel('Timer')
        timer_title.setStyleSheet(f'font-size: 16px; font-weight: 600; color: {colors["accent"]};')
        timer_title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        timer_layout.addWidget(timer_title)
        self.timer_lbl = QLabel('00:00')
        self.timer_lbl.setStyleSheet(f'font-size: 42px; font-weight: bold; color: {colors["accent"]};')
        self.timer_lbl.setAlignment(Qt.AlignmentFlag.AlignCenter)
        timer_layout.addWidget(self.timer_lbl)
        self.timer_activity_lbl = QLabel('No active activity')
        self.timer_activity_lbl.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.timer_activity_lbl.setStyleSheet(f'color: {colors["text_secondary"]}; font-size: 14px;')
        timer_layout.addWidget(self.timer_activity_lbl)
        btn_layout = QHBoxLayout()
        btn_layout.setSpacing(10)
        self.start_timer_btn = QPushButton('Start')
        self.start_timer_btn.setObjectName('startButton')
        self.start_timer_btn.clicked.connect(self.start_activity_timer)
        btn_layout.addWidget(self.start_timer_btn)
        self.stop_timer_btn = QPushButton('Stop')
        self.stop_timer_btn.setObjectName('stopButton')
        self.stop_timer_btn.setEnabled(False)
        self.stop_timer_btn.clicked.connect(self.stop_activity_timer)
        btn_layout.addWidget(self.stop_timer_btn)
        timer_layout.addLayout(btn_layout)
        side_panel.addWidget(self.timer_frame)
        video_layout.addLayout(side_panel, stretch=1)
        layout.addLayout(video_layout)
        layout.addStretch()
        return tab

    def _create_calendar_tab(self):
        tab = QWidget()
        main_layout = QVBoxLayout(tab)
        main_layout.setSpacing(15)
        main_layout.setContentsMargins(10, 10, 10, 10)
        info_label = QLabel('Calendar - Click a date to view/manage activities')
        info_label.setStyleSheet('font-size: 16px; font-weight: bold; padding: 10px;')
        main_layout.addWidget(info_label)
        calendar_frame = QFrame()
        calendar_frame.setObjectName('statusCard')
        calendar_layout = QHBoxLayout(calendar_frame)
        self.calendar = QCalendarWidget()
        self.calendar.setMaximumHeight(300)
        calendar_layout.addWidget(self.calendar)
        day_info_frame = QFrame()
        day_info_frame.setObjectName('statusCard')
        day_info_layout = QVBoxLayout(day_info_frame)
        self.selected_day_lbl = QLabel('Selected: Today')
        self.selected_day_lbl.setStyleSheet('font-size: 18px; font-weight: bold;')
        day_info_layout.addWidget(self.selected_day_lbl)
        self.selected_date_lbl = QLabel('Date: ' + self.selected_date)
        day_info_layout.addWidget(self.selected_date_lbl)
        self.selected_day_count = QLabel('0 activities')
        day_info_layout.addWidget(self.selected_day_count)
        day_info_layout.addStretch()
        calendar_layout.addWidget(day_info_frame)
        main_layout.addWidget(calendar_frame)
        self.table_activities = QTableWidget()
        self.table_activities.setColumnCount(5)
        self.table_activities.setHorizontalHeaderLabels(['Activity', 'Category', 'Start', 'End', ''])
        header = self.table_activities.horizontalHeader()
        header.setSectionResizeMode(0, QHeaderView.ResizeMode.Stretch)
        header.setSectionResizeMode(4, QHeaderView.ResizeMode.Fixed)
        header.resizeSection(4, 60)
        self.table_activities.setAlternatingRowColors(True)
        main_layout.addWidget(self.table_activities)
        btn_layout = QHBoxLayout()
        self.add_btn = QPushButton('Add Activity')
        self.add_btn.setObjectName('addButton')
        self.add_btn.clicked.connect(self.add_calendar_activity)
        btn_layout.addWidget(self.add_btn)
        btn_layout.addStretch()
        main_layout.addLayout(btn_layout)
        self.calendar.clicked.connect(self.on_calendar_clicked)
        self._update_calendar_theme()
        return tab

    def on_calendar_clicked(self, date):
        self.selected_date = date.toString('yyyy-MM-dd')
        self.selected_date_lbl.setText(f'Date: {self.selected_date}')
        self.load_calendar_activities()

    def load_calendar_activities(self):
        if not self.selected_date:
            return
        conn = db.get_connection()
        cur = conn.cursor()
        cur.execute('''SELECT id, activity, category, start_time, end_time, difficulty, priority
            FROM schedule WHERE user_id=? AND scheduled_date=?
            ORDER BY start_time''', (self.user_id, self.selected_date))
        self.table_activities.setRowCount(0)
        count = 0
        for act in cur.fetchall():
            r = self.table_activities.rowCount()
            self.table_activities.insertRow(r)
            self.table_activities.setItem(r, 0, QTableWidgetItem(str(act[1])))
            self.table_activities.setItem(r, 1, QTableWidgetItem(str(act[2])))
            self.table_activities.setItem(r, 2, QTableWidgetItem(str(act[3])))
            self.table_activities.setItem(r, 3, QTableWidgetItem(str(act[4])))
            delete_btn = QPushButton('🗑️')
            delete_btn.setObjectName('deleteButton')
            delete_btn.setFixedSize(36, 32)
            delete_btn.setToolTip('Delete activity')
            delete_btn.clicked.connect(lambda checked, act_id=act[0]: self.delete_calendar_row(act_id))
            cell_widget = QWidget()
            layout = QHBoxLayout(cell_widget)
            layout.setContentsMargins(0, 0, 0, 0)
            layout.setSpacing(0)
            layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
            layout.addWidget(delete_btn)
            cell_widget.setLayout(layout)
            self.table_activities.setCellWidget(r, 4, cell_widget)
            self.table_activities.setRowHeight(r, 58)
            count += 1
        self.selected_day_count.setText(f'{count} activities')
        conn.close()

    def select_calendar_activity(self, act_id, activity, category):
        self.activity_name = activity
        self.activity_category = category
        self.start_activity_timer()
        QMessageBox.information(self, 'Selected', f'{activity}')

    def add_calendar_activity(self):
        if not self.selected_date:
            QMessageBox.warning(self, 'Error', 'Select a date first')
            return
        dialog = AddActivityDialog(self, selected_date=self.selected_date)
        result = dialog.exec()
        if result == QDialog.DialogCode.Accepted:
            data = dialog.get_data()
            if data and data['activity']:
                conn = db.get_connection()
                cur = conn.cursor()
                cur.execute('''INSERT INTO schedule
                    (user_id, activity, category, start_time, end_time, difficulty, priority,
                    last_time, estimated_duration, scheduled_date)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)''',
                    (self.user_id, data['activity'], data['category'],
                    data['start_time'], data['end_time'],
                    data['difficulty'], data['priority'],
                    0.0, data['estimated_duration'], self.selected_date))
                conn.commit()
                conn.close()
                self.load_calendar_activities()
                QMessageBox.information(self, 'Success', 'Activity added')

    def delete_calendar_row(self, act_id):
        conn = db.get_connection()
        cur = conn.cursor()
        cur.execute('DELETE FROM schedule WHERE id=?', (act_id,))
        conn.commit()
        conn.close()
        self.load_calendar_activities()

    def _create_recommendations_tab(self):
        tab = QWidget()
        layout = QVBoxLayout(tab)
        layout.setSpacing(15)
        layout.setContentsMargins(10, 10, 10, 10)
        btn_layout = QHBoxLayout()
        self.get_rec_btn = QPushButton('Get Smart Recommendations')
        self.get_rec_btn.setObjectName('getRecButton')
        self.get_rec_btn.clicked.connect(self.show_time_input_and_get_recommendations)
        btn_layout.addWidget(self.get_rec_btn)
        self.select_manual_btn = QPushButton('Choose from Schedule')
        self.select_manual_btn.setObjectName('secondaryButton')
        self.select_manual_btn.clicked.connect(self.show_activity_selection_dialog)
        # Исправление размеров кнопки Choose from Schedule
        self.select_manual_btn.setMinimumWidth(240)
        self.select_manual_btn.setMinimumHeight(52)
        self.select_manual_btn.setStyleSheet('font-size: 16px; padding: 14px 24px;')
        btn_layout.addWidget(self.select_manual_btn)
        self.clear_rec_btn = QPushButton('Clear Recommendations')
        self.clear_rec_btn.setObjectName('clearButton')
        self.clear_rec_btn.clicked.connect(self.clear_recommendations)
        btn_layout.addWidget(self.clear_rec_btn)
        btn_layout.addStretch()
        layout.addLayout(btn_layout)
        rec_container = QFrame()
        rec_container.setObjectName('statusCard')
        rec_layout = QVBoxLayout(rec_container)
        self.rec_activity_lbl = QLabel('')
        self.rec_activity_lbl.setStyleSheet('font-size: 16px; font-weight: bold;')
        rec_layout.addWidget(self.rec_activity_lbl)
        self.rec_score_lbl = QLabel('')
        rec_layout.addWidget(self.rec_score_lbl)
        self.rec_reason_lbl = QLabel('')
        rec_layout.addWidget(self.rec_reason_lbl)
        choice_layout = QHBoxLayout()
        choice_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.use_rec_btn = QPushButton('Use Recommended')
        self.use_rec_btn.setObjectName('chooseButton')
        self.use_rec_btn.clicked.connect(self.use_recommended_activity)
        self.use_rec_btn.setEnabled(False)
        self.use_rec_btn.setMinimumWidth(240)
        self.use_rec_btn.setMinimumHeight(52)
        self.use_rec_btn.setStyleSheet('font-size: 16px; padding: 14px 36px;')
        choice_layout.addWidget(self.use_rec_btn)
        rec_layout.addLayout(choice_layout)
        layout.addWidget(rec_container)
        self.history_table = QTableWidget()
        self.history_table.setColumnCount(5)
        self.history_table.setHorizontalHeaderLabels(
            ['Activity', 'Category', 'Score', 'Time', 'Status']
        )
        self.history_table.horizontalHeader().setSectionResizeMode(0, QHeaderView.ResizeMode.Stretch)
        self.history_table.setAlternatingRowColors(True)
        layout.addWidget(QLabel('Recommendation History'))
        layout.addWidget(self.history_table)
        return tab

    def _create_productivity_overview_tab(self):
        tab = QWidget()
        main_layout = QVBoxLayout(tab)
        main_layout.setSpacing(15)
        main_layout.setContentsMargins(10, 10, 10, 10)
        btn_layout = QHBoxLayout()
        self.refresh_prod_btn = QPushButton('Refresh')
        self.refresh_prod_btn.setObjectName('refreshButton')
        self.refresh_prod_btn.clicked.connect(self.update_productivity_charts)
        btn_layout.addWidget(self.refresh_prod_btn)
        btn_layout.addStretch()
        main_layout.addLayout(btn_layout)
        self.productivity_frame = QFrame()
        self.productivity_frame.setObjectName('productivityCard')
        prod_layout = QVBoxLayout(self.productivity_frame)
        prod_layout.setSpacing(15)
        prod_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.score_lbl = QLabel('0%')
        self.score_lbl.setObjectName('productivityScore')
        self.score_lbl.setAlignment(Qt.AlignmentFlag.AlignCenter)
        prod_layout.addWidget(self.score_lbl)
        self.productivity_text_lbl = QLabel('Productivity Score')
        self.productivity_text_lbl.setObjectName('productivityLabel')
        self.productivity_text_lbl.setAlignment(Qt.AlignmentFlag.AlignCenter)
        prod_layout.addWidget(self.productivity_text_lbl)
        self.productivity_trend_lbl = QLabel('Trend: No data')
        self.productivity_trend_lbl.setAlignment(Qt.AlignmentFlag.AlignCenter)
        prod_layout.addWidget(self.productivity_trend_lbl)
        main_layout.addWidget(self.productivity_frame)
        self.stats_frame = QFrame()
        self.stats_frame.setObjectName('statusCard')
        stats_layout = QVBoxLayout(self.stats_frame)
        self.stats_lbl = QLabel('No data available')
        self.stats_lbl.setStyleSheet('color: #8b949e; font-size: 14px;')
        stats_layout.addWidget(self.stats_lbl)
        main_layout.addWidget(self.stats_frame)
        main_layout.addStretch()
        return tab

    def _create_productivity_charts_tab(self):
        tab = QWidget()
        main_layout = QVBoxLayout(tab)
        main_layout.setSpacing(15)
        main_layout.setContentsMargins(10, 10, 10, 10)
        self.chart_main = Chart(width=10, height=5)
        self.chart_main.setMinimumHeight(300)
        main_layout.addWidget(QLabel('Productivity Score Over Sessions'))
        main_layout.addWidget(self.chart_main, stretch=1)
        self.chart_session = Chart(width=10, height=4)
        self.chart_session.setMinimumHeight(250)
        main_layout.addWidget(QLabel('Current Session Productivity'))
        main_layout.addWidget(self.chart_session, stretch=1)
        self.chart_category = Chart(width=10, height=4)
        self.chart_category.setMinimumHeight(250)
        main_layout.addWidget(QLabel('Today Activity Distribution'))
        main_layout.addWidget(self.chart_category, stretch=1)
        main_layout.addStretch()
        return tab

    def _create_settings_tab(self):
        tab = QWidget()
        main_layout = QVBoxLayout(tab)
        main_layout.setContentsMargins(10, 10, 10, 10)
        settings_card = QFrame()
        settings_card.setObjectName('settingsCard')
        settings_layout = QVBoxLayout(settings_card)
        title = QLabel('Recommendation Settings')
        title.setStyleSheet('font-size: 20px; font-weight: bold;')
        settings_layout.addWidget(title)
        self.coeff_btn = QPushButton('Adjust Coefficients')
        self.coeff_btn.setObjectName('settingsButton')
        self.coeff_btn.clicked.connect(self.open_coefficients_dialog)
        settings_layout.addWidget(self.coeff_btn)
        main_layout.addWidget(settings_card)
        main_layout.addStretch()
        return tab

    def open_coefficients_dialog(self):
        dialog = CoefficientsDialog(self, self.engine.coefficients)
        if dialog.exec() == QDialog.DialogCode.Accepted:
            new_coeffs = dialog.get_coefficients()
            if self.engine.update_coefficients(new_coeffs):
                QMessageBox.information(self, 'Success', 'Coefficients updated')

    def show_activity_selection_dialog(self):
        activities = self._get_activities_from_schedule()
        if not activities:
            QMessageBox.warning(self, 'Error', 'No activities in schedule. Add activities first.')
            return
        dialog = ActivitySelectDialog(self, activities)
        if dialog.exec() == QDialog.DialogCode.Accepted:
            selected = dialog.get_selected_activity()
            if selected:
                self.activity_name = selected.get('activity', 'Unknown')
                self.activity_category = selected.get('category', 'mental')
                self.start_activity_timer()
                QMessageBox.information(self, 'Selected', f'Activity: {self.activity_name}')

    def show_time_input_and_get_recommendations(self):
        dialog = TimeInputDialog(self)
        planned_time = dialog.get_time()
        if planned_time:
            self.get_recommendations(planned_time)

    def get_recommendations(self, planned_time=30):
        user_state = self._get_user_state()
        activities = self._get_activities_from_schedule()
        if not activities:
            QMessageBox.warning(self, 'Error', 'Add activities to calendar first')
            return
        result = self.engine.get_recommendation(user_state, activities, planned_time)
        if result:
            self.recommendations = result['all_scores']
            self.engine.save_recommendation(
                result['activity']['activity'],
                result['activity']['category'],
                result['score'],
                result['factors'],
                planned_time
            )
            self.rec_activity_lbl.setText(f"{result['activity']['activity']}")
            self.rec_score_lbl.setText(f"Score: {result['score']:.2f}")
            self.rec_reason_lbl.setText(f"Reason: {result['reason']}")
            self.use_rec_btn.setEnabled(True)
            self.load_recommendation_history()
            QTimer.singleShot(500, self.update_productivity_charts)
            QMessageBox.information(self, 'Recommendation',
                f"Activity: {result['activity']['activity']}\n{result['reason']}")

    def use_recommended_activity(self):
        if self.recommendations:
            rec = self.recommendations[0]
            self.activity_name = safe_get(rec, 'activity', {}).get('activity', 'Unknown')
            self.activity_category = safe_get(rec, 'activity', {}).get('category', 'mental')
            self.start_activity_timer()

    def clear_recommendations(self):
        reply = QMessageBox.question(self, 'Clear Recommendations',
            'Are you sure you want to clear all recommendation history?',
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
            QMessageBox.StandardButton.No)
        if reply == QMessageBox.StandardButton.Yes:
            if self.engine.clear_recommendation_history():
                self.history_table.setRowCount(0)
                self.recommendations = []
                self.rec_activity_lbl.setText('')
                self.rec_score_lbl.setText('')
                self.rec_reason_lbl.setText('')
                self.use_rec_btn.setEnabled(False)
                QMessageBox.information(self, 'Success', 'Recommendation history cleared')

    def start_activity_timer(self):
        if not self.activity_name:
            QMessageBox.warning(self, 'Error', 'Select an activity first')
            return
        self._session_start_time = time.time()
        self.timer.start(self.activity_name, self.activity_category)
        self.start_timer_btn.setEnabled(False)
        self.stop_timer_btn.setEnabled(True)
        self.timer_activity_lbl.setText(f'Activity: {self.activity_name}')

    def stop_activity_timer(self):
        elapsed = self.timer.stop()
        elapsed_minutes = elapsed / 60.0
        self._session_start_time = None
        if self.activity_name:
            self.engine.log_activity(self.activity_category, elapsed_minutes,
                self.activity_name)
            feedback_dialog = FeedbackDialog(self, self.activity_name)
            feedback_result = feedback_dialog.exec()
            if feedback_result in [1, 0, -1]:
                QMessageBox.information(self, 'Completed', f'Time: {format_time(elapsed)}')
        self.start_timer_btn.setEnabled(True)
        self.stop_timer_btn.setEnabled(False)
        self.timer_lbl.setText('00:00')
        self.timer_activity_lbl.setText('No active activity')
        self.activity_name = None

    def update_timer_display(self, elapsed):
        self.timer_lbl.setText(format_time(elapsed))

    def update_session_productivity(self):
        if self._session_start_time and self.cam_thread:
            energy = self.cam_thread.get_energy()
            sleepiness = self.cam_thread.get_sleepiness()
            productivity = (energy * 0.7 + (1 - sleepiness) * 0.3) * 100
            self.engine.save_session_productivity(productivity)
            if self.tab_widget.currentIndex() == 4:
                self.update_session_chart()

    def update_session_chart(self):
        if not hasattr(self, 'chart_session') or not self.chart_session:
            return
        colors = get_theme_colors()
        if hasattr(self.chart_session, 'axes') and self.chart_session.axes:
            self.chart_session.axes.clear()
            self.chart_session.axes.set_facecolor(colors['bg_secondary'])
            figure = self._get_chart_figure(self.chart_session)
            if figure:
                figure.patch.set_facecolor(colors['bg_secondary'])
            session_data = self.engine.get_session_productivity()
            if session_data and len(session_data) > 0:
                productivity_values = [d[0] for d in session_data]
                timestamps = [d[1] for d in session_data]
                start_time = timestamps[0] if timestamps else time.time()
                x_values = [(t - start_time) / 60 for t in timestamps]
                self.chart_session.axes.plot(x_values, productivity_values,
                    color=colors['success'], linewidth=2, marker='o', markersize=4)
                self.chart_session.axes.fill_between(x_values, productivity_values, alpha=0.3, color=colors['success'])
                self.chart_session.axes.set_title('Current Session Productivity',
                    color=colors['text_primary'], fontsize=14, fontweight='bold')
                self.chart_session.axes.set_ylim(0, 100)
                self.chart_session.axes.grid(True, alpha=0.3, linestyle='--', color=colors['border'])
                self.chart_session.axes.tick_params(colors=colors['text_primary'])
                self.chart_session.axes.set_xlabel('Time (minutes)', color=colors['text_primary'], fontsize=12)
                self.chart_session.axes.set_ylabel('Productivity (%)', color=colors['text_primary'], fontsize=12)
            else:
                self.chart_session.axes.text(0.5, 0.5, 'Start a session to see real-time productivity',
                    transform=self.chart_session.axes.transAxes, ha='center',
                    va='center', color=colors['text_secondary'], fontsize=14)
            if hasattr(self.chart_session, 'draw'):
                self.chart_session.draw()

    def update_video_frame(self, frame_array):
        if hasattr(self, 'video_lbl') and self.video_lbl and frame_array is not None:
            h, w, ch = frame_array.shape
            qimage = QImage(frame_array.data, w, h, ch * w, QImage.Format.Format_RGB888)
            self.video_lbl.setPixmap(QPixmap.fromImage(qimage).scaled(
                self.video_lbl.size(), Qt.AspectRatioMode.KeepAspectRatio))

    def _update_energy_display(self, energy):
        colors = get_theme_colors()
        energy_percent = int(energy * 100)
        self.energy_value_lbl.setText(f'{energy_percent}%')
        self.energy_bar.setValue(energy_percent)
        if energy > 0.7:
            color = colors['energy_high']
        elif energy > 0.4:
            color = colors['energy_medium']
        else:
            color = colors['energy_low']
        self.energy_value_lbl.setStyleSheet(f'color: {color}; font-size: 36px; font-weight: bold;')
        self.energy_bar.setStyleSheet(f'''
            QProgressBar {{
                background-color: {colors["bg_tertiary"]};
                border-radius: 5px;
                height: 12px;
                border: 1px solid {colors["border"]};
            }}
            QProgressBar::chunk {{
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 {colors["accent"]}, stop:1 {color});
                border-radius: 5px;
            }}
        ''')

    def update_status(self, sleepiness, emotion, emotion_probs, energy):
        if hasattr(self, 'sleep_lbl'):
            self.sleep_lbl.setText(f'Sleepiness: {safe_format(sleepiness)}')
        if hasattr(self, 'emotion_lbl'):
            self.emotion_lbl.setText(f'Emotion: {emotion}')
        if hasattr(self, 'energy_bar'):
            self._update_energy_display(energy)

    def update_productivity_charts(self, force=False):
        current_time = time.time()
        if not force and current_time - self._last_update < 5:
            return
        self._last_update = current_time
        colors = get_theme_colors()
        prod_stats = self.engine.get_productivity_stats()
        if hasattr(self, 'score_lbl') and self.score_lbl:
            self.score_lbl.setText(f'{prod_stats["avg"]:.1f}%')
        if hasattr(self, 'productivity_trend_lbl') and self.productivity_trend_lbl:
            if prod_stats['trend'] > 5:
                trend_text = f'Trend: +{prod_stats["trend"]:.1f}%'
                self.productivity_trend_lbl.setObjectName('trendUp')
            elif prod_stats['trend'] < -5:
                trend_text = f'Trend: {prod_stats["trend"]:.1f}%'
                self.productivity_trend_lbl.setObjectName('trendDown')
            else:
                trend_text = f'Trend: {prod_stats["trend"]:.1f}%'
                self.productivity_trend_lbl.setObjectName('trendStable')
            self.productivity_trend_lbl.setText(trend_text)
            self.productivity_trend_lbl.setStyleSheet(self.styleSheet())
        factor_history = self.engine.get_factor_history_for_charts()
        if hasattr(self, 'chart_main') and self.chart_main:
            if hasattr(self.chart_main, 'axes') and self.chart_main.axes:
                self.chart_main.axes.clear()
                self.chart_main.axes.set_facecolor(colors['bg_secondary'])
                figure = self._get_chart_figure(self.chart_main)
                if figure:
                    figure.patch.set_facecolor(colors['bg_secondary'])
                if factor_history and len(factor_history) >= 1:
                    productivity_values = []
                    for h in factor_history:
                        S = h[0] if h[0] else 0
                        E = h[1] if h[1] else 0
                        P = h[2] if h[2] else 0
                        C = h[3] if h[3] else 0
                        score = self.engine.calculate_productivity_score(S, E, P, C)
                        productivity_values.append(score)
                    x_values = list(range(len(productivity_values)))
                    self.chart_main.axes.plot(x_values, productivity_values,
                        color=colors['accent'], linewidth=3, marker='o', markersize=6,
                        markerfacecolor=colors['accent'])
                    self.chart_main.axes.fill_between(x_values, productivity_values, alpha=0.3, color=colors['accent'])
                    self.chart_main.axes.set_title('Productivity Score Over Sessions',
                        color=colors['text_primary'], fontsize=16, fontweight='bold', pad=15)
                    self.chart_main.axes.set_ylim(0, 100)
                    self.chart_main.axes.grid(True, alpha=0.3, linestyle='--', linewidth=1, color=colors['border'])
                    self.chart_main.axes.tick_params(colors=colors['text_primary'], labelsize=11)
                    self.chart_main.axes.set_xlabel('Session', color=colors['text_primary'], fontsize=13)
                    self.chart_main.axes.set_ylabel('Score (%)', color=colors['text_primary'], fontsize=13)
                    self.chart_main.axes.set_xticks(x_values)
                    self.chart_main.axes.set_xticklabels([str(i + 1) for i in x_values], color=colors['text_primary'],
                        fontsize=10)
                    avg_score = sum(productivity_values) / len(productivity_values)
                    self.chart_main.axes.axhline(y=avg_score, color=colors['success'], linestyle='--',
                        linewidth=2, alpha=0.7, label=f'Avg: {avg_score:.1f}%')
                    self.chart_main.axes.legend(facecolor=colors['bg_secondary'], edgecolor=colors['border'],
                        labelcolor=colors['text_primary'], fontsize=10)
                else:
                    self.chart_main.axes.text(0.5, 0.5, 'Get recommendations to start tracking',
                        transform=self.chart_main.axes.transAxes, ha='center',
                        va='center', color=colors['text_secondary'], fontsize=16)
                if hasattr(self.chart_main, 'draw'):
                    self.chart_main.draw()
        self.update_session_chart()
        self.update_category_chart()
        stats = self.engine.get_activity_stats()
        if hasattr(self, 'stats_lbl') and self.stats_lbl:
            self.stats_lbl.setText(f'{len(stats) if stats else 0} categories tracked today')
            self.stats_lbl.setStyleSheet(
                f'color: {colors["success"]}; font-size: 14px;' if stats else f'color: {colors["text_secondary"]}; font-size: 14px;')

    def update_category_chart(self):
        if not hasattr(self, 'chart_category') or not self.chart_category:
            return
        colors = get_theme_colors()
        if hasattr(self.chart_category, 'axes') and self.chart_category.axes:
            self.chart_category.axes.clear()
            self.chart_category.axes.set_facecolor(colors['bg_secondary'])
            figure = self._get_chart_figure(self.chart_category)
            if figure:
                figure.patch.set_facecolor(colors['bg_secondary'])
            stats = self.engine.get_activity_stats()
            if stats and len(stats) > 0:
                categories = [s[0] for s in stats]
                times = [s[1] if s[1] else 0 for s in stats]
                colors_list = [
                    colors['accent'],
                    colors['success'],
                    colors['warning'],
                    colors['danger'],
                    colors['text_secondary']
                ]
                wedges, texts, autotexts = self.chart_category.axes.pie(times, labels=categories,
                    autopct='%1.1f%%',
                    colors=colors_list[:len(categories)])
                for autotext in autotexts:
                    autotext.set_color(colors['text_primary'])
                    autotext.set_fontweight('bold')
                    autotext.set_fontsize(11)
                for text in texts:
                    text.set_color(colors['text_primary'])
                    text.set_fontsize(11)
                self.chart_category.axes.set_title('Today Activity Distribution',
                    color=colors['text_primary'], fontsize=14, fontweight='bold', pad=15)
            else:
                self.chart_category.axes.text(0.5, 0.5, 'No activity data for today',
                    transform=self.chart_category.axes.transAxes, ha='center',
                    va='center', color=colors['text_secondary'], fontsize=16)
            if hasattr(self.chart_category, 'draw'):
                self.chart_category.draw()

    def _get_user_state(self):
        if self.cam_thread:
            return {
                't_closed': 0.0,
                'f_blink': self.cam_thread.get_blink_count() / max(1, time.time() / 60),
                'pose_angle': self.cam_thread.get_head_angle(),
                'emotion_probs': self.cam_thread.get_emotion_probs(),
                'current_hour': datetime.datetime.now().hour,
                'current_timestamp': time.time(),
            }
        return {
            't_closed': 0.0, 'f_blink': 0, 'pose_angle': 0,
            'emotion_probs': {'neutral': 1.0},
            'current_hour': datetime.datetime.now().hour,
            'current_timestamp': time.time(),
        }

    def _get_activities_from_schedule(self):
        conn = db.get_connection()
        cur = conn.cursor()
        cur.execute('''SELECT activity, category, start_time, end_time,
            difficulty, priority, estimated_duration, scheduled_date
            FROM schedule WHERE user_id=?''', (self.user_id,))
        result = [
            {
                'activity': r[0],
                'category': r[1],
                'start_time': r[2] if r[2] else '09:00',
                'end_time': r[3] if r[3] else '10:00',
                'difficulty': float(r[4]) if r[4] else 0.5,
                'priority': float(r[5]) if r[5] else 0.5,
                'estimated_duration': r[6] if len(r) > 6 else 60,
                'scheduled_date': r[7] if len(r) > 7 else None
            }
            for r in cur.fetchall()
        ]
        conn.close()
        return result

    def load_recommendation_history(self):
        history = self.engine.get_recommendation_history(10)
        self.history_table.setRowCount(0)
        for rec in history:
            r = self.history_table.rowCount()
            self.history_table.insertRow(r)
            self.history_table.setItem(r, 0, QTableWidgetItem(str(rec[0]) if rec[0] else 'N/A'))
            self.history_table.setItem(r, 1, QTableWidgetItem(str(rec[1]) if rec[1] else 'N/A'))
            score_val = float(rec[2]) if rec[2] is not None else 0.0
            self.history_table.setItem(r, 2, QTableWidgetItem(f'{score_val:.2f}'))
            timestamp = datetime.datetime.fromtimestamp(rec[3]).strftime('%Y-%m-%d %H:%M') if rec[3] else 'N/A'
            self.history_table.setItem(r, 3, QTableWidgetItem(timestamp))
            status = 'Done' if rec[5] else 'Pending'
            self.history_table.setItem(r, 4, QTableWidgetItem(status))

    def closeEvent(self, event):
        if self.cam_thread:
            self.cam_thread.running = False
            self.cam_thread.wait(3000)
            self.cam_thread = None
        if hasattr(self, 'timer') and self.timer:
            self.timer.stop()
        event.accept()