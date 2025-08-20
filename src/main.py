import sys
import os
import csv
import random
from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QHBoxLayout, QPushButton,
    QLabel, QLineEdit, QMessageBox, QFrame, QDialog, QDesktopWidget
)
from PyQt5.QtGui import QColor, QPalette, QIcon, QFont
from PyQt5.QtCore import Qt, QTimer
import functions

ICON = "assets/icon.ico"
RANKINGS = "data/rankings.csv"

def change_font_size(old_font, size=16, bold=True):
    font = QFont()
    font.setPointSize(size)
    font.setBold(bold)
    old_font.setFont(font)

BACKGROUND = """
    QWidget {
        background-color: #FFEFC5;
    }
"""

def style_button(button, bg_color, hover_color, text_color="white", font_size="11px"):
    button.setStyleSheet(f"""
        QPushButton {{
            background-color: {bg_color};
            color: {text_color};
            border-radius: 5px;
            padding: 8px;
            font-size: {font_size};
        }}
        QPushButton:hover {{
            background-color: {hover_color};
        }}
    """)

def center_window(window):
    qr = window.frameGeometry()
    cp = QDesktopWidget().availableGeometry().center()
    qr.moveCenter(cp)
    window.move(qr.topLeft())

class InitialScreen(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Letreco - Menu Inicial")
        self.setFixedSize(300, 200)
        self.setWindowIcon(QIcon(ICON))
        self.setStyleSheet(BACKGROUND)
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()

        title = QLabel("🎮 Bem-vindo ao Letreco!")
        title.setAlignment(Qt.AlignCenter)
        change_font_size(title)
        layout.addWidget(title)

        btn_play = QPushButton("Iniciar Jogo")
        btn_play.clicked.connect(self.start_game)
        layout.addWidget(btn_play)

        btn_rules = QPushButton("Ver Regras")
        btn_rules.clicked.connect(self.show_rules)
        layout.addWidget(btn_rules)

        btn_rankings = QPushButton("Melhores Pontuações")
        btn_rankings.clicked.connect(self.show_rankings)
        layout.addWidget(btn_rankings)

        btn_exit = QPushButton("Sair")
        btn_exit.clicked.connect(self.close)
        layout.addWidget(btn_exit)

        style_button(btn_play, "#4CAF50", "#45A049")
        style_button(btn_rules, "#2196F3", "#1976D2")
        style_button(btn_rankings, "#FFC107", "#FFB300", text_color="black")
        style_button(btn_exit, "#F44336", "#D32F2F")

        self.setLayout(layout)

    def start_game(self):
        self.hide()
        self.jogo = LetrecoGame()
        self.jogo.show()
        center_window(self.jogo)

    def show_rules(self):
        regras_dialog = RulesWindow()
        QTimer.singleShot(0, lambda: center_window(regras_dialog))
        regras_dialog.exec_()

    def show_rankings(self):
        rankings_dialog = RankingsWindow()
        QTimer.singleShot(0, lambda: center_window(rankings_dialog))
        rankings_dialog.exec_()

class RulesWindow(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Regras do Jogo")
        self.setFixedSize(400, 200)
        self.setWindowIcon(QIcon(ICON))
        self.setWindowFlags(self.windowFlags() & ~Qt.WindowContextHelpButtonHint)
        self.setStyleSheet(BACKGROUND)
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()

        explanations = [
            ("Letra correta na posição correta", QColor("green")),
            ("Letra correta na posição errada", QColor("yellow")),
            ("Letra não existe na palavra", QColor("lightgray")),
        ]

        for text, color in explanations:
            line = QHBoxLayout()
            color_box = QLineEdit()
            color_box.setReadOnly(True)
            color_box.setFixedWidth(40)
            color_box.setStyleSheet(f"background-color: {color.name()};")
            line.addWidget(color_box)

            label = QLabel(text)
            line.addWidget(label)

            layout.addLayout(line)

        instructions = QLabel(
            "\nVocê tem 6 tentativas para adivinhar a palavra de 5 letras.\n"
            "Após a primeira tentativa você tem 60 segundos para acertar a palavra.\n"
            "Digite uma letra por campo e pressione Enter ou clique em Testar Palavra.\n"
            "Letras com acento são consideradas DIFERENTES de letras sem acento."
        )
        layout.addWidget(instructions)

        self.setLayout(layout)

class RankingsWindow(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Melhores Pontuações")
        self.setFixedSize(300, 300)
        self.setWindowIcon(QIcon(ICON))
        self.setWindowModality(Qt.ApplicationModal)
        self.setWindowFlags(self.windowFlags() & ~Qt.WindowContextHelpButtonHint)
        self.setStyleSheet("""
            RankingsWindow {
                background-color: #FFEFC5;
            }
            QLineEdit#password_input {
                background-color: white;
                color: black;
                font-size: 13px;
                border: 1px solid #ccc;
                border-radius: 4px;
                padding: 4px;
            }
            QLineEdit#password_input::placeholder {
                color: gray;
                font-style: italic;
            }
        """)
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()
        label = QLabel("🏆 Top 10 Pontuações")
        change_font_size(label)
        label.setAlignment(Qt.AlignCenter)
        layout.addWidget(label)

        path = RANKINGS
        scores = []

        if os.path.exists(path):
            with open(path, newline='', encoding='utf-8') as f:
                reader = csv.reader(f)
                scores = [row[0] for row in reader][:10]
            for i in range(10):
                if i < len(scores):
                    try:
                        name, score = scores[i].split("_")
                        layout.addWidget(QLabel(f"{i+1}º - {name} → {score} pontos"))
                    except ValueError:
                        layout.addWidget(QLabel(f"{i+1}º - {scores[i]}"))  # fallback
                else:
                    layout.addWidget(QLabel(f"{i+1}º - "))
        else:
            spacer = QLabel()
            spacer.setFixedHeight(80)
            layout.addWidget(spacer)
            label = QLabel("Nenhuma pontuação registrada.")
            change_font_size(label, 12)
            layout.addWidget(label)
            spacer.setFixedHeight(100)
            layout.addWidget(spacer)

        action_layout = QHBoxLayout()

        self.password_input = QLineEdit()
        self.password_input.setPlaceholderText("Senha para apagar")
        self.password_input.setObjectName("password_input")
        self.password_input.setEchoMode(QLineEdit.Password)
        self.password_input.setFixedWidth(150)
        action_layout.addWidget(self.password_input)

        delete_btn = QPushButton("Apagar")
        style_button(delete_btn, "#F44336", "#D32F2F")
        delete_btn.clicked.connect(self.try_delete_rankings)
        action_layout.addWidget(delete_btn)

        layout.addLayout(action_layout)

        self.setLayout(layout)

    def try_delete_rankings(self):
        password = self.password_input.text().strip()
        if password == "SpSterne0813":
            path = RANKINGS
            if os.path.exists(path):
                os.remove(path)
                QMessageBox.information(self, "Arquivo apagado", "As pontuações foram apagadas.")
                self.close()
                nova_janela = RankingsWindow()
                QTimer.singleShot(0, lambda: center_window(nova_janela))
                nova_janela.exec_()
            else:
                QMessageBox.information(self, "Nada para apagar", "O arquivo já não existe.")
        else:
            QMessageBox.warning(self, "Senha incorreta", "Senha inválida. Tente novamente.")

class LetrecoGame(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Letreco")
        self.setWindowIcon(QIcon(ICON))
        self.word_list, self.word_set = self.load_words()
        self.chosen_word = random.choice(self.word_list)
        self.attempts = 0
        self.max_attempts = 6
        self.seconds_remaining = 60
        self.visual_timer = QTimer()

        self.setObjectName("game")
        self.setStyleSheet("""
            #game {
                background-color: #FFEFC5;
            }
        """)
        self.init_ui()

    def load_words(self):
        try:
            return functions.load_words('data/words.csv')
        except ValueError:
            QMessageBox.critical(self, "Erro", "A lista de palavras está vazia.")
            sys.exit()
        except Exception:
            QMessageBox.critical(self, "Erro ao carregar a lista de palavras.")
            sys.exit()

    def init_ui(self):
        layout = QVBoxLayout()

        difficulty = functions.classify_difficulty(self.chosen_word)
        cores = {
            "FÁCIL": "#4CAF50",   
            "MÉDIA": "#FF9800",
            "DIFÍCIL": "#F44336",
            "IMPOSSÍVEL": "#6A1B9A"
        }

        cor = cores.get(difficulty, "black")
        self.difficulty_label = QLabel(f'Dificuldade: <span style="color:{cor}; font-weight:bold;">{difficulty}</span>')
        layout.addWidget(self.difficulty_label)

        self.info_label = QLabel(f"Tentativas restantes: {self.max_attempts - self.attempts}")
        layout.addWidget(self.info_label)

        self.time_label = QLabel("⏱️ Tempo restante:")
        layout.addWidget(self.time_label)


        self.input_fields = []
        input_layout = QHBoxLayout()
        for i in range(5):
            field = QLineEdit()
            field.setMaxLength(1)
            field.setFixedWidth(40)
            field.setAlignment(Qt.AlignCenter)
            field.textChanged.connect(self.update_button_state)
            field.returnPressed.connect(lambda i=i: self.handle_enter(i))
            self.input_fields.append(field)
            input_layout.addWidget(field)
        layout.addLayout(input_layout)

        self.submit_button = QPushButton("Testar Palavra")
        style_button(self.submit_button, "#4CAF50", "#45A049")
        self.submit_button.setEnabled(False)
        self.submit_button.clicked.connect(self.check_input)
        self.submit_button.setDefault(True)
        layout.addWidget(self.submit_button)

        self.voltar_button = QPushButton("Voltar ao Menu")
        style_button(self.voltar_button, "#F44336", "#D32F2F")
        self.voltar_button.clicked.connect(self.return_to_menu)
        layout.addWidget(self.voltar_button)

        self.history_layout = QVBoxLayout()
        history_frame = QFrame()
        history_frame.setLayout(self.history_layout)
        layout.addWidget(QLabel("Tentativas anteriores:"))
        layout.addWidget(history_frame)

        self.setLayout(layout)
        self.input_fields[0].setFocus()

    def update_button_state(self):
        filled = all(field.text().strip() for field in self.input_fields)
        self.submit_button.setEnabled(filled)

    def handle_enter(self, index):
        if index < 4:
            self.input_fields[index + 1].setFocus()
        else:
            if self.submit_button.isEnabled():
                self.check_input()

    def check_input(self):
        user_word = ''.join([field.text().lower() for field in self.input_fields])
        if len(user_word) != 5:
            QMessageBox.warning(self, "Erro", "A palavra deve ter 5 letras.")
            return

        if user_word not in self.word_set:
            QMessageBox.warning(self, "Erro", "Essa palavra não é válida.")
            return

        try:
            result = functions.check_word(self.chosen_word, user_word)
        except ValueError:
            QMessageBox.critical(self, "Erro", "A palavra a ser adivinhada não tem 5 letras.")
            return
        except Exception:
            QMessageBox.critical(self, "Erro", "Ocorreu um erro ao comparar as palavras.")

        self.attempts += 1
        self.info_label.setText(f"Tentativas restantes: {self.max_attempts - self.attempts}")
        if self.attempts == 1:
            self.visual_timer.timeout.connect(self.update_timer)
            self.visual_timer.start(1000)
            self.time_label.setText(f"⏱️ Tempo restante: 60s")
        self.color_feedback(result)
        self.add_to_history(user_word, result)

        if user_word == self.chosen_word:
            self.visual_timer.stop()
            time = 60 - self.seconds_remaining
            score = max(1000 - (self.attempts - 1) * 100 - time * 5, 0)
            dialog = ScoreDialog(score, self)
            QTimer.singleShot(0, lambda: center_window(dialog))
            if dialog.exec_() == QDialog.Accepted:
                initials = dialog.get_initials()
                self.save_score(f"{initials}_{score}")
            self.restart_game()
        elif self.attempts >= self.max_attempts:
            self.visual_timer.stop()
            QMessageBox.information(self, "Fim de jogo", f"A palavra era: {self.chosen_word}")
            self.restart_game()
        else:
            for field in self.input_fields:
                field.clear()
            self.input_fields[0].setFocus()
            self.update_button_state()

    def update_timer(self):
        self.seconds_remaining -= 1
        self.time_label.setText(f"⏱️ Tempo restante: {self.seconds_remaining}s")
        if self.seconds_remaining <= 0:
            self.visual_timer.stop()
            QMessageBox.information(self, "Tempo esgotado", f"⏱️ Você perdeu! A palavra era: {self.chosen_word}")
            self.restart_game()

    def color_feedback(self, result):
        for i, status in enumerate(result):
            palette = self.input_fields[i].palette()
            if status == "correta":
                palette.setColor(QPalette.Base, QColor("green"))
            elif status == "existe":
                palette.setColor(QPalette.Base, QColor("yellow"))
            else:
                palette.setColor(QPalette.Base, QColor("lightgray"))
            self.input_fields[i].setPalette(palette)

    def add_to_history(self, word, result):
        row_layout = QHBoxLayout()
        for i, letter in enumerate(word):
            label = QLineEdit(letter.upper())
            label.setReadOnly(True)
            label.setFixedWidth(40)
            label.setAlignment(Qt.AlignCenter)
            palette = label.palette()
            if result[i] == "correta":
                palette.setColor(QPalette.Base, QColor("green"))
            elif result[i] == "existe":
                palette.setColor(QPalette.Base, QColor("yellow"))
            else:
                palette.setColor(QPalette.Base, QColor("lightgray"))
            label.setPalette(palette)
            row_layout.addWidget(label)
        self.history_layout.addLayout(row_layout)

    def save_score(self, score):
        caminho = RANKINGS
        os.makedirs("data", exist_ok=True)
        rankings = []

        if os.path.exists(caminho):
            with open(caminho, newline='', encoding='utf-8') as f:
                reader = csv.reader(f)
                rankings = [row[0] for row in reader]

        rankings.append(str(score))
        rankings = sorted(rankings, key=lambda x: int(x.split("_")[1]), reverse=True)[:10]

        with open(caminho, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            for score in rankings:
                writer.writerow([score])

    def return_to_menu(self):
        self.visual_timer.stop()
        self.close()
        self.menu = InitialScreen()
        self.menu.show()
        center_window(self.menu)

    def restart_game(self):
        self.close()
        nova_partida = LetrecoGame()
        nova_partida.show()
        center_window(nova_partida)

class ScoreDialog(QDialog):
    def __init__(self, score, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Salvar Pontuação")
        self.setFixedSize(250, 150)
        self.setWindowIcon(QIcon(ICON))
        self.setWindowModality(Qt.ApplicationModal)
        self.setWindowFlags(self.windowFlags() & ~Qt.WindowContextHelpButtonHint)
        self.setObjectName("score_dialog")
        self.setStyleSheet("""
            #score_dialog {
                background-color: #FFEFC5;
            }
            QLineEdit {
                font-size: 14px;
                color: black;
            }
            QLineEdit::placeholder {
                color: gray;
                font-style: italic;
            }
        """)
        layout = QVBoxLayout()

        label = QLabel(f"Pontuação: {score}")
        label.setAlignment(Qt.AlignCenter)
        layout.addWidget(label)

        label = QLabel("Digite suas iniciais")
        label.setAlignment(Qt.AlignCenter)
        layout.addWidget(label)

        self.input = QLineEdit()
        self.input.setMaxLength(3)
        self.input.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.input)

        btn = QPushButton("Salvar")
        style_button(btn, "#4CAF50", "#45A049")
        btn.clicked.connect(self.validate_and_accept)
        layout.addWidget(btn)

        self.setLayout(layout)

    def get_initials(self):
        return self.input.text().upper()
    
    def validate_and_accept(self):
        initials = self.input.text().strip().upper()
        if len(initials) != 3 or not initials.isalpha():
            QMessageBox.warning(
                self,
                "Iniciais inválidas",
                "Por favor, digite exatamente 3 letras."
            )
        else:
            self.accept()

    def closeEvent(self, event):
        reply = QMessageBox.question(
            self,
            "Confirmar saída",
            "Se você fechar agora, sua pontuação não será salva.\nDeseja continuar?",
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.No
        )

        if reply == QMessageBox.Yes:
            event.accept()
        else:
            event.ignore()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    menu = InitialScreen()
    menu.show()
    center_window(menu)
    sys.exit(app.exec_())
