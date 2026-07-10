import os 
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
    database="WALMART_DB",
    schema="GOLD"
    )

def load_table(table_name):
    query = f"SELECT * FROM {table_name}"
    return pd.read_sql(query, conn)

df_store_holiday = load_table("WEEKLYSALES_STORESHOLIDAY")
df_store_size = load_table("WEEKLYSALES_STORESIZE")
df_temp_year = load_table("WEEKLYSALES_TEMPYEAR")
df_type_month = load_table("WEEKLYSALES_TYPEMONTH")

#Weekly Sales by Store Holiday Seaborn/Plotly
plt.figure(figsize=(10,6))

sns.barplot(
    data=df_store_holiday,
    x="STORE_ID",
    y="TOTAL_SALES",
    hue="ISHOLIDAY"
)

plt.title("Weekly Sales by Store (Holiday vs Non-Holiday)")
plt.xticks(rotation=45)
plt.show()

#Weekly Sales by Store Holiday Plotly Express
fig = px.bar(
    df_store_holiday,
    x="STORE_ID",
    y="TOTAL_SALES",
    color="ISHOLIDAY",
    barmode="group",
    title="Weekly Sales by Store (Holiday vs Non-Holiday)"
)

fig.show()

#Weekly Sales by Store Size 
plt.figure(figsize=(14,6))

# sort values (important for smooth chart)
df_plot = df_store_size.sort_values("STORE_SIZE")

# line + shaded area
plt.fill_between(
    df_plot["STORE_SIZE"],
    df_plot["TOTAL_WEEKLY_SALES"],
    alpha=0.25
)

plt.plot(
    df_plot["STORE_SIZE"],
    df_plot["TOTAL_WEEKLY_SALES"],
    marker="o",
    linewidth=2
)

# labels on points (like your screenshot)
for x, y in zip(df_plot["STORE_SIZE"], df_plot["TOTAL_WEEKLY_SALES"]):
    plt.text(x, y, f"{y/1_000_000:.0f}M", ha="center", va="bottom", fontsize=8)

# formatting
plt.title("Weekly Sales by Store Size", fontsize=14)
plt.xlabel("Store Size")
plt.ylabel("Weekly Sales (Millions)")

# format y-axis to millions
plt.gca().yaxis.set_major_formatter(
    mtick.FuncFormatter(lambda x, pos: f"{x/1_000_000:.0f}M")
)

plt.grid(True, alpha=0.3)

plt.show()

#Weekly Sales by Temperature Year
plt.figure(figsize=(10,6))

sns.scatterplot(
    data=df_temp_year,
    x="TEMPERATURE",
    y="TOTAL_WEEKLY_SALES",
    hue="YEAR"
)

plt.title("Temperature vs Weekly Sales (by Year)")
plt.show()

#Weekly Sales by Store Type & Month 
plt.figure(figsize=(12,6))

ax = sns.lineplot(
    data=df_type_month,
    x="MONTH",
    y="TOTAL_WEEKLY_SALES",
    hue="STORE_TYPE"
)

ax.yaxis.set_major_formatter(
    mtick.FuncFormatter(lambda x, pos: f'{x/1_000_000:.0f}M')
)

plt.title("Weekly Sales by Store Type & Month")
plt.ylabel("Total Weekly Sales (Millions)")
plt.show()

def plot_bar_chart(df, x_col, y_col, color_col=None, table_name=None):
    """
    Generalized Plotly bar chart function.

    Parameters:
    df (pd.DataFrame): input dataframe
    x_col (str): column for x-axis
    y_col (str): column for y-axis
    color_col (str): optional grouping column
    table_name (str): Snowflake table name for auto-title
    """

    # auto-generate title
    title = f"Weekly Sales - {table_name}" if table_name else "Weekly Sales"

    fig = px.bar(
        df,
        x=x_col,
        y=y_col,
        color=color_col,
        barmode="group" if color_col else "group",
        title=title
    )

    fig.show()

plot_bar_chart(
    df_store_size,
    x_col="STORE_SIZE",
    y_col="TOTAL_WEEKLY_SALES",
    color_col=None,
    table_name="WEEKLYSALES_STORESIZE"
)

plot_bar_chart(
    df_type_month,
    x_col="MONTH",
    y_col="TOTAL_WEEKLY_SALES",
    color_col="STORE_TYPE",
    table_name="WEEKLYSALES_TYPEMONTH"
)
