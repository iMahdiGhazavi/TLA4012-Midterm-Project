import json
import sys


def dfa_initialization():
    # dfa = json.load(open(json_path))

    dfa = {
        "states": "{'q0','q1','q2','q3','q4'}",
        "input_symbols": "{'0','1'}",
        "transitions": {
            "q0": {
                "0": "q1",
                "1": "q3"
            },
            "q1": {
                "0": "q2",
                "1": "q4"
            },
            "q2": {
                "0": "q1",
                "1": "q4"
            },
            "q3": {
                "0": "q2",
                "1": "q4"
            },
            "q4": {
                "0": "q4",
                "1": "q4"
            }
        },
        "initial_state": "q0",
        "final_states": "{'q4'}"
    }

    dfa_states = [state[1: -1] for state in dfa['states'][1: -1].split(',')]
    dfa_alphabets = [alphabet[1: -1] for alphabet in dfa['input_symbols'][1: -1].split(',')]

    dfa_transitions = {}
    for key in dfa['transitions']:
        for k in dfa['transitions'][key].keys():
            dfa_transitions[(key, k)] = dfa['transitions'][key][k]

    dfa_initial_state = dfa['initial_state']
    dfa_final_states = [state[1: -1] for state in dfa['final_states'][1: -1].split(',')]

    return dfa_states, dfa_alphabets, dfa_transitions, dfa_initial_state, dfa_final_states


def output_format_generator(dfa_states, dfa_transitions, dfa_final_states, nfa_alphabets, nfa_initial_state):
    output = {}

    output_states = '{'
    for i in range(len(dfa_states)):
        if dfa_states[i]:
            state = ''
            for s in dfa_states[i]:
                state = state + s

        else:
            state = "TRAP"
        output_states = output_states + f"'{state}'"
        if not (i + 1) == len(dfa_states):
            output_states = output_states + ','

    output_states = output_states + '}'
    output['states'] = output_states

    alphabet = '{'
    for i in range(len(nfa_alphabets)):
        alphabet = alphabet + f"'{nfa_alphabets[i]}'"
        if not (i + 1) == len(nfa_alphabets):
            alphabet = alphabet + ','
    alphabet = alphabet + '}'
    output['input_symbols'] = alphabet

    new_dfs_states = []
    for index in dfa_states:
        state = ''
        for i in index:
            state = state + i

        new_dfs_states.append(state)

    new_dfa_transitions = {}
    for key in dfa_transitions.keys():
        string_state = ''
        for state in key[0]:
            string_state = string_state + state

        dest_state = ''
        for state in dfa_transitions[key]:
            dest_state = dest_state + state

        new_dfa_transitions[(string_state, key[1])] = dest_state

    output_transitions = {}
    for state in new_dfs_states:
        if not state:
            output_transitions["TRAP"] = {}
        else:
            output_transitions[state] = {}

    for state in output_transitions.keys():
        value = {}
        if state == "TRAP":
            for element in nfa_alphabets:
                value[element] = "TRAP"
            output_transitions[state] = value
            continue

        for transition in new_dfa_transitions.keys():
            if state == transition[0]:
                if not new_dfa_transitions[transition]:
                    value[transition[1]] = "TRAP"
                else:
                    value[transition[1]] = new_dfa_transitions[transition]
            if len(value.keys()) == len(nfa_alphabets):
                output_transitions[state] = value
                break

    output['transitions'] = output_transitions

    output['initial_state'] = nfa_initial_state

    output_final_states = '{'
    for i in range(len(dfa_final_states)):
        if dfa_final_states[i]:
            state = ''
            for s in dfa_final_states[i]:
                state = state + s

            output_final_states = output_final_states + f"'{state}'"
            if not (i + 1) == len(dfa_final_states):
                output_final_states = output_final_states + ','
    output_final_states = output_final_states + '}'
    output['final_states'] = output_final_states

    return output


if __name__ == '__main__':
    # args = sys.argv[1:]
    # json_path = args[0]
    dfa_states, dfa_alphabets, dfa_transitions, dfa_initial_state, dfa_final_states = dfa_initialization()
