from django.shortcuts import render_to_response
from django.http import Http404
from django.views.decorators.http import require_GET
from django.template import RequestContext

from apps.core.models import Category, Sub_Category,  Entity
from apps.core.extend.paginator import ExtentPaginator, PageNotAnInteger, EmptyPage


from django.utils.log import getLogger
log = getLogger('django')


@require_GET
def list(request, template='web/category/list.html'):

    _categories = Category.objects.filter(status=True)

    return render_to_response(
        template,
        {
            'categories': _categories,
        },
        context_instance = RequestContext(request),
    )


@require_GET
def detail(request, cid, template='web/category/detail.html'):
    _cid = cid
    _page = request.GET.get('page', 1)
    _entity_list = Entity.objects.filter(status=Entity.selection, category=_cid)
    _sub_category = Sub_Category.objects.get(pk = _cid)

    paginator = ExtentPaginator(_entity_list, 30)
    try:
        _entities = paginator.page(_page)
    except PageNotAnInteger:
        _entities = paginator.page(1)
    except EmptyPage:
        raise Http404

    return render_to_response(
        template,
        {
            'sub_category': _sub_category,
            'entities': _entities,
        },
        context_instance = RequestContext(request),
    )

__author__ = 'edison7500'
