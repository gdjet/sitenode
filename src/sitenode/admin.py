# -*- coding: utf-8 -*-
#!/usr/bin/env python
"""
    Unit Description

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
from django.contrib import admin
from sitenode.models import *
from tinymce.widgets import TinyMCE
from django.core.urlresolvers import reverse

class NodeAdmin(admin.ModelAdmin):
    list_display = ('pk', 'slug', 'title', 'public', 'parent', 'template')
    list_editable = ('title', 'slug', 'parent')

    fieldsets = (
        ('', {
            'fields': ('title', 'subtitle', 'slug', 'image'),
        }),
        ('Advanced', {
            'classes': ('grp-collapse grp-closed',),
            'fields' : ('template', 'icon_file', 'options',),
        }),
        ('Publicity', {
            'classes': ('grp-collapse grp-open',),
            'fields' : ('user', 'public', 'parent'),
        }),
    )

class NodeAliasAdmin(admin.ModelAdmin):
    list_display = ('pk', 'slug', 'title', 'public', 'parent', 'template')
    list_editable = ('title', 'slug', 'parent')

    fieldsets = (
        ('', {
            'fields': ('redirect',),
        }),
        ('Advanced', {
            'classes': ('grp-collapse grp-closed',),
            'fields' : ('title', 'subtitle', 'slug', 'image', 'template', 'icon_file', 'options',),
        }),
        ('Publicity', {
            'classes': ('grp-collapse grp-open',),
            'fields' : ('user', 'public', 'parent'),
        }),
    )


class NodeHtmlTinyMCEAdmin(NodeAdmin):
    list_editable = ('title',)
    fieldsets = (
        ('', {
            'fields': ('title', 'subtitle', 'slug', 'image', 'source'),
        }),
        ('Advanced', {
            'classes': ('grp-collapse grp-closed',),
            'fields' : ('template', 'icon_file', 'options', 'source_type'),
        }),
        ('Publicity', {
            'classes': ('grp-collapse grp-open',),
            'fields' : ('user', 'public', 'parent'),
        }),
    )

    def formfield_for_dbfield(self, db_field, **kwargs):
        if db_field.name == 'source':
            return db_field.formfield(widget=TinyMCE(
                attrs={'cols': 80, 'rows': 30},
                #mce_attrs={'plugin_preview_pageurl': reverse('tinymce-preview', 'NAME')},
                #mce_attrs={'external_link_list_url': reverse('tinymce.views.flatpages_link_list')},
            ))
        return super(NodeHtmlTinyMCEAdmin, self).formfield_for_dbfield(db_field, **kwargs)

admin.site.register(Node, NodeAdmin)
admin.site.register(NodeAlias, NodeAliasAdmin)
admin.site.register(NodeHtml, NodeHtmlTinyMCEAdmin)
