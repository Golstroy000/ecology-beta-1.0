import sqlite3
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput

class MenuScreen(BoxLayout):
    def __init__(self, username, score, **kwargs):
        super().__init__(**kwargs)

        self.orientation = 'vertical'

        self.label = Label(text=f"Привет, {username}!\nSCORE: {score}")
        self.add_widget(self.label)

        self.btn_start = Button(text="Старт", size_hint_x=None, width=300, size_hint_y=None, height=50)
        self.btn_start.bind(on_press=self.start)
        self.add_widget(self.btn_start)

    def start(self, instance):
        self.label.text = "Игра началась!"

    def update_label(self, username, score):
        self.label.text = f"Привет, {username}!\nSCORE: {score}"


class LoginScreen(BoxLayout):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.orientation = 'vertical'

        self.label = Label(text="Добро пожаловать!")
        self.add_widget(self.label)

        self.username_input = TextInput(hint_text="Введите имя пользователя", multiline=False)
        self.add_widget(self.username_input)

        self.password_input = TextInput(hint_text="Введите пароль", multiline=False, password=True)
        self.add_widget(self.password_input)

        self.btn_register = Button(text="Регистрация", size_hint_x=None, width=300, size_hint_y=None, height=50)
        self.btn_register.bind(on_press=self.register)
        self.add_widget(self.btn_register)

        self.btn_login = Button(text="Войти", size_hint_x=None, width=300, size_hint_y=None, height=50)
        self.btn_login.bind(on_press=self.login)
        self.add_widget(self.btn_login)

        self.conn = sqlite3.connect('users.db')
        self.cursor = self.conn.cursor()
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS users (
                            id INTEGER PRIMARY KEY,
                            username TEXT,
                            password TEXT,
                            score INTEGER DEFAULT 0
                            )''')
        self.conn.commit()

    def register(self, instance):
        username = self.username_input.text
        password = self.password_input.text

        self.cursor.execute("SELECT * FROM users WHERE username=?", (username,))
        existing_user = self.cursor.fetchone()
        if existing_user:
            self.label.text = "Пользователь уже существует!"
        else:
            self.cursor.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, password))
            self.conn.commit()
            self.label.text = "Пользователь зарегистрирован!"

    def login(self, instance):
        username = self.username_input.text
        password = self.password_input.text

        self.cursor.execute("SELECT * FROM users WHERE username=? AND password=?", (username, password))
        user = self.cursor.fetchone()
        if user:
            self.label.text = "Вы успешно вошли!"
            score = user[3] if len(user) > 3 else 0  # Получаем score из базы данных, если он существует
            menu_screen = MenuScreen(username=username, score=score)
            self.parent.add_widget(menu_screen)
            self.parent.remove_widget(self)
        else:
            self.label.text = "Неправильное имя пользователя или пароль!"


class MyApp(App):

    def build(self):
        return LoginScreen()


if __name__ == '__main__':
    MyApp().run()
