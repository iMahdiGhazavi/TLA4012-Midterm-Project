import json
import sys


def fa_initialization(fa):
    fa_states = eval(fa['states'])
    fa_alphabets = eval(fa['input_symbols'])
    fa_transitions = fa['transitions']
    fa_initial_state = fa['initial_state']
    fa_final_states = eval(fa['final_states'])

    return fa_states, fa_alphabets, fa_transitions, fa_initial_state, fa_final_states


def update_fa_states(fa, pump_num):
    fa['states'] = str(set([state[0] + str(int(state[1:]) + pump_num) for state in eval(fa['states'])]))
    fa['initial_state'] = fa['initial_state'][0] + str(int(fa['initial_state'][1:]) + pump_num)
    fa['final_states'] = str(set([state[0] + str(int(state[1:]) + pump_num) for state in eval(fa['final_states'])]))
    fa['transitions'] = {
        key: {k: str(set([state[0] + str(int(state[1:]) + pump_num) for state in eval(v)])) for k, v in
              value.items()} for key, value in fa['transitions'].items()}
    updated_transitions = {}
    for key, value in fa['transitions'].items():
        updated_transitions[key[0] + str(int(key[1:]) + pump_num)] = value

    fa['transitions'] = updated_transitions


def concatenate(fa1, fa2):
    fa1_states, fa1_alphabets, fa1_transitions, fa1_initial_state, fa1_final_states = fa_initialization(fa1)
    update_fa_states(fa2, len(fa1_states))
    fa2_states, fa2_alphabets, fa2_transitions, fa2_initial_state, fa2_final_states = fa_initialization(fa2)

    fa1_states.update(fa2_states)
    fa1_alphabets.update(fa2_alphabets)
    fa1_transitions.update(fa2_transitions)
    rfa_final_state = f'q{len(fa1_states)}'
    fa1_states.add(rfa_final_state)
    fa1_transitions[rfa_final_state] = {}

    for state in fa1_final_states:
        fa1_transitions[state].update({'': f"{{'{fa2_initial_state}'}}"})

    for state in fa2_final_states:
        fa1_transitions[state].update({'': f"{{'{rfa_final_state}'}}"})

    rfa = {
        'states': str(set(list(fa1_states))),
        'input_symbols': str(set(list(fa1_alphabets))),
        'transitions': fa1_transitions,
        'initial_state': fa1_initial_state,
        'final_states': '{' + f"'{rfa_final_state}'" + '}'
    }

    return rfa


def union(fa1, fa2):
    fa1_states, fa1_alphabets, fa1_transitions, fa1_initial_state, fa1_final_states = fa_initialization(fa1)
    update_fa_states(fa2, len(fa1_states))
    fa2_states, fa2_alphabets, fa2_transitions, fa2_initial_state, fa2_final_states = fa_initialization(fa2)

    fa1_states.update(fa2_states)
    fa1_alphabets.update(fa2_alphabets)
    fa1_transitions.update(fa2_transitions)

    rfa_initial_state = f'q{len(fa1_states)}'
    fa1_states.add(rfa_initial_state)
    fa1_transitions[rfa_initial_state] = {
        '': '{' + f"'{fa1_initial_state}','{fa2_initial_state}'" + '}'
    }
    rfa_final_state = f'q{len(fa1_states)}'
    fa1_states.add(rfa_final_state)
    fa1_transitions[rfa_final_state] = {}

    for state in fa1_final_states:
        fa1_transitions[state].update({'': f"{{'{rfa_final_state}'}}"})

    for state in fa2_final_states:
        fa1_transitions[state].update({'': f"{{'{rfa_final_state}'}}"})

    rfa = {
        'states': str(set(list(fa1_states))),
        'input_symbols': str(set(list(fa1_alphabets))),
        'transitions': fa1_transitions,
        'initial_state': rfa_initial_state,
        'final_states': '{' + f"'{rfa_final_state}'" + '}'
    }

    return rfa


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


if __name__ == '__main__':
    # # Inputs for Concatenation
    # args = sys.argv[1:]
    # fa1_json_path = args[0]
    # fa2_json_path = args[1]
    # fa1 = json.load(open(fa1_json_path))
    # fa2 = json.load(open(fa2_json_path))
    # rfa = concatenate(fa1, fa2)
    # with open('RFA.json', 'w') as f:
    #     json.dump(rfa, f)

    # # Inputs for Union
    # args = sys.argv[1:]
    # fa1_json_path = args[0]
    # fa2_json_path = args[1]
    # fa1 = json.load(open(fa1_json_path))
    # fa2 = json.load(open(fa2_json_path))
    # rfa = union(fa1, fa2)
    # with open('RFA.json', 'w') as f:
    #     json.dump(rfa, f)

    # Inputs for Star
    args = sys.argv[1:]
    fa_json_path = args[0]
    fa = json.load(open(fa_json_path))
    rfa = star(fa)
    with open('RFA.json', 'w') as f:
        json.dump(rfa, f)
