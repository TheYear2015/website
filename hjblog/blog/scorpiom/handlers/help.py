# -*- coding: utf-8 -*-

from tornado.web import HTTPError
from scorpiom.base.handler import BaseHandler
from tornado.web import RequestHandler

class HelpHandler(RequestHandler):
    def get(self, slug=""):
        if slug == "":
            slug = "about"
        elif slug == "about":
            self.redirect("/help")
            return

        self.render("help.html")


handlers = [(r"/help", HelpHandler),
            (r"/help/([a-z]{2,20})", HelpHandler),
            ]
