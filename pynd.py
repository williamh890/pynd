from character import Character


if __name__ == "__main__":
    stab = Character()

    with stab.load("benjen"):
        stab.show()
