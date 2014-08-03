from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _
# from ..models.base import BaseModel


class BaseModel(models.Model):

    class Meta:
        abstract = True

    def toDict(self):
        fields = []
        for f in  self._meta.fields:
            fields.append(f.column)
        d = {}
        for attr in fields:
            d[attr] = "%s" % getattr(self, attr)
        return d


class User_Profile(BaseModel):
    Man = u'M'
    Woman = u'F'
    Other = u'O'
    GENDER_CHOICES = (
        (Man, _('man')),
        (Woman,  _('woman')),
        (Other,  _('other')),
    )

    user = models.OneToOneField(User)
    nickname = models.CharField(max_length = 64, db_index = True, unique = True)
    location = models.CharField(max_length = 32, null = True, default = _('beijing'))
    city = models.CharField(max_length = 32, null = True, default = _('chaoyang'))
    gender = models.CharField(max_length = 2, choices = GENDER_CHOICES, default = Other)
    bio = models.CharField(max_length = 1024, null = True, blank = True)
    website = models.CharField(max_length = 1024, null = True, blank = True)
    avatar = models.CharField(max_length=255)
    email_verified = models.BooleanField(default = False)

    def __unicode__(self):
        return self.nickname


class Entity(BaseModel):

    (freeze, hide, show) = range(0, 3)
    ENTITY_STATUS_CHOICES = [
        (freeze, _("freeze")),
        (hide, _("hide")),
        (show, _("show")),
    ]

    user = models.ForeignKey(User, related_name='entity', null=True)
    entity_hash = models.CharField(max_length=32, unique=True, db_index=True)
    # creator_id = models.IntegerField(default=None, null=True, db_index=True)
    # category = models.ForeignKey(Category)
    # neo_category = models.ForeignKey(Neo_Category)
    brand = models.CharField(max_length=256, default='')
    title = models.CharField(max_length=256, default='')
    intro = models.TextField(default='')
    price = models.DecimalField(max_digits=20, decimal_places=2, default=0, db_index=True)
    # like_count = models.IntegerField(default=0, db_index=True)
    mark = models.IntegerField(default=0, db_index=True)
    chief_image = models.CharField(max_length=64)
    detail_images = models.TextField()
    created_time = models.DateTimeField(auto_now_add=True, db_index=True)
    updated_time = models.DateTimeField(auto_now=True, db_index=True)
    # novus_time = models.DateTimeField(db_index=True)
    status = models.IntegerField(choices=ENTITY_STATUS_CHOICES, default=0)
    # rank_score = models.IntegerField( default=0)

    # objects = EntityManager()

    @property
    def like_count(self):
        return self.likes.count()

    class Meta:
        ordering = ['-updated_time']

    def get_absolute_url(self):
        return "/detail/%s" % self.entity_hash

    def __unicode__(self):
        return self.title


class BuyLink(BaseModel):
    entity = models.ForeignKey(Entity, related_name='buylinks')
    origin_id = models.CharField(max_length=100)
    origin_source = models.CharField(max_length=255)
    link = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=20, decimal_places=2, default=0)
    volume = models.IntegerField(default=0)
    rank = models.IntegerField(default=0)

    def __unicode__(self):
        return self.link


class EntityLike(models.Model):
    entity = models.ForeignKey(Entity, related_name='likes')
    user = models.ForeignKey(User, related_name='likes')
    created_time = models.DateTimeField(auto_now_add = True, db_index=True)

    class Meta:
        ordering = ['-created_time']
        unique_together = ('entity', 'user')

class Note(models.Model):
    user = models.ForeignKey(User, related_name='note')
    entity = models.ForeignKey(Entity, related_name="notes")
    note = models.TextField(null = True)
    score = models.IntegerField(db_index = True, default = 0)
    figure = models.CharField(max_length = 256, null = False, default = '')
    post_time = models.DateTimeField(null = True, db_index = True)
    updated_time = models.DateTimeField(auto_now = True, db_index = True)

    class Meta:
        ordering = ['-post_time']
        unique_together = ('entity', 'user')

    def __unicode__(self):
        return self.note


class User_Follow(models.Model):
    follower = models.ForeignKey(User, related_name = "followings")
    followee = models.ForeignKey(User, related_name = "fans")
    followed_time = models.DateTimeField(auto_now_add = True, db_index = True)

    class Meta:
        ordering = ['-followed_time']
        unique_together = ("follower", "followee")

class Sina_Token(models.Model):
    user = models.OneToOneField(User, related_name='weibo')
    sina_id = models.CharField(max_length = 64, null = True, db_index = True)
    screen_name = models.CharField(max_length = 64, null = True, db_index = True)
    access_token = models.CharField(max_length = 255, null = True, db_index = True)
    create_time = models.DateTimeField(auto_now_add = True)
    expires_in = models.PositiveIntegerField(default = 0)
    updated_time = models.DateTimeField(auto_now = True, null = True)

    def __unicode__(self):
        return self.screen_name

class Taobao_Token(models.Model):
    user = models.OneToOneField(User, related_name='taobao')
    taobao_id = models.CharField(max_length = 64, null = True, db_index = True)
    screen_name = models.CharField(max_length = 64, null = True, db_index = True)
    access_token = models.CharField(max_length = 255, null = True, db_index = True)
    refresh_token = models.CharField(max_length = 255, null = True, db_index = True)
    create_time = models.DateTimeField(auto_now_add = True)
    expires_in = models.PositiveIntegerField(default = 0)
    re_expires_in = models.PositiveIntegerField(default = 0)
    updated_time = models.DateTimeField(auto_now = True, null = True)

    def __unicode__(self):
        return self.screen_name

__author__ = 'edison7500'