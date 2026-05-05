"""Views for the Django demo dashboard.

Each view renders a different page with a deep-vibe theme.
The Plotly view loads the bundled Iris CSV and renders interactive charts
server-side as HTML — no JS frameworks, just Python + Plotly.

The calculator view also handles a Text Analyzer POST form to demonstrate
classic Django request → server-side Python compute → rendered response.
"""
import re
from collections import Counter
from pathlib import Path

import pandas as pd
import plotly.express as px
from django.conf import settings
from django.shortcuts import render

DATA_PATH = settings.BASE_DIR / "data" / "iris.csv"


# ----- Deep-vibe color palette shared across Plotly charts ----------------
VIBE_COLORS = ["#b026ff", "#ff0080", "#06ffa5"]
PLOTLY_BG = "rgba(10, 8, 30, 0)"
PLOTLY_FONT = "#f0f0ff"
PLOTLY_GRID = "rgba(176, 38, 255, 0.15)"

# Common English stop-words for the text analyzer.
STOP_WORDS = {
    "the", "a", "an", "and", "or", "but", "is", "it", "to", "of", "in", "on",
    "at", "for", "with", "by", "as", "are", "was", "were", "be", "been",
    "being", "have", "has", "had", "do", "does", "did", "will", "would",
    "could", "should", "may", "might", "must", "shall", "can", "this",
    "that", "these", "those", "i", "you", "he", "she", "we", "they", "me",
    "him", "her", "us", "them", "my", "your", "his", "its", "our", "their",
    "if", "then", "than", "so", "such", "no", "not", "yes", "from", "up",
    "down", "out", "over", "under", "about", "into", "through",
}


def _load_iris() -> pd.DataFrame:
    """Load the bundled Iris dataset. Falls back to plotly's built-in copy."""
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


def _style_fig(fig):
    fig.update_layout(
        paper_bgcolor=PLOTLY_BG,
        plot_bgcolor=PLOTLY_BG,
        font=dict(color=PLOTLY_FONT, family="Inter, sans-serif"),
        margin=dict(l=40, r=20, t=50, b=40),
        legend=dict(
            bgcolor="rgba(20, 10, 40, 0.6)",
            bordercolor="rgba(176, 38, 255, 0.4)",
            borderwidth=1,
        ),
        title=dict(font=dict(size=18, color="#f0f0ff")),
    )
    fig.update_xaxes(gridcolor=PLOTLY_GRID, zerolinecolor=PLOTLY_GRID)
    fig.update_yaxes(gridcolor=PLOTLY_GRID, zerolinecolor=PLOTLY_GRID)
    return fig


def home(request):
    return render(request, "dashboard/home.html")


def plotly_dashboard(request):
    df = _load_iris()

    scatter = px.scatter(
        df, x="SepalLengthCm", y="PetalLengthCm", color="Species",
        size="PetalWidthCm", hover_data=df.columns,
        title="Sepal vs Petal Length by Species",
        color_discrete_sequence=VIBE_COLORS,
    )
    box = px.box(
        df, x="Species", y="PetalWidthCm", color="Species",
        title="Petal Width Distribution",
        color_discrete_sequence=VIBE_COLORS,
    )
    violin = px.violin(
        df, y="SepalWidthCm", x="Species", color="Species",
        box=True, points="all", title="Sepal Width — Violin View",
        color_discrete_sequence=VIBE_COLORS,
    )
    density = px.density_heatmap(
        df, x="PetalLengthCm", y="PetalWidthCm",
        nbinsx=20, nbinsy=20,
        title="Petal Length × Width Density",
        color_continuous_scale=["#0a0a1a", "#7928ca", "#ff0080", "#06ffa5"],
    )

    charts_html = {
        "scatter": _style_fig(scatter).to_html(full_html=False, include_plotlyjs="cdn"),
        "box": _style_fig(box).to_html(full_html=False, include_plotlyjs=False),
        "violin": _style_fig(violin).to_html(full_html=False, include_plotlyjs=False),
        "density": _style_fig(density).to_html(full_html=False, include_plotlyjs=False),
    }

    stats = {
        "rows": len(df),
        "species_count": df["Species"].nunique(),
        "avg_sepal": round(df["SepalLengthCm"].mean(), 2),
        "avg_petal": round(df["PetalLengthCm"].mean(), 2),
    }

    return render(
        request,
        "dashboard/plotly_dashboard.html",
        {"charts": charts_html, "stats": stats},
    )


def streamlit_one(request):
    return render(request, "dashboard/streamlit1.html")


def streamlit_two(request):
    return render(request, "dashboard/streamlit2.html")


def _analyze_text(text: str) -> dict:
    """Server-side text analysis — pure Python.

    Demonstrates Django doing real backend work: receive POST data,
    run computation in Python, return structured results to the template.
    """
    text = text.strip()
    if not text:
        return {}

    chars_total = len(text)
    chars_no_spaces = len(text.replace(" ", "").replace("\n", "").replace("\t", ""))
    words = re.findall(r"\b[\w']+\b", text.lower())
    word_count = len(words)
    sentences = [s for s in re.split(r"[.!?]+\s*", text) if s.strip()]
    sentence_count = len(sentences)
    paragraphs = [p for p in text.split("\n\n") if p.strip()]
    paragraph_count = len(paragraphs)

    avg_word_len = round(sum(len(w) for w in words) / word_count, 2) if word_count else 0
    reading_minutes = max(1, round(word_count / 225))

    meaningful = [w for w in words if w not in STOP_WORDS and len(w) > 2]
    top_words = Counter(meaningful).most_common(8)

    longest_word = max(words, key=len) if words else ""

    return {
        "submitted_text": text,
        "chars_total": chars_total,
        "chars_no_spaces": chars_no_spaces,
        "word_count": word_count,
        "sentence_count": sentence_count,
        "paragraph_count": paragraph_count,
        "avg_word_len": avg_word_len,
        "reading_minutes": reading_minutes,
        "top_words": top_words,
        "longest_word": longest_word,
        "unique_words": len(set(words)),
    }


def calculator(request):
    """Calculator + Text Analyzer page.

    The Loan / Tip / BMI tabs are pure client-side JS (instant feedback).
    The Text Analyzer tab uses a classic Django POST round-trip to prove
    out server-side Python compute — the bread-and-butter of Django.
    """
    context = {"active_tab": "loan"}
    if request.method == "POST" and "analyzer_text" in request.POST:
        analysis = _analyze_text(request.POST.get("analyzer_text", ""))
        context["analysis"] = analysis
        context["active_tab"] = "analyzer"
    return render(request, "dashboard/calculator.html", context)
