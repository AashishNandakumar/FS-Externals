from django.urls import path, re_path
from django.contrib.sitemaps.views import sitemap
from .views import *
from .sitemaps import *

sitemaps = {
    "book": BookSiteMap,
}

urlpatterns = [
    # function approach in URLConf
    path("download-csv/", generate_tie_students_csv),
    # string approach in URLConf (from the Project level)
    # path("download-pdf/", "views.generate_pdf"),
    path("download-pdf/", generate_pdf),
    path("rss/", LatestBookFeed()),
    path("atom/", AtomBooksFeed()),
    # Capturing Parameters in URLConf
    path("books/<int:pk>/", book_detail, name="book_detail"),
    path(
        "sitemap.xml",
        sitemap,
        {"sitemaps": sitemaps},
        name="django.contrib.sitemaps.views.sitemap",
    ),
    path("set-cookie/", set_cookie, name="set-cookie"),
    path("get-cookie/", get_cookie, name="get-cookie"),
    path("search/", search_view, name="search"),
    path("search-internship/", search_internship, name="search-internship"),
    path("register/", registration_view, name="register"),
    path("register-student/", register_student, name="register-student"),
    path("feedback/", feedback_view, name="feedback"),
    path("feedback/success/", feedback_success, name="feedback_success"),
    path("render-simple-template", render_simple_template),
    path("load-template", load_template),
    # regex to capture paramters from URL
    re_path(r"^(\d{4})/(\d{6})$", get_two_nos),
    path("validate-phonenumber/<str:phone_number>", validate_phonenumber),
]
