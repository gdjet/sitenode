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
from django.utils.safestring import mark_safe
from django.contrib.contenttypes.models import ContentType
from django.utils.html import escape, strip_tags, linebreaks
from django.template.defaultfilters import slugify
from sitenode import fields
#from sitenode.jsonstore import JSONField
from sitenode.settings import NODE_SOURCE_TYPES, NODE_DIV_TEMPLATE, SITENODE_BASE_URL
import logging
try:
    import markdown
except ImportError:
    logging.warning("Markdown not installed.")
    markdown = False

NODE_SOURCE_TYPES = NODE_SOURCE_TYPES or \
    ((0, 'Plain Text'), (1, 'HTML'), (2, 'MarkDown'),)

class Node(models.Model):
    user = models.ForeignKey(User, blank=True, null=True)
    slug = fields.PathSlugField(max_length=250, blank=True, unique=True, validators=[fields.validate_path_slug])
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
    image = fields.FileBrowseField("Image", max_length=200, directory="images/", 
                            extensions=[".jpg", ".png", ".gif"], blank=True, null=True)
    icon_file = models.ImageField(upload_to='icons', blank=True, null=True)
    content_type = models.ForeignKey(ContentType, editable=False, null=True,)
    options = models.TextField(blank=True, null=True)
    
    def get_absolute_url(self):
        return u'%s%s' % (SITENODE_BASE_URL, self.slug)

    def __unicode__(self):
        if self.parent:
            return u'%s > %s (%s)' % (self.parent.title, self.title, self.slug)
        else:
            return u'%s (%s)' % (self.title, self.slug)

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
                while Node.objects.filter(slug__iexact='%s%s' % (full_slug, number)).exists():
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

    def as_html(self):
        return mark_safe('<!-- No Entry -->')

    def object_template(self):
        """
            called by inclusion of node children iterations.
            anytime the node system iterates over node children, default is
            to include following template.
        """
        if not self.template:
            return NODE_DIV_TEMPLATE or 'site/node_div.html'
        return self.template

    def has_content(self):
        return False
    
class NodeAlias(Node):
    redirect = models.ForeignKey(Node, related_name='redirects')
    
    def as_leaf(self):
        if self.redirect:
            return self.redirect.as_leaf()
        else:
            return Node.as_leaf(self)

class NodeHtml(Node):
    """
        A Node which supports HTML.
    """
    source = models.TextField(blank=True, default='')
    source_type = models.PositiveIntegerField(default=1, choices=NODE_SOURCE_TYPES)

    def as_html(self):
        if self.source_type == 0:
            return mark_safe(linebreaks(self.source, autoescape=True))
        elif self.source_type == 2:
            if markdown is not False:
                md = markdown.Markdown(#extensions=['wikilinks2',],
                                   #extension_configs=
                                   #     { 'wikilinks2': [
                                   #             ('base_url', self.get_base_path()),
                                   #             ('end_url', '')
                                   #         ],
                                   #     }
                                    )
                # @todo: WikiLinks plugin.
                r = md.convert(self.source,)
                return mark_safe(r)
            else:
                return mark_safe('<!-- markdown not installed -->')
        # @todo: dynamic binding for other types (and move this to elif==1 then)
        return mark_safe(self.source)

    def has_content(self):
        if self.source:
            return True
        return False

#class BlogEntry(NodeHtml):
#    pass
