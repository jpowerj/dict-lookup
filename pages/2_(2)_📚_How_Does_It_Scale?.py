import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import json

st.logo("log_wide_crop.png", size="large")

st.set_page_config(
    page_title="Scaling Dictionary Lookup",
    page_icon="📚",
)

arr = np.random.normal(1, 1, size=100)
fig, ax = plt.subplots()
ax.hist(arr, bins=20)
st.pyplot(fig)
st.markdown(round(sum(st.session_state['all_bin_steps']) / len(st.session_state['all_bin_steps']), 2))
