from PyQt6.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout,
    QLabel, QLineEdit, QTextEdit,
    QPushButton, QMessageBox
)
from PyQt6.QtCore import Qt


class CreateProjectDialog(QDialog):
    """Это диалоговое окно для создания нового проекта"""

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Создание нового проекта")
        self.setFixedSize(450, 350)
        self.setObjectName("CreateProjectDialog")

        layout = QVBoxLayout(self)
        layout.setSpacing(15)

        # Заголовок:
        title_label = QLabel("Давайте создадим новый проект")
        title_label.setObjectName("DialogTitle")
        layout.addWidget(title_label)

        # Поле ввода названия
        layout.addWidget(QLabel("Название проекта:"))
        self.name_input = QLineEdit()
        self.name_input.setObjectName("DialogInput")
        self.name_input.setPlaceholderText("Например: Игровой ПК за 30к")
        layout.addWidget(self.name_input)

        # Поле ввода описания
        layout.addWidget(QLabel("Описание проекта:"))
        self.desc_input = QTextEdit()
        self.desc_input.setObjectName("DialogInput")
        self.desc_input.setMaximumHeight(80)
        self.desc_input.setPlaceholderText(
            "Краткое описание проекта и её назначение..."
        )
        layout.addWidget(self.desc_input)
        layout.addStretch()

        # Кнопки:
        btn_layout = QHBoxLayout()
        btn_layout.addStretch()

        cancel_btn = QPushButton("Отмена")
        cancel_btn.setObjectName("DialogButtonSecondary")
        cancel_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        cancel_btn.setFixedSize(100, 35)
        cancel_btn.clicked.connect(self.reject)

        continue_btn = QPushButton("Продолжить")
        continue_btn.setObjectName("DialogButtonPrimary")
        continue_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        continue_btn.setFixedSize(100, 35)
        continue_btn.clicked.connect(self.validate_and_accept)

        btn_layout.addWidget(cancel_btn)
        btn_layout.addWidget(continue_btn)
        layout.addLayout(btn_layout)

    def validate_and_accept(self):
        """Проверяет данные при закрытии окна"""
        name = self.name_input.text().strip()

        if not name:
            QMessageBox.warning(
                self, "Ошибка", "Название проекта не должно быть пустым!"
            )
            return

        desc = self.desc_input.toPlainText().strip()

        if not desc:
            QMessageBox.warning(
                self, "Ошибка", "Описание проекта не должно быть пустым!"
            )
            return

        return self.accept()

    def get_data(self):
        """Возвращает данные, которые ввел пользователь в виде словаря"""
        return {
            "name": self.name_input.text().strip(),
            "description": self.desc_input.toPlainText().strip(),
        }
