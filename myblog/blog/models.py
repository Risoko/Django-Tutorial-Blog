from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone
from django.urls import reverse
from django.utils.translation import gettext_lazy as _

from taggit.managers import TaggableManager


class PublishManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(status='published')


class Post(models.Model):
    STATUS_CHOICES = (
        ('draft', 'Draft'),
        ('published', 'Published')
    )
    author = models.ForeignKey(
        to=User,
        on_delete=models.CASCADE,
        verbose_name=_('author')
    )
    title = models.CharField(
        verbose_name=_("title"),
        max_length=250
    )
    slug = models.SlugField(
        verbose_name=_("slug"),
        max_length=250,
        unique_for_date='publish'
    )
    body = models.TextField(
        verbose_name=_('body')
    )
    publish = models.DateTimeField(
        verbose_name=_('publish'),
        default=timezone.now
    )
    created = models.DateTimeField(
        verbose_name=_('created'),
        auto_now_add=True
    )
    updated = models.DateTimeField(
        verbose_name=_('updated'),
        auto_now_add=True
    )
    status = models.CharField(
        verbose_name=_('status'),
        max_length=10,
        choices=STATUS_CHOICES,
        default='draft',
    )
    objects = models.Manager()
    published = PublishManager()
    tags = TaggableManager()
    
    class Meta:
        verbose_name = 'Post'
        verbose_name_plural = 'Posts'
        ordering = ('-publish',)

    def get_absolute_url(self):
        return reverse(
            viewname='blog:post_detail',
            args=[
                self.publish.year,
                self.publish.strftime('%m'),
                self.publish.strftime('%d'),
                self.slug
            ]
        )

    def __str__(self):
        return self.title


class Comment(models.Model): 
    post = models.ForeignKey(Post,
                             on_delete=models.CASCADE,
                             related_name='comments')
    name = models.CharField(max_length=80) 
    email = models.EmailField() 
    body = models.TextField() 
    created = models.DateTimeField(auto_now_add=True) 
    updated = models.DateTimeField(auto_now=True) 
    active = models.BooleanField(default=True) 
 
    class Meta: 
        ordering = ('created',) 
 
    def __str__(self): 
        return f'Comment by {self.name} on {self.post}'
