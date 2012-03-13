# -*- coding: utf-8 -*-
#!/usr/bin/env python
"""
    Settings used by sitenode.

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
from django.conf import settings

NODE_SOURCE_TYPES = getattr(settings, 'SITENODE_SOURCE_TYPES', (
        (0, 'Plain Text'),
        (1, 'HTML'),
        (2, 'MarkDown'),
        ))

NODE_LIST_TEMPLATE = getattr(settings, 'SITENODE_LIST_TEMPLATE',
                             'site/node_list.html')

NODE_DIV_TEMPLATE = getattr(settings, 'SITENODE_DIV_TEMPLATE',
                            'site/node_div.html')


