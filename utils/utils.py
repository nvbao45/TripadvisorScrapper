import re
import winreg

from dotenv import dotenv_values


config = dotenv_values("config.txt")
INTERNET_SETTINGS = winreg.OpenKey(winreg.HKEY_CURRENT_USER,
                                   r'Software\Microsoft\Windows\CurrentVersion\Internet Settings',
                                   0, winreg.KEY_ALL_ACCESS)


def print_progress_bar(iteration, total, prefix='', suffix='', decimals=1, length=100, fill='█', print_end="\r"):
    """
    Call in a loop to create terminal progress bar
    @params:
        iteration   - Required  : current iteration (Int)
        total       - Required  : total iterations (Int)
        prefix      - Optional  : prefix string (Str)
        suffix      - Optional  : suffix string (Str)
        decimals    - Optional  : positive number of decimals in percent complete (Int)
        length      - Optional  : character length of bar (Int)
        fill        - Optional  : bar fill character (Str)
        printEnd    - Optional  : end character (e.g. "\r", "\r\n") (Str)
    """

    if total != -1:
        percent = ("{0:." + str(decimals) + "f}").format(100 * (iteration / float(total)))
        filled_length = int(length * iteration // total)
        bar = fill * filled_length + '-' * (length - filled_length)
    else:
        percent = "0"
        bar = "cannot calculate percent"
    print(f'\r{prefix} |{bar}| {percent}% {suffix}', end=print_end)


def find_email(content):
    emails = re.findall(r'[\w.+-]+@[\w-]+\.[\w.-]+', content)
    emails = list(dict.fromkeys(emails))
    return "\r\n".join(emails)


def set_key(name, value):
    _, reg_type = winreg.QueryValueEx(INTERNET_SETTINGS, name)
    winreg.SetValueEx(INTERNET_SETTINGS, name, 0, reg_type, value)


def enable_proxy(proxy):
    set_key('ProxyEnable', 1)
    set_key('ProxyOverride', u'*.local;<local>')
    set_key('ProxyServer', f'{proxy}')


def disable_proxy():
    set_key('ProxyEnable', 0)
