import streamlit as st
import pandas as pd
from PIL import Image

st.title("Hello Test!")

st.write("This is my first Streamlit app.")

data = {

    "Name": ["Alice", "Bob", "Charlie"],

    "Age": [25, 30, 35]

}

 

df = pd.DataFrame(data)

 

st.dataframe(df)  # Scrollable, interactive table

st.table(df)      # Static table


 
