import json
import sys
from typing import List, Set


class NfaSimulator:

    def __init__(self, alphabets: Set[str], finalStates: Set[str], initialState: str, transitions: Set[List[str]]):
        self._alphabets = alphabets
        self._finalStates = finalStates
        self._initialState = initialState
        self._transitions = transitions

    def set_of_reachables(self, state: str, alphabet: str) -> Set[str]:
        next_states = set()
        for transition in self._transitions:
            if transition[0] != state:
                continue
            elif transition[1] == alphabet:
                next_states.add(transition[2])
            else:
                continue
        return next_states

    def find_states(self, current: Set[str], alphabet: str) -> Set[str]:
        next_states = set()
        for state in current:
            tmp = next_states.union(self.set_of_reachables(state, alphabet))
            next_states = set(tmp)
        return next_states

    def final_check(self, input_str: str) -> bool:
        current = set()
        current.add(self._initialState)
        tmp = current.union(self.find_states(current, "$"))
        current = set(tmp)
        for ch in input_str:
            if ch not in self._alphabets:
                return False
            else:
                current = self.find_states(current, ch)
                tmp = current.union(self.find_states(current, "$"))
                current = set(tmp)

        result = current.intersection(self._finalStates)
        if len(result) == 0:
            return False
        else:
            return True



def Finite_automata():
    Fa = {
        "states": "{'A','B'}",
        "input_symbols": "{'a','b'}",
        "transitions": {
            "A": {
                "a": "B",
                "b": "A"
            },
            "B": {
                "a": "B",
                "b": "B"
            }
        },
        "initial_state": "A",
        "final_states": "{'B'}"
    }
    Fa_states = [state[1: -1] for state in Fa['states'][1: -1].split(',')]
    Fa_alphabets = [alphabet[1: -1] for alphabet in Fa['input_symbols'][1: -1].split(',')]

    Fa_transitions = {}
    for key in Fa['transitions']:
        for k in Fa['transitions'][key].keys():
            result_states = [s[1: -1] for s in Fa['transitions'][key][k][1: -1].split(',')]
            for result_state in result_states:
                if (key, k) not in Fa_transitions:
                    Fa_transitions[(key, k)] = [result_state]
                else:
                    Fa_transitions[(key, k)].append(result_state)

    Fa_initial_state = Fa['initial_state']
    Fa_final_states = [state[1: -1] for state in Fa['final_states'][1: -1].split(',')]
    return Fa_states, Fa_alphabets, Fa_transitions, Fa_initial_state, Fa_final_states


if __name__ == "__main__":
    # inputStates = input().strip("{} \t\n\r")
    # inputAlphabet = input().strip("{} \t\n\r")
    # inputFinalStates = input().strip("{} \t\n\r")
    # inputTransitionsNo = int(input().strip("{} \t\n\r"))
    Fa_states, Fa_alphabets, Fa_transitions, Fa_initial_state, Fa_final_states = Finite_automata()

    inputTransitions = []
    # for i in range(inputTransitionsNo):
    #     inputTransitions.append(input().strip())
    for key in Fa_transitions.keys():
        inputTransitions.append(key)

    target = input().strip("{} \t\n\r")

    start_state = Fa_states[0]
    final_states = set(Fa_final_states)
    alphabets = set(Fa_alphabets)

    transitions = set()
    # for i in range(inputTransitionsNo):
    #     temp = inputTransitions[i].split(",")
    #     transitions.add([temp[0], temp[1], temp[2]])
    i=0
    for key in Fa_transitions.keys():
        temp=inputTransitions[i]
        transitions.add([temp[0], temp[1], temp[2]])
        i+=1

    simulator = NfaSimulator(alphabets, final_states, start_state, transitions)
    if simulator.final_check(target):
        print("Accepted")
    else:
        print("Rejected")
