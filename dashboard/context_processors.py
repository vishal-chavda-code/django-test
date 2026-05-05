from django.conf import settings


def streamlit_urls(request):
    """Inject Streamlit dashboard URLs into every template context."""
    return {
        "STREAMLIT_DASHBOARD_1_URL": settings.STREAMLIT_DASHBOARD_1_URL,
        "STREAMLIT_DASHBOARD_2_URL": settings.STREAMLIT_DASHBOARD_2_URL,
    }
