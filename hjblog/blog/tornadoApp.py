# -*- coding: utf-8 -*-

import tornado.ioloop
import tornado.web
import time
import os
import scorpiom.web as web

def make_app():

    op = web.options()

    op.title_suffix = "鉴"
    op.default_title = ""
    
    settings = dict(
        debug=False,
        template_path=os.path.join(os.path.dirname(__file__), "templates"),
        static_path=os.path.join(os.path.dirname(__file__), "static"),
        )
    return web.Application(**settings)

if __name__ == "__main__":
    app = make_app()
    app.listen(8888)
    tornado.ioloop.IOLoop.current().start()
