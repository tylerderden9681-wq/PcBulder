from PyQt6.QtCore import pyqtSignal, QSize, Qt
import qtawesome as qta
from PyQt6.QtWidgets import (
    QFrame, QVBoxLayout, QHBoxLayout,
    QLabel
)


class ProjectCard(QFrame):
    """
    Это кастомный виджет карточки проекта с отслеживанием наведения курсора
    """

    open_project = pyqtSignal(str)

    def __init__(
            self, project_id, project_name, desc,
            price, config, parent=None
    ):
        super().__init__(parent)
        self.project_id = project_id
        self.setObjectName("ProjectCard")
        self.setMinimumHeight(100)
        self.setFixedWidth(730)
        self.setMouseTracking(True)  # <- для того, чтобы отслеживать мышь

        self._build_ui(project_name, desc, price, config)

    def _build_ui(self, project_name, desc, price, config):
        card_layout = QVBoxLayout()
        card_layout.setSpacing(10)

        title_and_desc_layout = QHBoxLayout()

        # --- Заголовок --- :
        icon_label = QLabel()
        icon_label.setPixmap(
            qta.icon(
                "fa6s.diagram-project", color="blue"
            ).pixmap(QSize(15, 15))
        )
        icon_label.setFixedWidth(15)

        project_title_label = QLabel(f"Проект: {project_name}")
        project_title_label.setObjectName("ProjectTitle")

        title_and_desc_layout.addWidget(icon_label)
        title_and_desc_layout.addWidget(project_title_label)
        title_and_desc_layout.setSpacing(5)

        # --- Описание --- :
        project_desc_label = QLabel(f"<b>Описание:</b> {desc}")
        project_desc_label.setObjectName("ProjectDesc")
        project_desc_label.setWordWrap(True)
        title_and_desc_layout.addWidget(project_desc_label)

        card_layout.addLayout(title_and_desc_layout)

        # --- Конфигурация --- :
        config_container_layout = QHBoxLayout()
        config_container_layout.setSpacing(5)
        config_icon_label = QLabel()
        config_icon_label.setPixmap(
            qta.icon("fa6s.microchip", color="black").pixmap(QSize(18, 18))
        )
        config_icon_label.setFixedWidth(18)

        project_config_label = QLabel(f"<b>Конфигурация:</b> {config}")
        project_config_label.setObjectName("ProjectConfig")
        project_config_label.setWordWrap(True)

        config_container_layout.addWidget(config_icon_label)
        config_container_layout.addWidget(project_config_label)
        card_layout.addLayout(config_container_layout)

        # --- Цена + ссылка "Подробнее" (справа) ---
        price_container_layout = QHBoxLayout()
        price_container_layout.setSpacing(5)

        price_icon_label = QLabel()
        price_icon_label.setPixmap(
            qta.icon("fa6s.dollar-sign", color="green").pixmap(QSize(15, 15))
        )
        price_icon_label.setFixedWidth(15)
        price_icon_label.setObjectName("PriceIcon")
        price_icon_label.setAlignment(Qt.AlignmentFlag.AlignRight)

        project_price_label = QLabel(f"Цена: {price} руб.")
        project_price_label.setObjectName("ProjectPrice")
        project_price_label.setAlignment(Qt.AlignmentFlag.AlignRight)

        price_container_layout.addWidget(price_icon_label)
        price_container_layout.addWidget(project_price_label)

        # --- Ссылка "Подробнее" (скрыта по умолчанию) ---
        self.details_link = QLabel(
            f'<a href={self.project_id} style="color: #0078d7; text-decoration: none;">'
            f'Подробнее -></a>'
        )
        self.details_link.setObjectName("DetailsLink")
        self.details_link.setAlignment(Qt.AlignmentFlag.AlignRight)
        self.details_link.setCursor(Qt.CursorShape.PointingHandCursor)
        self.details_link.hide()  # <- по умолчанию скрыта
        # А при клике на нее сразу испускаем сигнал:
        self.details_link.linkActivated.connect(self._on_link_clicked)

        price_container_layout.addStretch()
        price_container_layout.addWidget(self.details_link)

        card_layout.addLayout(price_container_layout)
        self.setLayout(card_layout)

    def _on_link_clicked(self, link):
        self.open_project.emit(link)

    # --- Функции для отслеживания наведения мыши:
    def enterEvent(self, event):
        self.details_link.show()
        return super().enterEvent(event)

    def leaveEvent(self, event):
        self.details_link.hide()
        return super().leaveEvent(event)
