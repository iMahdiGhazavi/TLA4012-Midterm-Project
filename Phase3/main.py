import sys
import json
from typing import List, Tuple, Set


def set_of_reachables(transitions: List[Tuple[str, str, str]], state: str, alphabet: str) -> Set[str]:
    next_states = set()
    for transition in transitions:
        if transition[0] != state:
            continue
        elif transition[1] == alphabet:
            next_states.add(transition[2])
    return next_states


def find_states(current: Set[str], transitions: List[Tuple[str, str, str]], alphabet: str) -> Set[str]:
    next_states = set()
    for state in current:
        next_states.update(set_of_reachables(transitions, state, alphabet))
    return next_states


def final_check(in_str: str, alphabets: List[str], final_states: List[str], initial_state: str,
                transitions: List[Tuple[str, str, str]]) -> bool:
    current = set()
    current.add(initial_state)
    current.update(find_states(current, transitions, '$'))
    for ch in in_str:
        if ch not in alphabets:
            return False
        current = find_states(current, transitions, ch)
        current.update(find_states(current, transitions, '$'))
    result = current.intersection(final_states)
    if len(result) == 0:
        return False
    else:
        return True


def Finite_automata(json_path):
    Fa = json.load(open(json_path))

    # Fa = {
    #     "states": "{'A','B'}",
    #     "input_symbols": "{'a','b'}",
    #     "transitions": {
    #         "A": {
    #             "a": "B",
    #             "b": "A"
    #         },
    #         "B": {
    #             "a": "B",
    #             "b": "B"
    #         }
    #     },
    #     "initial_state": "A",
    #     "final_states": "{'B'}"
    # }
    Fa_states = ''
    for i in range(len(Fa['states'][1: -1].split(','))):
        Fa_states = Fa_states + Fa['states'][1: -1].split(',')[i][1: -1]
        if not (i + 1) == len(Fa['states'][1: -1].split(',')):
            Fa_states = Fa_states + ','

    Fa_alphabets = ''
    for i in range(len(Fa['input_symbols'][1: -1].split(','))):
        Fa_alphabets = Fa_alphabets + Fa['input_symbols'][1: -1].split(',')[i][1: -1]
        if not (i + 1) == len(Fa['input_symbols'][1: -1].split(',')):
            Fa_alphabets = Fa_alphabets + ','

    Fa_transitions = []
    for state, transitions in Fa['transitions'].items():
        for symbol in transitions.keys():
            Fa_transitions.append(f'{state},{symbol},{transitions[symbol]}')

    Fa_initial_state = Fa['initial_state']
    Fa_final_states = ''
    for i in range(len(Fa['final_states'][1: -1].split(','))):
        Fa_final_states = Fa_final_states + Fa['final_states'][1: -1].split(',')[i][1: -1]
        if not (i + 1) == len(Fa['final_states'][1: -1].split(',')):
            Fa_final_states = Fa_final_states + ','

    return Fa_states, Fa_alphabets, Fa_transitions, Fa_initial_state, Fa_final_states


if __name__ == '__main__':

    args = sys.argv[1:]
    json_path = args[0]

    Fa_states, Fa_alphabets, Fa_transitions, Fa_initial_state, Fa_final_states = Finite_automata(json_path)

    input_states = Fa_states
    input_alphabet = Fa_alphabets
    input_final_states = Fa_final_states
    input_transitions_no = len(Fa_transitions)

    input_transitions = Fa_transitions

    target = input().strip('{} \t\n\r')

    start_state = input_states.split(',')[0]
    final_states = set(input_final_states.split(','))
    alphabets = set(input_alphabet.split(','))

    transitions = []
    for i in range(input_transitions_no):
        temp = input_transitions[i].split(',')
        transitions.append((temp[0], temp[1], temp[2]))

    if final_check(target, alphabets, final_states, start_state, transitions):
        print("Accepted")
    else:
        print("Rejected")
