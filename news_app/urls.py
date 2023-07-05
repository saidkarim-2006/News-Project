from django.urls import path
from .views import NewsView, DetailView, HomePageView, ContactPageView, news_detail, LocalNewsView, ForeignNewsView, \
    TechnologyNewsView, SportNewsView, NewsUpdateView, NewsDeleteView, NewsCreateView, admin_page, SearchView

urlpatterns = [
    path('', HomePageView.as_view(), name='home_page'),
    path("news/", NewsView.as_view(), name="all_news_list"),
    path("news/<slug:news>/", news_detail, name="detail_view"),
    path("news/<slug>/update/", NewsUpdateView.as_view(), name="news_update"),
    path("news/<slug>/delete/", NewsDeleteView.as_view(), name="news_delete"),
    path("add/", NewsCreateView.as_view(), name="news_create"),
    path('contact/', ContactPageView.as_view(), name='contact_page'),
    path('mahalliy/', LocalNewsView.as_view(), name="local_news_page"),
    path('xorij/', ForeignNewsView.as_view(), name="foreign_news_page"),
    path('texnalogiya/', TechnologyNewsView.as_view(), name="technology_news_page"),
    path('sport/', SportNewsView.as_view(), name="sport_news_page"),
    path('adminpage/', admin_page, name='admin_page'),
    path('search/', SearchView.as_view(), name='search_result'),
]

