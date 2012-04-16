# Copyright (C) 2011, 2012 Philter Phactory Ltd.
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

import logging
import random
import re
import string

import models

def maybe(fun, probability=0.5, default=None):
    """Call fun with args if random(0..1) is less than probability."""
    result = default
    if random.random() < probability:
        result = fun()
    return result

def choose_one_of(choices):
    """Choose one of the parameters randomly."""
    return random.choice(choices)

def maybe_choose_one_of(choices, probability=0.5):
    """Choose one of the list or return None."""
    result = None
    if random.random() < probability:
        result = choose_one_of(choices)
    return result

def singular_for(the_string):
    singular = "a"
    if the_string and the_string[0] in "aeiouAEIOU":
        singular = "an"
    return singular

def singular_or_plural_for(the_string):
    result = "some"
    if the_string[-1] != "s":
        result = singular_for(the_string)
    return result

def nice_list(items):
    if len(items) == 1:
        result = items[0]
    elif len(items) == 2:
        result = " and ".join(items)
    else:
        result = "%s and %s " % ( ", ".join(items[:-1]), items[-1])
    return result

def jitter(text):
    for i in len(text):
        if random.random() < 0.1:
            text[i] = upper(text[i])

def verb():
    return choose_one_of(models.AestheticOptions.get_option('verb'))

def style():
    return choose_one_of(models.AestheticOptions.get_option('style'))

def a_format():
    return choose_one_of(models.AestheticOptions.get_option('format'))

def connected():
    return choose_one_of(models.AestheticOptions.get_option('connected'))

def adjective():
    return choose_one_of(models.AestheticOptions.get_option('adjective'))

def thing():
    return choose_one_of(models.AestheticOptions.get_option('thing'))

#def tags():
#    return maybe_choose_one_of(models.AestheticOptions.get_option('tag'))

def aesthetic_description():
    items = [verb(), style(), a_format(), connected(), adjective(), thing()]
    return " ".join(filter(bool, items)) + "."

def capitalize_start(string):
    words = string.split()
    words[0] = words[0].capitalize()
    return " ".join(words)

def null_aesthetic():
    '''An aesthetic'''
    description = aesthetic_description()
    return capitalize_start(description)
