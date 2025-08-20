# Letreco

Jogo de adivinhação de palavras no estilo Letreco.

## Como instalar

git clone https://github.com/Ractazar/Letreco 

cd Letreco 

pip install -r requirements.txt

## Criando o executável

pyinstaller --onefile --windowed --icon=assets/icon.ico src/main.py

Criar uma parta (ex:Letreco) e colocar o executável em dist dentro dela

copiar a pasta assets com o icon.ico para a pasta Letreco

copiar a pasta data com words.csv para a pasta Letreco

## Funções em functions.py

### load_words

Retorna list e set de todas as palavras no csv com 5 letras

### check_word

Verifica se cada letra da palavra inserida existe na palavra alvo, assim como se está na posição certa

### classify_difficulty

Classifica a dificuldade da palavra de acordo com acentos e letras incomuns

## Componentes em main.py

### InitialScreen

A tela inicial do jogador. Possui quatro botões: Iniciar Jogo, Ver Regras, Melhores Pontuações e Sair

### RulesWindow

Apresenta as regras do jogo, inclusive algumas caixas coloridas explicando as cores usadas e o significado delas

### RankingsWindow

Retorna a pontuação em "data/rankings.csv"

Caso não exista fala que não há pontuações registradas

Se existir, ordena elas em ordem decrescente e apresenta as 10 melhores junto com as iniciais do jogador

Possui uma função **try_delete_rankings** que deleta o arquivo, se existir, desde que a senha "SpSterne0813" seja fornecida e o botão clicado

### LetrecoGame

O jogo em si, possuindo diversas funções

Cria várias variáveis e um temporizador

**load_words** busca as palavras em "data/words.csv"

Chama a função **classify_difficulty** de functions.py

Cria cinco QLineEdit para o jogador chutar a palavra, letra por letra

Só permitindo clicar no botão de teste com as 5 letras preenchidas, graças a **update_button_state**

Possui umn botão pra voltar à tela inicial e um histórico com as tentativas realizadas

**handle_enter** permite ir de um campo de letra para o próximo teclando enter

**check_input** verifica se a palavra adivinhada e a real são válidas, começando o timer após a primeira tentativa válida

Essa função também atualiza a pontuação e o número de tentativas realizadas acabando o jogo ao acertar ou gastar todas as tentativas 

**update_timer**  atualiza o texto que mostra o tempo restante e acaba o jogo quando ele chega a zero

**color_feedback** só muda a cor do campo de acordo com acertos e posições das letras

**add_to_history** adiciona a adivinhação com as cores de cada letra ao histórico

**save_score** salva a pontuação no arquivo "data/rankings.csv"

## ScoreDialog

Abre uma janela que permite ao jogador salvar sua pontuação ao inserir suas iniciais

**validate_and_accept** checa se as iniciais são válidas

**closeEvent** avisa o jogador, se ele tentar fechar o jogo, que a pontuação não será salva se o fizer
