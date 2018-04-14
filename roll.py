import random
import sys


def parse(dice_str):
    num_dice, dice_type = (int(v) for v in dice_str.split('d'))

    total = 0
    for _ in range(num_dice):
        total += random.randint(1, dice_type)

    return total


if __name__ == "__main__":
    try:
        dice_str = sys.argv[1]
    except:
        print("python roll.py <dice-string>\n")
        exit()

    try:
        total = parse(dice_str)
    except:
        print(f"error parsing: {dice_str}")

    print(total)
