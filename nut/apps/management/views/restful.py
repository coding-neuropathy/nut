from django.views.generic import TemplateView

class AppView(TemplateView):
    template_name = 'management/restful/baseApp.html'
    def get_context_data(self, **kwargs):
        pass


class SbbannerAppView(TemplateView):
    template_name = 'management/restful/SBBannerApp.html'
    def get_context_data(self, **kwargs):
        pass


class ArticleAppView(TemplateView):
    template_name = 'management/restful/ArticleApp.html'


class FLinkAppView(TemplateView):
    template_name = 'management/restful/FriendLinkApp.html'