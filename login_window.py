from PySide6.QtWidgets import QMainWindow, QVBoxLayout, QWidget, QLabel, QLineEdit, QPushButton, QMessageBox
from PySide6.QtCore import Qt
from user_class import Connect, User
from main_window import FashionMainWindow

class LoginWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Вход в Fashion Store")
        self.setFixedSize(400, 300)
        self.setStyleSheet("""
            background-color: #f7e8f7;
            font-family: 'Roboto', sans-serif;
            color: #000000;
        """)

        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.layout = QVBoxLayout(self.central_widget)
        self.layout.setAlignment(Qt.AlignCenter)
        self.layout.setSpacing(15)

        self.title_label = QLabel("Fashion Store")
        self.title_label.setStyleSheet("""
            font-size: 28px;
            font-weight: bold;
            color: #4a2c4a;
            margin-bottom: 10px;
        """)
        self.layout.addWidget(self.title_label)

        self.username_input = QLineEdit()
        self.username_input.setPlaceholderText("Имя пользователя")
        self.username_input.setStyleSheet("""
            padding: 12px;
            border: 2px solid #d3a3d3;
            border-radius: 8px;
            background-color: white;
            font-size: 16px;
            color: #000000;
        """)
        self.layout.addWidget(self.username_input)

        self.password_input = QLineEdit()
        self.password_input.setPlaceholderText("Пароль")
        self.password_input.setEchoMode(QLineEdit.Password)
        self.password_input.setStyleSheet("""
            padding: 12px;
            border: 2px solid #d3a3d3;
            border-radius: 8px;
            background-color: white;
            font-size: 16px;
            color: #000000;
        """)
        self.layout.addWidget(self.password_input)

        self.login_button = QPushButton("Войти")
        self.login_button.setStyleSheet("""
            padding: 12px;
            background-color: #d3a3d3;
            color: white;
            border-radius: 8px;
            font-size: 16px;
            font-weight: bold;
            border: none;
        """)
        self.login_button.setCursor(Qt.PointingHandCursor)
        self.login_button.clicked.connect(self.check_login)
        self.layout.addWidget(self.login_button)

        self.session = Connect.create_connection()

    def check_login(self):
        username = self.username_input.text()
        password = self.password_input.text()
        user = self.session.query(User).filter_by(имя_пользователя=username, пароль=password).first()
        if user:
            self.main_window =FashionMainWindow(user)
            self.main_window.show()
            self.close()
        else:
            QMessageBox.warning(self, "Ошибка", "Неверное имя пользователя или пароль!")