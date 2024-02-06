from PyQt6.QtCore import Qt, pyqtSignal, QRectF
from PyQt6.QtGui import QPainter, QBrush, QColor, QFont, QPainterPath, QConicalGradient, QMouseEvent, QLinearGradient
from PyQt6.QtWidgets import QWidget

class ToggleSwitch(QWidget):
    # Enhanced signal that emits the switch state on toggle
    toggled = pyqtSignal(bool)

    def __init__(self, parent=None, width=60, height=30, on_color="#3498db", off_color="#95a5a6", handle_color="#fff", on_text="", off_text=""):
        super().__init__(parent)
        self.setFixedSize(width, height)
        self._is_on = False

        # Customizable properties
        self._handle_color = QColor(handle_color)
        self._on_color = QColor(on_color)
        self._off_color = QColor(off_color)
        # Initialize default gradients
        self._on_gradient_start = QColor(on_color)
        self._on_gradient_end = QColor(on_color).darker(120)
        self._off_gradient_start = QColor(off_color)
        self._off_gradient_end = QColor(off_color).darker(120)
        # Text
        self._on_text = on_text
        self._off_text = off_text
        self.text_size = 10
        self.text_font = 'Arial'
        self.text_color_on = "#fff"
        self.text_color_off = "#fff"

    # Setting gradients and shadow
    def set_on_gradient(self, start_color, end_color):
        self._on_gradient_start = QColor(start_color)
        self._on_gradient_end = QColor(end_color)
        if self._is_on:
            self.update()

    def set_off_gradient(self, start_color, end_color):
        self._off_gradient_start = QColor(start_color)
        self._off_gradient_end = QColor(end_color)
        if not self._is_on:
            self.update()

    def set_handle_shadow(self, start_color, end_color):
        self._handle_shadow_start = QColor(start_color)
        self._handle_shadow_end = QColor(end_color)
        self.update()

    # Update text size and text font
    def set_text_size(self, text_size):
        self.text_size = text_size
        self.update()

    def set_text_font(self, text_font):
        self.text_font = text_font
        self.update()

    def set_text_color(self, text_color_on, text_color_off):
        self.text_color_on = text_color_on
        self.text_color_off = text_color_off

    # Update paintEvent to use new properties
    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)

        # Draw the background with gradient for 3D effect
        gradient = QLinearGradient(0, 0, 0, self.height())
        if self._is_on:
            gradient.setColorAt(0, self._on_gradient_start)
            gradient.setColorAt(1, self._on_gradient_end)
        else:
            gradient.setColorAt(0, self._off_gradient_start)
            gradient.setColorAt(1, self._off_gradient_end)
        painter.setBrush(QBrush(gradient))
        painter.setPen(Qt.PenStyle.NoPen)  # No border
        painter.drawRoundedRect(0, 0, self.width(), self.height(), self.height() / 2, self.height() / 2)

        # Draw the handle with shadow for 3D effect
        handle_path = QPainterPath()
        handle_radius = self.width() // 2
        handle_position = self.width() - handle_radius - 2 if self._is_on else 2
        handle_path.addEllipse(handle_position, 1, handle_radius, handle_radius)
        shadow_gradient = QConicalGradient(handle_position + handle_radius / 2, self.height() / 2, 45)
        shadow_gradient.setColorAt(0, self._on_gradient_end.lighter(150))
        shadow_gradient.setColorAt(1, self._off_gradient_end.lighter(150))
        painter.setBrush(QBrush(shadow_gradient))
        painter.drawPath(handle_path)

        # Text on the "handle"
        painter.setFont(QFont(self.text_font, self.text_size, QFont.Weight.Bold))
        text = self._on_text if self._is_on else self._off_text
        if text:  # Only draw text if it's not an empty string
            if self._is_on:
                painter.setPen(QColor(self.text_color_on))
                painter.drawText(QRectF(self.width() // 8, 0, self.width() // 1.5, self.height()),
                         Qt.AlignmentFlag.AlignVCenter | Qt.AlignmentFlag.AlignLeft,
                         text)
            else:
                painter.setPen(QColor(self.text_color_off))
                painter.drawText(QRectF(self.width() // 4, 0, self.width() // 1.5, self.height()),
                         Qt.AlignmentFlag.AlignVCenter | Qt.AlignmentFlag.AlignRight,
                         text)

    def mousePressEvent(self, event: QMouseEvent):
        self._is_on = not self._is_on
        self.toggled.emit(self._is_on)
        self.update()

    def is_on(self):
        return self._is_on

    def set_on(self, on):
        if self._is_on != on:
            self._is_on = on
            self.toggled.emit(self._is_on)
            self.update()

    # Methods to customize the switch
    def set_colors(self, on_color, off_color, handle_color):
        self._on_color = QColor(on_color)
        self._off_color = QColor(off_color)
        self._handle_color = QColor(handle_color)
        self.update()

    def set_text(self, on_text, off_text):
        self._on_text = on_text
        self._off_text = off_text
        self.update()

    def set_size(self, width, height):
        self.setFixedSize(width, height)
        self.update()
