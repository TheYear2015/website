# -*- coding: utf-8 -*-

from tornado.web import HTTPError
from scorpiom.base.handler import BaseHandler
from tornado.web import RequestHandler
import re
import time
import scorpiom.base.context as context

class IndexHandler(RequestHandler):
    def get(self, slug=""):
        self.render("index.html", **self._context)

    def prepare(self):
        self._prepare_context()
        self._remove_slash()

    def _prepare_context(self):
        self._context = context.Context()
        self._context.prepare_time()
        self._context.prepare_request(self.request)

    def _remove_slash(self):
        if self.request.method == "GET":
            if _remove_slash_re.match(self.request.path):
                # remove trail slash in path
                uri = self.request.path.rstrip("/")
                if self.request.query:
                    uri += "?" + self.request.query

                self.redirect(uri)

_remove_slash_re = re.compile(".+/$")

handlers = [(r"/", IndexHandler),
            ]
