import streamlit as st
import pandas as pd
import plotly.express as px
from pathlib import Path

st.set_page_config(
    page_title="Global Health Indicators Dashboard",
    page_icon="📊",
    layout="wide"
)

st.title("Global Health Indicators Visual Analytics Dashboard")
st.write(
    "Explore health indicators across countries, regions, and years using interactive filters and charts."
)

SAMPLE_PATH = Path("data/sample_health_indicators.csv")


@st.cache_data
def load_sample_data():
    return pd.read_csv(SAMPLE_PATH)


def clean_columns(df):
    df = df.copy()
    df.columns = [str(col).strip() for col in df.columns]
    return df


def convert_wide_to_long(df):
    """
    Converts wide health data into long format when possible.
    Expected long format:
    Country, Region, Year, Indicator, Value

    Wide format example:
    Country, Region, Year, Obesity Rate, Smoking Rate, Diabetes Rate
    """
    df = clean_columns(df)

    required_long = {"Country", "Year", "Indicator", "Value"}
    if required_long.issubset(set(df.columns)):
        if "Region" not in df.columns:
            df["Region"] = "Unknown"
        return df[["Country", "Region", "Year", "Indicator", "Value"]]

    id_cols = [col for col in ["Country", "Region", "Year"] if col in df.columns]
    if "Country" not in id_cols or "Year" not in id_cols:
        st.error("Your CSV must include at least Country and Year columns.")
        st.stop()

    value_cols = [
        col for col in df.columns
        if col not in id_cols and pd.api.types.is_numeric_dtype(df[col])
    ]

    if not value_cols:
        st.error("No numeric indicator columns found. Please check your dataset.")
        st.stop()

    long_df = df.melt(
        id_vars=id_cols,
        value_vars=value_cols,
        var_name="Indicator",
        value_name="Value"
    )

    if "Region" not in long_df.columns:
        long_df["Region"] = "Unknown"

    return long_df[["Country", "Region", "Year", "Indicator", "Value"]]


uploaded_file = st.sidebar.file_uploader("Upload your health indicators CSV", type=["csv"])

if uploaded_file is not None:
    raw_df = pd.read_csv(uploaded_file)
else:
    raw_df = load_sample_data()
    st.info("Using sample data. Upload your own CSV from the sidebar to analyse your actual dataset.")

df = convert_wide_to_long(raw_df)
df = df.dropna(subset=["Country", "Year", "Indicator", "Value"])
df["Year"] = pd.to_numeric(df["Year"], errors="coerce")
df["Value"] = pd.to_numeric(df["Value"], errors="coerce")
df = df.dropna(subset=["Year", "Value"])
df["Year"] = df["Year"].astype(int)

st.sidebar.header("Dashboard Filters")

regions = sorted(df["Region"].dropna().unique())
selected_regions = st.sidebar.multiselect("Select region(s)", regions, default=regions)

countries = sorted(df[df["Region"].isin(selected_regions)]["Country"].dropna().unique())
selected_countries = st.sidebar.multiselect("Select country/countries", countries, default=countries[:8])

indicators = sorted(df["Indicator"].dropna().unique())
selected_indicators = st.sidebar.multiselect("Select indicator(s)", indicators, default=indicators[:3])

year_min = int(df["Year"].min())
year_max = int(df["Year"].max())
selected_year_range = st.sidebar.slider(
    "Select year range",
    min_value=year_min,
    max_value=year_max,
    value=(year_min, year_max)
)

filtered_df = df[
    (df["Region"].isin(selected_regions)) &
    (df["Country"].isin(selected_countries)) &
    (df["Indicator"].isin(selected_indicators)) &
    (df["Year"].between(selected_year_range[0], selected_year_range[1]))
]

if filtered_df.empty:
    st.warning("No data matches your selected filters.")
    st.stop()

st.subheader("Key Metrics")

metric_1, metric_2, metric_3, metric_4 = st.columns(4)
metric_1.metric("Countries", filtered_df["Country"].nunique())
metric_2.metric("Regions", filtered_df["Region"].nunique())
metric_3.metric("Indicators", filtered_df["Indicator"].nunique())
metric_4.metric("Average Value", round(filtered_df["Value"].mean(), 2))

st.divider()

st.subheader("Indicator Trend Over Time")
trend_df = (
    filtered_df
    .groupby(["Year", "Indicator"], as_index=False)["Value"]
    .mean()
)

trend_chart = px.line(
    trend_df,
    x="Year",
    y="Value",
    color="Indicator",
    markers=True,
    title="Average Indicator Value by Year"
)
st.plotly_chart(trend_chart, use_container_width=True)

st.subheader("Country Comparison")

single_indicator = st.selectbox(
    "Choose one indicator for country comparison",
    sorted(filtered_df["Indicator"].unique())
)

latest_year = int(filtered_df["Year"].max())
comparison_df = filtered_df[
    (filtered_df["Indicator"] == single_indicator) &
    (filtered_df["Year"] == latest_year)
].sort_values("Value", ascending=False)

bar_chart = px.bar(
    comparison_df,
    x="Country",
    y="Value",
    color="Region",
    title=f"{single_indicator} by Country in {latest_year}",
    text="Value"
)
st.plotly_chart(bar_chart, use_container_width=True)

st.subheader("Regional Average Comparison")

region_df = (
    filtered_df
    .groupby(["Region", "Indicator"], as_index=False)["Value"]
    .mean()
)

region_chart = px.bar(
    region_df,
    x="Region",
    y="Value",
    color="Indicator",
    barmode="group",
    title="Average Indicator Value by Region"
)
st.plotly_chart(region_chart, use_container_width=True)

st.subheader("Indicator Relationship Heatmap")

pivot_df = filtered_df.pivot_table(
    index=["Country", "Year"],
    columns="Indicator",
    values="Value",
    aggfunc="mean"
)

if pivot_df.shape[1] >= 2:
    corr_df = pivot_df.corr()
    heatmap = px.imshow(
        corr_df,
        text_auto=True,
        aspect="auto",
        title="Correlation Between Selected Indicators"
    )
    st.plotly_chart(heatmap, use_container_width=True)
else:
    st.write("Select at least two indicators to view the correlation heatmap.")

st.subheader("Filtered Data Table")
st.dataframe(filtered_df, use_container_width=True)

csv = filtered_df.to_csv(index=False).encode("utf-8")
st.download_button(
    label="Download filtered data as CSV",
    data=csv,
    file_name="filtered_health_indicators.csv",
    mime="text/csv"
)

st.caption(
    "Portfolio note: replace the sample data with your actual dataset before sharing this as a final project."
)
