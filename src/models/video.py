from colorama import Fore

class Video:
    def __init__(self):
        self.id = ''
        self.title = ''
        self.waiting = False
        self.watched = False

    def __str__(self):
        symbol =  f'{Fore.YELLOW}◻' if self.waiting else (f'{Fore.GREEN}✔' if self.watched else f'{Fore.RED}✖')
        return f'{symbol}{Fore.RESET} {self.id} :: {self.title}'
