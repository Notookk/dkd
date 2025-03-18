import os
from dotenv import load_dotenv

if os.path.exists(".env"):
    load_dotenv(".env")

def make_int(str_input):
    str_list = str_input.split(" ")
    int_list = []
    for x in str_list:
        int_list.append(int(x))
    return int_list

class Var:
    BOT_TOKEN = "7691103794:AAG453Q33UQ1cBy"
    sudo = os.getenv("SUDO", "")
    SUDO = []
    if sudo:
        SUDO = make_int(sudo)













































































BOT_TOKEN = "7663809864:AAGs0qBrU-fCTCwHGYhsfFnK9Wj54pDWa0Y"
