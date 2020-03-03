import streamlit as st

st.title('Yelp Explorer')

st.balloons()

st.show(range(0, 10))

st.spinner(text = 'happening')

import pandas as pd
import numpy as np
st.area_chart(pd.DataFrame(
np.random.randn(20, 3),
columns=['a', 'b', 'c']))