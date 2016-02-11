from django.contrib.auth.models import User
from django.db import models
from django.utils.translation import ugettext_lazy as _
from django import forms

from wagtail.wagtailcore.models import Page
from wagtail.wagtailcore import blocks
from wagtail.wagtailcore.fields import RichTextField, StreamField
from wagtail.wagtailimages.blocks import ImageChooserBlock
from wagtail.wagtailimages.edit_handlers import ImageChooserPanel
from wagtail.wagtailembeds.blocks import EmbedBlock
from wagtail.wagtailadmin.edit_handlers import FieldPanel, StreamFieldPanel, MultiFieldPanel
from wagtail.wagtailsnippets.edit_handlers import SnippetChooserPanel
from wagtail.wagtailsnippets.models import register_snippet
from wagtail.wagtailsearch import index


from oc_core.panels import ColorFieldPanel

from taggit.models import TaggedItemBase
from modelcluster.fields import ParentalKey
from modelcluster.tags import ClusterTaggableManager

from .blocks import CommonEditingBlock


class ArticlePageTag(TaggedItemBase):
    content_object = ParentalKey('ArticlePage', null=True, blank=True, related_name="%(app_label)s_%(class)s_taggeditems")


class BlockArticlePageTag(TaggedItemBase):
    content_object = ParentalKey('BlockArticlePage', null=True, blank=True, related_name="%(app_label)s_%(class)s_taggeditems")


class Category(models.Model):
    title = models.CharField(max_length=255, db_index=True, verbose_name=_('Title'))
    slug = models.SlugField(verbose_name=_('Slug'), max_length=255, blank=True, null=True)
    color = models.CharField(max_length=255)

    panels = [
        FieldPanel('title', classname="full title"),
        FieldPanel('slug', classname="col6"),
        ColorFieldPanel('color', classname="col6 colorpicker-field"),
    ]

    def get_children(self):
        return 

    class Meta:
        verbose_name = _('Category')
        verbose_name_plural = _('Categories')

    def __unicode__(self):
        return u"%s" % self.title

register_snippet(Category)

class ArticleMixin(models.Model):
    author = models.ForeignKey(User, null=True, blank=True, on_delete=models.SET_NULL)
    date = models.DateField(null=True, blank=True)
    category = models.ForeignKey('Category', null=True, blank=True, on_delete=models.SET_NULL)
    excerpt = RichTextField(blank=True, verbose_name=_('Excerpt'))
    subtitle = models.CharField(max_length=255, null=True, blank=True)
    styles_override = models.TextField(null=True, blank=True)
    header_image = models.ForeignKey(
        'wagtailimages.Image',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+'
    )

    class Meta:
        abstract = True

BASE_ARTICLE_CONTENT_PANELS = [
    FieldPanel('title'),
    FieldPanel('subtitle'),
    MultiFieldPanel([
        FieldPanel('author', classname="col6"),
        FieldPanel('date', classname="col6"),
    ], "Author and date"),
    SnippetChooserPanel('category', Category),
    FieldPanel('excerpt'),
    ImageChooserPanel('header_image'),
]


class ArticlePage(Page, ArticleMixin):
    """
    Basic article with a rich text editor for body.
    """
    tags = ClusterTaggableManager(through=ArticlePageTag, blank=True)
    body = RichTextField(blank=True)


ArticlePage.content_panels = BASE_ARTICLE_CONTENT_PANELS + [
    FieldPanel('tags'),
    FieldPanel('body'),
]

ArticlePage.settings_panels = Page.settings_panels + [
    FieldPanel('styles_override', widget=forms.widgets.Textarea({'rows':10})),
]

ArticlePage.search_fields = Page.search_fields + (
    index.SearchField('subtitle'),
    index.SearchField('body'),
)

class BlockArticlePage(Page, ArticleMixin):
    """
    ArticlePage built with multiple types of blocks.
    Blocks can be repeated and/or combined in any way.
    """
    tags = ClusterTaggableManager(through=BlockArticlePageTag, blank=True)
    body = StreamField(CommonEditingBlock())

BlockArticlePage.content_panels = BASE_ARTICLE_CONTENT_PANELS + [
    FieldPanel('tags'),
    StreamFieldPanel('body'),
]

BlockArticlePage.settings_panels = Page.settings_panels + [
    FieldPanel('styles_override'),
]

BlockArticlePage.search_fields = Page.search_fields + (
    index.SearchField('subtitle'),
    index.SearchField('body'),
)