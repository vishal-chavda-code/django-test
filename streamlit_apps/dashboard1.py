"""Streamlit Dashboard #1 — Iris Explorer.

Reads the bundled data/iris.csv file and renders an interactive explorer
themed to match the Django host site (deep purples, magentas, mint).
"""
from pathlib import Path

import pandas as pd
import plotly.express as px
import streamlit as st

# ---- Page config ----------------------------------------------------------
st.set_page_config(
    page_title="Iris Explorer",
    page_icon="◆",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ---- Deep-vibe theme via injected CSS -------------------------------------
DEEP_THEME_CSS = """
<style>
:root {
    --bg-0: #07041a;
    --bg-1: #14082e;
    --purple: #b026ff;
    --magenta: #ff0080;
    --mint: #06ffa5;
    --cyan: #00d9ff;
}
html, body, [class*="css"], .stApp {
    color: #f0f0ff !important;
}
.stApp {
    background:
        radial-gradient(900px 500px at 10% 0%, rgba(176, 38, 255, 0.35), transparent 60%),
        radial-gradient(700px 500px at 100% 0%, rgba(255, 0, 128, 0.25), transparent 60%),
        linear-gradient(180deg, #07041a 0%, #14082e 100%) !important;
}
[data-testid="stSidebar"] {
    background: rgba(7, 4, 26, 0.7) !important;
    backdrop-filter: blur(14px);
    border-right: 1px solid rgba(176, 38, 255, 0.3);
}
h1, h2, h3 { font-family: "Space Grotesk", system-ui, sans-serif !important; }
h1 {
    background: linear-gradient(135deg, #ff0080, #b026ff 50%, #00d9ff);
    -webkit-background-clip: text;
    background-clip: text;
    color: transparent !important;
}
[data-testid="stMetric"] {
    background: rgba(20, 8, 46, 0.55);
    border: 1px solid rgba(176, 38, 255, 0.3);
    border-radius: 14px;
    padding: 16px;
    backdrop-filter: blur(10px);
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
    background: linear-gradient(135deg, #7928ca, #ff0080);
    border-radius: 8px;
}
.stSlider [data-baseweb="slider"] > div { background: rgba(176, 38, 255, 0.35) !important; }
[data-testid="stHeader"] { background: transparent; }
</style>
"""
st.markdown(DEEP_THEME_CSS, unsafe_allow_html=True)


# ---- Data loading ---------------------------------------------------------
DATA_PATH = Path(__file__).resolve().parent.parent / "data" / "iris.csv"


@st.cache_data
def load_data() -> pd.DataFrame:
    if DATA_PATH.exists():
        return pd.read_csv(DATA_PATH)
    return px.data.iris().rename(
        columns={
            "sepal_length": "SepalLengthCm",
            "sepal_width": "SepalWidthCm",
            "petal_length": "PetalLengthCm",
            "petal_width": "PetalWidthCm",
            "species": "Species",
        }
    )


df = load_data()

VIBE = ["#b026ff", "#ff0080", "#06ffa5"]


def style(fig):
    fig.update_layout(
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(color="#f0f0ff", family="Inter, sans-serif"),
        margin=dict(l=10, r=10, t=40, b=10),
    )
    fig.update_xaxes(gridcolor="rgba(176, 38, 255, 0.15)")
    fig.update_yaxes(gridcolor="rgba(176, 38, 255, 0.15)")
    return fig


# ---- Sidebar filters ------------------------------------------------------
st.sidebar.title("◆ Filters")
st.sidebar.caption("Slice the Iris dataset")

species = st.sidebar.multiselect(
    "Species",
    options=sorted(df["Species"].unique()),
    default=sorted(df["Species"].unique()),
)

sepal_range = st.sidebar.slider(
    "Sepal length (cm)",
    float(df["SepalLengthCm"].min()),
    float(df["SepalLengthCm"].max()),
    (float(df["SepalLengthCm"].min()), float(df["SepalLengthCm"].max())),
    step=0.1,
)

petal_range = st.sidebar.slider(
    "Petal length (cm)",
    float(df["PetalLengthCm"].min()),
    float(df["PetalLengthCm"].max()),
    (float(df["PetalLengthCm"].min()), float(df["PetalLengthCm"].max())),
    step=0.1,
)

filtered = df[
    df["Species"].isin(species)
    & df["SepalLengthCm"].between(*sepal_range)
    & df["PetalLengthCm"].between(*petal_range)
]


# ---- Header ---------------------------------------------------------------
st.title("Iris Explorer")
st.caption("Streamlit dashboard #1 — interactive filtering on the bundled Iris CSV. Embedded inside the Django site.")

# ---- KPIs -----------------------------------------------------------------
c1, c2, c3, c4 = st.columns(4)
c1.metric("Rows", len(filtered))
c2.metric("Species", filtered["Species"].nunique())
c3.metric("Avg sepal cm", f"{filtered['SepalLengthCm'].mean():.2f}" if len(filtered) else "—")
c4.metric("Avg petal cm", f"{filtered['PetalLengthCm'].mean():.2f}" if len(filtered) else "—")

st.divider()

# ---- Charts ---------------------------------------------------------------
tab1, tab2, tab3 = st.tabs(["Scatter", "Distributions", "Pairs"])

with tab1:
    fig = px.scatter(
        filtered,
        x="SepalLengthCm",
        y="PetalLengthCm",
        color="Species",
        size="PetalWidthCm",
        hover_data=filtered.columns,
        color_discrete_sequence=VIBE,
        title="Sepal length vs petal length",
    )
    st.plotly_chart(style(fig), use_container_width=True)

with tab2:
    col_a, col_b = st.columns(2)
    feature = col_a.selectbox(
        "Feature",
        ["SepalLengthCm", "SepalWidthCm", "PetalLengthCm", "PetalWidthCm"],
    )
    bins = col_b.slider("Bins", 5, 60, 25)
    fig = px.histogram(
        filtered,
        x=feature,
        color="Species",
        nbins=bins,
        barmode="overlay",
        opacity=0.75,
        color_discrete_sequence=VIBE,
        title=f"{feature} distribution",
    )
    st.plotly_chart(style(fig), use_container_width=True)

with tab3:
    fig = px.scatter_matrix(
        filtered,
        dimensions=["SepalLengthCm", "SepalWidthCm", "PetalLengthCm", "PetalWidthCm"],
        color="Species",
        color_discrete_sequence=VIBE,
        title="Pairwise scatter matrix",
    )
    fig.update_traces(diagonal_visible=False)
    st.plotly_chart(style(fig), use_container_width=True)

st.divider()

with st.expander("Raw data"):
    st.dataframe(filtered, use_container_width=True)
