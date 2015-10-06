# -*- coding: utf-8 -*-
#!/usr/bin/env python
"""
    URLs for site app

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
from django.conf.urls import *
from django.conf import settings
from django.views.generic.edit import FormView, CreateView
from django.views.generic.base import TemplateView
from sitenode import models
from sitenode import views

urlpatterns = patterns('site.views',
        url(r'^(?P<node_url>[a-zA-Z0-9_\.\-/]+)/$',
                   views.NodesListView.as_view(
                                model=models.Node,
            ), name='nodes'),
        url(r'^$', views.NodesListView.as_view(
                               model=models.Node,
                               node_url=getattr(settings, 'SITENODE_ROOT', '/'),
            ), name='node-root'), # root.
       )
