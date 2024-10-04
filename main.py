import sys
from PyQt5.QtWidgets import QApplication, QDialog, QLineEdit, QPushButton, QVBoxLayout, QLabel


class Login(QDialog):
    def __init__(self):
        super(Login, self).__init__()

        # Cria os componentes da tela de login diretamente no código para teste
        self.email = QLineEdit(self)
        self.email.setPlaceholderText("E-mail")

        self.password = QLineEdit(self)
        self.password.setPlaceholderText("Senha")
        self.password.setEchoMode(QLineEdit.Password)

        self.loginbutton = QPushButton("Login", self)
        self.loginbutton.clicked.connect(self.loginfunction)

        # Layout simples para a tela de login
        layout = QVBoxLayout()
        layout.addWidget(self.email)
        layout.addWidget(self.password)
        layout.addWidget(self.loginbutton)

        self.setLayout(layout)

    def loginfunction(self):
        email = self.email.text()
        password = self.password.text()
        print(f"Tentativa de login com email: {email}, senha: {password}")

        # Simulação de autenticação: se o login for bem-sucedido, abre a segunda janela
        if email == "admin@example.com" and password == "1234":
            print("Login bem-sucedido")
            self.open_second_window()
        else:
            print("Login falhou")

    def open_second_window(self):
        self.second_window = SecondWindow()  # Cria a segunda janela
        self.second_window.show()  # Mostra a segunda janela
        self.close()  # Fecha a janela de login


class SecondWindow(QDialog):
    def __init__(self):
        super(SecondWindow, self).__init__()

        # Cria os componentes da segunda janela
        self.label = QLabel("Bem-vindo à segunda janela!", self)

        # Layout simples para a segunda janela
        layout = QVBoxLayout()
        layout.addWidget(self.label)

        self.setLayout(layout)


if __name__ == "__main__":
    app = QApplication(sys.argv)

    # Cria e exibe a tela de login
    mainwindow = Login()
    mainwindow.show()

    sys.exit(app.exec_())
