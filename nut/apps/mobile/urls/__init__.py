from django.conf.urls import url, patterns, include


urlpatterns = patterns(
    'apps.mobile.views',
    url(r'^homepage/$', 'homepage', name='mobile_homepage'),
    url(r'^selection/$', 'selection', name='mobile_selection'),
    url(r'^popular/$', 'popular', name='mobile_popular'),
    url(r'^unread/$', 'unread', name='mobile_unread'),
    url(r'^item/(?P<item_id>\w+)/$', 'visit_item', name='mobile_visit_item'),
)

urlpatterns += patterns(
    'apps.mobile.views.account',
    url(r'^login/$', 'login', name='mobile_login'),
    url(r'^register/$', 'register', name='mobile_register'),
    url(r'^logout/$', 'logout', name='mobile_logout'),
    url(r'^forget/password/$', 'forget_password', name='mobile_foreget_password'),
    url(r'^apns/token/$', 'apns_token', name='mobile_apns_token'),

    url(r'^sina/login/$', 'weibo.login_by_weibo', name="mobile_login_by_weibo"),
    url(r'^sina/register/$', 'weibo.register_by_weibo', name='mobile_register_by_weibo'),
    url(r'^taobao/login/$', 'taobao.login_by_taobao', name='mobile_login_by_taobao'),
    url(r'^taobao/register/$', 'taobao.register_by_taobao', name='mobile_register_by_taobao')
)

urlpatterns += patterns(
    'apps.mobile.views.entity',
    url(r'^entity/', include('apps.mobile.urls.entity')),
    url(r'^category/', include('apps.mobile.urls.category')),
    url(r'^user/', include('apps.mobile.urls.user')),
    url(r'^message/', include('apps.mobile.urls.message')),
    url(r'^feed/', include('apps.mobile.urls.feed')),
)


__author__ = 'edison7500'
