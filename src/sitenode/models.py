# -*- coding: utf-8 -*-
#!/usr/bin/env python
"""
    Models for the SiteNode Engine.

@author: g4b

LICENSE AND COPYRIGHT NOTICE:

Copyright (C) 2012 by  Gabor Guzmics, <gab(at)g4b(dot)org>

This program is free software; you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation; version 2 of the License.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.
"""
from django.contrib.auth.models import User
from django.db import models
from gdjet.models.fields import JSONField
from django.utils.safestring import mark_safe
from django.contrib.contenttypes.models import ContentType
from django.utils.html import escape, strip_tags, linebreaks
from django.template.defaultfilters import slugify
from filebrowser.fields import FileBrowseField
from sitenode import fields

try:
    import markdown
except ImportError:
    pass

from sitenode.settings import NODE_SOURCE_TYPES

class Node(models.Model):
    user = models.ForeignKey(User, blank=True, null=True)
    slug = fields.PathSlugField(max_length=250, blank=True, unique=True)
    parent = models.ForeignKey('self', blank=True, null=True,
                               related_name='children',
            help_text='Allows a node to have subnodes. subnodes cannot have\
                subnodes and are assigned to their parent. Think of it as\
                blogentries in a blog, etc.')
    public = models.BooleanField(default=True)
    template = models.CharField(max_length=60, blank=True, null=True)

    date_created = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True)

    title = models.CharField(max_length=180, null=True)
    subtitle = models.CharField(max_length=250, blank=True, null=True)
    image = FileBrowseField("Image", max_length=200, directory="images/", extensions=[".jpg", ".png", ".gif"], blank=True, null=True)
    icon_file = models.ImageField(upload_to='icons', blank=True, null=True)
    content_type = models.ForeignKey(ContentType, editable=False, null=True,)
    options = JSONField(blank=True, null=True)

    def __unicode__(self):
        if self.parent:
            return u'%s > %s' % (self.parent.title, self.title)
        else:
            return u'%s' % self.title

    def save(self, *args, **kwargs):
        if(not self.content_type):
            self.content_type = ContentType.objects.get_for_model(self.__class__)
        if not self.slug:
            self.slug = slugify(self.title.strip('/')[:60])
        if self.parent is not None: # i am a child!
            # check if my parent has a parent. otherwise, i am the child of that!
            if self.parent.parent is not None:
                self.parent = self.parent.parent
            # make sure slug is a subslug.
            if '/' in self.slug:
                subslug = self.slug.split('/')[-1]
            else:
                subslug = self.slug
            full_slug = '%s/%s' % (self.parent.slug, subslug)
            if Node.objects.filter(slug__iexact=full_slug).count() and self.pk is None:
                number = self.parent.children.count()
                while Node.objects.exists(slug__iexact='%s%s' % (full_slug, number)):
                    number += 1
                full_slug = '%s%s' % (full_slug, number)
            self.slug = full_slug
        super(Node, self).save(*args, **kwargs)

    def as_leaf(self):
        """
            gets this object as its leaf.
        """
        content_type = self.content_type
        if (not content_type):
            return self
        model = content_type.model_class()
        return model.objects.get(id=self.id)

    def object_template(self):
        """
            called by inclusion of node children iterations.
            anytime the node system iterates over node children, default is
            to include following template.
        """
        if not self.template:
            return 'site/node_div.html'
        return self.template

class NodeHtml(Node):
    """
        A Node which supports HTML.
    """
    source = models.TextField()
    source_type = models.PositiveIntegerField(default=1, choices=NODE_SOURCE_TYPES)

    def as_html(self):
        if self.source_type == 0:
            return mark_safe(linebreaks(self.source, autoescape=True))
        elif self.source_type == 2:
            try:
                md = markdown.Markdown(#extensions=['wikilinks2',],
                                   #extension_configs=
                                   #     { 'wikilinks2': [
                                   #             ('base_url', self.get_base_path()),
                                   #             ('end_url', '')
                                   #         ],
                                   #     }
                                    )
                # @todo: WikiLinks plugin.
                r = md.convert(self.text,)
                return mark_safe(r)
            except:
                raise NotImplementedError, "MarkDown either not installed or implemented yet."
        # @todo: dynamic binding for other types (and move this to elif==1 then)
        return mark_safe(self.source)

