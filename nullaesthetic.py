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

import hashlib
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

def md5(text, amount=3):
    m = hashlib.md5()
    m.update(text)
    return '#%s' % (m.hexdigest()[:amount].lower())

verbtrans = {'a':'@', 'e':'3', 'i':'1', 'o':'0', 'u':u'\/'}
jittertrans = {'a':'@', 'e':'3', 'i':'1', 'l':'|', 'o':'0', 'u':u'\/'}
jitter_probability = 0.4

def double_vowel_1337(twochars):
    vowels = twochars.group(0)
    print vowels
    return "%s%s" % (vowels[0], verbtrans.get(vowels[1], vowels[1]))

def trans_double_vowel_1337(text):
    return re.sub(r'[aeiou][aeiou]', double_vowel_1337, text)

def char_1337(char):
    if random.random() < jitter_probability:
        return jittertrans.get(char, char)
    else:
        return char

def random_hex_color():
    return  ('#%02X%02X%02X' % (random.randint(0, 256),
                               random.randint(0, 256),
                               random.randint(0, 256))).lower()

def color_range():
    colours = [random_hex_color(), random_hex_color()]
    colours.sort()
    return 'colored from %s to %s' % (colours[0], colours[1])

def jitter(text):
    jittered =  ''.join([char_1337(char) for char in text])
    return trans_double_vowel_1337(jittered)

def verb():
    return choose_one_of(models.AestheticOptions.get_option('verb'))

def style():
    return choose_one_of(models.AestheticOptions.get_option('style'))

def a_format():
    return choose_one_of(models.AestheticOptions.get_option('format'))

def connected(followed):
    conn = choose_one_of(models.AestheticOptions.get_option('connected'))
    if followed[0] in 'aeiou':
        conn = conn + 'n'
    return conn

def adjective():
    return choose_one_of(models.AestheticOptions.get_option('adjective'))

def thing():
    return choose_one_of(models.AestheticOptions.get_option('thing'))

#def tags():
#    return maybe_choose_one_of(models.AestheticOptions.get_option('tag'))

def amount():
    return str(random.randint(1, 50))

def aesthetic_description():
    adj = adjective()
    items = [verb(), amount(), style(), a_format(), connected(adj), adj,
             thing(), color_range()]
    description = " ".join(filter(bool, items)) + "."
    return "%s %s" % (md5(description), description)

def capitalize_start(string):
    words = string.split()
    words[0] = words[0].capitalize()
    return " ".join(words)

def null_aesthetic():
    '''An aesthetic'''
    description = aesthetic_description()
    return capitalize_start(description)
