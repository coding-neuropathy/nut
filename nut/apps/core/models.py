from django.db import models
from django.contrib.auth.models import AbstractBaseUser
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _
from django.utils.log import getLogger
from django.conf import settings

from apps.core.extend.list_field import ListObjectField
from apps.core.manager.account import GKUserManager
from apps.core.manager.entity import EntityManager

log = getLogger('django')
image_host = getattr(settings, 'IMAGE_HOST', None)

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

class GKUser(AbstractBaseUser, BaseModel):
    (remove, blocked, active) = (-1, 0, 1)
    USER_STATUS_CHOICES = [
        (active, _("active")),
        (blocked, _("blocked")),
        (remove, _("remove")),
    ]
    email = models.EmailField(max_length=255, unique=True)
    # is_active = models.BooleanField(_('active'), default=True)
    is_active = models.IntegerField(choices=USER_STATUS_CHOICES, default=active)
    is_admin = models.BooleanField(default=False)
    date_joined = models.DateTimeField(_('date joined'), default=timezone.now())

    objects = GKUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    class Meta:
        ordering = ['date_joined']

    def __unicode__(self):
        return self.email

    @property
    def is_staff(self):
        return self.is_admin

    @property
    def is_verified(self):
        return self.profile.email_verified

    @property
    def likes(self):
        return self.likes.count()

    @property
    def create_entity_count(self):
        return self.entity.count()

    @property
    def post_note_count(self):
        return self.note.count()

    @property
    def post_note_comment_count(self):
        return self.note_comment.count()

    def set_admin(self):
        self.is_admin = True
        self.save()



class User_Profile(BaseModel):
    Man = u'M'
    Woman = u'F'
    Other = u'O'
    GENDER_CHOICES = (
        (Man, _('man')),
        (Woman,  _('woman')),
        (Other,  _('other')),
    )

    user = models.OneToOneField(GKUser, related_name='profile')
    nickname = models.CharField(max_length = 64, db_index = True)
    location = models.CharField(max_length = 32, null = True, default = _('beijing'))
    city = models.CharField(max_length = 32, null = True, default = _('chaoyang'))
    gender = models.CharField(max_length = 2, choices = GENDER_CHOICES, default = Other)
    bio = models.CharField(max_length = 1024, null = True, blank = True)
    website = models.CharField(max_length = 1024, null = True, blank = True)
    avatar = models.CharField(max_length=255)
    email_verified = models.BooleanField(default = False)

    def __unicode__(self):
        return self.nickname

    @property
    def avatar_url(self):
        return "%s%s" % (image_host, self.avatar)


class Banner(BaseModel):
    content_type = models.CharField(max_length = 64, null = False)
    key = models.CharField(max_length = 1024)
    image = models.CharField(max_length = 64, null = False)
    created_time = models.DateTimeField(auto_now_add = True, editable=False, db_index = True)
    updated_time = models.DateTimeField(auto_now = True, editable=False, db_index = True)

    class Meta:
        ordering = ['-created_time']

    @property
    def url(self):
        if 'http://' in self.key:
            return self.key
        _url = "guoku://%s/%s" % (self.content_type, self.key)
        return _url

    @property
    def image_url(self):
        return "%s%s" % (image_host, self.image)


class Show_Banner(BaseModel):
    banner = models.ForeignKey(Banner, related_name='show')
    created_time = models.DateTimeField(auto_now_add=True, editable=False, db_index=True)

    class Meta:
        ordering = ['id']
    

class Category(BaseModel):
    title = models.CharField(max_length = 128, db_index = True)
    status = models.BooleanField(default = True, db_index = True)

    class Meta:
        ordering = ['id']

    def __unicode__(self):
        return self.title


class Sub_Category(BaseModel):
    group = models.ForeignKey(Category)
    title = models.CharField(max_length = 128, db_index = True)
    icon = models.CharField(max_length = 64, db_index = True, null = True, default = None)
    status = models.BooleanField(default = True, db_index = True)

    class Meta:
        ordering = ['id']

    def get_absolute_url(self):
        return "/c/%s" % self.id

    def __unicode__(self):
        return self.title


class Entity(BaseModel):

    (remove, freeze, new, selection) = (-2, -1, 0, 1)
    ENTITY_STATUS_CHOICES = [
        (selection, _("selection")),
        (new, _("new")),
        (freeze, _("freeze")),
        (remove, _("remove")),
    ]

    NO_SELECTION_ENTITY_STATUS_CHOICES = [
        (new, _("new")),
        (freeze, _("freeze")),
        (remove, _("remove")),
    ]

    user = models.ForeignKey(GKUser, related_name='entity', null=True)
    entity_hash = models.CharField(max_length=32, unique=True, db_index=True)
    category = models.ForeignKey(Sub_Category, related_name='category', db_index=True)
    brand = models.CharField(max_length=256, default='')
    title = models.CharField(max_length=256, default='')
    intro = models.TextField(default='')
    rate = models.DecimalField(max_digits=3, decimal_places=2, default=1.0)
    price = models.DecimalField(max_digits=20, decimal_places=2, default=0, db_index=True)
    mark = models.IntegerField(default=0, db_index=True)
    images = ListObjectField()
    created_time = models.DateTimeField(auto_now_add=True, db_index=True)
    updated_time = models.DateTimeField(auto_now=True, db_index=True)
    status = models.IntegerField(choices=ENTITY_STATUS_CHOICES, default=new)

    objects = EntityManager()

    class Meta:
        ordering = ['-created_time']

    @property
    def chief_image(self):
        # log.info("images, %s" % self.images)
        if len(self.images) > 0:
            return self.images[0]

    @property
    def detail_images(self):
        if len(self.images) > 1:
            return self.images[1:]
        return []

    @property
    def like_count(self):
        return self.likes.count()

    @property
    def note_count(self):
        return self.notes.count()

    @property
    def has_top_note(self):
        if self.notes.filter(status = 1):
            return True
        return False

    def get_absolute_url(self):
        return "/detail/%s" % self.entity_hash

    def __unicode__(self):
        return self.title


class Buy_Link(BaseModel):
    entity = models.ForeignKey(Entity, related_name='buylinks')
    origin_id = models.CharField(max_length=100)
    origin_source = models.CharField(max_length=255)
    link = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=20, decimal_places=2, default=0)
    volume = models.IntegerField(default=0)
    rank = models.IntegerField(default=0)

    def __unicode__(self):
        return self.link


class Entity_Like(models.Model):
    entity = models.ForeignKey(Entity, related_name='likes')
    user = models.ForeignKey(GKUser, related_name='likes')
    created_time = models.DateTimeField(auto_now_add = True, db_index=True)

    class Meta:
        ordering = ['-created_time']
        unique_together = ('entity', 'user')


class Note(models.Model):

    (remove, normal, top) = ( -1, 0, 1)
    NOTE_STATUS_CHOICES = [
        (top, _("top")),
        (normal, _("normal")),
        (remove, _("remove")),
    ]
    user = models.ForeignKey(GKUser, related_name='note')
    entity = models.ForeignKey(Entity, related_name="notes")
    note = models.TextField(null = True)
    post_time = models.DateTimeField(auto_created=True, editable=False, db_index = True)
    updated_time = models.DateTimeField(auto_now = True, db_index = True)
    status = models.IntegerField(choices=NOTE_STATUS_CHOICES, default=normal)

    class Meta:
        ordering = ['-post_time']
        # unique_together = ('entity', 'user')

    def __unicode__(self):
        return self.note

    @property
    def is_top(self):
        if self.status == self.top:
            return True
        return False

    @property
    def comment_count(self):
        return self.comments.count()


class Note_Comment(models.Model):
    note = models.ForeignKey(Note, related_name='comments')
    user = models.ForeignKey(GKUser, related_name='note_comment')
    content = models.TextField(null = False)
    # replied_comment = models.IntegerField(default = None, null = True)
    # replied_user = models.ForeignKey(GKUser, null = True)
    post_time = models.DateTimeField(auto_now = True, db_index = True)
    # updated_time = models.DateTimeField(auto_now = True, db_index = True)

    class Meta:
        ordering = ['-post_time']


    def __unicode__(self):
        return self.content


class Tag(models.Model):
    tag = models.CharField(max_length = 128, null = False, unique = True, db_index = True)
    tag_hash = models.CharField(max_length = 32, unique = True, db_index = True)
    status = models.IntegerField(default = 0, db_index = True)
    creator = models.ForeignKey(GKUser)
    created_time = models.DateTimeField(auto_now_add = True, db_index=True)
    updated_time = models.DateTimeField(auto_now = True, db_index = True)


    def get_absolute_url(self):

        return "/t/%s" % self.tag_hash

    class Meta:
        ordering = ['-created_time']


class User_Follow(models.Model):
    follower = models.ForeignKey(GKUser, related_name = "followings")
    followee = models.ForeignKey(GKUser, related_name = "fans")
    followed_time = models.DateTimeField(auto_now_add = True, db_index = True)

    class Meta:
        ordering = ['-followed_time']
        unique_together = ("follower", "followee")


class Sina_Token(models.Model):
    user = models.OneToOneField(GKUser, related_name='weibo')
    sina_id = models.CharField(max_length = 64, null = True, db_index = True)
    screen_name = models.CharField(max_length = 64, null = True, db_index = True)
    access_token = models.CharField(max_length = 255, null = True, db_index = True)
    create_time = models.DateTimeField(auto_now_add = True)
    expires_in = models.PositiveIntegerField(default = 0)
    updated_time = models.DateTimeField(auto_now = True, null = True)

    def __unicode__(self):
        return self.screen_name


class Taobao_Token(models.Model):
    user = models.OneToOneField(GKUser, related_name='taobao')
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