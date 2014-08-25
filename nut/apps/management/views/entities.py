from django.http import Http404
from django.shortcuts import render_to_response
from django.template import RequestContext
# from django.core.paginator import Paginator, EmptyPage, InvalidPage
from django.utils.log import getLogger

from apps.core.models import Entity
from apps.core.forms.entity import EntityForm
from apps.core.extend.paginator import ExtentPaginator, EmptyPage, InvalidPage

log = getLogger('django')


def list(request, template = 'management/entities/list.html'):

    status = request.GET.get('status', None)
    page = request.GET.get('page', 1)
    if status is None:
        entity_list  = Entity.objects.all()
    else:
        entity_list = Entity.objects.filter(status = int(status))

    paginator = ExtentPaginator(entity_list, 30)

    try:
        entities = paginator.page(page)
    except InvalidPage:
        entities = paginator.page(1)
    except EmptyPage:
        raise Http404
    # log.info(paginator.page_range)
    return render_to_response(template,
                            {
                                'entities': entities,
                                'page_range': paginator.page_range[int(page) - 1: 9 + int(page)],
                                'status': status,
                            },
                            context_instance = RequestContext(request))


def edit(request, entity_id,  template='management/entities/edit.html'):

    _update = None
    try:
        entity = Entity.objects.get(pk = entity_id)
    except Entity.DoesNotExist:
        raise Http404

    data = {
            'id':entity.pk,
            'creator':entity.user.profile.nickname,
            'brand':entity.brand,
            'title':entity.title,
            'price':entity.price,
            'status': entity.status,
            'category': entity.category.group_id,
            'sub_category': entity.category_id,
        }

    if request.method == "POST":
        _forms = EntityForm(
            entity,
            request.POST,
            initial=data
        )
        _update = 1

        if _forms.is_valid():
            _forms.save()
            _update = 0

    else:
        log.info(entity.category)
        _forms = EntityForm(
            entity = entity,
            initial=data
        )

    return render_to_response(template,
                        {
                            'entity': entity,
                            'forms': _forms,
                            'update': _update,
                        },
                        context_instance = RequestContext(request))


__author__ = 'edison7500'
