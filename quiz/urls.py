from django.urls import path

from . import views

urlpatterns = [
    path("", views.entry, name="entry"),
    path("logout/", views.logout_view, name="logout"),
    path("home/", views.home, name="home"),
    path("quiz/<str:category>/", views.take_quiz, name="quiz"),
    path("result/<str:code>/", views.result_page, name="result"),
    path("certificate/<str:code>/", views.certificate, name="certificate"),
    path("verify/", views.verify, name="verify"),
    path("results/", views.results_json, name="results"),
    path("results/<str:student_name>/", views.student_results_json, name="student_results"),
    path("summary/", views.summary_json, name="summary"),
]
