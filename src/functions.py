import csv

_word_list = None
_word_set = None

def load_words(filepath):
    global _word_list, _word_set
    if _word_list is not None and _word_set is not None:
        return _word_list, _word_set

    words = []
    with open(filepath, encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            word = row['palavra'].strip().lower()
            if len(word) == 5:
                words.append(word)

    if not words:
        raise ValueError("The list must not be empty.")

    _word_list = words
    _word_set = set(words)
    return _word_list, _word_set

def check_word(correct_word, user_word):
    if len(correct_word) != 5 or len(user_word) != 5:
        raise ValueError("Both words must have 5 letters!")

    result = ["inexistente"] * 5
    used = [False] * 5  # Marca letras já usadas da palavra correta
    user_word = user_word.lower()

    # verificar letras corretas (verde)
    for i in range(5):
        if user_word[i] == correct_word[i]:
            result[i] = "correta"
            used[i] = True

    # verificar letras existentes em outra posição (amarelo)
    for i in range(5):
        if result[i] == "correta":
            continue
        for j in range(5):
            if not used[j] and user_word[i] == correct_word[j]:
                result[i] = "existe"
                used[j] = True
                break

    return result

def classify_difficulty(word):
    word = word.upper()

    impossible = set("YÂÔÓ")
    very_hard = set("XZJÇÍÚÊ")
    moderate = set("HÁÃÉÕ")


    score = 0
    for letter in word:
        if letter in impossible:
            score += 4
        elif letter in very_hard:
            score += 2
        elif letter in moderate:
            score += 1

    if score == 0:
        return "FÁCIL"
    elif score == 1:
        return "MÉDIA"
    elif score >= 2:
        return "DIFÍCIL"
    else:
        return "IMPOSSÍVEL"