import sys
from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtGui import QPainter, QBrush, QColor, QFont, QPen, QPainterPath, QMouseEvent, QLinearGradient, QConicalGradient
from PyQt6.QtWidgets import QApplication, QWidget

class ToggleSwitch(QWidget):
    # Signal to emit when the switch is toggled
    toggled = pyqtSignal(bool)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setFixedSize(150, 50)  # Updated size
        self._is_on = False  # The switch state
        self._handle_color = QColor('#fff')  # Handle color
        self._on_color = QColor('#3498db')  # On state color
        self._off_color = QColor('#95a5a6')  # Off state color

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)

        # Draw the background with gradient for 3D effect
        bg_color = self._on_color if self._is_on else self._off_color
        gradient = QLinearGradient(0, 0, 0, self.height())
        gradient.setColorAt(0, bg_color.lighter(120))
        gradient.setColorAt(1, bg_color.darker(120))
        painter.setBrush(QBrush(gradient))
        painter.setPen(Qt.PenStyle.NoPen)  # No border
        painter.drawRoundedRect(0, 0, self.width(), self.height(), self.height() / 2, self.height() / 2)

        # Draw the handle with shadow for 3D effect
        handle_path = QPainterPath()
        handle_radius = self.height() - 4
        handle_position = self.width() - handle_radius - 2 if self._is_on else 2
        handle_path.addEllipse(handle_position, 2, handle_radius, handle_radius)
        shadow_gradient = QConicalGradient(handle_position + handle_radius / 2, self.height() / 2, 45)
        shadow_gradient.setColorAt(0, self._handle_color.darker(150))
        shadow_gradient.setColorAt(1, self._handle_color.lighter(150))
        painter.setBrush(QBrush(shadow_gradient))
        painter.drawPath(handle_path)

        # Draw the text
        painter.setPen(QColor('#fff' if self._is_on else '#000'))  # Text color
        painter.setFont(QFont('Arial', 12, QFont.Weight.Bold))  # Slightly bigger font
        text = "Happy" if self._is_on else "Sad"
        painter.drawText(self.rect(), Qt.AlignmentFlag.AlignCenter, text)

    def mousePressEvent(self, event: QMouseEvent):
        self._is_on = not self._is_on
        self.toggled.emit(self._is_on)
        self.update()  # Trigger a repaint

    def is_on(self):
        return self._is_on

    def set_on(self, on):
        self._is_on = on
        self.update()

# Example Usage
class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Custom Toggle Switch Example')
        self.setGeometry(100, 100, 300, 150)  # Adjusted for new switch size

        # Initialize the switch button
        self.switch_button = ToggleSwitch(self)
        self.switch_button.move(75, 50)  # Centered
        self.switch_button.toggled.connect(self.on_toggled)

    def on_toggled(self, is_on):
        print('Switch is on:', is_on)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
