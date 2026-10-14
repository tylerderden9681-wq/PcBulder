from PyQt6.QtWidgets import (
    QDialog, QVBoxLayout, QTextEdit,
    QPushButton, QHBoxLayout, QLabel,
)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QKeySequence, QShortcut


class EditDialog(QDialog):
    """Кастомный диалог для редактирования текста"""

    def __init__(self, title, label_text, initial_text="", parent=None):
        super().__init__(parent)
        self.setWindowTitle(title)
        self.setFixedSize(500, 400)  # ← любой размер!
        self.setObjectName("EditDialog")

        layout = QVBoxLayout(self)
        layout.setSpacing(15)

        # Заголовок
        label = QLabel(label_text)
        label.setObjectName("EditDialogLabel")
        label.setWordWrap(True)
        layout.addWidget(label)

        # Многострочное поле ввода
        self.text_edit = QTextEdit()
        self.text_edit.setObjectName("EditDialogTextEdit")
        self.text_edit.setPlainText(initial_text)
        layout.addWidget(self.text_edit)

        # Кнопки OK / Cancel
        button_layout = QHBoxLayout()
        button_layout.addStretch()

        cancel_button = QPushButton("Отмена")
        cancel_button.setObjectName("EditDialogButton")
        cancel_button.setCursor(Qt.CursorShape.PointingHandCursor)
        cancel_button.setFixedSize(100, 35)
        cancel_button.clicked.connect(self.reject)

        ok_button = QPushButton("Сохранить")
        ok_button.setObjectName("EditDialogButton")
        ok_button.setCursor(Qt.CursorShape.PointingHandCursor)
        ok_button.setFixedSize(100, 35)
        ok_button.clicked.connect(self.accept)

        button_layout.addWidget(cancel_button)
        button_layout.addWidget(ok_button)
        layout.addLayout(button_layout)

        # Настроим хоткеи:
        # Ctrl+Enter -> Сохраняем текст:
        save_shortcut = QShortcut(QKeySequence("Ctrl+Return"), self)
        save_shortcut.activated.connect(self.accept)

    def get_text(self):
        """Возвращает введённый текст"""
        return self.text_edit.toPlainText()
