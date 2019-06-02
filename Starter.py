from VKBot import VKBot
from config import token
from CoreBot import jumper, Repo
from DFA_init import DFA_init

DFA_init()
print('Start VKBot')

while True:
    try:
        Repo.file_load()
        VKBot(token, '182858848', jumper).start()
    except Exception as e:
        print(e)


