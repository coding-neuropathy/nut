from django.conf.urls import url, patterns

urlpatterns = patterns(
    'apps.management.views.category',
    # url(r'^(?P<category_id>\d+)/$', 'list', name='management_category_list'),
    url(r'^$', 'list', name='management_category_list'),
    url(r'^create/$', 'create', name='management_category_create'),
    url(r'^(?P<cid>\d+)/edit/$', 'edit', name='management_category_edit'),

    url(r'^(?P<cid>\d+)/sub/category/$', 'sub_category_list', name='management_sub_category_list'),
    url(r'^(?P<cid>\d+)/sub/category/create/$', 'sub_category_create', name='management_sub_categoy_create'),
    url(r'^(?P<scid>\d+)/sub/category/edit/$', 'sub_category_edit', name='management_sub_category_edit'),

    url(r'^(?P<cid>\d+)/entity/$', 'category_entity_list', name='management_category_entities'),
    url(r'^sub/(?P<scid>\d+)/entity/$', 'sub_category_entity_list', name='management_sub_category_entities'),
)

__author__ = 'edison'
