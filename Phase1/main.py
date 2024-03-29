import json
import sys


def find_lambda_transitions(state):
    result = []
    if nfa_transitions.get((state, '')):
        for lambda_transition in nfa_transitions[(state, '')]:
            if lambda_transition not in result:
                result.append(lambda_transition)

    for item in result:
        lambda_states = find_lambda_transitions(item)
        for lambda_state in lambda_states:
            result.append(lambda_state)

    return result


def transition_states(state, alphabet, result):
    if nfa_transitions.get((state, alphabet)):
        for transition_state in nfa_transitions[(state, alphabet)]:
            if transition_state not in result:
                result.append(transition_state)

    lambda_transitions = result.copy()
    for s in lambda_transitions:
        lambda_states = find_lambda_transitions(s)
        for lambda_state in lambda_states:
            if lambda_state not in result:
                result.append(lambda_state)

    lambda_states = find_lambda_transitions(state)
    for item in lambda_states:
        transition_states(item, alphabet, result)

    return result


def find_new_states(current_state):
    for nfa_alphabet in nfa_alphabets:
        resulting_states = []
        for state in current_state:
            result = transition_states(state, nfa_alphabet, [])
            for item in result:
                if item not in resulting_states:
                    resulting_states.append(item)

        resulting_states = sorted(resulting_states)

        dfa_transitions[(tuple(current_state), nfa_alphabet)] = resulting_states
        if resulting_states not in dfa_states:
            dfa_states.append(resulting_states)

            if len(resulting_states) > 0:
                new_states.append(resulting_states)


def nfa_initialization(json_path):
    nfa = json.load(open(json_path))

    nfa_states = [state[1: -1] for state in nfa['states'][1: -1].split(',')]
    nfa_alphabets = [alphabet[1: -1] for alphabet in nfa['input_symbols'][1: -1].split(',')]

    nfa_transitions = {}
    for key in nfa['transitions']:
        for k in nfa['transitions'][key].keys():
            result_states = [s[1: -1] for s in nfa['transitions'][key][k][1: -1].split(',')]
            for result_state in result_states:
                if (key, k) not in nfa_transitions:
                    nfa_transitions[(key, k)] = [result_state]
                else:
                    nfa_transitions[(key, k)].append(result_state)

    nfa_initial_state = nfa['initial_state']
    nfa_final_states = [state[1: -1] for state in nfa['final_states'][1: -1].split(',')]

    return nfa_states, nfa_alphabets, nfa_transitions, nfa_initial_state, nfa_final_states


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

    nfa_states, nfa_alphabets, nfa_transitions, nfa_initial_state, nfa_final_states = nfa_initialization(json_path)

    dfa_initial_state = [nfa_initial_state]
    dfa_states = [dfa_initial_state]
    dfa_transitions = {}
    dfa_final_states = []
    new_states = [dfa_initial_state]

    for start_state in new_states:
        find_new_states(start_state)

    for state in dfa_states:
        for final_state in nfa_final_states:
            if final_state in state:
                dfa_final_states.append(state)
                break

    generated_dfa = output_format_generator(dfa_states, dfa_transitions, dfa_final_states, nfa_alphabets, nfa_initial_state)

    with open('out.json', 'w') as f:
        json.dump(generated_dfa, f)
