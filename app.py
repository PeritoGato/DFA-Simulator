import streamlit as st
import graphviz
import time

# Minimal DFA class for validation and path tracking
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

        for char in input_string:
            if (current_state, char) in self.transitions:
                current_state = self.transitions[(current_state, char)]
                path.append(current_state)
            else:
                # No valid transition => reject
                message = f"No transition from state {current_state} on symbol '{char}'."
                return False, path, message

        if current_state in self.accept_states:
            return True, path, "String accepted."
        else:
            return False, path, f"Ended in non-accepting state {current_state}."

# Render DFA graph with Graphviz
def render_dfa(transitions, start, accept, current_state=None, next_state=None):
    dot = graphviz.Digraph(format="png")
    dot.attr(rankdir='LR')

    dot.node('', shape='none')  # Starting arrow

    # Collect all states including trap states
    states = set()
    for (src, _), dst in transitions.items():
        states.add(src)
        states.add(dst)

    for state in states:
        if state.startswith('T'):  # Trap states colored gray
            fill = 'lightgray'
            shape = 'circle'
        else:
            shape = 'doublecircle' if state in accept else 'circle'
            fill = 'lightblue' if state == current_state else 'yellow' if state == next_state else 'white'
        dot.node(state, shape=shape, style='filled', fillcolor=fill)

    dot.edge('', start)

    for (src, symbol), dst in transitions.items():
        color = 'red' if src == current_state and dst == next_state else 'black'
        penwidth = '2' if color == 'red' else '1'
        dot.edge(src, dst, label=symbol, color=color, penwidth=penwidth)

    return dot

# Define DFA states and trap states
states = {f'q{i}' for i in range(1, 29)}
trap_states = {'T3', 'T8', 'T9'}  # unique trap states for q3, q8, q9
states.update(trap_states)

alphabet = {'a', 'b'}
transitions = {
    ('q1', 'a'): 'q2',
    ('q1', 'b'): 'q3',
    ('q2', 'b'): 'q4',
    ('q3', 'a'): 'q4',
    ('q3', 'b'): 'T3',  # q3's unique trap state
    ('q4', 'a'): 'q5',
    ('q4', 'b'): 'q6',
    ('q5', 'a'): 'q9',
    ('q9', 'a'): 'q10',
    ('q9', 'b'): 'T9',  # q9's unique trap state
    ('q5', 'b'): 'q7',
    ('q7', 'a'): 'q10',
    ('q7', 'b'): 'q3',
    ('q6', 'b'): 'q8',
    ('q6', 'a'): 'q4',
    ('q8', 'b'): 'q10',
    ('q8', 'a'): 'T8',  # q8's unique trap state
    ('q10','b'): 'q11',
    ('q11','a'): 'q12',
    ('q10','a'): 'q10',
    ('q11','b'): 'q11',
    ('q12','b'): 'q13',
    ('q13','a'): 'q14',
    ('q14','a'): 'q19',
    ('q12','a'): 'q15',
    ('q15','b'): 'q16',
    ('q15','a'): 'q17',
    ('q17','b'): 'q16',
    ('q16','a'): 'q14',
    ('q16','b'): 'q19',
    ('q14','b'): 'q13',
    ('q13','b'): 'q18',
    ('q18','b'): 'q19',
    ('q18','a'): 'q12',
    ('q17','a'): 'q19',
    ('q19','b'): 'q20',
    ('q20','b'): 'q21',
    ('q21','a'): 'q22',
    ('q22','b'): 'q27',
    ('q27','a'): 'q26',
    ('q21','b'): 'q21',
    ('q19','a'): 'q24',
    ('q24','a'): 'q23',
    ('q23','a'): 'q23',
    ('q23','b'): 'q25',
    ('q24','b'): 'q25',
    ('q25','b'): 'q21',
    ('q20','a'): 'q22',
    ('q25','a'): 'q26',
    ('q26','a'): 'q23',
    ('q27','b'): 'q21',
    ('q22','a'): 'q23',
    ('q26','b'): 'q27',
}

start_state = 'q1'
accept_states = {'q21', 'q23', 'q26', 'q27'}

dfa = DFA(states, alphabet, transitions, start_state, accept_states)

st.title("🔁 DFA Simulator with Separate Trap States")

user_input = st.text_input("Enter a string using only 'a' and 'b':")

if st.button("Validate"):
    if not user_input:
        st.warning("Please enter a string.")
    else:
        is_accepted, path, message = dfa.validate_string(user_input)

        st.subheader("DFA Animation:")
        graph_placeholder = st.empty()

        if len(path) == 1:
            graph_placeholder.graphviz_chart(render_dfa(transitions, start_state, accept_states, current_state=path[0]))
        else:
            graph_placeholder.graphviz_chart(render_dfa(transitions, start_state, accept_states, current_state=path[0]))
            for i in range(len(path) - 1):
                time.sleep(1)
                curr = path[i]
                next_ = path[i + 1]
                graph_placeholder.graphviz_chart(render_dfa(transitions, start_state, accept_states, current_state=curr, next_state=next_))
            
            time.sleep(1)
            graph_placeholder.graphviz_chart(render_dfa(transitions, start_state, accept_states, current_state=path[-1]))

        st.subheader("Final Result:")
        if is_accepted:
            st.success(f"✅ Accepted! Reached accepting state: {path[-1]}")
            st.balloons()
        else:
            st.error(f"❌ Rejected: {message}")
