from .models import News, Category


def base_latest_news(request):
    latest_news = News.published.all()[:10]
    base_categorys = Category.objects.all()

    context = {
        'latest_news': latest_news,
        'base_categorys': base_categorys
    }

    return context

