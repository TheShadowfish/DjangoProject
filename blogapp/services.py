from django.core.cache import cache

from blogapp.models import Article
from config import settings


def get_cached_article_list(recached: bool = False):
    if settings.CACHE_ENABLED:
        key = f'article_list'
        if recached:
            article_list = Article.objects.all()
            cache.set(key, article_list)
        else:
            article_list = cache.get(key)
            if article_list is None:
                article_list = Article.objects.all()
                cache.set(key, article_list)
    else:
        article_list = Article.objects.all()
    return article_list
