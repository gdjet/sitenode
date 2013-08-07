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
from endless_pagination.views import AjaxListView
from django.shortcuts import get_object_or_404
from sitenode.models import Node, NodeAlias
from sitenode.settings import NODE_LIST_TEMPLATE

class NodesListView(AjaxListView):
    CHILDREN_SORT = '-date_created'
    template_name = NODE_LIST_TEMPLATE or 'site/node_list.html'
    node_url = ''

    def get_queryset(self):
        node_url = self.node_url or self.kwargs.get('node_url', '')
        self.node = get_object_or_404(Node, slug=node_url)
        try:
            alias = NodeAlias.objects.get(pk=self.node.pk)
            self.node = alias.redirect
        except NodeAlias.DoesNotExist:
            pass
        return self.node.children.filter(public=True).order_by(self.CHILDREN_SORT)

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super(NodesListView, self).get_context_data(**kwargs)
        context['node'] = self.node
        return context

    def get_template_names(self):
        try:
            if self.node is not None and self.node.template:
                print "Returning: %s" % self.node.template
                self.template_name = self.node.template
                return '%s' % self.node.template
        finally:
            return super(NodesListView, self).get_template_names()
