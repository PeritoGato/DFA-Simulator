# dfa.py

class DFA:
    def __init__(self, states, alphabet, transitions, start_state, accept_states):
        self.states = states
        self.alphabet = alphabet
        self.transitions = transitions
        self.start_state = start_state
        self.accept_states = accept_states

    def validate_string(self, input_string):
        current_state = self.start_state
        path = [current_state]

        for symbol in input_string:
            if symbol not in self.alphabet:
                return False, path, f"Symbol '{symbol}' not in alphabet."

            current_state = self.transitions.get((current_state, symbol))
            if current_state is None:
                return False, path, f"No transition for ({path[-1]}, '{symbol}')."

            path.append(current_state)

        if current_state in self.accept_states:
            return True, path, "String accepted."
        else:
            return False, path, "Reached non-accepting state."
