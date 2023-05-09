import json
import sys


def fa_initialization(fa):
    fa_states = eval(fa['states'])
    fa_alphabets = eval(fa['input_symbols'])
    fa_transitions = fa['transitions']
    fa_initial_state = fa['initial_state']
    fa_final_states = eval(fa['final_states'])

    return fa_states, fa_alphabets, fa_transitions, fa_initial_state, fa_final_states


def star(fa):
    fa_states, fa_alphabets, fa_transitions, fa_initial_state, fa_final_states = fa_initialization(fa)

    rfa_initial_state = f'q{len(fa_states)}'
    fa_states.add(rfa_initial_state)
    rfa_final_state = f'q{len(fa_states)}'
    fa_states.add(rfa_final_state)
    fa_transitions[rfa_initial_state] = {
        '': '{' + f"'{fa_initial_state}','{rfa_final_state}'" + '}'
    }
    fa_transitions[rfa_final_state] = {
        '': '{' + f"'{rfa_initial_state}'" + '}'
    }

    for state in fa_final_states:
        fa_transitions[state].update({'': f"{{'{rfa_final_state}'}}"})

    rfa = {
        'states': str(set(list(fa_states))),
        'input_symbols': str(set(list(fa_alphabets))),
        'transitions': fa_transitions,
        'initial_state': rfa_initial_state,
        'final_states': '{' + f"'{rfa_final_state}'" + '}'
    }

    return rfa


if __name__ == "__main__":
    args = sys.argv[1:]
    fa_json_path = args[0]
    fa = json.load(open(fa_json_path))
    rfa = star(fa)
    with open('RFA.json', 'w') as f:
        json.dump(rfa, f)
