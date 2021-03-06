from django.core.exceptions import ImproperlyConfigured


class ExtraQueryMixin(object):
    def __init__(self, *args, **kwargs):
        self.extra_query_dic = {}
        return super(ExtraQueryMixin, self).__init__(*args, **kwargs)

    def get_extra_query(self):
        if self.extra_query_dic is None:
            return ''

        qs = ''
        for key, value in self.extra_query_dic.iteritems():
            qs = qs + key + '=' + str(value) + '&'

        return qs

    def get_context_data(self, *args, **kwargs):
        context = super(ExtraQueryMixin, self).get_context_data(*args, **kwargs)
        context['extra_query'] = self.get_extra_query()
        context['extra_query_dic'] = self.extra_query_dic
        return context


class FilterMixin(object):
    """
    View mixin which provides filtering for ListView.
    """
    default_filter_field = None
    default_filter_value = 'all'

    def filter_queryset(self, qs, filter_param):
        """
        Filter the queryset `qs`, given the selected `filter_param`. Default
        implementation does no filtering at all.
        """
        return qs

    def get_default_filter_field(self):
        return self.get_default_filter_field

    def get_default_filter_value(self):
        return self.default_filter_value


    def get_filter_field(self):
        return self.request.GET.get('filterfield',self.get_default_filter_field())

    def get_filter_value(self):
        return self.request.GET.get('filtervalue',self.get_default_filter_value())

    def get_filter_param(self):
        return self.get_filter_field(), self.get_filter_value()

    def get_queryset(self):
        return self.filter_queryset(
            super(FilterMixin, self).get_queryset(),
            self.get_filter_param())

    def get_context_data(self, *args, **kwargs):
        context = super(FilterMixin, self).get_context_data(*args, **kwargs)
        context.update({
            'filterfield': self.get_filter_field(),
            'filtervalue' : self.get_filter_value(),
        })
        return context


class SortMixin(object):
    """
    View mixin which provides sorting for ListView.
    """
    default_sort_params = None

    def sort_queryset(self, qs, sort_by, order):
        return qs

    def get_default_sort_params(self):
        if self.default_sort_params is None:
            raise ImproperlyConfigured(
                "'SortMixin' requires the 'default_sort_params' attribute "
                "to be set.")
        return self.default_sort_params

    def get_sort_params(self):
        default_sort_by, default_order = self.get_default_sort_params()
        sort_by = self.request.GET.get('sort_by', default_sort_by)
        order = self.request.GET.get('order', default_order)
        return (sort_by, order)

    def get_queryset(self):
        return self.sort_queryset(
            super(SortMixin, self).get_queryset(),
            *self.get_sort_params())

    def get_context_data(self, *args, **kwargs):
        context = super(SortMixin, self).get_context_data(*args, **kwargs)
        sort_by, order = self.get_sort_params()
        context.update({
            'sort_by': sort_by,
            'order': order,
        })
        return context