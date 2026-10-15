from PyQt6.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QLabel,
    QLineEdit, QPushButton, QScrollArea, QWidget, QFrame,
    QMessageBox
)
from PyQt6.QtGui import QKeySequence, QShortcut
from PyQt6.QtCore import Qt


class ConfigDialog(QDialog):
    """
    Диалоговое окно для настройки конфигурации проекта.
    Позволяет заполнить характеристики сборки: CPU, GPU, RAM и т.д.
    """

    def __init__(self, project_name, parent=None):
        super().__init__(parent)
        self.project_name = project_name
        self.setWindowTitle(f"Конфигурация: {project_name}")
        self.setFixedSize(550, 650)
        self.setObjectName("ConfigDialog")

        self._build_ui()

    def _build_ui(self):
        layout = QVBoxLayout(self)
        layout.setSpacing(10)
        layout.setContentsMargins(20, 20, 20, 20)

        # === Заголовок ===
        title_label = QLabel(f"Настройка сборки «{self.project_name}»")
        title_label.setObjectName("ConfigDialogTitle")
        title_label.setWordWrap(True)
        layout.addWidget(title_label)

        # === Подсказка ===
        hint_label = QLabel(
            "Заполните характеристики сборки. Поля можно оставить пустыми."
        )
        hint_label.setObjectName("ConfigDialogHint")
        hint_label.setWordWrap(True)
        layout.addWidget(hint_label)

        # === Скролл для полей ===
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setFrameShape(QFrame.Shape.NoFrame)
        scroll.setObjectName("ConfigDialogScroll")

        fields_widget = QWidget()
        fields_widget.setObjectName("ConfigDialogFields")
        fields_layout = QVBoxLayout(fields_widget)
        fields_layout.setSpacing(8)

        # === Поля конфигурации ===
        # Формат: (ключ_в_словаре, текст_метки, placeholder)
        self.inputs = {}
        fields = [
            ("cpu", "Процессор", "Например: Intel Core i5-13400K"),
            ("gpu", "Видеокарта", "Например: NVIDIA RTX 4060 8GB"),
            ("mat", "Материнская плата", "Например: ASUS ROG Strix B760-G"),
            ("ram", "Оперативная память",
             "Например: Kingston 32GB DDR5 5600MHz"
             ),
            ("ssd", "Накопитель (SSD)", "Например: Samsung 980 Pro 1TB"),
            ("case", "Корпус", "Например: NZXT H5 Flow"),
            ("cooling", "Охлаждение", "Например: DeepCool AK400"),
            ("pb", "Блок питания", "Например: DeepCool PX850W"),
            ("price", "Стоимость (руб.)", "Например: 64990"),
        ]

        for key, label_text, placeholder in fields:
            row = QHBoxLayout()
            row.setSpacing(10)

            # Метка слева
            label = QLabel(label_text)
            label.setObjectName("ConfigDialogLabel")
            label.setFixedWidth(160)
            row.addWidget(label)

            # Поле ввода справа
            line_edit = QLineEdit()
            line_edit.setObjectName("ConfigDialogInput")
            line_edit.setPlaceholderText(placeholder)
            row.addWidget(line_edit)

            # Сохраняем ссылку на поле, чтобы потом получить значение
            self.inputs[key] = line_edit
            fields_layout.addLayout(row)

        scroll.setWidget(fields_widget)
        layout.addWidget(scroll)

        # === Кнопки ===
        btn_layout = QHBoxLayout()
        btn_layout.addStretch()

        skip_btn = QPushButton("Пропустить")
        skip_btn.setObjectName("DialogButtonSecondary")
        skip_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        skip_btn.setFixedSize(100, 35)
        skip_btn.clicked.connect(self.accept)

        save_btn = QPushButton("Сохранить")
        save_btn.setObjectName("DialogButtonPrimary")
        save_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        save_btn.setFixedSize(120, 35)
        save_btn.clicked.connect(self.validate_and_accept)

        btn_layout.addWidget(skip_btn)
        btn_layout.addWidget(save_btn)
        layout.addLayout(btn_layout)

        # === Хоткеи ===
        # Ctrl+Enter или Ctrl+S → сохранить
        QShortcut(QKeySequence("Ctrl+Return"), self).activated.connect(
            self.validate_and_accept
        )
        QShortcut(QKeySequence("Ctrl+S"), self).activated.connect(
            self.validate_and_accept
        )
        # Escape → пропустить (закрыть без заполнения)
        QShortcut(QKeySequence("Escape"), self).activated.connect(self.accept)

    def validate_and_accept(self):
        """Проверяет, что цена — это число (если введена)"""
        price_text = self.inputs["price"].text().strip()
        if price_text and not price_text.isdigit():
            QMessageBox.warning(
                self,
                "Ошибка",
                "Стоимость должна быть числом (например: 64990)"
            )
            self.inputs["price"].setFocus()
            return
        self.accept()

    def get_config_data(self):
        """
        Возвращает словарь с введёнными данными.
        Если поле пустое — подставляет "Не указано".
        """
        data = {}
        for key, line_edit in self.inputs.items():
            value = line_edit.text().strip()
            data[key] = value if value else "Не указано"

        # Если цена пустая — ставим 0
        if data["price"] == "Не указано":
            data["price"] = "0"

        return data
