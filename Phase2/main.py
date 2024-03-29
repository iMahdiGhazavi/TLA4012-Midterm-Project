import json
import sys


def has_reachable_states(state, dfa_alphabets, dfa_transitions, reachable_states):
    for alphabet in dfa_alphabets:
        if dfa_transitions[(state, alphabet)] not in reachable_states:
            return True

    return False


def find_reachable_states(dfa_state, dfa_alphabets, dfa_transitions, reachable_states):
    found_states = []
    for alphabet in dfa_alphabets:
        resulting_state = dfa_transitions[(dfa_state, alphabet)]
        if resulting_state not in reachable_states:
            reachable_states[resulting_state] = True
            found_states.append(resulting_state)

    for state in found_states:
        if has_reachable_states(state, dfa_alphabets, dfa_transitions, reachable_states):
            find_reachable_states(state, dfa_alphabets, dfa_transitions, reachable_states)


def remove_non_reachable_states(dfa_states, reachable_states):
    temp_states = dfa_states.copy()
    for state in temp_states:
        if state not in reachable_states:
            dfa_states.remove(state)


def divide_final_states(dfa_states, dfa_final_states, transition_table):
    for i in range(len(dfa_states)):
        for j in range(len(dfa_states)):
            if dfa_states[i] in dfa_final_states and dfa_states[j] in dfa_final_states:
                transition_table[i][j][0] = 1
            elif dfa_states[i] not in dfa_final_states and dfa_states[j] not in dfa_final_states:
                transition_table[i][j][0] = 1


def are_equivalent(i, j, k, dfa_states, dfa_alphabets, dfa_transitions, transition_table):
    for alphabet in dfa_alphabets:
        state1 = dfa_transitions[(dfa_states[i], alphabet)]
        state1_idx = dfa_states.index(state1)

        state2 = dfa_transitions[(dfa_states[j], alphabet)]
        state2_idx = dfa_states.index(state2)

        if transition_table[state1_idx][state2_idx][k] == 0:
            return False

    return True


def divide_equivalent_states(dfa_states, dfa_alphabets, dfa_transitions, transition_table):
    for k in range(1, len(dfa_states) - 1):
        for i in range(len(dfa_states)):
            for j in range(len(dfa_states)):
                if transition_table[i][j][k - 1] == 1 and are_equivalent(i, j, k - 1, dfa_states, dfa_alphabets,
                                                                         dfa_transitions, transition_table):
                    transition_table[i][j][k] = 1


def find_sdfa_states(dfa_states, transition_table):
    visited_states = [0 for _ in range(len(dfa_states))]
    sdfa_states = []
    for i in range(len(dfa_states)):
        if visited_states[i] == 1:
            continue

        visited_states[i] = 1
        sdfa_states.append([dfa_states[i]])

        for j in range(i + 1, len(dfa_states)):
            if transition_table[i][j][len(dfa_states) - 2] == 1:
                sdfa_states[-1].append(dfa_states[j])
                visited_states[j] = 1

    return sdfa_states


def find_sdfa_transitions(sdfa_states, dfa_alphabets, dfa_transitions):
    sdfa_transitions = {}
    for start_state in sdfa_states:
        for alphabet in dfa_alphabets:
            for resulting_state in sdfa_states:
                if dfa_transitions[(start_state[0], alphabet)] in resulting_state:
                    sdfa_transitions[(tuple(start_state), alphabet)] = tuple(resulting_state)

    return sdfa_transitions


def find_sdfa_final_states(sdfa_states, dfa_final_states):
    sdfa_final_states = []
    for state in sdfa_states:
        if state[0] in dfa_final_states:
            sdfa_final_states.append(state)

    return sdfa_final_states


def dfa_initialization(json_path):
    dfa = json.load(open(json_path))

    # dfa = {
    #     "states": "{'q0','q1','q2','q3','q4'}",
    #     "input_symbols": "{'0','1'}",
    #     "transitions": {
    #         "q0": {
    #             "0": "q1",
    #             "1": "q3"
    #         },
    #         "q1": {
    #             "0": "q2",
    #             "1": "q4"
    #         },
    #         "q2": {
    #             "0": "q1",
    #             "1": "q4"
    #         },
    #         "q3": {
    #             "0": "q2",
    #             "1": "q4"
    #         },
    #         "q4": {
    #             "0": "q4",
    #             "1": "q4"
    #         }
    #     },
    #     "initial_state": "q0",
    #     "final_states": "{'q4'}"
    # }

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
    args = sys.argv[1:]
    json_path = args[0]
    dfa_states, dfa_alphabets, dfa_transitions, dfa_initial_state, dfa_final_states = dfa_initialization(json_path)

    reachable_states = {
        dfa_states[0]: True,
    }
    find_reachable_states(dfa_states[0], dfa_alphabets, dfa_transitions, reachable_states)
    remove_non_reachable_states(dfa_states, reachable_states)

    transition_table = [[[0 for _ in range(len(dfa_states) - 1)] for _ in range(len(dfa_states))] for _ in
                        range(len(dfa_states))]

    divide_final_states(dfa_states, dfa_final_states, transition_table)

    divide_equivalent_states(dfa_states, dfa_alphabets, dfa_transitions, transition_table)

    sdfa_states = find_sdfa_states(dfa_states, transition_table)

    sdfa_transitions = find_sdfa_transitions(sdfa_states, dfa_alphabets, dfa_transitions)

    sdfa_final_states = find_sdfa_final_states(sdfa_states, dfa_final_states)

    sdfa = output_format_generator(sdfa_states, sdfa_transitions, sdfa_final_states, dfa_alphabets, dfa_initial_state)

    with open('SDFA.json', 'w') as f:
        json.dump(sdfa, f)
