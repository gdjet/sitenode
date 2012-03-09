# -*- coding: utf-8 -*-
#!/usr/bin/env python
"""
    Custom Django fields for SiteNode

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
from django.core.validators import RegexValidator
import re
from django.db.models.fields import SlugField
from django.forms import SlugField as SlugFormField
slug_re = re.compile(r'^[-\w/]+$')
validate_path_slug = RegexValidator(slug_re, u"Enter a valid 'slug' consisting of letters, numbers, underscores, slashes, or hyphens.", 'invalid')

class PathSlugFormField(SlugFormField):
    default_validators = [validate_path_slug]

class PathSlugField(SlugField):
    def formfield(self, **kwargs):
        defaults = {'form_class': PathSlugFormField}
        defaults.update(kwargs)
        return super(SlugField, self).formfield(**defaults)


