# -*- coding: utf-8 -*-
# Generated by Django 1.9.1 on 2016-02-10 13:36
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('wowair', '0047_merge'),
        ('oc_article', '0018_auto_20151228_1645'),
    ]

    operations = [       

        migrations.RenameModel('Article','ArticlePage'),
        migrations.RenameModel('ArticleTag','ArticlePageTag'),
        migrations.RenameModel('BlockArticle','BlockArticlePage'),
        migrations.RenameModel('BlockArticleTag','BlockArticlePageTag'),
        migrations.RunSQL(
            "UPDATE django_content_type set model = 'articlepagetag' where model = 'articletag'",
            "UPDATE django_content_type set model = 'articletag' where model = 'articlepagetag'"),
        migrations.RunSQL(
            "UPDATE django_content_type set model = 'blockarticlepagetag' where model = 'blockarticletag'",
            "UPDATE django_content_type set model = 'blockarticletag' where model = 'blockarticlepagetag'"),
        migrations.RunSQL(
            "UPDATE django_content_type set model = 'articlepage' where model = 'article'",
            "UPDATE django_content_type set model = 'article' where model = 'articlepage'"),
        migrations.RunSQL(
            "UPDATE django_content_type set model = 'blockarticlepage' where model = 'blockarticle'",
            "UPDATE django_content_type set model = 'blockarticle' where model = 'blockarticlepage'"),
    ]
