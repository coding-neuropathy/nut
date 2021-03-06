# coding=utf-8
from apps.core.models import Entity, Selection_Entity, Entity_Like
from apps.wechat.models import Token, RobotDic
from datetime import datetime
from django.utils.log import getLogger
from haystack.query import SearchQuerySet

import re

auto_replies = {
    u'合作': u'合作事宜请发邮件到 bd@guoku.com',
    u'转载': u'文章转载授权请联系 alka@guoku.com',
    u'糯言': u'''哈喽，果库妹给你送福利啦：
<a href="https://taoquan.taobao.com/coupon/unify_apply.htm?sellerId=2186239207&activityId=fa282ab6e48b4c439dd223864059081a">糯言5.00元商品优惠劵</a>
<a href="https://taoquan.taobao.com/coupon/unify_apply.htm?sellerId=2186239207&activityId=fc5cec52fd2646f5a4135c365fd49d54">糯言10.00元商品优惠劵</a>''',
    u'果库商城': u'''Hi，等你很久啦~
开心的事要分享，福利也要“分享”哦！
请把这篇<a href="https://guoku.me">果库 X Fighting Pod 首发丨工位虽小，五脏俱全</a>文章，分享到朋友圈，
然后截图发到微信后台，我们将在10月16日抽出4位朋友送出巧克力，让你和我们一起甜到心里~'''
}

log = getLogger('django')


def regex(content, pattern):
    p = re.compile(pattern)
    return p.search(content.decode('utf-8'))


def handle_reply(raw_content):
    raw_content = raw_content.lower()
    content = raw_content.decode('utf-8')

    log.info(content)

    if content == u'精选':
        _refresh_datetime = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        entities = Selection_Entity.objects.published().filter(pub_time__lte=_refresh_datetime)
        return [row.entity for row in entities[:5]]
    elif content == u'热门':
        popular_list = Entity_Like.objects.popular_random()
        entities = Entity.objects.filter(id__in=popular_list)
        return entities[:5]
    elif content in auto_replies:
        return auto_replies[content]
    elif RobotDic.objects.filter(keyword=raw_content).count() == 1:
        return RobotDic.objects.get(keyword=raw_content)
    else:
        sqs = SearchQuerySet()
        results = sqs.auto_query(content).models(Entity).order_by('-like_count')
        res = []
        for row in results:
            if Entity.objects.filter(pk=row.pk).exists():
                res.append(Entity.objects.get(pk=row.pk))
            if len(res) >= 10:
                break
        return res


def handle_event(content):
    items = []
    if content['EventKey'] == "V1001_SELECTION":
        _refresh_datetime = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        entities = Selection_Entity.objects.published().filter(pub_time__lte=_refresh_datetime)

        for row in entities[:5]:
            items.append(row.entity)
    elif content['EventKey'] == "V1002_POPULAR":
        popular_list = Entity_Like.objects.popular_random()
        entities = Entity.objects.filter(id__in=popular_list)
        items = entities[:5]
    elif content['EventKey'] == "V2001_USER_LIKE":
        open_id = content['FromUserName']
        try:
            token = Token.objects.get(open_id=open_id)
        except Token.DoesNotExist, e:
            log.info(e)
            return None

        el = Entity_Like.objects.filter(user=token.user)
        for row in el[:5]:
            items.append(row.entity)

    return items
