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
import re

from base_prosthetic import Prosthetic

import nullaesthetic
import models

class NullAesthetic(Prosthetic):
    '''A prosthetic that publishes Null Aesthetics conjectures.'''

    @classmethod
    def time_between_runs(cls):
        return 3600 * 4

    def act(self, force=False):
        state = self.get("/1/weavr/state/")
        if not state["awake"]:
            return "Not posting nullaesthetic, asleep"
        
        aesthetic, qr_code = nullaesthetic.null_aesthetic()

        body = u'<img src="%s" />' % (qr_code,)
        
        logging.info("posting nullaesthetic: %s" % aesthetic)
        logging.info("body: %s" % body)
        
        self.post("/1/weavr/post/", {
            "category":"article",
            "title":unicode(aesthetic),
            "body":body, 
            "keywords": "%s nullaesthetic" % state["emotion"],
        })
        
        return unicode(aesthetic)
