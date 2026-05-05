# DjangoVibe — a Django + Streamlit + Plotly demo

A four-page demo site built on the classic **Iris** Kaggle dataset, designed
to show the **range** of what Django can do alongside the rest of the
Python data stack — all wrapped in a deep-vibe (purple/magenta/mint) theme.

| Page          | Built with        | Highlights |
| ------------- | ----------------- | ---------- |
| Home          | Django templates  | Animated gradient hero, navigation cards |
| Plotly        | Django + Plotly   | 4 interactive charts rendered server-side from pandas |
| Streamlit I   | Streamlit (8501)  | Iris explorer with sliders, filters, scatter matrix |
| Streamlit II  | Streamlit (8502)  | Gapminder dashboard — animated bubbles + world map |
| Tools         | Django + JS       | Loan / Tip / BMI calculators **and** a server-side Text Analyzer |

---

## Is Django really 100% Python?

**Yes — from the developer's perspective, every line of logic in this
project is Python.** That includes:

- **Front end (HTML rendering)** — Django's template engine generates HTML
  in Python, on the server. You write `.html` files but they run through
  Python before the browser ever sees them.
- **Back end (logic, routing, data)** — Django views, URL routing, ORM,
  forms, sessions: all Python.
- **Charts** — Plotly figures are built in Python; the chart's JS is
  produced by Plotly automatically and dropped into the page.
- **Dashboards** — Streamlit apps are pure Python files. No HTML, no JS.
- **Data** — pandas reads the CSV, the same way you'd do in Jupyter Lab.

The browser still ultimately runs HTML/CSS/JS (because that's all browsers
can run), but **you don't have to write any of it** unless you want
custom client-side interactivity. The small `calculator.js` in this repo
is the only non-Python code, and it exists only to demonstrate the
*alternative*. The Text Analyzer tab in the same page shows the
**Django-native, fully-Python equivalent**: form → POST → Python →
rendered response.

So yes, if you have a Jupyter Lab server, the same Python skills you use
there carry straight over to Django, Streamlit, and Plotly.

---

## Architecture in one picture

```
┌──────────────────────────────────────────────────────────┐
│  Browser                                                 │
│    http://localhost:8000  (Django pages)                 │
│      │                                                   │
│      │ HTML rendered by Python (Django templates)        │
│      │ Plotly charts injected as inline HTML/JS          │
│      │ Two <iframe> tags pointing at Streamlit ↓         │
└──────┼───────────────────────────────────────────────────┘
       │                                  │              │
       ▼                                  ▼              ▼
┌──────────────┐               ┌─────────────────┐  ┌────────────┐
│ Django :8000 │               │ Streamlit :8501 │  │ St :8502  │
│ Python views │               │ Iris Explorer   │  │ Gapminder │
│ pandas, etc. │               │ (Python)        │  │ (Python)  │
└──────┬───────┘               └────────┬────────┘  └─────┬──────┘
       │                                │                 │
       └──────── data/iris.csv ─────────┘                 │
                            (Plotly built-in datasets) ───┘
```

All three servers are Python processes. They run side-by-side on
different ports.

---

## ⚡ Don't want to read? Hand it to your AI assistant.

If you're using **Claude Code**, **GitHub Copilot Chat**, **Cursor**, or any
agentic coding assistant, just clone the repo, open the folder, and paste
the prompt below. It'll bootstrap and launch everything for you.

````
You're working in a freshly-cloned Django + Streamlit + Plotly demo repo
called "django-test" (the DjangoVibe demo). It has no .env file and
doesn't need one — safe defaults are baked into django_demo/settings.py.

Please do the following, in order, in the project root:

1. Create a Python venv:    python -m venv venv
2. Activate it:
     - Windows PowerShell:  venv\Scripts\Activate.ps1
     - Windows cmd:         venv\Scripts\activate.bat
     - macOS/Linux:         source venv/bin/activate
3. Install dependencies:    pip install -r requirements.txt
4. Run Django migrations:   python manage.py migrate
5. Start all three servers, each in its own background process:
     - streamlit run streamlit_apps/dashboard1.py --server.port 8501
     - streamlit run streamlit_apps/dashboard2.py --server.port 8502
     - python manage.py runserver 8000
   On Windows you can just run `run.bat`. On macOS/Linux `./run.sh`.
6. Once all three are up, confirm by hitting:
     - http://localhost:8000/           (Django home)
     - http://localhost:8000/plotly/    (Plotly dashboard)
     - http://localhost:8000/streamlit-1/ (embeds :8501)
     - http://localhost:8000/streamlit-2/ (embeds :8502)
     - http://localhost:8000/calculator/ (Tools page)
7. Tell me the URL to open and any errors from the logs. Don't modify
   any files unless something is actually broken.
````

That's it — paste the block above into any AI coding assistant from this
project's directory and it'll set everything up. No manual reading
required.

---

## Quick start

### Prerequisites
- Python 3.10+ (tested on 3.12)
- Git

### Setup (one-time)

```bash
# Clone
git clone https://github.com/vishal-chavda-code/django-test.git
cd django-test

# Create virtualenv
python -m venv venv

# Activate it
# Windows (PowerShell):
venv\Scripts\Activate.ps1
# Windows (cmd):
venv\Scripts\activate.bat
# macOS / Linux:
source venv/bin/activate

# Install everything
pip install -r requirements.txt

# Apply Django's built-in migrations (admin, sessions, etc.)
python manage.py migrate
```

> **No `.env` file needed.** The site runs on safe defaults baked into
> `django_demo/settings.py`. A `.env.example` is included in case you
> want to override the secret key, debug flag, or Streamlit URLs later.

### Run all three servers

**Windows:**
```bash
run.bat
```

**macOS / Linux:**
```bash
./run.sh
```

Or run them yourself in three terminals:

```bash
# Terminal 1
streamlit run streamlit_apps/dashboard1.py --server.port 8501

# Terminal 2
streamlit run streamlit_apps/dashboard2.py --server.port 8502

# Terminal 3
python manage.py runserver
```

Then open: **http://localhost:8000**

---

## Project layout

```
django-test/
├── manage.py                       # Django entry point
├── requirements.txt                # Python deps
├── .env.example                    # Optional env vars (the demo runs without it)
├── .gitignore                      # Excludes venv, .env, db.sqlite3, etc.
├── run.bat / run.sh                # One-command launcher
│
├── django_demo/                    # Django project (settings, URLs, WSGI)
│   ├── settings.py                 # Safe defaults — no .env required
│   ├── urls.py
│   └── wsgi.py
│
├── dashboard/                      # The Django app — pages live here
│   ├── views.py                    # 5 views (home/plotly/st1/st2/tools)
│   ├── urls.py
│   ├── context_processors.py       # Streamlit URLs into every template
│   ├── templates/dashboard/
│   │   ├── base.html               # Nav + footer + theme
│   │   ├── home.html
│   │   ├── plotly_dashboard.html
│   │   ├── streamlit1.html         # iframe -> :8501
│   │   ├── streamlit2.html         # iframe -> :8502
│   │   └── calculator.html         # Loan/Tip/BMI + Text Analyzer
│   └── static/dashboard/
│       ├── css/style.css           # Deep-vibe theme
│       └── js/calculator.js        # Client-side calculators
│
├── streamlit_apps/                 # Pure Python Streamlit dashboards
│   ├── dashboard1.py               # Iris Explorer
│   └── dashboard2.py               # Gapminder Pulse
│
├── .streamlit/
│   └── config.toml                 # Theme + iframe-friendly server config
│
└── data/
    └── iris.csv                    # The Kaggle dataset (150 rows, bundled)
```

---

## What each piece is doing

### 1. Django — the front-end framework (still Python)
Django serves the page shell: nav, layout, theme, and static files. Each
page has a Python view in `dashboard/views.py` that renders an HTML
template. The template engine is Python — no Node.js, no React, no build
step.

### 2. Plotly dashboard — server-rendered charts
`views.plotly_dashboard` loads the Iris CSV with pandas, builds four
Plotly figures in Python, themes them with the project palette, and uses
`fig.to_html(...)` to produce the chart HTML/JS. The template just drops
the result into the page with `{{ chart|safe }}`.

### 3. Streamlit dashboards — embedded as iframes
Streamlit can't run inside Django (it has its own server), so the two
Streamlit apps run on `:8501` and `:8502`, and the Django pages embed
them as `<iframe>` elements. Streamlit handles all interactivity — the
slider state, re-renders, charts — entirely in Python.

### 4. Tools page — Django's range on a single page
The Loan / Tip / BMI calculators are vanilla JavaScript (instant
feedback, no server round-trip). The **Text Analyzer** tab is the
opposite: a `<form method="post">` that round-trips through Django's
view, runs pure-Python text analysis (regex, `Counter`, stop-words),
and the template renders the results. Same page, both extremes of the
Django range.

---

## Tweaking colors

All theme tokens live in CSS variables at the top of
`dashboard/static/dashboard/css/style.css`. Change those and the entire
site re-themes. The Streamlit apps duplicate the same palette via
injected CSS so they match end-to-end.

---

## Notes for the team

- The SQLite `db.sqlite3` file is git-ignored. After cloning, run
  `python manage.py migrate` once to create it.
- Static files are served by Django's dev server in DEBUG mode; for
  production you'd run `python manage.py collectstatic`.
- The Streamlit iframes need the two streamlit servers running. If you
  open Streamlit pages without them, you'll see a blank/connection-error
  iframe — that's expected; just start the streamlit servers.
- The Iris dataset is the one most "Hello World" Kaggle datasets ship
  with — it's small, classic, and excellent for visual demos.
