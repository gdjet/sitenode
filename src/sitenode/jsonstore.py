# -*- coding: utf-8 -*-
"""
    JSONStore.
    
    from the gdjet library.
    
    @author: g4b

Copyright (C) 2010 by  Gabor Guzmics, <gab(at)g4b(dot)org>

This program is free software; you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation; version 2 of the License.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

"""

# JSONFIELD
# @author Jasber
# @author g4b
# after http://djangosnippets.org/snippets/1478/
# modified to be serializable.
# modified to understand other formats

from django.db import models
from django.utils import simplejson as json, datetime_safe
from django.http import HttpResponse
from django.utils import simplejson
from django.core.serializers.json import DjangoJSONEncoder
from django.utils.functional import Promise

import datetime
import decimal
from time import mktime, struct_time

class GdjetJSONEncoder(DjangoJSONEncoder):
    """
    JSONEncoder subclass that knows how to encode date/time and decimal types.
    
    g4b: enhanced to understand struct_time,
        and Promise objects
    @todo: file patch report, keep this one up to date.
    
    """
    DATE_FORMAT = "%Y-%m-%d"
    TIME_FORMAT = "%H:%M:%S"

    def default(self, o):
        if isinstance(o, struct_time):
            o = datetime.datetime.fromtimestamp(mktime(o))
            # we go on, super will do the rest.
        if isinstance(o, Promise):
            return unicode(o)
        else:
            return super(GdjetJSONEncoder, self).default(o)

class JSONDict(object):
    """
        @author g4b
        Simple JSON dictionary Object for Responses.
    """
    di = {}
    repr = ''

    def __init__(self, di={}):
        if not self.di:
            self.di = di
        else:
            self.di.update(di)

    def dictify(self, di={}):
        return simplejson.dumps(di, cls=GdjetJSONEncoder,)

    def out(self):
        if not self.repr:
            self.repr = self.dictify(self.di)
        return self.repr

    def __repr__(self):
        return self.out()

    def __unicode__(self):
        return u"%s" % self.out()

    def __str__(self):
        return self.out()

    def add(self, key, value):
        self.di[key] = value
        self.repr = self.dictify(self.di)
        return self

    def delete(self, key):
        if key in self.di.keys():
            del self.di[key]
            self.repr = self.diify(self.di)
        return self

    def get(self, key, default=None):
        if key in self.di.keys():
            return self.di[key]
        return default

class JSONResponse(HttpResponse):
    """
        a http response, which renders itself as json response.
        only dumps json if data is changed from model-based-data
        subclass this with your most used responses.
        
        http_accept_scan: tries to scan the HTTP_ACCEPT for
        application/json and changes content_type to it.
        
        you can either change content_type directly in subclass, 
        or check your request with http_accept_scan to set it right.
        
        by default it will use text/plain for all json answers to be
        compatible with older browsers.
    """
    status_code = 200
    default_content = ''
    default_dict = {}
    content_type = 'text/plain'

    def http_accept_scan(self, request):
        try:
            if 'application/json' in request.META.get('HTTP_ACCEPT', ''):
                self.content_type = 'application/json'
        except:
            pass

    def update(self, content):
        if isinstance(content, dict):
            self.default_content.update(content)

    def __init__(self, content=None, verbose=False, **kwargs):

        if content is None:
            content = self.default_content
        elif isinstance(content, dict):
            c = {}
            c.update(self.default_dict)
            c.update(content)
            content = JSONDict(c).out()
        elif isinstance(content, JSONDict):
            content = content.out()
        if verbose:
            print content

        HttpResponse.__init__(self, content,
                              content_type=self.content_type, **kwargs)

class JSONField(models.TextField):
    """JSONField is a generic textfield that neatly serializes/unserializes
    JSON objects seamlessly"""

    # Used so to_python() is called
    __metaclass__ = models.SubfieldBase
    def __init__(self, *args, **kwargs):
        if 'json_encoder' in kwargs.keys():
            self.json_encoder = kwargs['json_encoder']
            del kwargs['json_encoder']
        else:
            self.json_encoder = GdjetJSONEncoder
        super(JSONField, self).__init__(*args, **kwargs)

    def to_python(self, value):
        """Convert our string value to JSON after we load it from the DB"""

        if value == "":
            return None

        try:
            if isinstance(value, basestring):
                return json.loads(value)
        except ValueError:
            pass

        return value

    def get_prep_value(self, value):
        """Convert our JSON object to a string before we save"""
        if value == "":
            return None
        if isinstance(value, dict) or isinstance(value, list):
            value = json.dumps(value, cls=self.json_encoder)
        return super(JSONField, self).get_prep_value(value)

    def value_to_string(self, obj):
        """ called by the serializer.
        """
        value = self._get_val_from_obj(obj)
        return self.get_db_prep_value(value)

#try:
#    from south.modelsinspector import add_introspection_rules
#    add_introspection_rules([
#    (
#        [JSONField], # Class(es) these apply to
#        [], # Positional arguments (not used)
#        {}, # Keyword arguments.
#    ),
#    ], ["^jsonstore\.JSONField"])
#except ImportError:
#    pass
