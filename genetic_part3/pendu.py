




def choose_word(word=""):
    if word == "":
        word = "romeo"
    return list(word)

def default_word(word):
    return list("*" * len(word))

def guest_similarity(word, guess):
    score = 0
    for i in range(len(word)):
        if word[i] == guess[i]:
            score += 1
    return score

def possible_letters():
    return list("abcdefghijklmnopqrstuvwxyz")

if __name__ == "__main__":
    print(possible_letters())
    