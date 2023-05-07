import sys
import json


def set_of_reachable_states(transitions, state, alphabet):
    next_states = []
    for transition in transitions:
        if transition[0] != state:
            continue
        elif transition[1] == alphabet:
            next_states.append(transition[2])

    return next_states


def find_states(current_states, transitions, alphabet):
    next_states = []
    for state in current_states:
        next_states += list(set_of_reachable_states(transitions, state, alphabet))

    return list(set(next_states))


def final_fa_check(input_string, alphabets, final_states, initial_state, transitions):
    current_states = []
    current_states.append(initial_state)
    current_states += find_states(current_states, transitions, '$')
    for char in input_string:
        if char not in alphabets:
            return False

        current_states = find_states(current_states, transitions, char)
        current_states += find_states(current_states, transitions, '$')

    result = set(current_states).intersection(set(final_states))
    if not result:
        return False
    else:
        return True


def fa_initialization(json_path):
    fa = json.load(open(json_path))

    fa_states = ''
    for i in range(len(fa['states'][1: -1].split(','))):
        fa_states = fa_states + fa['states'][1: -1].split(',')[i][1: -1]
        if not (i + 1) == len(fa['states'][1: -1].split(',')):
            fa_states = fa_states + ','

    fa_alphabets = ''
    for i in range(len(fa['input_symbols'][1: -1].split(','))):
        fa_alphabets = fa_alphabets + fa['input_symbols'][1: -1].split(',')[i][1: -1]
        if not (i + 1) == len(fa['input_symbols'][1: -1].split(',')):
            fa_alphabets = fa_alphabets + ','

    fa_transitions = []
    for state, transitions in fa['transitions'].items():
        for symbol in transitions.keys():
            fa_transitions.append(f'{state},{symbol},{transitions[symbol]}')

    fa_initial_state = fa['initial_state']
    fa_final_states = ''
    for i in range(len(fa['final_states'][1: -1].split(','))):
        fa_final_states = fa_final_states + fa['final_states'][1: -1].split(',')[i][1: -1]
        if not (i + 1) == len(fa['final_states'][1: -1].split(',')):
            fa_final_states = fa_final_states + ','

    return fa_states, fa_alphabets, fa_transitions, fa_initial_state, fa_final_states


if __name__ == '__main__':
    args = sys.argv[1:]
    json_path = args[0]

    fa_states, fa_alphabets, fa_transitions, fa_initial_state, fa_final_states = fa_initialization(json_path)

    input_states = fa_states
    input_alphabet = fa_alphabets
    input_final_states = fa_final_states
    input_transitions = fa_transitions
    target = input().strip('{} \t\n\r')
    initial_state = input_states.split(',')[0]
    final_states = set(input_final_states.split(','))
    alphabets = set(input_alphabet.split(','))

    transitions = []
    for i in range(len(fa_transitions)):
        temp = input_transitions[i].split(',')
        transitions.append((temp[0], temp[1], temp[2]))

    if final_fa_check(target, list(alphabets), list(final_states), initial_state, transitions):
        print("Accepted")
    else:
        print("Rejected")
