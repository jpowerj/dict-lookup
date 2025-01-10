import streamlit as st
import pandas as pd
import numpy as np
rng = np.random.default_rng(seed=5500)
import altair as alt

st.logo("log_wide_crop.png", size="large")

st.set_page_config(
    page_title="Part 2: Scalability",
    page_icon="📚",
)

st.markdown("""<style>
.stAppHeader {
    background-color: rgba(255, 255, 255, 0.0);  /* Transparent background */
    visibility: visible;  /* Ensure the header is visible */
}

.block-container {
    padding-top: 2rem;
    padding-bottom: 0rem;
    padding-left: 2rem;
    padding-right: 2rem;
}
div[data-testid="stSidebarHeader"] > img, div[data-testid="collapsedControl"] > img {
    height: 3rem;
    width: auto;
}
  
div[data-testid="stSidebarHeader"], div[data-testid="stSidebarHeader"] > *,
div[data-testid="collapsedControl"], div[data-testid="collapsedControl"] > * {
    display: flex;
    align-items: center;
    justify-content: center;
}
.small-font {
    font-size:8pt !important;
}
</style>""", unsafe_allow_html=True)

st.title("📚 Part 2: Scalability")
st.subheader("*How do they perform as the dictionary grows?*")

if 'lookup_df' not in st.session_state:
    st.session_state['lookup_df'] = pd.DataFrame(columns=['n','method','steps'])

st.markdown("In this demo, rather than manually typing in words, we simulate running a dictionary app: Users query words from a growing dictionary (think of a social media site with more and more content over time!), and we examine how the average-case and worst-case runtime grows as the dictionary grows.")

@st.cache_data
def load_data():
    unigram_df = pd.read_csv("unigram_freq.csv")
    word_list = list(unigram_df['word'].values)
    return [str(w) for w in word_list]

dict_entries = load_data()

intro = st.empty()
intro.markdown("Choose a sample size $N$ and click the button in the sidebar to simulate looking up 100 randomly-chosen words from a dictionary of that size!")
result = st.empty()

with st.sidebar:
    dict_size = st.slider("Dictionary Size", min_value=100, max_value=300000, value=1000, step=100)

lin_col, bin_col = st.columns(2, border=True)
with lin_col:
    lin_text = st.markdown("**Linear Search**")
with bin_col:
    bin_text = st.markdown("**Binary Search**")

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
    dict_size_num = int(dict_size)
    result_words, result_indices, result_bin_lookups = perform_lookups(dict_size_num)
    lookup_times_lin = [i+1 for i in result_indices]
    lookup_words_str = ", ".join(result_words[:3] + ["⋯"] + result_words[-4:-1])
    lin_mean_time = sum(lookup_times_lin) / len(lookup_times_lin)
    bin_mean_time = sum(result_bin_lookups) / len(result_bin_lookups)
    intro.markdown(f"Looked up **100 words** from dictionary containing **{dict_size_num} words**: {lookup_words_str}")
    lin_text.markdown(f"**Linear Search**: {lin_mean_time} lookups")
    bin_text.markdown(f"**Binary Search**: {bin_mean_time} lookups")
    cur_data_df = pd.DataFrame({'n': [dict_size_num, dict_size_num], 'method': ['linear', 'binary'], 'steps':[lin_mean_time, bin_mean_time]})
    # st.write(cur_data_df)
    # st.write(cur_data_df.dtypes)
    # And append to the df
    st.session_state['lookup_df'] = pd.concat([st.session_state['lookup_df'], cur_data_df], ignore_index=True)
    # st.write(st.session_state['lookup_df'])

c = (
   alt.Chart(st.session_state['lookup_df'])
   .mark_line(point=True)
   .encode(x="n", y="steps", color="method", tooltip=["n", "steps", "method"])
)

st.altair_chart(c, use_container_width=True)