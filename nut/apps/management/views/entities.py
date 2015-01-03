from django.http import Http404, HttpResponseNotAllowed, HttpResponseRedirect, HttpResponse
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.core.urlresolvers import reverse
# from django.views.generic.list import ListView
# from django.core.paginator import Paginator, EmptyPage, InvalidPage
from django.utils.log import getLogger
from django.core.files.storage import default_storage

from apps.core.models import Entity, Buy_Link
from apps.core.forms.entity import EntityForm, EntityImageForm, BuyLinkForm, CreateEntityForm, load_entity_info
from apps.core.extend.paginator import ExtentPaginator, EmptyPage, PageNotAnInteger
from apps.core.utils.http import SuccessJsonResponse

log = getLogger('django')

#
# class EntityListView(ListView):
#     model = Entity
#     template_name = 'management/entities/list.html'
#     context_object_name = "entities"
#     paginate_by = 30
#     http_method_names = [u'get',]
#
#     def get_queryset(self):
#         page = self.request.GET.get('page', 1)
#         status = self.request.GET.get('status', None)


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
    except PageNotAnInteger:
        entities = paginator.page(1)
    except EmptyPage:
        raise Http404
    # log.info(paginator.page_range)
    return render_to_response(
        template,
        {
            'entities': entities,
                                # 'page_range': paginator.page_range_ext,
            'status': status,
        },
        context_instance = RequestContext(request)
    )


def edit(request, entity_id, template='management/entities/edit.html'):

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

    return render_to_response(
        template,
        {
            'entity': entity,
            'forms': _forms,
            'update': _update,
        },
        context_instance = RequestContext(request)
    )


def create(request, template='management/entities/new.html'):

    # res = dict()
    _url = request.GET.get('url')

    if _url is None:
        raise Http404
        # print(_url)
    res = load_entity_info(_url)

    if request.method == "POST":
        _forms = CreateEntityForm(request=request, data=request.POST, initial=res)
        # _forms = EntityURLFrom(request=request, data=request.POST)
        # if _forms.is_valid():
        #     res = _forms.load()
        #     log.info(res)
        #     return HttpResponse("OK")
    else:

        # log.info(res)
        _forms = CreateEntityForm(request=request, initial=res)

    return render_to_response(
        template,
        {
            'res': res,
            'forms': _forms,
        },
        context_instance = RequestContext(request)
    )


# def add_link(request, template=""):
#
#
#     return render_to_response(
#         template,
#         {
#
#         },
#
#     )

def buy_link(request, entity_id, template='management/entities/buy_link.html'):

    # _buy_link_list = Buy_Link.objects.filter(entity_id = entity_id)
    try:
        _entity = Entity.objects.get(pk=entity_id)
    except Entity.DoesNotExist:
        raise Http404

    if request.method == 'POST':
        _forms = BuyLinkForm(entity=_entity, data=request.POST)
        if _forms.is_valid():
            _forms.save()
            return HttpResponseRedirect(reverse('management_entity_edit', args=[entity_id]))
    else:
        _forms = BuyLinkForm(entity=_entity)

    return render_to_response(
        template,
        {
            'entity':_entity,
            'forms':_forms,
            # 'buy_link_list': _buy_link_list,
        },
        context_instance = RequestContext(request)
    )



def image(request, entity_id, template='management/entities/upload_image.html'):

    try:
        _entity = Entity.objects.get(pk=entity_id)
    except Entity.DoesNotExist:
        raise Http404

    if request.method == "POST":
        _forms = EntityImageForm(entity=_entity, data=request.POST, files=request.FILES)
        if _forms.is_valid():
            _forms.save()
    else:
        _forms = EntityImageForm(entity=_entity)

    return render_to_response(
        template,
        {
            'entity': _entity,
            'forms': _forms,
        },
        context_instance = RequestContext(request)
    )


from django.views.decorators.csrf import csrf_exempt
@csrf_exempt
def delete_image(request, entity_id):

    if request.method == 'POST':
        _index = request.POST.get('index', None)
        log.info(_index)
        try:
            _entity = Entity.objects.get(pk=entity_id)
            images = _entity.images
            log.info(images)
            images.remove(_index)
            _entity.images = images
            _entity.save()
        except Entity.DoesNotExist:
            raise Http404

        status = True
        if 'http://imgcdn.guoku.com/' in _index:
            image_name = _index.replace('http://imgcdn.guoku.com/', '')
            status = default_storage.delete(image_name)
        return SuccessJsonResponse(data={'status': status})

    return HttpResponseNotAllowed



__author__ = 'edison7500'
