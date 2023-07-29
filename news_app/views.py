from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required, user_passes_test
from django.db.models import Q
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from hitcount.utils import get_hitcount_model

from news_project.custom_permissions import OnlyLoggedSuperUser

from .models import News, Category
from django.views.generic import ListView, DetailView, TemplateView, UpdateView, DeleteView, CreateView
from .forms import ContactForm, CommentForm
from hitcount.views import HitCountDetailView, HitCountMixin


# def news_list(request):
#     news_list = News.objects.all()
#     context = {
#         "news_list": news_list
#     }
#
#     return render(request, "news/news_list.html", context=context)


class NewsView(ListView):
    model = News
    template_name = 'news/news_list.html'
    context_object_name = 'news'


# class DetailView(DetailView):
#     model = News
#     template_name = "news/news_detail.html"
#     context_object_name = "new"


def news_detail(request, news):
    new = get_object_or_404(News, slug=news, status=News.Status.Published)
    context = {}
    # hitcount logic
    hit_count = get_hitcount_model().objects.get_for_object(new)
    hits = hit_count.hits
    hitcontext = context['hitcount'] = {'pk': hit_count.pk}
    hit_count_response = HitCountMixin.hit_count(request, hit_count)
    if hit_count_response.hit_counted:
        hits = hits + 1
        hitcontext['hit_counted'] = hit_count_response.hit_counted
        hitcontext['hit_message'] = hit_count_response.hit_message
        hitcontext['total_hits'] = hits

    comments = new.comments.filter(active=True)
    comment_count = comments.count()
    new_comment = None
    if request.method == 'POST':
        comment_form = CommentForm(data=request.POST)
        if comment_form.is_valid():
            # yangi komment obyektini yaratamiz lekn DB ga saqlamaymiz
            new_comment = comment_form.save(commit=False)
            new_comment.new = new
            # izoh egasini so'rov yuborayotgan userga bog'ladik
            new_comment.user = request.user
            # ma'lumotlar bazasiga saqlaymiz
            new_comment.save()
            comment_form = CommentForm()
    else:
        comment_form = CommentForm()
    context = {
        "new": new,
        'comments': comments,
        'comment_count': comment_count,
        'new_comment': new_comment,
        'comment_form': comment_form
    }

    return render(request, 'news/news_detail.html', context)


# def HomePageView(request):
#     slider_news = News.published.all().order_by('-publish_time')[:10]
#     lasted_news = News.published.all().order_by('-publish_time')[:5]
#     business_one = News.published.filter(category__name='Biznes')[:1]
#     business_news = News.published.all().filter(category__name='Biznes')[1:6]
#     categories = Category.objects.all()
#     context = {
#         'slider_news': slider_news,
#         'categories': categories,
#         'lasted_news': lasted_news,
#         'business_news': business_news,
#         'business_one': business_one
#     }
#
#     return render(request, 'news/index.html', context)


class HomePageView(ListView):
    model = News
    template_name = 'news/index.html'
    context_object_name = 'news'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.all()
        context['slider_news'] = News.published.all().order_by('-publish_time')[:10]
        context['lasted_news'] = News.published.all().order_by('-publish_time')[:5]
        context['business_one'] = News.published.filter(category__name_uz='Iqtisodiyot')[:1]
        context['business_news'] = News.published.all().filter(category__name_uz='Iqtisodiyot')[:5]
        context['technology_news'] = News.published.all().filter(category__name_uz='Texnalogiya')[:6]
        context['foreign_news'] = News.published.all().filter(category__name_uz='Xorij')[:6]
        context['sport_news'] = News.published.all().filter(category__name_uz='Sport')[:6]
        return context


# def ContactPageView(request):
#     form = ContactForm(request.POST or None)
#     if request.method == "POST" and form.is_valid():
#         form.save()
#         return HttpResponse("<h2>Biz bilan bog'langaningiz uchun tashakkur!</h2>")
#     context = {
#         "form": form
#     }
#
#     return render(request, 'news/contact.html', context)

class ContactPageView(TemplateView):
    template_name = 'news/contact.html'

    def get(self, request, *args, **kwargs):
        form = ContactForm()
        context = {
            'form': form
        }
        return render(request, 'news/contact.html', context)

    def post(self, request, *args, **kwargs):
        form = ContactForm(request.POST)
        if request.method == "POST" and form.is_valid():
            form.save()
            return render(request, 'news/contact_done.html')

        context = {
            'form': form
        }
        return render(request, 'news/contact.html', context)


def error_404(request, exception):
    return render(request, 'news/404.html')


class LocalNewsView(ListView):
    model = News
    template_name = 'news/category.html'
    context_object_name = 'category_news'

    def get_queryset(self):
        news = self.model.published.all().filter(category__name_uz="Mahalliy")
        return news


class ForeignNewsView(ListView):
    model = News
    template_name = 'news/category.html'
    context_object_name = 'category_news'

    def get_queryset(self):
        news = self.model.published.all().filter(category__name_uz="Xorij")
        return news


class TechnologyNewsView(ListView):
    model = News
    template_name = 'news/category.html'
    context_object_name = 'category_news'

    def get_queryset(self):
        news = self.model.published.all().filter(category__name_uz="Texnalogiya")
        return news


class SportNewsView(ListView):
    model = News
    template_name = 'news/category.html'
    context_object_name = 'category_news'

    def get_queryset(self):
        news = self.model.published.all().filter(category__name_uz="Sport")
        return news


class EconomyNewsView(ListView):
    model = News
    template_name = 'news/category.html'
    context_object_name = 'category_news'
    title = 'Iq'

    def get_queryset(self):
        news = self.model.published.all().filter(category__name_uz="Iqtisodiyot")
        return news


class NewsUpdateView(OnlyLoggedSuperUser, UpdateView):
    model = News
    fields = (
        'title', 'title_uz', 'title_en', 'title_ru', 'body', 'body_uz', 'body_en', 'body_ru', 'image', 'category',
        'status')
    template_name = 'crud/news_edit.html'


class NewsDeleteView(OnlyLoggedSuperUser, DeleteView):
    model = News
    template_name = 'crud/news_delete.html'
    success_url = reverse_lazy('home_page')


class NewsCreateView(OnlyLoggedSuperUser, CreateView):
    model = News
    template_name = 'crud/news_create.html'
    fields = (
        'title', 'title_uz', 'title_en', 'title_ru', 'body', 'body_uz', 'body_en', 'body_ru', 'image', 'category',
        'status')


@login_required
@user_passes_test(lambda u: u.is_superuser)
def admin_page(request):
    admin_users = User.objects.filter(is_superuser=True)

    context = {
        "admin_users": admin_users
    }
    return render(request, 'pages/admin_page.html', context)


class SearchView(ListView):
    model = News
    template_name = 'news/search.html'
    context_object_name = 'searched_news'

    def get_queryset(self):
        query = self.request.GET.get('q')
        return News.objects.filter(
            Q(title__icontains=query) | Q(body__icontains=query)
        )
