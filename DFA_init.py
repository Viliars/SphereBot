from CoreBot import DFA, PF
from messages import *

def DFA_init():
    DFA.add_state("some_words_1")
    DFA.add_state("some_words_2")
    DFA.add_state("input_phone")
    DFA.add_state("input_email")
    DFA.add_state("input_phone_error")
    DFA.add_state("input_email_error")
    DFA.add_state("end_input")
    DFA.add_state("problem_1")
    DFA.add_state("endprob_1")
    DFA.add_state("problem_2")
    DFA.add_state("endprob_2")
    DFA.add_state("problem_3")
    DFA.add_state("endprob_3")
    DFA.add_state("problem_4")
    DFA.add_state("endprob_4")
    DFA.add_state("feedback_1")
    DFA.add_state("feedback_2")

    reph = r'^ *(\+? *7|8)? *-? *(\(9\d\d\)|9\d\d) *( *-? *\d){7} *$'
    reem = r'''(?:[a-z0-9!#$%&'*+/=?^_`{|}~-]+(?:\.[a-z0-9!#$%&'*+/=?^_`{|}~-]+)*|"(?:[\x01-\x08\x0b\x0c\x0e-\x1f\x21\x23-\x5b\x5d-\x7f]|\\[\x01-\x09\x0b\x0c\x0e-\x7f])*")@(?:(?:[a-z0-9](?:[a-z0-9-]*[a-z0-9])?\.)+[a-z0-9](?:[a-z0-9-]*[a-z0-9])?|\[(?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?|[a-z0-9-]*[a-z0-9]:(?:[\x01-\x08\x0b\x0c\x0e-\x1f\x21-\x5a\x53-\x7f]|\\[\x01-\x09\x0b\x0c\x0e-\x7f])+)\])'''

    # -------------------------
    # DFA.add_transition(regex, source, dest, func)
    DFA.add_transition('.*', "some_words_1", "some_words_2", PF.any)
    DFA.add_transition('.*', "some_words_2", "input_phone", PF.any)
    DFA.add_transition(reph, "input_phone", "input_email", PF.parse_phone)
    DFA.add_transition('.*', "input_phone", "input_phone_error", PF.any)  # ERROR
    DFA.add_transition(reph, "input_phone_error", "input_email", PF.parse_phone)  # OK
    DFA.add_transition('.*', "input_phone_error", "input_phone_error", PF.any)  # ERROR
    DFA.add_transition(reem, "input_email", "end_input", PF.parse_email)
    DFA.add_transition('.*', "input_email", "input_email_error", PF.any)  # ERROR
    DFA.add_transition(reem, "input_email_error", "end_input", PF.parse_email)  # OK
    DFA.add_transition('.*', "input_email_error", "input_email_error", PF.any)  # ERROR

    # ----- Задачи -----
    DFA.add_transition('.*', "end_input", "problem_1", PF.any)
    DFA.add_transition('.*', "problem_1", "endprob_1", PF.any_save)
    DFA.add_transition('.*', "endprob_1", "problem_2", PF.any)
    DFA.add_transition('.*', "problem_2", "endprob_2", PF.any_save)
    DFA.add_transition('.*', "endprob_2", "problem_3", PF.any)
    DFA.add_transition('.*', "problem_3", "endprob_3", PF.any_save)
    DFA.add_transition('.*', "endprob_3", "problem_4", PF.any)
    DFA.add_transition('.*', "problem_4", "endprob_4", PF.any_save)
    DFA.add_transition('.*', "endprob_4", "feedback_1", PF.get_feedback)
    DFA.add_transition('.*', "feedback_1", "feedback_2", PF.get_feedback)
    DFA.add_transition('.*', "feedback_2", "feedback_2", PF.any)

    DFA.add_template("some_words_1", {'message': msg['start'],
                                           'keyboard':
                                               [
                                                   [but['b1']],
                                               ]
                                                })
    DFA.add_template("some_words_2", {'message': msg['q1'],
                                           'keyboard':
                                               [
                                                   [but['b2']],
                                               ]
                                                })
    DFA.add_template("input_phone", {'message': msg['phone']})
    DFA.add_template("input_email", {'message': msg['email']})
    DFA.add_template("input_phone_error", {'message': msg['error1']})
    DFA.add_template("input_email_error", {'message': msg['error2']})
    DFA.add_template("end_input", {'message': msg['main'],
                                           'keyboard':
                                               [
                                                   [but['b3']],
                                               ]
                                                })
    DFA.add_template("problem_1", {'message': task['1']})
    DFA.add_template("endprob_1", {'message': msg['buf'],
                                           'keyboard':
                                               [
                                                   [but['b4']],
                                               ]
                                                })
    DFA.add_template("problem_2", {'message': task['2']})
    DFA.add_template("endprob_2", {'message': msg['buf'],
                                           'keyboard':
                                               [
                                                   [but['b4']],
                                               ]
                                                })
    DFA.add_template("problem_3", {'message': task['3']})
    DFA.add_template("endprob_3", {'message': msg['buf'],
                                           'keyboard':
                                               [
                                                   [but['b4']],
                                               ]
                                                })
    DFA.add_template("problem_4", {'message': task['4'], 'attachments': ['task4.jpg']})
    DFA.add_template("endprob_4", {'message': [msg['ok'], msg['feedback1']],
                                           'keyboard':
                                               [
                                                   ['Очень легкие'],
                                                   ['Средней сложности'],
                                                   ['Очень сложные']
                                               ]
                                                })

    DFA.add_template("feedback_1", {'message': msg['feedback2'],
                                           'keyboard':
                                               [
                                                   ['3'],
                                                   ['2'],
                                                   ['1']
                                               ]
                                                })
    DFA.add_template("feedback_2", {'message': msg['end']})
