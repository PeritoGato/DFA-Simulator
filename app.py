from dfa import DFA
import streamlit as st
from dfa import DFA
import graphviz

# Define a sample DFA
states = {f'q{1}' for i in range (28)}
alphabet = {'a', 'b'}
transitions = {
    ('q1', 'a'): 'q2',
    ('q1', 'b'): 'q3',
    ('q2', 'b'): 'q4',
    ('q3', 'a'): 'q4',
    ('q4', 'a'): 'q5',
    ('q4', 'b'): 'q6',
    ('q5', 'a'): 'q9',
    ('q9', 'a'): 'q10',
    ('q5', 'b'): 'q7',
    ('q7', 'a'): 'q10',
    ('q6', 'b'): 'q8',
    ('q8', 'b'): 'q10',
    ('q6', 'a'): 'q4',
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
    ('q21','b'): 'q21'
}
start_state = 'q1'
accept_states = {'q21', 'q23', 'q26', 'q27'}

dfa = DFA(states, alphabet, transitions, start_state, accept_states)

# Streamlit UI
st.title("DFA Simulator")

user_input = st.text_input("Enter a binary string (a and b):")

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
