import streamlit as st
import pandas as pd
import numpy as np
rng = np.random.default_rng(seed=5500)
import matplotlib.pyplot as plt
import json

st.logo("log_wide_crop.png", size="large")

st.set_page_config(
    page_title="Part 2: Scalability",
    page_icon="📚",
)

st.title("📖 Part 2: Scalability")
st.subheader("*How does our algorithm perform as the dictionary grows?*")

if 'lookup_df' not in st.session_state:
    st.session_state['lookup_df'] = pd.DataFrame(columns=['n','linear','binary'])

st.markdown("In this demo, rather than manually typing in words, we simulate running a dictionary app: Users query words from a growing dictionary (think of a social media site with more and more content over time!), and we examine how the average-case and worst-case runtime grows as the dictionary grows.")

@st.cache_data
def load_data():
    unigram_df = pd.read_csv("unigram_freq.csv")
    word_list = list(unigram_df['word'].values)
    return [str(w) for w in word_list]

# Create a text element and let the reader know the data is loading.
data_load_state = st.text('Loading data (333000 words)...')
dict_entries = load_data()
# Notify the reader that the data was successfully loaded.
data_load_state.text(f'Loading data (333000 words)... done!')

intro = st.empty()
intro.markdown("Choose a sample size $N$ and click the button in the sidebar to simulate looking up 100 randomly-chosen words from a dictionary of that size!")
result = st.empty()

with st.sidebar:
    slider_col, submit_col = st.columns([0.8, 0.2], vertical_alignment="center")
    with slider_col:
        dict_size = st.slider("Dictionary Size", min_value=100, max_value=300000, value=1000, step=100)
    with submit_col:
        st.button("&rarr;")

def lookup_word_bin(word_query, all_words):
    low_index = 0
    high_index = len(all_words) - 1
    words_checked = []
    while low_index <= high_index:
        mid_index = (low_index + high_index) // 2
        mid_elt = all_words[mid_index]
        words_checked.append(mid_elt)
        if word_query < mid_elt:
            high_index = mid_index - 1
        elif word_query == mid_elt:
            return words_checked
        else:
            low_index = mid_index + 1
    return words_checked

def perform_lookups(dict_size):
    sub_entries = sorted(dict_entries[:dict_size])
    sample_indices = rng.integers(low=0, high=dict_size, size=100)
    sample_words = [sub_entries[i] for i in sample_indices]
    # Binary search
    bin_results = [len(lookup_word_bin(sample_word, sub_entries)) for sample_word in sample_words]
    return sample_words, sample_indices, bin_results

if dict_size:
    result_words, result_indices, result_bin_lookups = perform_lookups(dict_size)
    lookup_times_lin = [i+1 for i in result_indices]
    lookup_words_str = ", ".join(result_words[:3] + ["⋯"] + result_words[-4:-1])
    lin_mean_time = sum(lookup_times_lin) / len(lookup_times_lin)
    bin_mean_time = sum(result_bin_lookups) / len(result_bin_lookups)
    st.markdown(f"Looked up the following words:\n\n{lookup_words_str}")
    st.markdown(f"Linear mean lookups: {lin_mean_time}")
    st.markdown(f"Binary mean lookups: {bin_mean_time}")
    cur_data_df = pd.DataFrame({'n': [dict_size], 'linear': [lin_mean_time], 'binary':[bin_mean_time]})
    #st.write(cur_data_df)
    # And append to the df
    st.session_state['lookup_df'] = pd.concat([st.session_state['lookup_df'], cur_data_df])
    #st.write(st.session_state['lookup_df'])

fig, ax = plt.subplots()
df_plot_fig = st.session_state['lookup_df'].set_index('n').plot(style='.-').figure
st.pyplot(df_plot_fig)

