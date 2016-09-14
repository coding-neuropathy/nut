# encoding: utf-8
import json
from django.views.decorators.csrf import csrf_exempt
from apps.core.forms.entity import EntityImageForm, AddEntityForm, AddEntityFormForSeller, CreateEntityFormForSeller
from apps.core.extend.paginator import ExtentPaginator
from apps.core.forms.entity import EditEntityForm
from apps.core.mixins.views import FilterMixin, SortMixin
from apps.management.views.entities import Add_local, Import_entity
from apps.order.models import OrderItem
from braces.views import JSONResponseMixin,AjaxResponseMixin, UserPassesTestMixin
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.db.models import Sum
from django.http import HttpResponseRedirect
from django.shortcuts import render, render_to_response
from django.shortcuts import get_object_or_404
from apps.management.forms.sku import SKUForm,SwitchSkuStatusForm
from apps.core.utils.http import SuccessJsonResponse
from apps.core.models import Entity
from apps.order.models import SKU, Order
from django.template import RequestContext
from django.views.generic import ListView, CreateView, DeleteView, UpdateView,DetailView, View
from django.http import Http404,HttpResponseNotAllowed
from apps.management.decorators import staff_only, staff_and_editor
from apps.core.utils.http import JSONResponse
from datetime import datetime, timedelta

from apps.web.views.user import get_seller_entities

TIME_FORMAT = '%Y-%m-%d 8:00:00'


class SKUUserPassesTestMixin(UserPassesTestMixin):
    def test_func(self, user):
        self.entity_id = self.kwargs.get('entity_id')
        self.sku_id = self.kwargs.get('pk')
        sku = SKU.objects.get(pk=self.sku_id)
        return user.has_sku(sku)
    def no_permissions_fail(self, request=None):
        raise Http404

class EntityUserPassesTestMixin(UserPassesTestMixin):
    def test_func(self, user):
        self.entity_id = self.kwargs.get('entity_id')
        entity = Entity.objects.get(id=self.entity_id)
        return entity in user.seller_entities
        # TODO : potential performance hit , when seller has lots of entities
        # return user.has_entity(entity)
    def no_permissions_fail(self, request=None):
        raise Http404

class IsAuthorizedSeller(UserPassesTestMixin):
    def test_func(self, user):
        return user.is_authorized_seller
    def no_permissions_fail(self, request=None):
        raise Http404


class SellerManagement(IsAuthorizedSeller, FilterMixin, SortMixin,  ListView):
    default_sort_params = ('dupdated_time', 'desc')
    http_method_names = ['get']
    paginator_class = ExtentPaginator
    model = Entity
    paginate_by = 20
    template_name = 'web/seller_management/seller_management.html'

    def get(self, request, *args, **kwargs):
        if request.GET.get('print') == 'true':
            return self.get_qrimage(request)
        return super(SellerManagement, self).get(self, request, *args, **kwargs)

    def get_qrimage(self, request):
        self.object_list = self.get_queryset()
        context = self.get_context_data()
        for entity in context['object_list']:
            try:
                entity.buy_link = entity.buy_links.all()[0]
            except:
                entity.buy_link = ''
            entity.qr_info = [entity.brand, entity.title, "", entity.price, entity.buy_link]
        return render_to_response('web/seller_management/qr_image.html', {'entities': context['object_list']},
                                  context_instance=RequestContext(request)
                                  )

    def get_queryset(self):
        qs = self.request.user.seller_entities
        return self.sort_queryset(self.filter_queryset(qs,self.get_filter_param()), *self.get_sort_params())

    def get_context_data(self, **kwargs):
        context = super(SellerManagement, self).get_context_data(**kwargs)
        for entity in context['object_list']:
            entity.sku_list = entity.skus.all()
            entity.stock = entity.sku_list.aggregate(Sum('stock')).get('stock__sum', 0) or 0
            entity.title=entity.title[:15]
        context['sort_by'] = self.get_sort_params()[0]
        context['extra_query'] = 'sort_by=' + context['sort_by']
        context['current_url'] = self.request.get_full_path()
        return context

    def filter_queryset(self, qs, filter_param):
        filter_field, filter_value = filter_param
        if filter_field == 'title':
            qs = qs.filter(title__icontains=filter_value.strip())
        else:
            pass
        return qs

    def sort_queryset(self, qs, sort_by, order):
        #if sort_by == 'dprice':
            #qs = qs.order_by('-price')
        #elif sort_by == 'uprice':
         #   qs = qs.order_by('price')
        if sort_by == 'dupdated_time':
            qs = qs.order_by('-updated_time')
        elif sort_by == 'uupdated_time':
            qs = qs.order_by('updated_time')
        elif sort_by == 'ustock':
            qs = sorted(qs, key=lambda x: x.total_stock, reverse=False)
        elif sort_by == 'dstock':
            qs = sorted(qs,key=lambda x: x.total_stock, reverse=True)
        else:
            pass
        return qs

class QrcodeListView(IsAuthorizedSeller,  AjaxResponseMixin,  JSONResponseMixin,  ListView):
    template_name = 'web/seller_management/qr_image.html'

    def get(self, request, *args, **kwargs):
        print_entities_jsonstring = request.GET.get('entity_ids',None)
        if print_entities_jsonstring:
            print_entities = json.loads(print_entities_jsonstring)
            self.object_list = self.get_checked_entities(print_entities)
        else:
            self.object_list = self.get_queryset()

        host = request.get_host()
        for entity in self.object_list:
          entity.title = entity.title[:15]
          entity.qr_info = [entity.brand, entity.title, "", entity.price, host + entity.qrcode_url]
        return render_to_response(self.template_name, {'entities': self.object_list},
                                  context_instance=RequestContext(request)
                                  )

    def get_queryset(self):
        qs = self.request.user.entities.all()
        return qs

    def get_checked_entities(self, checked_entities):
        checked_entities_to_print = self.request.user.entities.all().filter(entity_hash__in=checked_entities)
        return checked_entities_to_print


class IsAuthorizedSeller(UserPassesTestMixin):
    def test_func(self, user):
        return user.is_authorized_seller

    def no_permissions_fail(self, request=None):
        raise Http404



class SellerManagementAddEntity(Add_local):
    template_name = 'web/seller_management/add_entity.html'
    form_class = AddEntityFormForSeller

    def post(self, request, *args, **kwargs):
        form = self.form_class(request, data=request.POST, files=request.FILES)
        if form.is_valid():
            entity = form.save()
            return HttpResponseRedirect(reverse('web_seller_management_entity_edit', args=[entity.id]))
        return render(request, self.template_name, {'forms': form})

@login_required
def image(request, entity_id,
          template='web/seller_management/seller_upload_image.html'):
    try:
        _entity = Entity.objects.get(pk=entity_id)
    except Entity.DoesNotExist:
        raise Http404

    if request.method == "POST":
        _forms = EntityImageForm(entity=_entity, data=request.POST,
                                 files=request.FILES)
        if _forms.is_valid():
            _forms.save()
            return HttpResponseRedirect(reverse('web_seller_management_entity_edit', args=[_entity.id]))

    else:
        _forms = EntityImageForm(entity=_entity)

    return render_to_response(
        template,
        {
            'entity': _entity,
            'forms': _forms,
        },
        context_instance=RequestContext(request)
    )
@login_required
def seller_management_entity_edit(request, entity_id, template='web/seller_management/edit_entity.html'):
    #Todo 拆分模版
    _update = None
    try:
        entity = Entity.objects.get(pk=entity_id)
    except Entity.DoesNotExist:
        raise Http404
    data = {
        # 'id':entity.pk,
        'creator': entity.user.profile.nickname,
        'brand': entity.brand,
        'title': entity.title,
        'price': entity.price,
        'status': entity.status,
        'category': entity.category.group_id,
        'sub_category': entity.category_id,
    }

    if request.method == "POST":
        _forms = EditEntityForm(
            entity,
            request.POST,
            initial=data
        )
        _update = 1

        if _forms.is_valid():
            _forms.save()
            _update = 0

    else:
        _forms = EditEntityForm(
            entity=entity,
            initial=data
        )

    return render_to_response(
        template,
        {
            'entity': entity,
            'forms': _forms,
            'update': _update,
        },
        context_instance=RequestContext(request)
    )
@csrf_exempt
@login_required
def delete_image(request, entity_id):
    if request.method == 'POST':
        _index = request.POST.get('index', None)
        try:
            _entity = Entity.objects.get(pk=entity_id)
            images = _entity.images
            images.remove(_index)
            _entity.images = images
            _entity.save()
        except Entity.DoesNotExist:
            raise Http404

        status = True
        # if 'http://imgcdn.guoku.com/' in _index:
        #     image_name = _index.replace('http://imgcdn.guoku.com/', '')
        #     status = default_storage.delete(image_name)
        return SuccessJsonResponse(data={'status': status})

    return HttpResponseNotAllowed

class SellerManagementEntitySave(JSONResponseMixin, AjaxResponseMixin, View):
    model = Entity
    def save_update(self,sku_id, price, stock):
        sku_id = int(json.loads(sku_id))
        sku = SKU.objects.get(id=sku_id)
        if price:
            price = float(json.loads(price))
            sku.promo_price = price
        if stock:
            stock = int(json.loads(stock))
            sku.stock = stock
        sku.save()
        return

    def post_ajax(self, request, *args, **kwargs):
        price = request.POST.get('price', None)
        stock = request.POST.get('stock')
        sku_id = request.POST.get('sku_id', None)
        try:
            self.save_update(sku_id, price, stock)
            return self.render_json_response({'status': '1'}, 200)
        except:
            return self.render_json_response({'status': '-1'}, 404)

class SellerEntitySKUCreateView(EntityUserPassesTestMixin, CreateView):
    model = SKU
    form_class = SKUForm
    template_name = 'web/seller_management/create_sku.html'
    def get_success_url(self):
        return reverse('management_entity_skus', args=[self.entity_id])

    def get_initial(self):
        return {
            'entity':self.entity_id
        }

class SKUStatusChangeView(EntityUserPassesTestMixin, JSONResponseMixin, UpdateView):

    form_class = SwitchSkuStatusForm
    model = SKU
    pk_url_kwarg = 'sku_id'

    def form_invalid(self, form):
        res = {'error':1}
        return self.render_json_response(res)
    def form_valid(self, form):
        form.save()
        res = {'error':0}
        return self.render_json_response(res)


class SKUListView(EntityUserPassesTestMixin, SortMixin, ListView):
    default_sort_params = ('dstock', 'desc')
    template_name = 'web/seller_management/sku_list.html'

    def get_queryset(self):
        entity = get_object_or_404(Entity, id=self.entity_id)
        return self.sort_queryset(entity.skus.all(), *self.get_sort_params())

    def get_context_data(self, **kwargs):
        context = super(SKUListView, self).get_context_data(**kwargs)
        context['entity'] = get_object_or_404(Entity, id=self.entity_id)
        context['sort_by'] = self.get_sort_params()[0]
        context['extra_query'] = 'sort_by=' + context['sort_by']
        # for sku in context['object_list']:
        #     l = sku.attrs_display.split(';')
        #     for item in l:
        #         new = item.replace('_', ':')

        return context

    def sort_queryset(self, qs, sort_by, order):
        if sort_by == 'dstock':
            qs = qs.order_by('-stock')
        elif sort_by == 'ustock':
            qs = qs.order_by('stock')
        elif sort_by == 'dorigin_price':
            qs = qs.order_by('-origin_price')
        elif sort_by == 'uorigin_price':
            qs = qs.order_by('origin_price')
        elif sort_by == 'dpromotion_price':
            qs = qs.order_by('-promo_price')
        elif sort_by == 'upromotion_price':
            qs = qs.order_by('promo_price')
        elif sort_by == 'dstatus':
            qs = qs.order_by('-status')
        elif sort_by == 'ustatus':
            qs = qs.order_by('status')
        else:
            pass
        return qs


#class SKUCreateView(EntityUserPassesTestMixin, CreateView):
#    model = SKU
#    form_class = SKUForm
#    template_name = 'web/seller_management/add_sku.html'
#    def get_success_url(self):
#        return reverse('sku_list_management', args=[self.entity_id])
#    def get_context_data(self, **kwargs):
#        context = super(CreateView,self).get_context_data(**kwargs)
#        context['entity_id']=self.entity_id
#        return context
#    def get_initial(self):
#        return {
#            'entity':self.entity_id
#        }

class SKUCreateView(EntityUserPassesTestMixin, AjaxResponseMixin, CreateView):
    model = SKU
    form_class = SKUForm
    template_name = 'web/seller_management/sku/sku_add_template.html'

    def post_ajax(self, request, *args, **kwargs):
        _forms = SKUForm(request.POST)
        if _forms.is_valid():
            _forms.save()
            return JSONResponse(data={'result': 1},status=200)
        elif _forms.repeatstatus:
            return JSONResponse(data={'result': -1},status=406)
        else :
            return JSONResponse(data={'result': 0},status=400)
    def get_success_url(self):
        return reverse('sku_list_management', args=[self.entity_id])
    def get_context_data(self, **kwargs):
        context = super(SKUCreateView,self).get_context_data(**kwargs)
        context['entity_id']=self.entity_id
        return context
    def get_initial(self):
        initial_price = Entity.objects.get(pk=self.entity_id).price
        return {
            'entity':self.entity_id,
            'origin_price':initial_price,
            'promo_price':initial_price
        }

class SKUUpdateView(SKUUserPassesTestMixin, AjaxResponseMixin,UpdateView):
    model = SKU
    form_class = SKUForm
    template_name = 'web/seller_management/sku/sku_edit_template.html'
    def post_ajax(self, request, *args, **kwargs):
        instance = SKU.objects.get(pk=kwargs['pk'])
        _forms = SKUForm(request.POST,instance=instance)
        if _forms.is_valid():
            _forms.save()
            return JSONResponse(data={'result': 1},status=200)
        elif _forms.repeatstatus:
            return JSONResponse(data={'result': -1},status=406)
        else:
            return JSONResponse(data={'result': 0},status=400)
    def get_context_data(self, **kwargs):
        context = super(SKUUpdateView,self).get_context_data(**kwargs)
        context['entity_id']=self.entity_id
        return context
    def get_success_url(self):
        return reverse('sku_list_management', args=[self.entity_id])


class SKUDeleteView(SKUUserPassesTestMixin, DeleteView):
    model = SKU
    template_name = 'web/seller_management/delete_sku.html'

    def get_success_url(self):
        return reverse('sku_list_management', args=[self.entity_id])

class OrderDetailView(UserPassesTestMixin,DetailView):
    pk_url_kwarg = 'order_number'
    context_object_name = 'order'
    model = Order
    http_method_names = ['get']
    paginator_class = ExtentPaginator
    paginate_by = 10
    template_name = 'web/seller_management/order_detail.html'
    def test_func(self, user):
        self.order_number = self.kwargs.get('order_number')
        order = Order.objects.get(pk=self.order_number)
        for i in order.items.all():
            if i.sku.entity in user.entities.all():
                return True
        return False
    def no_permissions_fail(self, request=None):
        raise Http404
    def get_context_data(self, **kwargs):
        context = super(OrderDetailView, self).get_context_data(**kwargs)
        context['order_item'] = context['order'].items.all().filter(sku__entity__in = self.request.user.entities.all())
        #context['order_item'] = context['order'].items.all()
        context['order_number']=self.order_number
        context['promo_total_price']=context['order'].promo_total_price
        context['origin_total_price']=context['order'].grand_total_price
        context['count']=context['order'].items.all().count()
        return context


class SellerManagementOrders(IsAuthorizedSeller, FilterMixin, SortMixin,  ListView):
    default_sort_params = ('dnumber','desc')
    http_method_names = ['get']
    paginator_class = ExtentPaginator
    model = Order
    paginate_by = 10
    template_name = 'web/seller_management/order_list.html'

    def get_queryset(self):
        entities = self.request.user.entities.all()
        order_items = OrderItem.objects.filter(sku__entity_id__in=entities)
        order_ids = order_items.values_list('order')
        qs = Order.objects.filter(id__in=order_ids)
        self.status = self.request.GET.get('status')
        if self.status == 'waiting_for_payment':
            qs = qs.filter(status__in=[1,2,4])
        elif self.status == 'paid':
            qs = qs.filter(status=3)
        return self.sort_queryset(self.filter_queryset(qs,self.get_filter_param()), *self.get_sort_params())

    def filter_queryset(self, qs, filter_param):
        filter_field, filter_value = filter_param
        #if filter_field == 'id':
            #qs = qs.filter(id=filter_value.strip())
        if filter_field == 'number':
            qs = qs.filter(number__icontains=filter_value.strip())
        else:
            pass
        return qs
    def sort_queryset(self, qs, sort_by, order):
        if sort_by == 'dprice':
            qs = sorted(qs, key=lambda x: x.order_total_value, reverse=True)
        elif sort_by == 'uprice':
            qs = sorted(qs, key=lambda x: x.order_total_value, reverse=False)
        elif sort_by == 'dnumber':
            qs = qs.order_by('-number')
        elif sort_by == 'unumber':
            qs = qs.order_by('number')
        elif sort_by == 'status':
            qs =  qs.order_by('-status')
        else:
            pass
        return qs

    def get_context_data(self, **kwargs):
        context = super(SellerManagementOrders, self).get_context_data(**kwargs)
        context['status']=self.status
        for order in context['object_list']:
            order_items = order.items.all()
            order.skus = [order_item.sku for order_item in order_items]
            order.count=order.items.all().count()
            order.itemslist=order.items.all()[1:order.count]
        return context


class SellerManagementSoldEntityList(IsAuthorizedSeller, FilterMixin, SortMixin,  ListView):

    default_sort_params = ('dsold_count', 'desc')
    http_method_names = ['get']
    paginator_class = ExtentPaginator
    model = Entity
    paginate_by = 10
    template_name = 'web/seller_management/sold_entity_list.html'

    def get_queryset(self):
        entities = self.request.user.entities.all()
        self.order_items = OrderItem.objects.filter(sku__entity_id__in=entities)
        order_ids = self.order_items.values_list('order')
        self.orders = Order.objects.filter(id__in=order_ids).filter(status__in=[3,5])
        sku_ids = [ ]
        if self.orders:
            for order in self.orders:
                if sku_ids:
                    sku_ids += list(order.items.values_list('sku'))
                else:
                    sku_ids = list(order.items.values_list('sku'))
        if sku_ids:
            for i in range(len(sku_ids)):
                sku_ids[i]=sku_ids[i][0]
        #sku_ids = self.order_items.values_list('sku')
        qs = SKU.objects.filter(id__in=sku_ids).filter(entity_id__in=entities)
        # qs = list(set([item.sku for item in self.order_items]))
        return self.sort_queryset(self.filter_queryset(qs,self.get_filter_param()), *self.get_sort_params())

    def sort_queryset(self, qs, sort_by, order):
        d={}
        for order in self.order_items:
            if order.sku.id not in d.keys():
                d[order.sku.id] = order.volume
            else:
                d[order.sku.id] += order.volume
        for i in qs:
            i.sold_count=d[i.id]
        if sort_by == 'dsold_count':
            qs = sorted(qs, key=lambda x: x.sold_count, reverse=True)
        elif sort_by == 'usold_count':
            qs = sorted(qs, key=lambda x: x.sold_count, reverse=False)
        elif sort_by == 'dstock':
            qs = qs.order_by('-stock')
        elif sort_by == 'ustock':
            qs = qs.order_by('stock')
        else:
            pass
        return qs

    def get_context_data(self, **kwargs):
        context = super(SellerManagementSoldEntityList, self).get_context_data(**kwargs)
        for sku in context['object_list']:
            sku.title=sku.entity.title[:15]

        d = {}
        for ord in self.orders:
            for order in ord.items.all():
                if order.sku.id not in d.keys():
                    d[order.sku.id] = order.volume
                else:
                    d[order.sku.id] += order.volume
        for object in context['object_list']:
            object.sold_count = d[object.id]
        context['sort_by'] = self.get_sort_params()[0]
        context['extra_query'] = 'sort_by=' + context['sort_by']
        return context

    def filter_queryset(self, qs, filter_param):
        filter_field, filter_value = filter_param
        if filter_field == 'title':
            qs = qs.filter(entity__title__icontains=filter_value.strip())
        else:
            pass
        return qs


class SellerManagementSkuSave(AjaxResponseMixin, JSONResponseMixin, View):
    model = SKU

    def save_update(self, id, price, stock):
        sku = SKU.objects.get(id=id)
        sku.promo_price = price
        sku.stock = stock
        sku.save()
        return

    def post_ajax(self, request, *args, **kwargs):
        price = request.POST.get('price', None)
        id = request.POST.get('id', None)
        stock = request.POST.get('stock', None)
        price = json.loads(price)
        id = json.loads(id)
        stock = json.loads(stock)
        try:
            self.save_update(id, price, stock)
        except:
            pass
        return HttpResponseRedirect(reverse('web_seller_management'))


class SellerManagementImportEntity(Import_entity):
    def __init__(self):
        super(SellerManagementImportEntity, self).__init__(template='web/seller_management/import_entity.html',
                                                           entity_edit_url='web_seller_management_entity_edit',
                                                           form=CreateEntityFormForSeller)


def get_time_range():
    if datetime.now().hour > 8:
        today_start = datetime.now().strftime(TIME_FORMAT)
        today_end = (datetime.now() + timedelta(days=1)).strftime(TIME_FORMAT)
    else:
        today_start = (datetime.now() - timedelta(days=1)).strftime(TIME_FORMAT)
        today_end = datetime.now().strftime(TIME_FORMAT)

    return today_start, today_end

from django.db import connection
def get_finished_count(user_id):
    cursor = connection.cursor()
    cursor.execute( "select date(created_datetime),count(*) as finished_count from( "\
                    "select order_order.number,order_order.created_datetime,"\
                    "order_sku.attrs "\
                    "from order_order "\
                    "join order_orderitem "\
                    "on order_orderitem.order_id=order_order.id "\
                    "join order_sku "\
                    "on order_orderitem.sku_id=order_sku.id "\
                    "join core_entity "\
                    "on order_sku.entity_id=core_entity.id "\
                    "where core_entity.user_id=%s "\
                    "and order_order.status<6 and order_order.status>2 "\
                    "group by order_order.id) as temp "\
                    "group by date(created_datetime)", [user_id])  # find finished orders of this user
    res = cursor.fetchall()
    return parse_data(res)

def get_income(user_id):
    cursor = connection.cursor()
    cursor.execute( "select date(created_datetime),sum(income) from"\
                    "(select order_order.created_datetime,order_sku.attrs,"\
                    "order_orderitem.promo_total_price as income "\
                    "from order_order join order_orderitem on order_order.id=order_orderitem.order_id join order_sku on order_orderitem.sku_id=order_sku.id "\
                    "join core_entity on order_sku.entity_id=core_entity.id "\
                    " where core_entity.user_id=%s "\
                    "and order_order.status<6 and order_order.status>2 "\
                    "order by date(created_datetime)) as temp  "\
                    "group by date(created_datetime)",[user_id])
    res=cursor.fetchall()
    return parse_data(res)
def parse_data(res):
    if res:
        start=res[0][0]
        key_list=[x[0] for x in res]
        while(start<datetime.now().date()):
            start=start+timedelta(1)
            if start not in key_list:
                res+=(start,0),
    res=sorted(res,key=lambda x:x[0])
    return res

class SellerManagementFinancialReport(IsAuthorizedSeller,ListView):
    model = Order
    template_name = 'web/seller_management/financial_report/seller_financial_report.html'
    def get_queryset(self):
        return Order.objects.none()
    def get_context_data(self, **kwargs):
        context = super(SellerManagementFinancialReport, self).get_context_data(**kwargs)
        user_id = self.request.user.id
        finished_count = get_finished_count(user_id)
        income = get_income(user_id)
        context["finished_count_x"]=[str(x[0].day) for x in finished_count]
      #  context['finished_count_x']=["Red", "Blue", "Yellow", "Green", "Purple", "Orange"]
        context["finished_count_y"]=[int(x[1]) for x in finished_count]
        context["income_x"]=[str(x[0].day) for x in income]
        context['income_y']=[int(x[1]) for x in income]
        return context

