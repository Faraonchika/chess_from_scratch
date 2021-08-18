letters = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H']


def give_2d_pos(array, elem):
    letter = 0
    number = 0
    for i in range(8):
        for j in range(8):
            if array[i][j].cash_pos == elem.cash_pos:
                letter = i
                number = j
                break
    return letter, number


def to_idx(letter, number):
    return letters.index(letter) - 1, number - 1
