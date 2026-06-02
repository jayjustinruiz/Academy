import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import plotly.express as px
import altair as alt



# Sample data

chart_data = pd.DataFrame(
    np.random.randn(20, 3),
    columns=["A", "B", "C"]
)

st.line_chart(chart_data)
st.area_chart(chart_data)
st.bar_chart(chart_data)

#MatPlot 

fig, ax = plt.subplots()

ax.plot([1, 2, 3, 4], [10, 20, 25, 30])

ax.set_title("Matplotlib Line Chart")

st.pyplot(fig)

#Plotly 

df = pd.DataFrame({
    "Fruit": ["Apple", "Banana", "Orange", "Apple", "Banana", "Orange"],
    "Amount": [4, 1, 2, 2, 4, 5],
    "City": ["NY", "NY", "NY", "LA", "LA", "LA"]
})

fig = px.bar(df, x="Fruit", y="Amount", color="City", barmode="group")

st.plotly_chart(fig)

#Altair

df = pd.DataFrame({
    'x': range(1, 11),
    'y': [x**2 for x in range(1, 11)]
})

chart = alt.Chart(df).mark_line().encode(
    x='x',
    y='y'
)

st.altair_chart(chart, use_container_width=True)
