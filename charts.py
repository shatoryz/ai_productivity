from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg
from matplotlib.figure import Figure
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QSizePolicy
from styles import get_theme_colors


class Chart(QWidget):
    def __init__(self, width=8, height=4, dpi=100, parent=None):
        super().__init__(parent)
        self.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Preferred)
        self.setMinimumHeight(250)
        self._update_colors()

        self.fig = Figure(figsize=(width, height), dpi=dpi, facecolor=self.bg_color)
        self.fig.tight_layout()
        self.axes = self.fig.add_subplot(111)
        self.axes.set_facecolor(self.bg_color)
        self.axes.tick_params(colors=self.text_color, labelsize=10)
        for spine in self.axes.spines.values():
            spine.set_color(self.border_color)

        self.canvas = FigureCanvasQTAgg(self.fig)
        self.canvas.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Preferred)
        self.canvas.setParent(self)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(5, 5, 5, 5)
        layout.addWidget(self.canvas)

    def _update_colors(self):
        colors = get_theme_colors()
        self.bg_color = colors['bg_secondary']
        self.text_color = colors['text_primary']
        self.border_color = colors['border']

    def update_theme(self):
        self._update_colors()
        self.fig.set_facecolor(self.bg_color)
        self.axes.set_facecolor(self.bg_color)
        self.axes.tick_params(colors=self.text_color, labelsize=10)
        for spine in self.axes.spines.values():
            spine.set_color(self.border_color)
        for text in self.axes.texts:
            text.set_color(self.text_color)
        if self.axes.get_title():
            self.axes.set_title(self.axes.get_title(), color=self.text_color)
        if self.axes.get_xlabel():
            self.axes.set_xlabel(self.axes.get_xlabel(), color=self.text_color)
        if self.axes.get_ylabel():
            self.axes.set_ylabel(self.axes.get_ylabel(), color=self.text_color)

    def draw(self):
        self.fig.tight_layout()
        self.canvas.draw()
        self.canvas.flush_events()

    def clear(self):
        self._update_colors()
        self.axes.clear()
        self.axes.set_facecolor(self.bg_color)
        self.axes.tick_params(colors=self.text_color, labelsize=10)
        for spine in self.axes.spines.values():
            spine.set_color(self.border_color)