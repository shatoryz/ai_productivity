DARK_THEME = True

DARK_STYLES = '''
QMainWindow {
    background: qlineargradient(x1:0, y1:0, x2:1, y2:1, stop:0 #0d1117, stop:1 #161b22);
}

QWidget {
    background-color: transparent;
    color: #c9d1d9;
    font-family: 'Segoe UI', 'Roboto', Arial, sans-serif;
    font-size: 14px;
}

QTabWidget::pane {
    background-color: #161b22;
    border: 1px solid #30363d;
    border-radius: 12px;
    padding: 15px;
}

QTabBar::tab {
    background-color: #21262d;
    color: #8b949e;
    padding: 14px 28px;
    border-top-left-radius: 10px;
    border-top-right-radius: 10px;
    margin-right: 3px;
    font-weight: 600;
    min-width: 140px;
    border: 1px solid transparent;
}

QTabBar::tab:selected {
    background: qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 #1f6feb, stop:1 #388bfd);
    color: #ffffff;
    border: 1px solid #1f6feb;
}

QTabBar::tab:hover:!selected {
    background-color: #30363d;
    color: #c9d1d9;
}

QPushButton {
    background: qlineargradient(x1:0, y1:0, x2:0, y2:1, stop:0 #238636, stop:1 #2ea043);
    color: #ffffff;
    border: none;
    border-radius: 8px;
    font-weight: 600;
    padding: 12px 24px;
    min-height: 48px;
    min-width: 160px;
    font-size: 14px;
}

QPushButton:hover {
    background: qlineargradient(x1:0, y1:0, x2:0, y2:1, stop:0 #2ea043, stop:1 #3fb950);
}

QPushButton:disabled {
    background: #30363d;
    color: #8b949e;
}

QPushButton#secondaryButton {
    background: qlineargradient(x1:0, y1:0, x2:0, y2:1, stop:0 #21262d, stop:1 #30363d);
    border: 1px solid #30363d;
    min-width: 280px;
    min-height: 52px;
    padding: 14px 24px;
    color: #c9d1d9;
    font-size: 16px;
}

QPushButton#secondaryButton:hover {
    background: qlineargradient(x1:0, y1:0, x2:0, y2:1, stop:0 #30363d, stop:1 #404750);
}

QPushButton#startButton {
    background: qlineargradient(x1:0, y1:0, x2:0, y2:1, stop:0 #1f6feb, stop:1 #388bfd);
    min-width: 160px;
}

QPushButton#startButton:hover {
    background: qlineargradient(x1:0, y1:0, x2:0, y2:1, stop:0 #388bfd, stop:1 #58a6ff);
}

QPushButton#stopButton {
    background: qlineargradient(x1:0, y1:0, x2:0, y2:1, stop:0 #da3633, stop:1 #f85149);
    min-width: 160px;
}

QPushButton#stopButton:hover {
    background: qlineargradient(x1:0, y1:0, x2:0, y2:1, stop:0 #f85149, stop:1 #ff7b72);
}

QPushButton#deleteButton {
    background: qlineargradient(x1:0, y1:0, x2:0, y2:1, stop:0 #da3633, stop:1 #f85149);
    min-width: 36px;
    max-width: 36px;
    min-height: 32px;
    max-height: 32px;
    padding: 0px;
    font-size: 18px;
    border-radius: 6px;
    margin: 0px;
}

QPushButton#deleteButton:hover {
    background: qlineargradient(x1:0, y1:0, x2:0, y2:1, stop:0 #f85149, stop:1 #ff7b72);
}

QPushButton#selectButton {
    background: qlineargradient(x1:0, y1:0, x2:0, y2:1, stop:0 #1f6feb, stop:1 #388bfd);
    min-width: 100px;
    max-width: 120px;
    min-height: 36px;
    max-height: 40px;
    padding: 8px 16px;
    font-size: 14px;
    border-radius: 6px;
    color: #ffffff;
    font-weight: 600;
    margin: 0px;
}

QPushButton#selectButton:hover {
    background: qlineargradient(x1:0, y1:0, x2:0, y2:1, stop:0 #388bfd, stop:1 #58a6ff);
}

QPushButton#addButton {
    background: qlineargradient(x1:0, y1:0, x2:0, y2:1, stop:0 #8b5cf6, stop:1 #a78bfa);
    min-width: 180px;
}

QPushButton#addButton:hover {
    background: qlineargradient(x1:0, y1:0, x2:0, y2:1, stop:0 #a78bfa, stop:1 #c4b5fd);
}

QPushButton#refreshButton {
    background: qlineargradient(x1:0, y1:0, x2:0, y2:1, stop:0 #1f6feb, stop:1 #388bfd);
    min-width: 160px;
}

QPushButton#refreshButton:hover {
    background: qlineargradient(x1:0, y1:0, x2:0, y2:1, stop:0 #388bfd, stop:1 #58a6ff);
}

QPushButton#clearButton {
    background: qlineargradient(x1:0, y1:0, x2:0, y2:1, stop:0 #da3633, stop:1 #f85149);
    min-width: 200px;
}

QPushButton#clearButton:hover {
    background: qlineargradient(x1:0, y1:0, x2:0, y2:1, stop:0 #f85149, stop:1 #ff7b72);
}

QPushButton#loginButton {
    background: qlineargradient(x1:0, y1:0, x2:0, y2:1, stop:0 #1f6feb, stop:1 #388bfd);
    font-size: 16px;
    padding: 14px 36px;
    min-width: 240px;
    min-height: 52px;
}

QPushButton#loginButton:hover {
    background: qlineargradient(x1:0, y1:0, x2:0, y2:1, stop:0 #388bfd, stop:1 #58a6ff);
}

QPushButton#registerButton {
    background: qlineargradient(x1:0, y1:0, x2:0, y2:1, stop:0 #238636, stop:1 #2ea043);
    font-size: 16px;
    padding: 14px 36px;
    min-width: 240px;
    min-height: 52px;
}

QPushButton#registerButton:hover {
    background: qlineargradient(x1:0, y1:0, x2:0, y2:1, stop:0 #2ea043, stop:1 #3fb950);
}

QPushButton#saveButton {
    background: qlineargradient(x1:0, y1:0, x2:0, y2:1, stop:0 #238636, stop:1 #2ea043);
    min-width: 140px;
}

QPushButton#saveButton:hover {
    background: qlineargradient(x1:0, y1:0, x2:0, y2:1, stop:0 #2ea043, stop:1 #3fb950);
}

QPushButton#themeButton {
    background: qlineargradient(x1:0, y1:0, x2:0, y2:1, stop:0 #6e7681, stop:1 #8b949e);
    min-width: 55px;
    max-width: 55px;
    min-height: 55px;
    max-height: 55px;
    border-radius: 27px;
    font-size: 24px;
    padding: 0px;
}

QPushButton#themeButton:hover {
    background: qlineargradient(x1:0, y1:0, x2:0, y2:1, stop:0 #8b949e, stop:1 #c9d1d9);
}

QPushButton#eyeButton {
    background: qlineargradient(x1:0, y1:0, x2:0, y2:1, stop:0 #21262d, stop:1 #30363d);
    border: 1px solid #30363d;
    min-width: 45px;
    max-width: 45px;
    min-height: 45px;
    max-height: 45px;
    border-radius: 8px;
    font-size: 18px;
    padding: 0px;
    margin-left: 5px;
    color: #c9d1d9;
}

QPushButton#eyeButton:hover {
    background: qlineargradient(x1:0, y1:0, x2:0, y2:1, stop:0 #30363d, stop:1 #404750);
    border: 1px solid #1f6feb;
}

QPushButton#getRecButton {
    background: qlineargradient(x1:0, y1:0, x2:0, y2:1, stop:0 #8b5cf6, stop:1 #a78bfa);
    min-width: 200px;
}

QPushButton#getRecButton:hover {
    background: qlineargradient(x1:0, y1:0, x2:0, y2:1, stop:0 #a78bfa, stop:1 #c4b5fd);
}

QPushButton#chooseButton {
    background: qlineargradient(x1:0, y1:0, x2:0, y2:1, stop:0 #238636, stop:1 #2ea043);
    min-width: 240px;
    min-height: 52px;
}

QPushButton#chooseButton:hover {
    background: qlineargradient(x1:0, y1:0, x2:0, y2:1, stop:0 #2ea043, stop:1 #3fb950);
}

QPushButton#settingsButton {
    background: qlineargradient(x1:0, y1:0, x2:0, y2:1, stop:0 #8b5cf6, stop:1 #a78bfa);
    min-width: 200px;
}

QPushButton#settingsButton:hover {
    background: qlineargradient(x1:0, y1:0, x2:0, y2:1, stop:0 #a78bfa, stop:1 #c4b5fd);
}

QGroupBox {
    background-color: #161b22;
    border: 1px solid #30363d;
    border-radius: 12px;
    margin-top: 20px;
    padding-top: 20px;
    color: #58a6ff;
    font-weight: 600;
    font-size: 15px;
}

QFrame#recCard {
    background-color: #161b22;
    border: 2px solid #30363d;
    border-radius: 14px;
    padding: 24px;
}

QFrame#recCard:hover {
    border: 2px solid #1f6feb;
}

QFrame#timerCard {
    background: qlineargradient(x1:0, y1:0, x2:1, y2:1, stop:0 #161b22, stop:1 #1f2937);
    border: 2px solid #1f6feb;
    border-radius: 14px;
    padding: 24px;
}

QFrame#productivityCard {
    background: qlineargradient(x1:0, y1:0, x2:1, y2:1, stop:0 #161b22, stop:1 #0d291e);
    border: 2px solid #238636;
    border-radius: 14px;
    padding: 28px;
}

QFrame#statusCard {
    background-color: #161b22;
    border: 1px solid #30363d;
    border-radius: 12px;
    padding: 24px;
}

QFrame#energyCard {
    background: qlineargradient(x1:0, y1:0, x2:1, y2:1, stop:0 #161b22, stop:1 #291616);
    border: 2px solid #f85149;
    border-radius: 14px;
    padding: 24px;
}

QFrame#authCard {
    background-color: #161b22;
    border: 1px solid #30363d;
    border-radius: 16px;
    padding: 48px;
    max-width: 480px;
}

QFrame#settingsCard {
    background-color: #161b22;
    border: 1px solid #8b5cf6;
    border-radius: 12px;
    padding: 24px;
}

QTableWidget {
    background-color: #161b22;
    border: 1px solid #30363d;
    border-radius: 12px;
    color: #c9d1d9;
    alternate-background-color: #1c2128;
    gridline-color: #30363d;
    selection-background-color: #1f6feb;
}

QTableWidget::viewport {
    background-color: #161b22;
}

QTableWidget::item {
    padding: 12px;
    border-bottom: 1px solid #30363d;
    background-color: #161b22;
}

QTableWidget::item:selected {
    background: qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 #1f6feb, stop:1 #388bfd);
    color: #ffffff;
}

QTableWidget::item:hover {
    background-color: #21262d;
}

QHeaderView::section {
    background: qlineargradient(x1:0, y1:0, x2:0, y2:1, stop:0 #21262d, stop:1 #30363d);
    color: #8b949e;
    padding: 14px;
    border: none;
    font-weight: 600;
    border-bottom: 2px solid #30363d;
}

QTableCornerButton::section {
    background-color: #21262d;
    border: none;
    border-bottom: 2px solid #30363d;
    border-right: 1px solid #30363d;
}

QLineEdit, QComboBox, QSpinBox, QDoubleSpinBox, QDateTimeEdit, QTimeEdit {
    background-color: #0d1117;
    border: 1px solid #30363d;
    border-radius: 8px;
    padding: 12px 16px;
    min-height: 48px;
    color: #c9d1d9;
    font-size: 14px;
}

QLineEdit:focus, QComboBox:focus, QSpinBox:focus, QDoubleSpinBox:focus, QDateTimeEdit:focus, QTimeEdit:focus {
    border: 2px solid #1f6feb;
    background-color: #161b22;
}

QProgressBar {
    background-color: #21262d;
    border-radius: 8px;
    height: 14px;
    text-align: center;
    border: 1px solid #30363d;
}

QProgressBar::chunk {
    background: qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 #1f6feb, stop:1 #388bfd);
    border-radius: 6px;
}

QSlider::groove:horizontal {
    background: #30363d;
    height: 8px;
    border-radius: 4px;
}

QSlider::handle:horizontal {
    background: qlineargradient(x1:0, y1:0, x2:0, y2:1, stop:0 #1f6feb, stop:1 #388bfd);
    width: 22px;
    margin: -7px 0;
    border-radius: 11px;
}

QLabel#trendUp {
    color: #3fb950;
    font-weight: bold;
    font-size: 16px;
}

QLabel#trendDown {
    color: #f85149;
    font-weight: bold;
    font-size: 16px;
}

QLabel#trendStable {
    color: #d29922;
    font-weight: bold;
    font-size: 16px;
}

QLabel#productivityScore {
    font-size: 64px;
    font-weight: bold;
    color: #238636;
}

QLabel#productivityLabel {
    font-size: 18px;
    color: #8b949e;
}

QLabel#sleepinessLabel {
    color: #f85149;
    font-size: 15px;
    font-weight: 500;
}

QLabel#emotionLabel {
    color: #3fb950;
    font-size: 15px;
    font-weight: 500;
}

QLabel#authTitle {
    font-size: 36px;
    font-weight: bold;
    color: #58a6ff;
}

QLabel#authSubtitle {
    font-size: 14px;
    color: #8b949e;
}

QCalendarWidget {
    background-color: #161b22;
    color: #c9d1d9;
    border-radius: 12px;
    border: 1px solid #30363d;
}

QCalendarWidget QToolButton {
    background-color: #21262d;
    color: #c9d1d9;
    border-radius: 8px;
    padding: 10px;
    min-height: 40px;
    font-weight: 600;
}

QCalendarWidget QToolButton:hover {
    background-color: #30363d;
}

QCalendarWidget QMenu {
    background-color: #161b22;
    color: #c9d1d9;
    border: 1px solid #30363d;
    border-radius: 8px;
}

QCalendarWidget QWidget#qt_calendar_navigationbar {
    background-color: #21262d;
    border: 1px solid #30363d;
    border-radius: 8px;
}

QCalendarWidget QSpinBox {
    background-color: #0d1117;
    color: #c9d1d9;
    border: 1px solid #30363d;
    border-radius: 6px;
}

QCalendarWidget QLabel {
    color: #c9d1d9;
}

QCalendarWidget QAbstractItemView {
    background-color: #161b22;
    color: #c9d1d9;
    selection-background-color: #1f6feb;
    selection-color: #ffffff;
    gridline-color: #30363d;
}

QCalendarWidget QAbstractItemView::item {
    background-color: #161b22;
    border: none;
}

QCalendarWidget QAbstractItemView::item:selected {
    background-color: #1f6feb;
    color: #ffffff;
}

QScrollBar:vertical {
    background: #161b22;
    width: 14px;
    border-radius: 7px;
    margin: 2px;
}

QScrollBar::handle:vertical {
    background: qlineargradient(x1:0, y1:0, x2:0, y2:1, stop:0 #30363d, stop:1 #404750);
    border-radius: 7px;
    min-height: 40px;
}

QScrollBar::handle:vertical:hover {
    background: qlineargradient(x1:0, y1:0, x2:0, y2:1, stop:0 #1f6feb, stop:1 #388bfd);
}

QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {
    height: 0px;
}

QDialog {
    background-color: #0d1117;
    border-radius: 16px;
}

QMessageBox {
    background-color: #161b22;
    border-radius: 12px;
}

QMessageBox QLabel {
    color: #c9d1d9;
    font-size: 14px;
}
'''

LIGHT_STYLES = '''
QMainWindow {
    background: qlineargradient(x1:0, y1:0, x2:1, y2:1, stop:0 #f6f8fa, stop:1 #ffffff);
}

QWidget {
    background-color: transparent;
    color: #24292f;
    font-family: 'Segoe UI', 'Roboto', Arial, sans-serif;
    font-size: 14px;
}

QTabWidget::pane {
    background-color: #ffffff;
    border: 1px solid #d0d7de;
    border-radius: 12px;
    padding: 15px;
}

QTabBar::tab {
    background-color: #f6f8fa;
    color: #57606a;
    padding: 14px 28px;
    border-top-left-radius: 10px;
    border-top-right-radius: 10px;
    margin-right: 3px;
    font-weight: 600;
    min-width: 140px;
    border: 1px solid transparent;
}

QTabBar::tab:selected {
    background: qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 #8250df, stop:1 #a371f7);
    color: #ffffff;
    border: 1px solid #8250df;
}

QTabBar::tab:hover:!selected {
    background-color: #eaeef2;
    color: #24292f;
}

QPushButton {
    background: qlineargradient(x1:0, y1:0, x2:0, y2:1, stop:0 #2da44e, stop:1 #2c974b);
    color: #ffffff;
    border: none;
    border-radius: 8px;
    font-weight: 600;
    padding: 12px 24px;
    min-height: 48px;
    min-width: 160px;
    font-size: 14px;
}

QPushButton:hover {
    background: qlineargradient(x1:0, y1:0, x2:0, y2:1, stop:0 #2c974b, stop:1 #28a046);
}

QPushButton:disabled {
    background: #eaeef2;
    color: #8c959f;
}

QPushButton#secondaryButton {
    background: qlineargradient(x1:0, y1:0, x2:0, y2:1, stop:0 #f6f8fa, stop:1 #eaeef2);
    border: 1px solid #d0d7de;
    min-width: 280px;
    min-height: 52px;
    padding: 14px 24px;
    color: #24292f;
    font-size: 16px;
}

QPushButton#secondaryButton:hover {
    background: qlineargradient(x1:0, y1:0, x2:0, y2:1, stop:0 #eaeef2, stop:1 #d0d7de);
}

QPushButton#startButton {
    background: qlineargradient(x1:0, y1:0, x2:0, y2:1, stop:0 #8250df, stop:1 #a371f7);
    min-width: 160px;
}

QPushButton#startButton:hover {
    background: qlineargradient(x1:0, y1:0, x2:0, y2:1, stop:0 #a371f7, stop:1 #c297f9);
}

QPushButton#stopButton {
    background: qlineargradient(x1:0, y1:0, x2:0, y2:1, stop:0 #cf222e, stop:1 #da3633);
    min-width: 160px;
}

QPushButton#stopButton:hover {
    background: qlineargradient(x1:0, y1:0, x2:0, y2:1, stop:0 #da3633, stop:1 #f85149);
}

QPushButton#deleteButton {
    background: qlineargradient(x1:0, y1:0, x2:0, y2:1, stop:0 #cf222e, stop:1 #da3633);
    min-width: 36px;
    max-width: 36px;
    min-height: 32px;
    max-height: 32px;
    padding: 0px;
    font-size: 18px;
    border-radius: 6px;
    margin: 0px;
}

QPushButton#deleteButton:hover {
    background: qlineargradient(x1:0, y1:0, x2:0, y2:1, stop:0 #da3633, stop:1 #f85149);
}

QPushButton#selectButton {
    background: qlineargradient(x1:0, y1:0, x2:0, y2:1, stop:0 #8250df, stop:1 #a371f7);
    min-width: 100px;
    max-width: 120px;
    min-height: 36px;
    max-height: 40px;
    padding: 8px 16px;
    font-size: 14px;
    border-radius: 6px;
    color: #ffffff;
    font-weight: 600;
    margin: 0px;
}

QPushButton#selectButton:hover {
    background: qlineargradient(x1:0, y1:0, x2:0, y2:1, stop:0 #a371f7, stop:1 #c297f9);
}

QPushButton#addButton {
    background: qlineargradient(x1:0, y1:0, x2:0, y2:1, stop:0 #8250df, stop:1 #a371f7);
    min-width: 180px;
}

QPushButton#addButton:hover {
    background: qlineargradient(x1:0, y1:0, x2:0, y2:1, stop:0 #a371f7, stop:1 #c297f9);
}

QPushButton#refreshButton {
    background: qlineargradient(x1:0, y1:0, x2:0, y2:1, stop:0 #8250df, stop:1 #a371f7);
    min-width: 160px;
}

QPushButton#refreshButton:hover {
    background: qlineargradient(x1:0, y1:0, x2:0, y2:1, stop:0 #a371f7, stop:1 #c297f9);
}

QPushButton#clearButton {
    background: qlineargradient(x1:0, y1:0, x2:0, y2:1, stop:0 #cf222e, stop:1 #da3633);
    min-width: 200px;
}

QPushButton#clearButton:hover {
    background: qlineargradient(x1:0, y1:0, x2:0, y2:1, stop:0 #da3633, stop:1 #f85149);
}

QPushButton#loginButton {
    background: qlineargradient(x1:0, y1:0, x2:0, y2:1, stop:0 #8250df, stop:1 #a371f7);
    font-size: 16px;
    padding: 14px 36px;
    min-width: 240px;
    min-height: 52px;
}

QPushButton#loginButton:hover {
    background: qlineargradient(x1:0, y1:0, x2:0, y2:1, stop:0 #a371f7, stop:1 #c297f9);
}

QPushButton#registerButton {
    background: qlineargradient(x1:0, y1:0, x2:0, y2:1, stop:0 #2da44e, stop:1 #2c974b);
    font-size: 16px;
    padding: 14px 36px;
    min-width: 240px;
    min-height: 52px;
}

QPushButton#registerButton:hover {
    background: qlineargradient(x1:0, y1:0, x2:0, y2:1, stop:0 #2c974b, stop:1 #28a046);
}

QPushButton#saveButton {
    background: qlineargradient(x1:0, y1:0, x2:0, y2:1, stop:0 #2da44e, stop:1 #2c974b);
    min-width: 140px;
}

QPushButton#saveButton:hover {
    background: qlineargradient(x1:0, y1:0, x2:0, y2:1, stop:0 #2c974b, stop:1 #28a046);
}

QPushButton#themeButton {
    background: qlineargradient(x1:0, y1:0, x2:0, y2:1, stop:0 #6e7781, stop:1 #8c959f);
    min-width: 55px;
    max-width: 55px;
    min-height: 55px;
    max-height: 55px;
    border-radius: 27px;
    font-size: 24px;
    padding: 0px;
}

QPushButton#themeButton:hover {
    background: qlineargradient(x1:0, y1:0, x2:0, y2:1, stop:0 #8c959f, stop:1 #afb8c1);
}

QPushButton#eyeButton {
    background: qlineargradient(x1:0, y1:0, x2:0, y2:1, stop:0 #f6f8fa, stop:1 #eaeef2);
    border: 1px solid #d0d7de;
    min-width: 45px;
    max-width: 45px;
    min-height: 45px;
    max-height: 45px;
    border-radius: 8px;
    font-size: 18px;
    padding: 0px;
    margin-left: 5px;
    color: #24292f;
}

QPushButton#eyeButton:hover {
    background: qlineargradient(x1:0, y1:0, x2:0, y2:1, stop:0 #eaeef2, stop:1 #d0d7de);
    border: 1px solid #8250df;
}

QPushButton#getRecButton {
    background: qlineargradient(x1:0, y1:0, x2:0, y2:1, stop:0 #8250df, stop:1 #a371f7);
    min-width: 200px;
}

QPushButton#getRecButton:hover {
    background: qlineargradient(x1:0, y1:0, x2:0, y2:1, stop:0 #a371f7, stop:1 #c297f9);
}

QPushButton#chooseButton {
    background: qlineargradient(x1:0, y1:0, x2:0, y2:1, stop:0 #8250df, stop:1 #a371f7);
    min-width: 240px;
    min-height: 52px;
}

QPushButton#chooseButton:hover {
    background: qlineargradient(x1:0, y1:0, x2:0, y2:1, stop:0 #a371f7, stop:1 #c297f9);
}

QPushButton#settingsButton {
    background: qlineargradient(x1:0, y1:0, x2:0, y2:1, stop:0 #8250df, stop:1 #a371f7);
    min-width: 200px;
}

QPushButton#settingsButton:hover {
    background: qlineargradient(x1:0, y1:0, x2:0, y2:1, stop:0 #a371f7, stop:1 #c297f9);
}

QGroupBox {
    background-color: #ffffff;
    border: 1px solid #d0d7de;
    border-radius: 12px;
    margin-top: 20px;
    padding-top: 20px;
    color: #8250df;
    font-weight: 600;
    font-size: 15px;
}

QFrame#recCard {
    background-color: #ffffff;
    border: 2px solid #d0d7de;
    border-radius: 14px;
    padding: 24px;
}

QFrame#recCard:hover {
    border: 2px solid #8250df;
}

QFrame#timerCard {
    background: qlineargradient(x1:0, y1:0, x2:1, y2:1, stop:0 #ffffff, stop:1 #f6f8fa);
    border: 2px solid #8250df;
    border-radius: 14px;
    padding: 24px;
}

QFrame#productivityCard {
    background: qlineargradient(x1:0, y1:0, x2:1, y2:1, stop:0 #ffffff, stop:1 #dafbe1);
    border: 2px solid #2da44e;
    border-radius: 14px;
    padding: 28px;
}

QFrame#statusCard {
    background-color: #ffffff;
    border: 1px solid #d0d7de;
    border-radius: 12px;
    padding: 24px;
}

QFrame#energyCard {
    background: qlineargradient(x1:0, y1:0, x2:1, y2:1, stop:0 #ffffff, stop:1 #ffebe9);
    border: 2px solid #cf222e;
    border-radius: 14px;
    padding: 24px;
}

QFrame#authCard {
    background-color: #ffffff;
    border: 1px solid #d0d7de;
    border-radius: 16px;
    padding: 48px;
    max-width: 480px;
}

QFrame#settingsCard {
    background-color: #ffffff;
    border: 1px solid #8250df;
    border-radius: 12px;
    padding: 24px;
}

QTableWidget {
    background-color: #ffffff;
    border: 1px solid #d0d7de;
    border-radius: 12px;
    color: #24292f;
    alternate-background-color: #f6f8fa;
    gridline-color: #d0d7de;
    selection-background-color: #8250df;
}

QTableWidget::viewport {
    background-color: #ffffff;
}

QTableWidget::item {
    padding: 12px;
    border-bottom: 1px solid #d0d7de;
    background-color: #ffffff;
}

QTableWidget::item:selected {
    background: qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 #8250df, stop:1 #a371f7);
    color: #ffffff;
}

QTableWidget::item:hover {
    background-color: #f6f8fa;
}

QHeaderView::section {
    background: qlineargradient(x1:0, y1:0, x2:0, y2:1, stop:0 #f6f8fa, stop:1 #eaeef2);
    color: #57606a;
    padding: 14px;
    border: none;
    font-weight: 600;
    border-bottom: 2px solid #d0d7de;
}

QTableCornerButton::section {
    background-color: #f6f8fa;
    border: none;
    border-bottom: 2px solid #d0d7de;
    border-right: 1px solid #d0d7de;
}

QLineEdit, QComboBox, QSpinBox, QDoubleSpinBox, QDateTimeEdit, QTimeEdit {
    background-color: #ffffff;
    border: 1px solid #d0d7de;
    border-radius: 8px;
    padding: 12px 16px;
    min-height: 48px;
    color: #24292f;
    font-size: 14px;
}

QLineEdit:focus, QComboBox:focus, QSpinBox:focus, QDoubleSpinBox:focus, QDateTimeEdit:focus, QTimeEdit:focus {
    border: 2px solid #8250df;
    background-color: #f6f8fa;
}

QProgressBar {
    background-color: #eaeef2;
    border-radius: 8px;
    height: 14px;
    text-align: center;
    border: 1px solid #d0d7de;
}

QProgressBar::chunk {
    background: qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 #8250df, stop:1 #a371f7);
    border-radius: 6px;
}

QSlider::groove:horizontal {
    background: #eaeef2;
    height: 8px;
    border-radius: 4px;
}

QSlider::handle:horizontal {
    background: qlineargradient(x1:0, y1:0, x2:0, y2:1, stop:0 #8250df, stop:1 #a371f7);
    width: 22px;
    margin: -7px 0;
    border-radius: 11px;
}

QLabel#trendUp {
    color: #1a7f37;
    font-weight: bold;
    font-size: 16px;
}

QLabel#trendDown {
    color: #cf222e;
    font-weight: bold;
    font-size: 16px;
}

QLabel#trendStable {
    color: #9a6700;
    font-weight: bold;
    font-size: 16px;
}

QLabel#productivityScore {
    font-size: 64px;
    font-weight: bold;
    color: #2da44e;
}

QLabel#productivityLabel {
    font-size: 18px;
    color: #57606a;
}

QLabel#sleepinessLabel {
    color: #cf222e;
    font-size: 15px;
    font-weight: 500;
}

QLabel#emotionLabel {
    color: #1a7f37;
    font-size: 15px;
    font-weight: 500;
}

QLabel#authTitle {
    font-size: 36px;
    font-weight: bold;
    color: #8250df;
}

QLabel#authSubtitle {
    font-size: 14px;
    color: #57606a;
}

QCalendarWidget {
    background-color: #ffffff;
    color: #24292f;
    border-radius: 12px;
    border: 1px solid #d0d7de;
}

QCalendarWidget QToolButton {
    background-color: #f6f8fa;
    color: #24292f;
    border-radius: 8px;
    padding: 10px;
    min-height: 40px;
    font-weight: 600;
}

QCalendarWidget QToolButton:hover {
    background-color: #eaeef2;
}

QCalendarWidget QMenu {
    background-color: #ffffff;
    color: #24292f;
    border: 1px solid #d0d7de;
    border-radius: 8px;
}

QCalendarWidget QWidget#qt_calendar_navigationbar {
    background-color: #f6f8fa;
    border: 1px solid #d0d7de;
    border-radius: 8px;
}

QCalendarWidget QSpinBox {
    background-color: #ffffff;
    color: #24292f;
    border: 1px solid #d0d7de;
    border-radius: 6px;
}

QCalendarWidget QLabel {
    color: #24292f;
}

QCalendarWidget QAbstractItemView {
    background-color: #ffffff;
    color: #24292f;
    selection-background-color: #8250df;
    selection-color: #ffffff;
    gridline-color: #d0d7de;
}

QCalendarWidget QAbstractItemView::item {
    background-color: #ffffff;
    border: none;
}

QCalendarWidget QAbstractItemView::item:selected {
    background-color: #8250df;
    color: #ffffff;
}

QScrollBar:vertical {
    background: #f6f8fa;
    width: 14px;
    border-radius: 7px;
    margin: 2px;
}

QScrollBar::handle:vertical {
    background: qlineargradient(x1:0, y1:0, x2:0, y2:1, stop:0 #d0d7de, stop:1 #afb8c1);
    border-radius: 7px;
    min-height: 40px;
}

QScrollBar::handle:vertical:hover {
    background: qlineargradient(x1:0, y1:0, x2:0, y2:1, stop:0 #8250df, stop:1 #a371f7);
}

QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {
    height: 0px;
}

QDialog {
    background-color: #f6f8fa;
    border-radius: 16px;
}

QMessageBox {
    background-color: #ffffff;
    border-radius: 12px;
}

QMessageBox QLabel {
    color: #24292f;
    font-size: 14px;
}
'''


def get_current_theme():
    return DARK_STYLES if DARK_THEME else LIGHT_STYLES


def toggle_theme():
    global DARK_THEME
    DARK_THEME = not DARK_THEME
    return get_current_theme()


def get_theme_colors():
    if DARK_THEME:
        return {
            'bg_primary': '#0d1117',
            'bg_secondary': '#161b22',
            'bg_tertiary': '#21262d',
            'text_primary': '#c9d1d9',
            'text_secondary': '#8b949e',
            'border': '#30363d',
            'accent': '#1f6feb',
            'success': '#238636',
            'danger': '#da3633',
            'warning': '#d29922',
            'energy_high': '#238636',
            'energy_medium': '#d29922',
            'energy_low': '#da3633',
        }
    else:
        return {
            'bg_primary': '#f6f8fa',
            'bg_secondary': '#ffffff',
            'bg_tertiary': '#f6f8fa',
            'text_primary': '#24292f',
            'text_secondary': '#57606a',
            'border': '#d0d7de',
            'accent': '#8250df',
            'success': '#2da44e',
            'danger': '#cf222e',
            'warning': '#9a6700',
            'energy_high': '#2da44e',
            'energy_medium': '#9a6700',
            'energy_low': '#cf222e',
        }


def is_dark():
    return DARK_THEME