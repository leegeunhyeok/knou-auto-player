from datetime import datetime
from colorama import Fore

class Logger:
    def _get_timestamp(self):
        return datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')

    def _log(self, level, *args):
        m = level + ' ' + (' '.join(args[0]))
        tm = self._get_timestamp() + ' - ' + m
        print(tm)

    def empty(self):
        print()

    def info(self, *args):
        self._log(f'[{Fore.CYAN}INFO{Fore.RESET}]', args)

    def success(self, *args):
        self._log(f'[{Fore.GREEN}SUCCESS{Fore.RESET}]', args)

    def warning(self, *args):
        self._log(f'[{Fore.YELLOW}WARNING{Fore.RESET}]', args)

    def error(self, *args):
        self._log(f'[{Fore.RED}ERROR{Fore.RESET}]', args)

    def danger(self, *args):
        self._log(f'[{Fore.RED}DANGER{Fore.RESET}]', args)

    def critical(self, *args):
        self._log(f'[{Fore.MAGENTA}CRITICAL{Fore.RESET}]', args)

logger = Logger()
