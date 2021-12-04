def line_generator(fname):
    with open(fname) as fp:
        for line in fp:
            yield line.rstrip()

line_gen = line_generator("input-04.txt")
numbers = next(line_gen).split(',')
print(numbers)

cards = []
card_size = 5
while next(line_gen, 'EOF') == "":
    card = [
        [num for num in filter(len, line.split(' '))] for line in (
            next(line_gen) for _ in range(card_size)
        )
    ]
    print(card)
    cards.append(card)

def is_bingo_line(chars):
    count = 0
    for ch in chars:
        if ch != "*":
            return False
        count += 1
    assert(count == card_size)
    return True

def is_bingo(card):
    for line in card:
        if is_bingo_line(line):
            return True
    for col in range(card_size):
        if is_bingo_line(line[col] for line in card):
            return True
    return False

def update_card(card, target_num):
    return [
        ["*" if num == target_num else num for num in line] for line in card
    ]

def play(cards, numbers):
    for number in numbers:
        new_cards = []
        for card in cards:
            card = update_card(card, number)
            new_cards.append(card)
            if is_bingo(card):
                print("Bingo", card)
                remainder = sum(sum(
                    int(num) if num != "*" else 0 for num in line
                ) for line in card)
                print(remainder, number, remainder * int(number))
                return
        cards = new_cards

play(cards, numbers)