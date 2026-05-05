"""Streamlit Dashboard #2 — Gapminder Pulse.

Uses Plotly's bundled gapminder dataset (no download required) for an
animated, interactive world view themed to match the Django host site.
"""
import pandas as pd
import plotly.express as px
import streamlit as st

st.set_page_config(
    page_title="Gapminder Pulse",
    page_icon="◆",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Same deep-vibe theme as dashboard1 — duplicated to keep apps independent.
DEEP_THEME_CSS = """
<style>
.stApp {
    background:
        radial-gradient(900px 500px at 90% 0%, rgba(255, 0, 128, 0.32), transparent 60%),
        radial-gradient(700px 500px at 0% 30%, rgba(0, 217, 255, 0.22), transparent 60%),
        linear-gradient(180deg, #07041a 0%, #14082e 100%) !important;
}
html, body, [class*="css"], .stApp { color: #f0f0ff !important; }
[data-testid="stSidebar"] {
    background: rgba(7, 4, 26, 0.7) !important;
    backdrop-filter: blur(14px);
    border-right: 1px solid rgba(255, 0, 128, 0.3);
}
h1, h2, h3 { font-family: "Space Grotesk", system-ui, sans-serif !important; }
h1 {
    background: linear-gradient(135deg, #00d9ff, #b026ff 50%, #ff0080);
    -webkit-background-clip: text;
    background-clip: text;
    color: transparent !important;
}
[data-testid="stMetric"] {
    background: rgba(20, 8, 46, 0.55);
    border: 1px solid rgba(255, 0, 128, 0.3);
    border-radius: 14px;
    padding: 16px;
}
[data-testid="stMetricValue"] {
    background: linear-gradient(135deg, #06ffa5, #00d9ff);
    -webkit-background-clip: text;
    background-clip: text;
    color: transparent !important;
}
.stTabs [data-baseweb="tab-list"] {
    background: rgba(7, 4, 26, 0.6);
    border-radius: 12px;
    padding: 4px;
}
.stTabs [data-baseweb="tab"][aria-selected="true"] {
    background: linear-gradient(135deg, #ff0080, #00d9ff);
    border-radius: 8px;
}
[data-testid="stHeader"] { background: transparent; }
</style>
"""
st.markdown(DEEP_THEME_CSS, unsafe_allow_html=True)


@st.cache_data
def load_data() -> pd.DataFrame:
    return px.data.gapminder()


df = load_data()
VIBE_SEQ = ["#ff0080", "#b026ff", "#06ffa5", "#00d9ff", "#ec38bc"]


def style(fig):
    fig.update_layout(
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(color="#f0f0ff", family="Inter, sans-serif"),
        margin=dict(l=10, r=10, t=40, b=10),
    )
    fig.update_xaxes(gridcolor="rgba(255, 0, 128, 0.15)")
    fig.update_yaxes(gridcolor="rgba(255, 0, 128, 0.15)")
    return fig


# ---- Sidebar filters ------------------------------------------------------
st.sidebar.title("◆ Filters")
st.sidebar.caption("Slice the Gapminder dataset")

continents = st.sidebar.multiselect(
    "Continents",
    options=sorted(df["continent"].unique()),
    default=sorted(df["continent"].unique()),
)

year_min, year_max = int(df["year"].min()), int(df["year"].max())
year_range = st.sidebar.slider("Year range", year_min, year_max, (year_min, year_max), step=5)

show_top_n = st.sidebar.slider("Top N countries by GDP", 5, 30, 12)

filtered = df[
    df["continent"].isin(continents)
    & df["year"].between(*year_range)
]


# ---- Header ---------------------------------------------------------------
st.title("Gapminder Pulse")
st.caption("Streamlit dashboard #2 — life expectancy, population & GDP across continents over time.")

latest_year = filtered["year"].max() if len(filtered) else None
latest = filtered[filtered["year"] == latest_year] if latest_year else filtered

c1, c2, c3, c4 = st.columns(4)
c1.metric("Countries", filtered["country"].nunique())
c2.metric("Years", filtered["year"].nunique())
c3.metric(
    "Avg life exp" + (f" ({latest_year})" if latest_year else ""),
    f"{latest['lifeExp'].mean():.1f}" if len(latest) else "—",
)
c4.metric(
    "Avg GDP/cap" + (f" ({latest_year})" if latest_year else ""),
    f"${latest['gdpPercap'].mean():,.0f}" if len(latest) else "—",
)

st.divider()


tab1, tab2, tab3, tab4 = st.tabs(["Bubble", "Trends", "Top GDP", "Map"])

with tab1:
    fig = px.scatter(
        filtered,
        x="gdpPercap",
        y="lifeExp",
        size="pop",
        color="continent",
        hover_name="country",
        log_x=True,
        size_max=55,
        animation_frame="year",
        animation_group="country",
        range_y=[20, 90],
        color_discrete_sequence=VIBE_SEQ,
        title="GDP per capita vs life expectancy (animated by year)",
    )
    st.plotly_chart(style(fig), use_container_width=True)

with tab2:
    by_continent = (
        filtered.groupby(["year", "continent"], as_index=False)
        .agg(lifeExp=("lifeExp", "mean"), pop=("pop", "sum"), gdpPercap=("gdpPercap", "mean"))
    )
    metric = st.radio("Metric", ["lifeExp", "gdpPercap", "pop"], horizontal=True)
    fig = px.line(
        by_continent,
        x="year",
        y=metric,
        color="continent",
        markers=True,
        color_discrete_sequence=VIBE_SEQ,
        title=f"{metric} by continent over time",
    )
    st.plotly_chart(style(fig), use_container_width=True)

with tab3:
    if latest_year:
        top = (
            filtered[filtered["year"] == latest_year]
            .nlargest(show_top_n, "gdpPercap")
            .sort_values("gdpPercap")
        )
        fig = px.bar(
            top,
            x="gdpPercap",
            y="country",
            orientation="h",
            color="continent",
            color_discrete_sequence=VIBE_SEQ,
            title=f"Top {show_top_n} countries by GDP/capita ({latest_year})",
        )
        st.plotly_chart(style(fig), use_container_width=True)
    else:
        st.info("Adjust filters to include some data.")

with tab4:
    if latest_year:
        snapshot = filtered[filtered["year"] == latest_year]
        fig = px.choropleth(
            snapshot,
            locations="iso_alpha",
            color="lifeExp",
            hover_name="country",
            color_continuous_scale=["#0a0a1a", "#7928ca", "#ff0080", "#06ffa5"],
            title=f"Life expectancy world map ({latest_year})",
        )
        fig.update_geos(
            bgcolor="rgba(0,0,0,0)",
            lakecolor="rgba(0,0,0,0)",
            showframe=False,
            showcoastlines=False,
        )
        st.plotly_chart(style(fig), use_container_width=True)
    else:
        st.info("Adjust filters to include some data.")

st.divider()
with st.expander("Raw data"):
    st.dataframe(filtered, use_container_width=True)
