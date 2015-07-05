from django.conf.urls import url, patterns
from django.views.generic import RedirectView


urlpatterns = patterns(
    'apps.management.views.selection',

    url(r'^$', RedirectView.as_view(url="/management/selection/published/"), name='management_selection_list'),
    url(r'^published/$', 'published', name='management_selection_published'),
    url(r'^pending/$', 'pending', name='management_selection_pending'),
    url(r'^publish/(?P<sid>\d+)/edit/$', 'edit_publish', name='management_selection_edit_publish'),

    url(r'^set/publish/datetime/$', 'set_publish_datetime', name='management_set_publish_datetime'),

    url(r'^popular/$', 'popular', name='management_selection_popular'),

    url(r'^usite/publish/$', 'usite_published', name='management_usite_published'),
)

__author__ = 'edison7500'
