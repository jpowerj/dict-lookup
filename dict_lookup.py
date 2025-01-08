import streamlit as st
import json
import time

st.title("📖 Dictionary Lookup Demo")
st.subheader("Linear vs. Logarithmic Time")

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

with st.sidebar:
    st.header("Enter Word")
    query = st.text_input("Type your word here", placeholder="Enter a word to look up")

def lookup_word(word_query):
    try:
        word_index = dict_entries.index(word_query)
    except ValueError:
        word_index = -1
    return word_index

if query:
    intro.empty()
    st.markdown(f"Your query is: **{query}**")
    word_index = lookup_word(query)
    if word_index > -1:
        st.markdown(f"Your word was **found**, at index **`{word_index}`**")
    else:
        st.markdown(f"Your word was not found! However, it took **`{len(dict_entries)}` steps** to find out that it was not in this dictionary 😳")
