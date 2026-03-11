import sys
from PyQt6.QtWidgets import QApplication
from PyQt6.QtGui import QColor, QPalette
from styles import DARK_THEME
from windows import LoginWindow

if __name__ == '__main__':
    app = QApplication(sys.argv)
    app.setStyle('Fusion')

    palette = QPalette()
    if DARK_THEME:
        palette.setColor(QPalette.ColorRole.Window, QColor('#0d1117'))
        palette.setColor(QPalette.ColorRole.WindowText, QColor('#c9d1d9'))
        palette.setColor(QPalette.ColorRole.Base, QColor('#161b22'))
        palette.setColor(QPalette.ColorRole.Text, QColor('#c9d1d9'))
        palette.setColor(QPalette.ColorRole.Button, QColor('#21262d'))
        palette.setColor(QPalette.ColorRole.ButtonText, QColor('#c9d1d9'))
        palette.setColor(QPalette.ColorRole.Highlight, QColor('#1f6feb'))
    else:
        palette.setColor(QPalette.ColorRole.Window, QColor('#f6f8fa'))
        palette.setColor(QPalette.ColorRole.WindowText, QColor('#24292f'))
        palette.setColor(QPalette.ColorRole.Base, QColor('#ffffff'))
        palette.setColor(QPalette.ColorRole.Text, QColor('#24292f'))
        palette.setColor(QPalette.ColorRole.Button, QColor('#f6f8fa'))
        palette.setColor(QPalette.ColorRole.ButtonText, QColor('#24292f'))
        palette.setColor(QPalette.ColorRole.Highlight, QColor('#0969da'))

    app.setPalette(palette)
    login = LoginWindow()
    login.show()
    sys.exit(app.exec())