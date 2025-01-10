import streamlit as st
import json
import matplotlib.pyplot as plt

st.logo("log_wide_crop.png", size="large")

st.set_page_config(
    page_title="Part 1: Static Dictionary Lookup",
    page_icon="📖",
)

st.title("📖 Part 1: Static Dictionary")
st.subheader("*Linear vs. Logarithmic Time*")

st.markdown(
    """
        <style>
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
</style>
        """,
    unsafe_allow_html=True,
)

st.markdown("Here we load an old version of Webster's dictionary, containing $N = 102105$ words, to introduce the differences between linear and binary search. Once you've gotten a feel for this, open the **'How Does It Scale?'** demo in the left sidebar, where you'll see the full benefit of binary over linear search!")

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
data_load_state = st.text('Loading data (102105 words)...')
dict_entries = load_data()
# Notify the reader that the data was successfully loaded.
data_load_state.text('Loading data (102105 words)... done!')

# st.text(','.join(dict_entries[:10]))

intro = st.empty()
intro.markdown("Enter a word in the sidebar and press Enter to begin!")
result = st.empty()

lin_col, bin_col = st.columns(2, border=True)
with lin_col:
    st.header("Linear Search")
    lin_text = st.markdown("&nbsp;\n\n")
    # lin_sep = st.markdown("---")
    lin_footer = st.empty()
with bin_col:
    st.header("Binary Search")
    bin_text = st.markdown("&nbsp;\n\n")
    # bin_sep = st.markdown("---")
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
        result.markdown(f"Your query was: **{query}**... ✅ Your word was **found**, at index **`{word_index}`**! It took...")
        lin_text.markdown(f"**{word_index + 1} steps** to find the word:\n\n<p class='small-font'>{lin_path_str}</p>", unsafe_allow_html=True)
        bin_text.markdown(f"**{bin_steps} steps** to find the word:\n\n<p class='small-font'>{bin_path}</p>", unsafe_allow_html=True)
    else:
        result.markdown(f"Your query was: **{query}**... ❌ Your word was not found! However, it took...")
        lin_text.markdown(f"**`{len(dict_entries)}` steps** to find out that it was not in this dictionary 😳")
        bin_text.markdown(f"**`17` steps** to find out that it was not in this dictionary 😎")
    mean_lin_steps = round(sum(st.session_state['all_lin_steps']) / len(st.session_state['all_lin_steps']), 2)
    worst_lin_steps = max(st.session_state['all_lin_steps'])
    lin_footer.markdown(f"Running average: **{mean_lin_steps} steps**\n\nWorst case: **{worst_lin_steps} steps**")
    mean_bin_steps = round(sum(st.session_state['all_bin_steps']) / len(st.session_state['all_bin_steps']), 2)
    bin_footer.markdown(f"Running average: **{mean_bin_steps} steps**")
    step_ratio = round(mean_lin_steps / mean_bin_steps)
    st.markdown(f"On average, binary search has worked **{step_ratio} times faster!**")