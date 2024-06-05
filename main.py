# main.py
from mainGUI import MainMenu
import argparse


def main():
    # parser = argparse.ArgumentParser(description="Start the Main Menu with a player's name.")
    # parser.add_argument('-n', '--name', type=str, help="Player's name", default=None)
    # args = parser.parse_args()
    
    # name = args.name
    # if not args.name: name = "Enter Your NAME in terminal eg: python main.py --name 'Knoxy' "
    name = "bob"
    main_menu = MainMenu(name)
    main_menu.run()

if __name__ == "__main__":
    main()
