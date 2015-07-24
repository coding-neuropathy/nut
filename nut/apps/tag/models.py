from django.db import models, connection
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes import generic
from django.conf import settings
from apps.core.models import BaseModel

from django.db.models import Count
from django.core.cache import cache

from django.utils.log import getLogger
# from apps.core.manager import dictfetchall
import random

log = getLogger('django')

def dictfetchall(cursor):
    desc = cursor.description
    return [
        dict(zip([col[0] for col in desc], row))
        for row in cursor.fetchall()
    ]

class ContentTagQuerySet(models.query.QuerySet):
    def user_tags(self, user):
        return self.filter(user=user).values('tag').annotate(tcount=Count('tag')).order_by('-tcount')
        # self.raw()
        # return

    def popular(self):
        return self.annotate(tcount=Count('tag')).order_by('-tcount')[:300]


class ContentTagManager(models.Manager):

    def popular_entity_tag(self):
        key = 'new_entity_tag_popular_all'
        res = cache.get(key)
        if res:
            return list(res)

        res = self.get_queryset().popular()
        #TODO : make the timeout to 1 day
        cache.set(key, res , timeout=86400)
        return res

    def popular_random(self, tag_count=15):
        key = 'new_entity_tag_popular_random_%s' % tag_count
        res = cache.get(key)
        log.info(res)
        if res:
            return res

        popularTags = self.popular_entity_tag()
        if popularTags.count  < tag_count:
            res =  popularTags;
        else:
            res =  random.sample(popularTags, tag_count)
        #TODO: make the timeout to 15 minute
        cache.set(key, res , timeout=900)

        return res

    def get_queryset(self):
        return ContentTagQuerySet(self.model, using = self._db)

    def user_tags(self, user):

        obj = self.raw('SELECT id, tag_id, COUNT(tag_id) AS entity_count \
                        FROM tag_content_tags WHERE creator_id=%s AND target_content_type_id = 24 GROUP BY tag_id ORDER BY entity_count DESC' % user)

        res = list()
        for row in obj:
            data = {
                'tag_id': row.tag_id,
                'tag': row.tag.name,
                'tag_hash': row.tag.hash,
                'entity_count': row.entity_count,
            }
            # print  dict
            res.append(data)
            # print row.tag
        return res

    def tags(self, tag_id_list):
        key_string = ','.join(str(s) for s in tag_id_list)
        obj = self.raw("SELECT id, tag_id, COUNT(tag_id) AS entity_count \
                        FROM tag_content_tags WHERE tag_id IN (%s) AND target_content_type_id = 24 GROUP BY tag_id ORDER BY entity_count DESC" % key_string)
        # c = connection.cursor()
        # sql = "SELECT tag_id, core_tag.tag, core_tag.tag_hash, count(tag_id) as entity_count \
        #           from core_entity_tag join core_tag on tag_id = core_tag.id \
        #            where tag_id in (%s) group by tag_id ORDER BY entity_count DESC" % key_string
        #
        # # log.info(sql)
        # c.execute(sql)
        # # try:
        # #     c.execute(sql)
        # # finally:
        # #     c.close()
        # res = dictfetchall(c)
        res = list()
        for row in obj:
            data = {
                'tag_id': row.tag_id,
                'tag': row.tag.name,
                'tag_hash': row.tag.hash,
                'entity_count': row.entity_count,
            }
            res.append(data)

        return res

class Tags(BaseModel):
    name = models.CharField(max_length=100, unique=True, db_index=True)
    hash = models.CharField(max_length=32, unique=True, db_index=True)
    status = models.BooleanField(default=False)
    image = models.URLField(max_length=255, null=True)

    class Meta:
        ordering = ["-id"]

    def __unicode__(self):
        return self.name

    @property
    def tag_hash(self):
        return self.hash[:8]

    def get_absolute_url(self):
        return "/tag/%s/" % self.name


class Content_Tags(BaseModel):
    tag = models.ForeignKey(Tags)
    creator = models.ForeignKey(settings.AUTH_USER_MODEL)

    target_content_type = models.ForeignKey(ContentType, related_name='tag_target', blank=True, null=True)
    target_object_id = models.BigIntegerField(null=True)
    target = generic.GenericForeignKey('target_content_type', 'target_object_id')

    created_datetime = models.DateTimeField(auto_now_add=True, editable=True, db_index=True)
    # created_datetime = models.DateTimeField(db_index=True)

    objects = ContentTagManager()

    class Meta:
        unique_together = ('tag', 'creator', 'target_content_type', 'target_object_id')
        ordering = ["-created_datetime"]


__author__ = 'xiejiaxin'
