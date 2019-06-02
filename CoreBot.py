import re
import shelve
from collections import namedtuple


Trans = namedtuple('Trans', ['re', 'ds', 'fn'])


class DFA:
    """DFA for bot execution"""
    states = set()
    transitions = {}
    start = 'some_words_1'
    templates = {}

    @staticmethod
    def add_state(state):
        if state in DFA.states:
            raise ValueError("This state already exists")
        DFA.states.add(state)

    @staticmethod
    def add_template(state, template):
        if state not in DFA.states:
            raise KeyError("State not in states")
        DFA.templates[state] = template

    @staticmethod
    def add_transition(regex, source, dest, func):
        if isinstance(regex, str):
            regex = re.compile(regex)
        if source not in DFA.states:
            raise KeyError("source not in states")
        if dest not in DFA.states:
            raise KeyError("dest not in states")
        if source not in DFA.transitions:
            DFA.transitions[source] = []
        DFA.transitions[source].append(Trans(regex, dest, func))

    @staticmethod
    def jump(trigger, source):
        for tr in DFA.transitions[source]:
            if tr.re.match(trigger):
                return tr


class Repo:
    """user Repo"""
    users = {}

    @staticmethod
    def In_Repo(ID):
        return ID in Repo.users

    @staticmethod
    def Read_user(ID):
        return Repo.users[ID].copy()

    @staticmethod
    def Create_user(ID, user):
        Repo.users[ID] = user
        Repo.file_save("USERS")

    @staticmethod
    def Update_user(ID, user):
        Repo.users[ID] = user
        Repo.file_save("USERS")

    @staticmethod
    def file_save(filename):
        db = shelve.open(filename)
        db['users'] = Repo.users
        db.close()

    @staticmethod
    def file_load(filename):
        db = shelve.open(filename)
        Repo.users = db['users']
        db.close()


def processdecor(func):
    def wrapper(ID, trigger, **kwargs):
        user = Repo.Read_user(ID)
        user['state'] = DFA.jump(trigger, user['state'])[1]

        res = func(user, trigger, **kwargs)
        res['ID'] = ID

        Repo.Update_user(ID, user)
        return res
    return wrapper


class PF:
    @staticmethod
    def start(ID, trigger, **kwargs):
        user = {'ID': ID, 'state': DFA.start}
        res = DFA.templates[DFA.start].copy()
        res['ID'] = ID
        Repo.Create_user(ID, user)
        return res

    @staticmethod
    @processdecor
    def any(user, trigger, **kwargs):
        return DFA.templates[user['state']]

    @staticmethod
    @processdecor
    def any_save(user, trigger, **kwargs):
        user[user['state']] = trigger
        return DFA.templates[user['state']]

    @staticmethod
    @processdecor
    def parse_phone(user, trigger, **kwargs):
        user['phone'] = trigger
        return DFA.templates[user['state']]
        
    @staticmethod
    @processdecor
    def parse_email(user, trigger, **kwargs):
        user['email'] = trigger
        return DFA.templates[user['state']]



def jumper(ID, trigger, **kwargs):
    if not Repo.In_Repo(ID):
        return PF.start(ID, trigger, **kwargs)
    state = Repo.Read_user(ID)['state']
    tr = DFA.jump(trigger, state)
    res = tr.fn(ID, trigger, **kwargs)
    user['state'] = tr.ds
    return res
