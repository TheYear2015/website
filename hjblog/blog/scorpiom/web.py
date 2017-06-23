# -*- coding: utf-8 -*-

import tornado
import scorpiom.urls as urls
import os
from scorpiom.base.context import options as _context_op

def options():
    return _context_op

class Application(tornado.web.Application):
    def __init__(self, **settings):
        super(Application, self).__init__(urls.handlers, **settings)
