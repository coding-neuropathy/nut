from django.conf.urls import url, patterns
from apps.v4.views.user import APIUserSearchView, APIUserIndexView, \
    APIUserNotesView, APIUserLikeView, APIUserVerifiedView, APIUserArticlesView, APIUserDigArticlesView


urlpatterns = patterns(
    'apps.v4.views.user',

    url(r'^(?P<user_id>\d+)/$', APIUserIndexView.as_view(), name='v4_user_info'),
    url(r'^(?P<user_id>\d+)/tag/$', 'tag_list', name='v4_user_tag_list'),
    url(r'^(?P<user_id>\d+)/tag/(?P<tag>\w+)/$', 'tag_detail', name='v4_user_tag_detail'),
    # url(r'^(?P<user_id>\d+)/like/$', 'entity_like', name='v4_user_entity_like'),
    url(r'^(?P<user_id>\d+)/like/$', APIUserLikeView.as_view(), name='v4_user_entity_like'),
    url(r'^(?P<user_id>\d+)/entity/note/$', 'entity_note', name='v4_user_entity_note'),
    url(r'^(?P<user_id>\d+)/notes/$', APIUserNotesView.as_view(), name='v4_user_notes'),
    url(r'^(?P<user_id>\d+)/dig/articles/$', APIUserDigArticlesView.as_view(), name='v4_dig_articles'),

    url(r'^(?P<user_id>\d+)/articles/$', APIUserArticlesView.as_view(), name='v4_user_articles'),

    url(r'^search/$', APIUserSearchView.as_view(), name='v4_user_search'),

# update user profile
    url(r'^update/$', 'update', name='v4_user_update'),
    url(r'^update/account/$', 'update_account', name="v4_user_update_account"),
    url(r'^update/email/$', 'update_email', name='v4_user_update_email'),

# reset password
    url(r'^reset/password/$', 'rest_password', name='v4_user_reset_password'),

# verified mail
    url(r'^email/verified/$', APIUserVerifiedView.as_view(), name='v4_user_email_verified'),

#   user relationship
    url(r'^(?P<user_id>\d+)/following/$', 'following_list', name='v4_user_following'),
    url(r'^(?P<user_id>\d+)/fan/$', 'fans_list', name='v4_user_fans'),

    url(r'^(?P<user_id>\d+)/follow/(?P<target_status>\d+)/$', 'follow_action', name='v4_user_follow_action'),
)

__author__ = 'edison7500'
