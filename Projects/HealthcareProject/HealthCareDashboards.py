import os 
import streamlit as st
import snowflake.connector
import seaborn as sns
import pandas as pd
import plotly.express as px
import matplotlib.pyplot as plt
import matplotlib.ticker as mtick

PASSWORD = os.getenv('SNOWSQL_PWD')

conn = snowflake.connector.connect(
    user='JAYUANRUIZ',
    password=PASSWORD,
    account='joc66147.us-east-1',
    warehouse="AWS_Warehouse",
    database="Healthcare_DB",
    schema="Silver"
    )

def load_object(object_name):
    query = f"SELECT * FROM {object_name}"
    return pd.read_sql(query, conn)

df_monthly_occupancy = load_object("Monthly_Occupancy_VW")
df_quarterly_occupancy = load_object("Quarterly_Occupancy_VW")
df_nursehours_state = load_object("NurseHRS_StateSummary_VW")
df_totalhours_monthlyagg = load_object("NURSESTAFFING_MONTHLYTOTALHOURS_VW")
df_totalhours_nurses = load_object("NURSESTAFFING_TOTALHOURS_VW")
#df_provider_statistics = load_object("PROVIDER_CALCULATEDHOURS_VW")

st.title("Monthly Occupancy by Nursing Home")

# Dropdown filter
selected_ccn = st.selectbox(
    "Select Nursing Home (CCN_ID)",
    df_monthly_occupancy["CCN_ID"].unique()
)

# Filter data
filtered_df = df_monthly_occupancy[
    df_monthly_occupancy["CCN_ID"] == selected_ccn
]

filtered_df = filtered_df.sort_values("WORK_MONTH")

# Get provider name
provider_name = filtered_df["PROVIDER_NAME"].iloc[0]

# -----------------------------
# Line Chart
# -----------------------------
fig1 = px.line(
    filtered_df,
    x="WORK_MONTH",
    y="MONTHLY_OCCUPANCY",
    markers=True,
    title=f"Monthly Occupancy Trend - {provider_name}",
)

fig1.update_layout(
    xaxis_title="Month",
    yaxis_title="Monthly Occupancy",
    yaxis=dict(tickformat=".0%"),
    template="plotly_white"
)

st.plotly_chart(fig1, use_container_width=True)

# Quarterly Occupancy Visualization 
st.subheader("Quarterly Occupancy Bubble View")

selected_quarter = st.selectbox(
    "Select Quarter",
    sorted(df_quarterly_occupancy["QUARTER"].unique())
)
occupancy_filter = st.selectbox(
    "Select Occupancy Filter",
    ["All", "<= 1", "> 1"]
)

filtered_df = df_quarterly_occupancy[
    df_quarterly_occupancy["QUARTER"] == selected_quarter
]

# Apply occupancy filter
if occupancy_filter == "<= 1":
    filtered_df = filtered_df[filtered_df["QUARTERLY_OCCUPANCY"] <= 1]
elif occupancy_filter == "> 1":
    filtered_df = filtered_df[filtered_df["QUARTERLY_OCCUPANCY"] > 1]

fig_bubble = px.scatter(
    filtered_df,
    x="BED_COUNT",
    y="AVERAGE_PATIENTS_QUARTERLY",
    size="QUARTERLY_OCCUPANCY",
    color="QUARTERLY_OCCUPANCY",
    hover_name="PROVIDER_NAME",
    hover_data=[
        "CCN_ID",
        "QUARTERLY_OCCUPANCY"
    ],
    title=f"Quarterly Occupancy Comparison Across Facilities - {selected_quarter}",
    color_continuous_scale="Viridis"
)

fig_bubble.update_layout(
    xaxis_title="Bed Count",
    yaxis_title="Average Patient Count",
    template="plotly_white",
    height=600,
    showlegend=False
)

st.plotly_chart(fig_bubble, use_container_width=True)

# Visualization 3
st.subheader("Compare Facilities Monthly Occupany")

# Create dropdown labels (CCN + Provider Name)
# ----------------------------------------
df_monthly_occupancy["CCN_PROVIDER"] = (
    df_monthly_occupancy["CCN_ID"].astype(str)
    + " - "
    + df_monthly_occupancy["PROVIDER_NAME"]
)

# Create mapping back to CCN
ccn_mapping = df_monthly_occupancy[["CCN_PROVIDER", "CCN_ID"]].drop_duplicates()

selected_labels = st.multiselect(
    "Select Facilities to Compare",
    ccn_mapping["CCN_PROVIDER"].unique(),
    default=list(ccn_mapping["CCN_PROVIDER"].unique()[:3])
)

# Convert selected labels back to CCNs
selected_ccns = ccn_mapping[
    ccn_mapping["CCN_PROVIDER"].isin(selected_labels)
]["CCN_ID"]

compare_df = df_monthly_occupancy[
    df_monthly_occupancy["CCN_ID"].isin(selected_ccns)
]

# Ensure months are numeric and sorted correctly
compare_df["WORK_MONTH"] = pd.to_numeric(
    compare_df["WORK_MONTH"],
    errors="coerce"
)

compare_df = compare_df.sort_values("WORK_MONTH")

fig_compare = px.line(
    compare_df,
    x="WORK_MONTH",
    y="MONTHLY_OCCUPANCY",
    color="CCN_ID",
    hover_data=["PROVIDER_NAME"],
    markers=True,
    title="Facility Comparison"
)

fig_compare.update_layout(
    xaxis_title="Month",
    yaxis_title="Monthly Occupancy",
    yaxis=dict(tickformat=".0%"),
    template="plotly_white"
)

st.plotly_chart(fig_compare, use_container_width=True)

# ----------------------------------------
# State Filter
# ----------------------------------------

selected_state = st.selectbox(
    "Select State",
    sorted(df_totalhours_monthlyagg["STATE"].unique())
)

# Filter dataframe by state
state_filtered_df = df_totalhours_monthlyagg[
    df_totalhours_monthlyagg["STATE"] == selected_state
]

# ----------------------------------------
# Provider Filter
# ----------------------------------------

selected_provnum = st.selectbox(
    "Select Provider (PROVNUM)",
    sorted(state_filtered_df["PROVNUM"].unique())
)

# Filter dataframe by provider
filtered_df = state_filtered_df[
    state_filtered_df["PROVNUM"] == selected_provnum
]
provider_name = filtered_df["PROVNAME"].iloc[0]
# Sort by month
filtered_df = filtered_df.sort_values("WORK_MONTH")

# ----------------------------------------
# Reshape Data for Stacked Bar Chart
# ----------------------------------------

hours_columns = [
    "TOTAL_HRS_RNDON",
    "TOTAL_HRS_RNADMIN",
    "TOTAL_HRS_RN",
    "TOTAL_HRS_LPNADMIN",
    "TOTAL_HRS_LPN",
    "TOTAL_HRS_CNA",
    "TOTAL_HRS_NATRN",
    "TOTAL_HRS_MEDAIDE"
]

# ----------------------------------------
# Keep only columns with actual values
# ----------------------------------------

present_columns = [
    col for col in hours_columns
    if filtered_df[col].fillna(0).sum() > 0
]

# ----------------------------------------
# Order staff types by total hours DESC
# ----------------------------------------

staff_order = (
    filtered_df[present_columns]
    .sum()
    .sort_values(ascending=False)
    .index
    .tolist()
)

# ----------------------------------------
# Reshape Data
# ----------------------------------------

melted_df = filtered_df.melt(
    id_vars=["WORK_MONTH"],
    value_vars=staff_order,
    var_name="Staff_Type",
    value_name="Hours"
)

# ----------------------------------------
# Stacked Bar Chart
# ----------------------------------------

fig_bar = px.bar(
    melted_df,
    x="WORK_MONTH",
    y="Hours",
    color="Staff_Type",
    category_orders={"Staff_Type": staff_order},
    title=f"Monthly Nursing Hours Breakdown - {provider_name}",
    barmode="stack"
)

fig_bar.update_layout(
    xaxis_title="Month",
    yaxis_title="Total Hours",
    template="plotly_white",
    height=600
)

st.plotly_chart(fig_bar, use_container_width=True)

# ----------------------------------------
# New Bubble Viz 
# ----------------------------------------

st.subheader("Total Hours by Provider (State + Month View)")

# ----------------------------------------
# State Filter
# ----------------------------------------
selected_state = st.selectbox(
    "Select State",
    sorted(df_totalhours_monthlyagg["STATE"].unique()),
    key="bubble_state_select"
)

state_df = df_totalhours_monthlyagg[
    df_totalhours_monthlyagg["STATE"] == selected_state
]

# ----------------------------------------
# Month Filter
# ----------------------------------------
month_options = ["All"] + sorted(state_df["WORK_MONTH"].unique().tolist())

selected_month = st.selectbox(
    "Select Month",
    month_options,
    key="bubble_month_select"
)

# Apply filtering
if selected_month == "All":
    filtered_df = state_df
else:
    filtered_df = state_df[
        state_df["WORK_MONTH"] == selected_month
    ]
# Dynamic Color Logic
# ----------------------------------------
if selected_month == "All":
    color_col = "WORK_MONTH"
else:
    color_col = "TOTAL_HRS"

# ----------------------------------------
# Bubble Chart
# ----------------------------------------
fig_bubble_state = px.scatter(
    filtered_df,
    x="AVERAGE_PATIENTS",
    y="TOTAL_HRS",
    size="TOTAL_HRS",
    color=color_col,
    hover_name="PROVNAME",
    hover_data=["STATE", "WORK_MONTH", "TOTAL_HRS"],
    title=f"Total Nursing Hours - {selected_state} ({selected_month})",
    color_continuous_scale="Viridis"
)

fig_bubble_state.update_layout(
    xaxis_title="Average Patient Count",
    yaxis_title="Total Hours",
    template="plotly_white",
    height=600,
    showlegend=False
)

st.plotly_chart(fig_bubble_state, use_container_width=True)