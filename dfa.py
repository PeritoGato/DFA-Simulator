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
                return False, path, f"Invalid symbol '{symbol}' not in alphabet."

            key = (current_state, symbol)
            if key not in self.transitions:
                return False, path, f"No transition defined for state '{current_state}' with input '{symbol}'."

            next_state = self.transitions[key]
            current_state = next_state
            path.append(current_state)

            # Trap state rejection (optional: can be accepted or rejected depending on DFA design)
            if current_state == 'T':  # If trap state means automatic reject
                return False, path, "Entered trap state."

        if current_state in self.accept_states:
            return True, path, "String accepted."
        else:
            return False, path, "Did not end in accepting state."
