from CoreBot import DFA, PF


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

    # -------------------------
    # DFA.add_transition(regex, source, dest, func)
    DFA.add_transition(None, "some_words_1", "some_words_2", PF.any)
    DFA.add_transition(None, "some_words_2", "input_phone", PF.any)
    DFA.add_transition(None, "input_phone", "input_email", PF.parse_phone)
    DFA.add_transition(None, "input_phone", "input_phone_error", PF.any)  # ERROR
    DFA.add_transition(None, "input_phone_error", "input_phone_error", PF.any)  # ERROR
    DFA.add_transition(None, "input_phone_error", "input_email", PF.parse_phone)  # OK
    DFA.add_transition(None, "input_email", "end_input", PF.parse_email)
    DFA.add_transition(None, "input_email", "input_email_error", PF.any)  # ERROR
    DFA.add_transition(None, "input_email_error", "input_email_error", PF.any)  # ERROR
    DFA.add_transition(None, "input_email_error", "end_input", PF.parse_email)  # OK

    # ----- Задачи -----
    DFA.add_transition(None, "end_input", "problem_1", PF.any)
    DFA.add_transition(None, "problem_1", "endprob_1", PF.any_save)
    DFA.add_transition(None, "endprob_1", "problem_2", PF.any)
    DFA.add_transition(None, "problem_2", "endprob_2", PF.any_save)
    DFA.add_transition(None, "endprob_2", "problem_3", PF.any)
    DFA.add_transition(None, "problem_3", "endprob_3", PF.any_save)
    DFA.add_transition(None, "endprob_3", "problem_4", PF.any)
    DFA.add_transition(None, "problem_4", "endprob_4", PF.any_save)
    DFA.add_transition(None, "endprob_4", "endprob_4", PF.any)
