from PyQt6 import QtCore
from PyQt6.QtGui import QPainter, QPen
from PyQt6.QtWidgets import QCheckBox

class SwitchButton(QCheckBox):
    """
    Switch button is a QCheckBox with a custom paint event.
    """

    def __init__(self, parent=None):
        super().__init__(parent)

    def paintEvent(self, event):
        # Adjust dimensions for a slightly larger toggle switch
        rect_height = int(0.6 * self.rect().height())
        circle_radius = int(0.8 * rect_height)
        rect_width = int(2 * circle_radius)

        offset = self.rect().width() - rect_width
        x_rect = int(self.rect().x() + offset / 2)
        y_rect = int(self.rect().y() + (self.rect().height() - rect_height) / 2)

        x_circle = x_rect
        y_circle = y_rect

        if not self.isChecked():
            x_circle += circle_radius

        foreground_color = self.palette().light().color()
        background_color = (
            self.palette().dark().color()
            if self.isChecked()
            else self.palette().highlight().color()
        )

        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        painter.setPen(QPen(background_color))
        painter.setBrush(background_color)
        painter.drawRoundedRect(
            x_rect,
            y_rect,
            rect_width,
            rect_height,
            0.5 * rect_height,
            0.5 * rect_height,
        )
        painter.setPen(QPen(foreground_color))
        painter.setBrush(foreground_color)
        painter.drawEllipse(x_circle, y_circle, circle_radius, circle_radius)
        painter.end()

    def mousePressEvent(self, event):
        self.setChecked(not self.isChecked())  # Corrected boolean negation
        self.clicked.emit(self.isChecked())
        super().mousePressEvent(event)

    def sizeHint(self):
        # Adjust size hint to be a little larger
        return QtCore.QSize(60, 30)
