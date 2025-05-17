from dfa import DFA
import streamlit as st
from dfa import DFA
import graphviz

# Define a sample DFA
states = {'q0', 'q1'}
alphabet = {'0', '1'}
transitions = {
    ('q0', '0'): 'q0',
    ('q0', '1'): 'q1',
    ('q1', '0'): 'q1',
    ('q1', '1'): 'q0'
}
start_state = 'q0'
accept_states = {'q1'}

dfa = DFA(states, alphabet, transitions, start_state, accept_states)

# Streamlit UI
st.title("DFA Simulator")

user_input = st.text_input("Enter a binary string (0s and 1s):")

if st.button("Validate"):
    if dfa.validate_string(user_input):
        st.success("✅ String is VALID and accepted by the DFA!")
    else:
        st.error("❌ String is INVALID or rejected by the DFA.")

# DFA Diagram
def render_dfa(transitions, start, accept):
    dot = graphviz.Digraph(format="png")
    dot.attr(rankdir='LR')

    dot.node('', shape='none')  # fake start arrow
    for state in set([s for s, _ in transitions.keys()] + list(transitions.values())):
        if state in accept:
            dot.node(state, shape='doublecircle')
        else:
            dot.node(state)

    dot.edge('', start)

    for (src, symbol), dst in transitions.items():
        dot.edge(src, dst, label=symbol)

    return dot

st.graphviz_chart(render_dfa(transitions, start_state, accept_states))
