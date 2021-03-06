from django.conf.urls import url, patterns
from apps.v4.views.articles import ArticlesListView, ArticleSearchView, \
                                    ArticleTagView, ArticleDigView, \
                                    ArticleUnDigView, ArticleView, ArticleComment

urlpatterns = patterns(
    'apps.v4.views.articles',
    url(r'^$', ArticlesListView.as_view(), name='v4_articles_list'),
    url(r'^(?P<article_id>\d+)/$', ArticleView.as_view(), name='v4_article'),
    url(r'^search/?$', ArticleSearchView.as_view(), name='v4_articles_search'),
    url(r'^tags/(?P<tag_name>\w+)/?', ArticleTagView.as_view(), name='v4_articles_tags'),

    url(r'^(?P<article_id>\d+)/comments/$', ArticleComment.as_view(), name='v4_article_comments'),

    url(r'^dig/$', ArticleDigView.as_view(), name='v4_article_dig'),
    url(r'^undig/$', ArticleUnDigView.as_view(), name='v4_article_undig'),
)

__author__ = 'xiejiaxin'
