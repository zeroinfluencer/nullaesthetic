# Copyright (C) 2012 Philter Phactory Ltd.
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE X
# CONSORTIUM BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN
# ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION
# WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
#
# Except as contained in this notice, the name of Philter Phactory Ltd. shall
# not be used in advertising or otherwise to promote the sale, use or other
# dealings in this Software without prior written authorization from Philter
# Phactory Ltd.

import datetime
import logging
import string

from django.db import models
from google.appengine.api import memcache

class AestheticOptions(models.Model):
    VALID_OPTIONS = (
        ('verb', 'Verb'),
        ('style', 'Style'),
        ('format', 'Format'),
        ('connected', 'Connected'),
        ('adjective', 'Adjective'),
        ('thing', 'Thing'),
    )
    VALID_OPTION_NAMES = tuple([x[0] for x in VALID_OPTIONS])
    cache_key = 'nullaesthetic__AestheticOptions__get_option_%s'
    name = models.CharField(max_length=128, primary_key=True) #, choices=VALID_OPTIONS)
    updated = models.DateTimeField(auto_now=True)
    option_list = models.TextField(help_text=u"Newline-seperated list of option values")

    def save(self, **kwargs):
        options = set([x.strip() for x in string.split(self.option_list, '\n') if x.strip() != ''])
        self.option_list = '\n'.join(options)
        models.Model.save(self, **kwargs)
        memcache.delete(self.cache_key)

    @classmethod
    def get_option(cls, name):
        if not name in cls.VALID_OPTION_NAMES:
            raise ValueError(u"%s is not a valid option" % name)
        cache_key = cls.cache_key % name
        cache_result = memcache.get(cache_key)
        if cache_result:
            return cache_result
        all = list(cls.objects.filter(name=name).order_by('-updated'))
        if not all:
            import data
            result = list(getattr(data, '%s_options' % name, []))
        else:
            result = string.split(all[0].option_list, '\n')
        memcache.set(cls.cache_key, result)
        return result

    @classmethod
    def ensure_defaults(cls):
        import data
        for k in cls.VALID_OPTION_NAMES:
            result = list(getattr(data, '%s_options' % k))
            logging.debug("%s defaults is: %r" % (k, result))
            v = '\n'.join([x.strip() for x in result])
            cls.objects.get_or_create(name=k, defaults={'option_list':v})
