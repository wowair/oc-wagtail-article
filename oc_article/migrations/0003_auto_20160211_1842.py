# -*- coding: utf-8 -*-
# Generated by Django 1.9.1 on 2016-02-11 18:42
from __future__ import unicode_literals

from django.db import migrations
import django.db.models.deletion
import modelcluster.fields


class Migration(migrations.Migration):

    dependencies = [
        ('oc_article', '0002_auto_20160211_1548'),
    ]

    operations = [
        migrations.AlterField(
            model_name='articlepagetag',
            name='content_object',
            field=modelcluster.fields.ParentalKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='oc_article_articlepagetag_taggeditems', to='oc_article.ArticlePage'),
        ),
        migrations.AlterField(
            model_name='blockarticlepagetag',
            name='content_object',
            field=modelcluster.fields.ParentalKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='oc_article_blockarticlepagetag_taggeditems', to='oc_article.BlockArticlePage'),
        ),
    ]
