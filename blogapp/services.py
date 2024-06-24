from django.core.cache import cache

from blogapp.models import Article
from config import settings


def get_cached_article_list(recached: bool = False):
    if settings.CACHE_ENABLED:
        print('get_cached_article_list')
        key = f'article_list'
        if recached:
            # print('get_cached_article_list - recached')
            article_list = Article.objects.all()
            cache.set(key, article_list)
        else:
            # print('get_cached_article_list -  cache.get(key)')
            article_list = cache.get(key)
            if article_list is None:
                # print('get_cached_article_list - cache.set(key, article_list)')
                article_list = Article.objects.all()
                cache.set(key, article_list)
    else:
        article_list = Article.objects.all()
    return article_list
