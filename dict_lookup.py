import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import json

st.title("📖 Dictionary Lookup Demo")
st.subheader("*Linear vs. Logarithmic Time*")

if 'queries' not in st.session_state:
    st.session_state['queries'] = []
if 'all_lin_steps' not in st.session_state:
    st.session_state['all_lin_steps'] = []
if 'all_bin_steps' not in st.session_state:
    st.session_state['all_bin_steps'] = []

@st.cache_data
def load_data():
    with open("dict_clean.json", 'r', encoding='utf-8') as infile:
        dict_entries = json.load(infile)
    return dict_entries

# Create a text element and let the reader know the data is loading.
data_load_state = st.text('Loading data (102118 words)...')
dict_entries = load_data()
# Notify the reader that the data was successfully loaded.
data_load_state.text('Loading data (102118 words)... done!')

# st.text(','.join(dict_entries[:10]))

intro = st.empty()
intro.markdown("Enter a word in the sidebar and press Enter to begin!")
result = st.empty()

lin_col, bin_col = st.columns(2, border=True)
with lin_col:
    st.header("Linear Search")
    lin_text = st.markdown("&nbsp;\n\n")
    lin_sep = st.markdown("---")
    lin_footer = st.empty()
with bin_col:
    st.header("Binary Search")
    bin_text = st.markdown("&nbsp;\n\n")
    bin_sep = st.markdown("---")
    bin_footer = st.empty()

with st.sidebar:
    st.header("Enter Word")
    input_col, button_col = st.columns([0.8, 0.2], vertical_alignment="bottom", gap="small")
    with input_col:
        query = st.text_input("Type word here", placeholder="Enter a word to look up")
    with button_col:
        st.button("&rarr;")

def lookup_word_lin(word_query):
    try:
        word_index = dict_entries.index(word_query)
    except ValueError:
        word_index = -1
    return word_index

def lookup_word_bin(word_query):
    low_index = 0
    high_index = len(dict_entries) - 1
    words_checked = []
    while low_index <= high_index:
        mid_index = (low_index + high_index) // 2
        mid_elt = dict_entries[mid_index]
        words_checked.append(mid_elt)
        if word_query < mid_elt:
            high_index = mid_index - 1
        elif word_query == mid_elt:
            return words_checked
        else:
            low_index = mid_index + 1
    return words_checked

def construct_path_str(path_entries):
    if len(path_entries) <= 4:
        return " ➡️ ".join(path_entries)
    else:
        return f"{path_entries[0]} ➡️ {path_entries[1]} ➡️ ⋯ ➡️ {path_entries[-2]} ➡️ {path_entries[-1]}"

if query:
    st.session_state['queries'].append(query)
    intro.empty()
    intro.markdown(f"Your query is: **{query}**")
    word_index = lookup_word_lin(query)
    lin_steps = word_index + 1 if word_index > -1 else len(dict_entries)
    st.session_state['all_lin_steps'].append(lin_steps)
    if word_index < 4:
        lin_path = dict_entries[:word_index]
    else:
        lin_path = dict_entries[0:2] + ["..."] + dict_entries[(word_index-1):(word_index+1)]
    lin_path_str = construct_path_str(lin_path)
    bin_checks = lookup_word_bin(query)
    bin_steps = len(bin_checks)
    st.session_state['all_bin_steps'].append(bin_steps)
    bin_path = " ➡️ ".join(bin_checks)
    if word_index > -1:
        result.markdown(f"✅ Your word was **found**, at index **`{word_index}`**! It took...")
        lin_text.markdown(f"**{word_index + 1} steps** to find the word:\n\n{lin_path_str}")
        bin_text.markdown(f"**{bin_steps} steps** to find the word:\n\n{bin_path}")
    else:
        result.markdown(f"❌ Your word was not found! However, it took...")
        lin_text.markdown(f"**`{len(dict_entries)}` steps** to find out that it was not in this dictionary 😳")
        bin_text.markdown(f"**`17` steps** to find out that it was not in this dictionary 😎")
    lin_footer.markdown(round(sum(st.session_state['all_lin_steps']) / len(st.session_state['all_lin_steps']), 2))
    arr = np.random.normal(1, 1, size=100)
    fig, ax = plt.subplots()
    ax.hist(arr, bins=20)
    st.pyplot(fig)
    bin_footer.markdown(round(sum(st.session_state['all_bin_steps']) / len(st.session_state['all_bin_steps']), 2))
