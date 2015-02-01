from django.http import Http404
from django.shortcuts import render_to_response
from django.template import RequestContext
# from django.core.paginator import Paginator, EmptyPage, InvalidPage
from django.contrib.auth.decorators import  login_required

from apps.core.models import Show_Banner, Sub_Category
from apps.core.utils.http import SuccessJsonResponse
from apps.report.models import Selection
from apps.management.decorators import staff_only
from datetime import datetime, timedelta

from django.utils.log import getLogger
# import binascii

log = getLogger('django')


@login_required
@staff_only
def dashboard(request, template='management/dashboard.html'):
    now = datetime.now()
    range_date = now - timedelta(days=7)
    if request.is_ajax():
        res = {}


        query = "select id, group_id, count(*) as ccount from core_sub_category where id in \
	                (select category_id from core_entity where id in \
	                (select entity_id from core_selection_entity where pub_time between '%s' and '%s'))group by group_id;" % (range_date.strftime("%Y-%m-%d"), now.strftime("%Y-%m-%d"))

        s_c = Sub_Category.objects.raw(query)
        # log.info(s_c.query)
        res['category'] = []
        # color = 0xF7464A
        # highlight = 0xFF5A5E
        for row in s_c:
            data = {
                'value':row.ccount,
                # 'color': hex(color).replace('0x', '#'),
                # 'highlight': hex(highlight).replace('0x', '#'),
                'label': row.title,
            }
            res['category'].append(data)
            # color = color - 100000
            # highlight = highlight - 100000
            #
            # log.info(hex(color))


        s_report = Selection.objects.filter(pub_date__range=(range_date.strftime("%Y-%m-%d"), now.strftime("%Y-%m-%d")))
    # page = request.GET.get('page', 1)
        res['selection'] = []
        for row in s_report:
            res['selection'].append(row.toDict())
        # log.info(res)
        return SuccessJsonResponse(res)

    # innqs = Selection_Entity.objects.filter(pub_time__range=(range_date.strftime("%Y-%m-%d"), now.strftime("%Y-%m-%d")))
    # e = Entity.objects.filter(id__in=innqs).values_list('category', flat=True).distinct()
    # log.info(e)
    show_banners = Show_Banner.objects.all()

    # selection_entity_list = Entity.objects.filter(status = Entity.selection)

    # paginator = Paginator(selection_entity_list, 30)
    #
    # try:
    #     selection_entities = paginator.page(page)
    # except InvalidPage:
    #     selection_entities = paginator.page(1)
    # except EmptyPage:
    #     raise Http404


    return render_to_response(template,
                                {
                                    'show_banners': show_banners,
                                    # 'selection_entities': selection_entities,
                                },
                                context_instance = RequestContext(request))


# @login_required
# @staff_only
# def

__author__ = 'edison7500'
