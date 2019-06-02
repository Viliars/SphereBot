from VKBot import VKBot
from config import token
from CoreBot import jumper
from DFA_init import DFA_init

DFA_init()
print('Start VKBot')

while True:
    try:
        VKBot(token, '181244512', jumper).start()
    except Exception as e:
        pass


