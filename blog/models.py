from django.db import models
from django.utils import timezone
from django.contrib.syndication.views import Feed
from django.core.urlresolvers import reverse


class Tag(models.Model):
    name = models.CharField(max_length=50)
        
    def __str__(self):
        return u'%s' % self.name
        
        
class Post(models.Model):
    author = models.ForeignKey('auth.User')
    title = models.CharField(max_length=200)
    text = models.TextField()
    created_date = models.DateTimeField(default=timezone.now)
    published_date = models.DateTimeField(blank=True, null=True)
    tags = models.ManyToManyField(Tag)

    class Meta:
        ordering = ('-created_date',)

    def publish(self):
        self.published_date = timezone.now()
        self.save()

    def __str__(self):
        return self.title


class NewPostFeed(Feed):
    title = "like a spruce on a windowsill"
    link = '/blog/feed/'
    description = 'Последние новости из Батумской квартиры'

    def items(self):
        return Post.objects.all()

    def item_title(self, item):
        return item.title
    
    def item_description(self, item):
        return item.text[:160]

    def item_link(self, item):
        return reverse('post_detail', args=[item.pk])
