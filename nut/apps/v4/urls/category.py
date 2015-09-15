from django.conf.urls import url, patterns
from apps.v4.views.category import CategoryListView, CategorySelectionView


urlpatterns = patterns(
    'apps.v4.views.category',
    # url(r'^$', 'category_list', name='v4_category_list'),
    url(r'^$', CategoryListView.as_view(), name='v4_category_list'),
    url(r'^(?P<category_id>\d+)/stat/$', 'stat', name='v4_category_stat'),
    url(r'^(?P<category_id>\d+)/entity/$', 'entity', name='v4_category_entity'),
    url(r'^(?P<category_id>\d+)/entity/note/$', 'entity_note', name='v4_category_entity_note'),
    url(r'^(?P<category_id>\d+)/user/(?P<user_id>\d+)/like/$', 'user_like', name='v4_category_user_like'),

    url(r'^(?P<group_id>\d+)/selection/$', CategorySelectionView.as_view(), name='v4_category_selection'),
)

__author__ = 'edison'
