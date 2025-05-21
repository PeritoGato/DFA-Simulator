import streamlit as st
import graphviz
import time

# --- DFA class ---
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
                return False, path, f"No transition from state {current_state} on symbol '{char}'."
        if current_state in self.accept_states:
            return True, path, "String accepted."
        else:
            return False, path, f"Ended in non-accepting state {current_state}."

# --- DFA rendering ---
def render_dfa(transitions, start, accept, current_state=None, next_state=None):
    dot = graphviz.Digraph(format="png")
    dot.attr(rankdir='LR')
    dot.node('', shape='none')

    states = set()
    for (src, _), dst in transitions.items():
        states.add(src)
        states.add(dst)

    for state in states:
        shape = 'doublecircle' if state in accept else 'circle'
        fill = 'lightblue' if state == current_state else 'yellow' if state == next_state else 'white'
        dot.node(state, shape=shape, style='filled', fillcolor=fill)

    dot.edge('', start)

    for (src, symbol), dst in transitions.items():
        color = 'red' if src == current_state and dst == next_state else 'black'
        penwidth = '2' if color == 'red' else '1'
        dot.edge(src, dst, label=symbol, color=color, penwidth=penwidth)

    return dot

# --- DFA definitions ---
def get_dfa_ab():
    states = {f'q{i}' for i in range(1, 29)} | {'T3', 'T8', 'T9'}
    alphabet = {'a', 'b'}
    start_state = 'q1'
    accept_states = {'q21', 'q23', 'q26', 'q27'}
    transitions = {
        ('q1', 'a'): 'q2', ('q1', 'b'): 'q3', ('q2', 'b'): 'q4',
        ('q3', 'a'): 'q4', ('q3', 'b'): 'T3', ('q4', 'a'): 'q5',
        ('q4', 'b'): 'q6', ('q5', 'a'): 'q9', ('q9', 'a'): 'q10',
        ('q9', 'b'): 'T9', ('q5', 'b'): 'q7', ('q7', 'a'): 'q10',
        ('q7', 'b'): 'q3', ('q6', 'b'): 'q8', ('q6', 'a'): 'q4',
        ('q8', 'b'): 'q10', ('q8', 'a'): 'T8', ('q10', 'b'): 'q11',
        ('q11', 'a'): 'q12', ('q10', 'a'): 'q10', ('q11', 'b'): 'q11',
        ('q12', 'b'): 'q13', ('q13', 'a'): 'q14', ('q14', 'a'): 'q19',
        ('q12', 'a'): 'q15', ('q15', 'b'): 'q16', ('q15', 'a'): 'q17',
        ('q17', 'b'): 'q16', ('q16', 'a'): 'q14', ('q16', 'b'): 'q19',
        ('q14', 'b'): 'q13', ('q13', 'b'): 'q18', ('q18', 'b'): 'q19',
        ('q18', 'a'): 'q12', ('q17', 'a'): 'q19', ('q19', 'b'): 'q20',
        ('q20', 'b'): 'q21', ('q21', 'a'): 'q22', ('q22', 'b'): 'q27',
        ('q27', 'a'): 'q26', ('q21', 'b'): 'q21', ('q19', 'a'): 'q24',
        ('q24', 'a'): 'q23', ('q23', 'a'): 'q23', ('q23', 'b'): 'q25',
        ('q24', 'b'): 'q25', ('q25', 'b'): 'q21', ('q20', 'a'): 'q22',
        ('q25', 'a'): 'q26', ('q26', 'a'): 'q23', ('q27', 'b'): 'q21',
        ('q22', 'a'): 'q23', ('q26', 'b'): 'q27'
    }
    return DFA(states, alphabet, transitions, start_state, accept_states), transitions, start_state, accept_states

def get_dfa_01():
    states = {str(i) for i in range(1, 49)} | {'T'}
    alphabet ={'0', '1'}
    start_state = '1'
    accept_states ={'32'}
    transitions = {
            ('1', '0'): '24', ('1', '1'): '33', ('2', '0'): '9', ('2', '1'): '10',
            ('3', '0'): '11', ('3', '1'): '6', ('4', '0'): '9', ('4', '1'): '12',
            ('5', '0'): '13', ('5', '1'): '6', ('6', '0'): '14', ('6', '1'): '15',
            ('7', '0'): '16', ('7', '1'): '38', ('8', '0'): '17', ('8', '1'): '15',
            ('9', '0'): '16', ('9', '1'): 'T', ('10', '0'): '17', ('10', '1'): '18',
            ('11', '0'): '19', ('11', '1'): 'T', ('12', '0'): '9', ('12', '1'): '20',
            ('13', '0'): '21', ('13', '1'): '22', ('14', '0'): '39', ('14', '1'): '23',
            ('15', '0'): '25', ('15', '1'): '26', ('16', '0'): '27', ('16', '1'): '22',
            ('17', '0'): 'T', ('17', '1'): '23', ('18', '0'): '28', ('18', '1'): '26',
            ('19', '0'): '29', ('19', '1'): '22', ('20', '0'): '28', ('20', '1'): '30',
            ('21', '0'): '21', ('21', '1'): '31', ('22', '0'): '14', ('22', '1'): '31',
            ('23', '0'): '7', ('23', '1'): '8', ('24', '0'): '34', ('24', '1'): 'T',
            ('25', '0'): '47', ('25', '1'): '31', ('26', '0'): '9', ('26', '1'): '31',
            ('27', '0'): '11', ('27', '1'): '31', ('28', '0'): '16', ('28', '1'): '31',
            ('29', '0'): '13', ('29', '1'): '31', ('30', '0'): '28', ('30', '1'): '31',
            ('31', '0'): '32', ('31', '1'): '31', ('32', '0'): '32', ('32', '1'): '32',
            ('33', '0'): '35', ('33', '1'): '35', ('34', '0'): '36', ('34', '1'): '36',
            ('35', '0'): 'T', ('35', '1'): '36', ('36', '0'): '37', ('36', '1'): '38',
            ('37', '0'): '39', ('37', '1'): '38', ('38', '0'): '37', ('38', '1'): '40',
            ('39', '0'): '41', ('39', '1'): '42', ('40', '0'): '43', ('40', '1'): '44',
            ('41', '0'): '45', ('41', '1'): '42', ('42', '0'): '14', ('42', '1'): '46',
            ('43', '0'): '47', ('43', '1'): '38', ('44', '0'): '17', ('44', '1'): '48',
            ('45', '0'): 'T', ('45', '1'): '49', ('46', '0'): '43', ('46', '1'): '2',
            ('47', '0'): '3', ('47', '1'): '42', ('48', '0'): '17', ('48', '1'): '4',
            ('T', '0'): 'T', ('T', '1'): 'T'
        }

    return DFA(states, alphabet, transitions, start_state, accept_states), transitions, start_state, accept_states

# --- App start ---
st.title("🧠 DFA / CFG / PDA Visualizer")

# Store view state
if "view_mode" not in st.session_state:
    st.session_state.view_mode = "dfa_ab"

regex_options = {
    "Regex (a, b)": "ab",
    "Regex (0, 1)": "01"
}
selected_label = st.selectbox("Choose a regular expression:", list(regex_options.keys()))
regex_key = regex_options[selected_label]

# Map view mode depending on choice
if st.session_state.view_mode.startswith("dfa") and not st.session_state.view_mode.endswith(regex_key):
    st.session_state.view_mode = f"dfa_{regex_key}"

# Show CFG/PDA/Back buttons
col1, col2, col3 = st.columns(3)
with col1:
    if st.button("📘 View CFG"):
        st.session_state.view_mode = f"cfg_{regex_key}"
with col2:
    if st.button("📗 View PDA"):
        st.session_state.view_mode = f"pda_{regex_key}"
with col3:
    if st.button("🔁 Back to DFA"):
        st.session_state.view_mode = f"dfa_{regex_key}"

# Show CFG
if st.session_state.view_mode == f"cfg_{regex_key}":
    st.subheader(f"📘 Context-Free Grammar for {selected_label}")
    st.image(f"Pictures\cfg_{regex_key}.png", caption=f"CFG for {selected_label}", use_container_width=True)

# Show PDA
elif st.session_state.view_mode == f"pda_{regex_key}":
    st.subheader(f"📗 Pushdown Automaton for {selected_label}")
    st.image(f"Pictures\pda_{regex_key}.png", caption=f"PDA for {selected_label}", use_container_width=True)

# Show DFA
elif st.session_state.view_mode == f"dfa_{regex_key}":
    # Load correct DFA
    if regex_key == "ab":
        dfa, transitions, start_state, accept_states = get_dfa_ab()
    else:
        dfa, transitions, start_state, accept_states = get_dfa_01()

    alphabet_display = ", ".join(sorted(dfa.alphabet))
    user_input = st.text_input(f"Enter a string using only: '{alphabet_display}'")

    if st.button("✅ Validate"):
        if not user_input:
            st.warning("Please enter a string.")
        elif not set(user_input).issubset(dfa.alphabet):
            st.error(f"❌ Invalid input. Use only: {alphabet_display}")
        else:
            is_accepted, path, message = dfa.validate_string(user_input)

            st.subheader("📍 Path Taken:")
            st.write(" > ".join(path))

            st.subheader("🌀 DFA Animation:")
            graph_placeholder = st.empty()
            graph_placeholder.graphviz_chart(render_dfa(transitions, start_state, accept_states, current_state=path[0]))

            for i in range(len(path) - 1):
                time.sleep(1)
                graph_placeholder.graphviz_chart(render_dfa(
                    transitions, start_state, accept_states,
                    current_state=path[i], next_state=path[i + 1]
                ))
            time.sleep(1)
            graph_placeholder.graphviz_chart(render_dfa(
                transitions, start_state, accept_states, current_state=path[-1]
            ))

            st.subheader("🏁 Final Result:")
            if is_accepted:
                st.success(f"✅ Accepted! Reached accepting state: {path[-1]}")
                st.balloons()
            else:
                st.error(f"❌ Rejected: {message}")
