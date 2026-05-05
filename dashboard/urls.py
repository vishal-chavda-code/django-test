from django.urls import path
from . import views

app_name = "dashboard"

urlpatterns = [
    path("", views.home, name="home"),
    path("plotly/", views.plotly_dashboard, name="plotly"),
    path("streamlit-1/", views.streamlit_one, name="streamlit_one"),
    path("streamlit-2/", views.streamlit_two, name="streamlit_two"),
    path("calculator/", views.calculator, name="calculator"),
]
