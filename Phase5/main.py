import json
import sys


def fa_initialization(fa):
    fa_states = eval(fa['states'])
    fa_alphabets = eval(fa['input_symbols'])
    fa_transitions = fa['transitions']
    fa_initial_state = fa['initial_state']
    fa_final_states = eval(fa['final_states'])

    return fa_states, fa_alphabets, fa_transitions, fa_initial_state, fa_final_states


def fa_to_regex(fa):
    fa_states, fa_alphabets, fa_transitions, fa_initial_state, fa_final_states = fa_initialization(fa)
    equations = {}
    # for key, value in fa_transitions.items():
    #     equations[key] = [[[k, state] for state in eval(v)] for k, v in value.items()]

    for key, value in fa_transitions.items():
        state_transitions = []
        for k, v in value.items():
            state_transitions = state_transitions + [[k, state] for state in eval(v)]

        for state_transition1 in state_transitions:
            for state_transition2 in state_transitions[state_transitions.index(state_transition1)+1:]:
                if state_transition1[1] == state_transition2[1]:
                    state_transition1[0] = state_transition1[0] + '+' + state_transition2[0]
                    state_transitions.remove(state_transition2)

        equations[key] = state_transitions

    for state in fa_final_states:
        equations[state] = equations[state] + ['']




if __name__ == '__main__':
    # args = sys.argv[1:]
    # fa_json_path = args[0]
    # fa = json.load(open(fa_json_path))
    # regex = fa_to_regex(fa)

    fa = {
        "states": "{'q0','q1','q2'}",
        "input_symbols": "{'a','b'}",
        "transitions": {
            "q0": {
                "b": "{'q1'}"
            },
            "q1": {
                "a": "{'q0','q2'}",
                "b": "{'q1','q2'}"
            },
            "q2": {
                "b": "{'q2'}"
            }
        },
        "initial_state": "q0",
        "final_states": "{'q2'}"
    }

    regex = fa_to_regex(fa)
    print("ok")


    # for _ in range(len(equations.items())):
    #     for key, value in equations.items():
    #         for element in value:
    #             if len(element) > 1 and element[1] == key and (len(element) == 0 or len(element) == 1):
    #                 equations[key] = [element[0][0] + '*' + element[1]]
    #                 for k, v in equations.items():
    #                     for transition in v:
    #                         if len(transition) > 1 and transition[1] == key:
    #                             transition.remove(key)
    #                             transition[0] = transition[0] + equations[key]
    #
    # print(equations)