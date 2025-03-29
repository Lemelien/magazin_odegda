from PySide6.QtWidgets import (QApplication, QMainWindow, QVBoxLayout, QWidget, QHBoxLayout, QLabel, QPushButton, 
                               QLineEdit, QComboBox, QDialog, QFormLayout, QGroupBox, QScrollArea, QMessageBox, 
                               QGridLayout, QSizePolicy, QFrame, QGraphicsOpacityEffect)
from PySide6.QtGui import QPixmap, QFont, QIcon, QPalette, QColor
from PySide6.QtCore import Qt, QPropertyAnimation, QSize, QEasingCurve
import sys
from user_class import Connect, Brand, Category, ClothingItem, Order, OrderItem, User

# Тест на стиль
class StyleQuizDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Найди свой стиль!")
        self.setFixedSize(600, 700)
        self.setStyleSheet("""
            background-color: #f5e6f5;
            font-family: 'Arial', sans-serif;
            color: #000000;
        """)
        self.answers = {}
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()
        layout.setSpacing(20)

        welcome_label = QLabel("Привет! Давай узнаем, какой стиль тебе подходит!")
        welcome_label.setFont(QFont("Arial", 18, QFont.Bold))
        welcome_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(welcome_label)

        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll_content = QWidget()
        scroll_layout = QVBoxLayout(scroll_content)
        scroll_layout.setSpacing(15)

        questions = [
            ("Какой твой идеальный выходной?", ["Прогулка по городу, кофе, шопинг", "День на природе: пикник, лес", 
                                                "Вечеринка с друзьями", "Домашний вечер: сериалы, чай"]),
            ("Какой цвет ты чаще выбираешь в одежде?", ["Черный, белый, нейтральное", "Земляные тона: бежевый, оливковый", 
                                                        "Яркие: красный, неон", "Пастельные: розовый, голубой"]),
            ("Что важнее в одежде?", ["Дорого и элегантно", "Удобство и натуральность", "Чтобы заметили", "Мило и уютно"]),
            ("Какой аксессуар ты бы взял?", ["Часы или кольцо", "Шляпа или тканевая сумка", "Большие серьги или шарф", 
                                             "Ободок или заколки"]),
            ("Как относишься к трендам?", ["Только вечные вещи", "Люблю природные тренды", "Обожаю новое и необычное", 
                                           "Беру милые тренды"])
        ]

        self.buttons = {}
        for i, (question, options) in enumerate(questions):
            group = QGroupBox(question)
            group.setStyleSheet("""
                QGroupBox { 
                    font-size: 16px; 
                    font-weight: bold; 
                    border: 2px solid #d4a5d4; 
                    border-radius: 10px; 
                    padding: 10px; 
                    margin-top: 10px;
                    color: #000000;
                }
                QGroupBox::title { 
                    subcontrol-origin: margin; 
                    subcontrol-position: top center; 
                    padding: 0 5px;
                }
            """)
            group_layout = QVBoxLayout()
            for j, option in enumerate(options):
                btn = QPushButton(option)
                btn.setStyleSheet("""
                    QPushButton {
                        background-color: #ffffff;
                        color: #000000;
                        padding: 10px;
                        border: 1px solid #d4a5d4;
                        border-radius: 8px;
                        font-size: 14px;
                    }
                    QPushButton:hover {
                        background-color: #e6c9e6;
                    }
                    QPushButton:pressed {
                        background-color: #d4a5d4;
                        color: white;
                    }
                """)
                btn.clicked.connect(lambda checked, q=i, a=j: self.select_answer(q, a))
                group_layout.addWidget(btn)
                self.buttons[(i, j)] = btn
            group.setLayout(group_layout)
            scroll_layout.addWidget(group)

        scroll.setWidget(scroll_content)
        layout.addWidget(scroll)

        submit_btn = QPushButton("Узнать мой стиль!")
        submit_btn.setStyleSheet("""
            background-color: #d4a5d4;
            color: white;
            padding: 12px;
            border-radius: 10px;
            font-size: 16px;
            font-weight: bold;
        """)
        submit_btn.clicked.connect(self.calculate_style)
        layout.addWidget(submit_btn, alignment=Qt.AlignCenter)

        self.setLayout(layout)

    def select_answer(self, question, answer):
        self.answers[question] = answer
        for i in range(4):
            btn = self.buttons[(question, i)]
            if i == answer:
                btn.setStyleSheet("""
                    background-color: #d4a5d4;
                    color: white;
                    padding: 10px;
                    border: 1px solid #d4a5d4;
                    border-radius: 8px;
                    font-size: 14px;
                """)
            else:
                btn.setStyleSheet("""
                    background-color: #ffffff;
                    color: #000000;
                    padding: 10px;
                    border: 1px solid #d4a5d4;
                    border-radius: 8px;
                    font-size: 14px;
                """)

    def calculate_style(self):
        if len(self.answers) != 5:
            QMessageBox.warning(self, "Ошибка", "Ответьте на все вопросы!")
            return
        
        style_scores = {'A': 0, 'B': 0, 'C': 0, 'D': 0}
        for answer in self.answers.values():
            style_scores[chr(65 + answer)] += 1
        
        max_style = max(style_scores, key=style_scores.get)
        styles = {
            'A': ("Минимализм и классика", "Ты любишь чистые линии и timeless образы. Идеально подойдут строгие пальто, белые рубашки и классические джинсы."),
            'B': ("Бохо или эко-стиль", "Ты душа природы! Свободные силуэты, натуральные ткани и уютные кардиганы — твой стиль."),
            'C': ("Смелый и экстравагантный", "Ты звезда! Яркие цвета, необычные сочетания и statement-вещи — это про тебя."),
            'D': ("Коттеджкор или романтика", "Твой стиль — нежность и уют. Платья с цветочным принтом и пастельные оттенки созданы для тебя.")
        }
        self.result = styles[max_style]
        self.accept()

# Окно с подробностями о товаре
class ItemViewDialog(QDialog):
    def __init__(self, item, parent=None):
        super().__init__(parent)
        self.setWindowTitle(f"{item.название}")
        self.setFixedSize(500, 600)
        self.setStyleSheet("""
            background-color: #fff0ff;
            font-family: 'Arial', sans-serif;
            color: #000000;
            border-radius: 15px;
        """)
        self.item = item
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()
        layout.setSpacing(20)

        # Заголовок
        title = QLabel(f"{self.item.название}")
        title.setFont(QFont("Arial", 22, QFont.Bold))
        title.setAlignment(Qt.AlignCenter)
        layout.addWidget(title)

        # Изображение
        image_frame = QFrame()
        image_frame.setStyleSheet("border: 2px solid #d4a5d4; border-radius: 10px; background-color: white;")
        image_layout = QVBoxLayout()
        image_label = QLabel()
        if self.item.изображение:
            pixmap = QPixmap(self.item.изображение).scaled(200, 200, Qt.KeepAspectRatio, Qt.SmoothTransformation)
            image_label.setPixmap(pixmap)
        else:
            image_label.setText("Нет изображения")
        image_label.setAlignment(Qt.AlignCenter)
        image_layout.addWidget(image_label)
        image_frame.setLayout(image_layout)
        layout.addWidget(image_frame)

        # Характеристики
        info_group = QGroupBox("Характеристики")
        info_group.setStyleSheet("""
            QGroupBox {
                font-size: 16px;
                font-weight: bold;
                border: 2px solid #d4a5d4;
                border-radius: 10px;
                margin-top: 10px;
                color: #000000;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                subcontrol-position: top center;
                padding: 0 5px;
            }
        """)
        info_layout = QFormLayout()
        info_layout.setSpacing(10)
        info_layout.addRow("Бренд:", QLabel(self.item.бренд.название))
        info_layout.addRow("Категория:", QLabel(self.item.категория.название))
        info_layout.addRow("Цена:", QLabel(f"{self.item.цена:.2f} руб."))
        info_layout.addRow("Цвет:", QLabel(self.item.цвет))
        info_layout.addRow("Размер:", QLabel(self.item.размер))
        info_layout.addRow("Описание:", QLabel(self.item.описание or "Нет описания"))
        info_group.setLayout(info_layout)
        layout.addWidget(info_group)

        # Кнопка закрытия
        close_btn = QPushButton("Закрыть")
        close_btn.setStyleSheet("""
            background-color: #d4a5d4;
            color: white;
            padding: 12px;
            border-radius: 10px;
            font-size: 16px;
            font-weight: bold;
        """)
        close_btn.clicked.connect(self.close)
        layout.addWidget(close_btn, alignment=Qt.AlignCenter)

        self.setLayout(layout)

# Главное окно
class FashionMainWindow(QMainWindow):
    def __init__(self, user):
        super().__init__()
        self.user = user
        self.session = Connect.create_connection()
        self.setWindowTitle(f"StyleFinder - {self.user.имя_пользователя}")
        self.setGeometry(100, 100, 1400, 900)
        self.setStyleSheet("""
            background-color: #f5e6f5;
            font-family: 'Arial', sans-serif;
            color: #000000;
        """)
        self.cart = []

        # Пройти тест на стиль
        self.style = None
        self.show_style_quiz()
        self.init_ui()

    def show_style_quiz(self):
        quiz = StyleQuizDialog(self)
        if quiz.exec():
            self.style = quiz.result
            QMessageBox.information(self, "Твой стиль", f"Твой стиль: {self.style[0]}\n{self.style[1]}")

    def init_ui(self):
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout(central_widget)
        main_layout.setSpacing(20)

        # Верхняя панель с поиском и фильтрами
        top_bar = QHBoxLayout()
        top_bar.setSpacing(15)

        # Разворачиваемый поиск
        search_frame = QFrame()
        search_frame.setFixedHeight(40)
        search_layout = QHBoxLayout(search_frame)
        search_layout.setContentsMargins(0, 0, 0, 0)
        
        self.search_icon = QPushButton()
        self.search_icon.setIcon(QIcon("search_icon.png"))  # Замените на ваш путь к иконке
        self.search_icon.setFixedSize(40, 40)
        self.search_icon.setStyleSheet("""
            background-color: transparent;
            border: none;
        """)
        self.search_icon.enterEvent = lambda e: self.expand_search()
        self.search_icon.leaveEvent = lambda e: self.collapse_search()
        
        self.search_input = QLineEdit()
        self.search_input.setFixedWidth(0)  # Начальная ширина 0
        self.search_input.setStyleSheet("""
            border: 2px solid #d4a5d4;
            border-radius: 10px;
            padding: 5px;
            font-size: 14px;
            color: #000000;
            background-color: white;
        """)
        self.search_input.textChanged.connect(self.filter_items)

        search_layout.addWidget(self.search_icon)
        search_layout.addWidget(self.search_input)
        top_bar.addWidget(search_frame)

        # Фильтры
        self.brand_combo = QComboBox()
        self.brand_combo.addItem("Все бренды", 0)
        for brand in self.session.query(Brand).all():
            self.brand_combo.addItem(brand.название, brand.id)
        self.brand_combo.setStyleSheet("padding: 8px; border: 2px solid #d4a5d4; border-radius: 10px;")
        self.brand_combo.currentIndexChanged.connect(self.filter_items)
        top_bar.addWidget(QLabel("Бренд:"))
        top_bar.addWidget(self.brand_combo)

        self.category_combo = QComboBox()
        self.category_combo.addItem("Все категории", 0)
        for cat in self.session.query(Category).all():
            self.category_combo.addItem(cat.название, cat.id)
        self.category_combo.setStyleSheet("padding: 8px; border: 2px solid #d4a5d4; border-radius: 10px;")
        self.category_combo.currentIndexChanged.connect(self.filter_items)
        top_bar.addWidget(QLabel("Категория:"))
        top_bar.addWidget(self.category_combo)

        top_bar.addStretch()
        
        cart_btn = QPushButton("Корзина")
        cart_btn.setStyleSheet("""
            background-color: #d4a5d4;
            color: white;
            padding: 10px;
            border-radius: 10px;
            font-size: 14px;
        """)
        cart_btn.clicked.connect(self.show_cart)
        top_bar.addWidget(cart_btn)

        orders_btn = QPushButton("Мои заказы")
        orders_btn.setStyleSheet("""
            background-color: #d4a5d4;
            color: white;
            padding: 10px;
            border-radius: 10px;
            font-size: 14px;
        """)
        orders_btn.clicked.connect(self.view_orders)
        top_bar.addWidget(orders_btn)

        main_layout.addLayout(top_bar)

        # Область с товарами
        self.items_widget = QWidget()
        self.items_layout = QGridLayout(self.items_widget)
        self.items_layout.setSpacing(20)
        
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setWidget(self.items_widget)
        scroll.setStyleSheet("border: none;")
        main_layout.addWidget(scroll)

        self.load_items()

    def expand_search(self):
        anim = QPropertyAnimation(self.search_input, b"minimumWidth")
        anim.setDuration(300)
        anim.setStartValue(0)
        anim.setEndValue(300)
        anim.setEasingCurve(QEasingCurve.InOutQuad)
        anim.start()

    def collapse_search(self):
        if not self.search_input.text():
            anim = QPropertyAnimation(self.search_input, b"minimumWidth")
            anim.setDuration(300)
            anim.setStartValue(300)
            anim.setEndValue(0)
            anim.setEasingCurve(QEasingCurve.InOutQuad)
            anim.start()

    def load_items(self):
        for i in range(self.items_layout.count()):
            self.items_layout.itemAt(i).widget().deleteLater()
        
        items = self.session.query(ClothingItem).all()
        for index, item in enumerate(items):
            card = self.create_item_card(item)
            self.items_layout.addWidget(card, index // 4, index % 4)

    def create_item_card(self, item):
        card = QFrame()
        card.setFixedSize(300, 400)
        card.setStyleSheet("""
            background-color: white;
            border: 2px solid #d4a5d4;
            border-radius: 15px;
            padding: 10px;
        """)
        layout = QVBoxLayout(card)

        # Изображение
        image_label = QLabel()
        if item.изображение:
            pixmap = QPixmap(item.изображение).scaled(250, 250, Qt.KeepAspectRatio, Qt.SmoothTransformation)
            image_label.setPixmap(pixmap)
        else:
            image_label.setText("Нет изображения")
        image_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(image_label)

        # Название и бренд
        name_label = QLabel(f"{item.название}")
        name_label.setFont(QFont("Arial", 14, QFont.Bold))
        name_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(name_label)

        brand_label = QLabel(f"{item.бренд.название}")
        brand_label.setStyleSheet("font-size: 12px; color: #666;")
        brand_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(brand_label)

        # Цена
        price_label = QLabel(f"{item.цена:.2f} руб.")
        price_label.setFont(QFont("Arial", 12))
        price_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(price_label)

        # Кнопки
        btn_layout = QHBoxLayout()
        view_btn = QPushButton("Подробнее")
        view_btn.setStyleSheet("""
            background-color: #d4a5d4;
            color: white;
            padding: 8px;
            border-radius: 8px;
            font-size: 12px;
        """)
        view_btn.clicked.connect(lambda: self.view_item(item))
        btn_layout.addWidget(view_btn)

        cart_btn = QPushButton("В корзину")
        cart_btn.setStyleSheet("""
            background-color: #a5d4a5;
            color: white;
            padding: 8px;
            border-radius: 8px;
            font-size: 12px;
        """)
        cart_btn.clicked.connect(lambda: self.add_to_cart(item))
        btn_layout.addWidget(cart_btn)

        layout.addLayout(btn_layout)

        return card

    def filter_items(self):
        for i in range(self.items_layout.count()):
            self.items_layout.itemAt(i).widget().deleteLater()

        query = self.session.query(ClothingItem)
        brand_id = self.brand_combo.currentData()
        category_id = self.category_combo.currentData()
        search_text = self.search_input.text().lower()

        if brand_id != 0:
            query = query.filter(ClothingItem.бренд_id == brand_id)
        if category_id != 0:
            query = query.filter(ClothingItem.категория_id == category_id)
        if search_text:
            query = query.filter(ClothingItem.название.ilike(f"%{search_text}%"))

        items = query.all()
        for index, item in enumerate(items):
            card = self.create_item_card(item)
            self.items_layout.addWidget(card, index // 4, index % 4)

    def view_item(self, item):
        dialog = ItemViewDialog(item, self)
        dialog.exec()

    def add_to_cart(self, item):
        self.cart.append(item)
        QMessageBox.information(self, "Успех", f"{item.название} добавлен в корзину!")

    def show_cart(self):
        if not self.cart:
            QMessageBox.warning(self, "Корзина", "Корзина пуста!")
            return
        
        dialog = QDialog(self)
        dialog.setWindowTitle("Ваша корзина")
        dialog.setFixedSize(600, 400)
        dialog.setStyleSheet("background-color: #f5e6f5; color: #000000;")
        layout = QVBoxLayout()

        total = 0
        for item in self.cart:
            item_label = QLabel(f"{item.название} ({item.бренд.название}) - {item.цена:.2f} руб.")
            item_label.setStyleSheet("font-size: 14px;")
            layout.addWidget(item_label)
            total += item.цена

        total_label = QLabel(f"Итого: {total:.2f} руб.")
        total_label.setFont(QFont("Arial", 16, QFont.Bold))
        layout.addWidget(total_label)

        # Кнопки управления корзиной
        button_layout = QHBoxLayout()
        
        order_btn = QPushButton("Оформить заказ")
        order_btn.setStyleSheet("""
            background-color: #d4a5d4;
            color: white;
            padding: 10px;
            border-radius: 10px;
            font-size: 14px;
        """)
        order_btn.clicked.connect(lambda: self.create_order(dialog))
        button_layout.addWidget(order_btn)

        clear_cart_btn = QPushButton("Очистить корзину")
        clear_cart_btn.setStyleSheet("""
            background-color: #ff4d4d;
            color: white;
            padding: 10px;
            border-radius: 10px;
            font-size: 14px;
        """)
        clear_cart_btn.clicked.connect(lambda: self.clear_cart(dialog))
        button_layout.addWidget(clear_cart_btn)

        close_btn = QPushButton("Закрыть")
        close_btn.setStyleSheet("""
            background-color: #a5a5a5;
            color: white;
            padding: 10px;
            border-radius: 10px;
            font-size: 14px;
        """)
        close_btn.clicked.connect(dialog.close)
        button_layout.addWidget(close_btn)

        layout.addLayout(button_layout)
        dialog.setLayout(layout)
        dialog.exec()

    def clear_cart(self, dialog):
        reply = QMessageBox.question(self, "Подтверждение", "Вы уверены, что хотите очистить корзину?",
                                     QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if reply == QMessageBox.Yes:
            self.cart.clear()
            dialog.close()
            QMessageBox.information(self, "Успех", "Корзина очищена!")

    def create_order(self, dialog):
        total = sum(item.цена for item in self.cart)
        order_items = [OrderItem(товар_id=item.id, количество=1, цена_за_единицу=item.цена) for item in self.cart]
        new_order = Order(пользователь_id=self.user.id, общая_сумма=total, товары=order_items)
        self.session.add(new_order)
        self.session.commit()
        self.cart.clear()
        QMessageBox.information(self, "Успех", f"Заказ на {total:.2f} руб. оформлен!")
        dialog.close()

    def view_orders(self):
        dialog = OrdersDialog(self.user, self.session, self)
        dialog.exec()

class OrdersDialog(QDialog):
    def __init__(self, user, session, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Мои заказы")
        self.setFixedSize(600, 400)
        self.setStyleSheet("background-color: #f5e6f5; color: #000000;")
        self.session = session
        self.user = user
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll_content = QWidget()
        scroll_layout = QVBoxLayout(scroll_content)

        orders = self.session.query(Order).filter_by(пользователь_id=self.user.id).all()
        for order in orders:
            order_frame = QFrame()
            order_frame.setStyleSheet("border: 2px solid #d4a5d4; border-radius: 10px; padding: 10px;")
            order_layout = QVBoxLayout()
            order_layout.addWidget(QLabel(f"Заказ #{order.id} от {order.дата_заказа.strftime('%Y-%m-%d')}"))
            order_layout.addWidget(QLabel(f"Сумма: {order.общая_сумма:.2f} руб."))
            order_layout.addWidget(QLabel(f"Статус: {order.статус}"))
            order_frame.setLayout(order_layout)
            scroll_layout.addWidget(order_frame)

        scroll.setWidget(scroll_content)
        layout.addWidget(scroll)

        close_btn = QPushButton("Закрыть")
        close_btn.setStyleSheet("""
            background-color: #d4a5d4;
            color: white;
            padding: 10px;
            border-radius: 10px;
            font-size: 14px;
        """)
        close_btn.clicked.connect(self.close)
        layout.addWidget(close_btn)

        self.setLayout(layout)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    # Предположим, что у нас есть тестовый пользователь
    session = Connect.create_connection()
    test_user = session.query(User).first()  # Замените на реального пользователя
    if not test_user:
        test_user = User(имя_пользователя="test", пароль="123", email="test@example.com")
        session.add(test_user)
        session.commit()
    window = FashionMainWindow(test_user)
    window.show()
    sys.exit(app.exec())