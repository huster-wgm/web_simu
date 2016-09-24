from django.db import models

from wagtail.wagtailsearch import index
from wagtail.wagtailcore import blocks
from wagtail.wagtailcore.models import Page
from wagtail.wagtailcore.fields import RichTextField
from wagtail.wagtailcore.fields import StreamField
from wagtail.wagtailadmin.edit_handlers import FieldPanel, StreamFieldPanel
from wagtail.wagtailimages.blocks import ImageChooserBlock
from wagtail.wagtailembeds.blocks import EmbedBlock
from modelcluster.fields import ParentalKey
from modelcluster.contrib.taggit import ClusterTaggableManager
from taggit.models import TaggedItemBase

class PageTag(TaggedItemBase):
    content_object = ParentalKey('blog.Post', related_name='tagged_items')


class Post(Page):
    tags = ClusterTaggableManager(through=PageTag, blank=True)


    intro = models.CharField(max_length=250)
    body = StreamField([
        ('heading', blocks.CharBlock(classname="full title")),
        ('paragraph', blocks.RichTextBlock()),
        ('image', ImageChooserBlock()),
        ('Html_code',blocks.RawHTMLBlock()),
        ('Embed',EmbedBlock())
    ])

    search_fields = Page.search_fields + [
        index.SearchField('intro'),
        index.SearchField('body'),
    ]

    content_panels = Page.content_panels + [
        FieldPanel('tags'),
        FieldPanel('intro'),
        StreamFieldPanel('body'),
    ]


class HomePage(Page):
    intro = models.CharField(max_length=250)

    content_panels = Page.content_panels + [
        FieldPanel('intro'),
    ]