from tkInit import initWindow


if __name__ == "__main__":

    with open('assets/spellings.txt', 'r') as f:
        spellings = f.readlines()
    initWindow(spellings)
