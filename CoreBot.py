import re
from collections import namedtuple


Trans = namedtuple('Trans', ['re', 'ds', 'fn'])


class DFA:
    """DFA for bot execution"""
    states = set()
    transitions = {}
    start = 'start'
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

    @staticmethod
    def Update_user(ID, user):
        Repo.users[ID] = user

    @staticmethod
    def Delete_user(ID):
        del Repo.users[ID]

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


class PF:
    pass


def jumper(ID, trigger, **kwargs):
    if not Repo.In_Repo(ID):
        return PF.start(ID, trigger, **kwargs)
    state = Repo.Read_user(ID).state
    tr = DFA.jump(trigger, state)
    res = tr.fn(ID, trigger, **kwargs)
    user.state = tr.ds
    return res
