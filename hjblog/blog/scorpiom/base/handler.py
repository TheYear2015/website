# -*- coding: utf-8 -*-

import re
import http.client
import urllib
import traceback
import time

from tornado.web import RequestHandler, HTTPError
from tornado.options import options
from tornado import ioloop, escape


class BaseHandler(RequestHandler):
    _first_running = True

    def __init__(self, application, request, **kwargs):
        if BaseHandler._first_running:
            self._after_prefork()
            BaseHandler._first_running = False

        super(BaseHandler, self).__init__(application, request, **kwargs)

    def _after_prefork(self):
        return None

    def prepare(self):
        self._prepare_context()
        self._remove_slash()

    def _prepare_context(self):
        self._context = Context()
        self.current_time = time.strftime("%Y-%m-%d %T", time.localtime(time.time()))
        self.remote_ip = self.request.remote_ip

    def render_string(self, template_name, **kwargs):
        """Override default render_string, add context to template."""
        assert "context" not in kwargs, "context is a reserved word for \
                template context valuable."
        kwargs['url_escape'] = escape.url_escape

        return super(BaseHandler, self).render_string(template_name, **kwargs)

    def flush(self, include_footers=False):
        """Flushes the current output buffer to the network."""

        chunk = b"".join(self._write_buffer)
        # keep write buffer for cache
        # self._write_buffer = []

        headers = b""

        # Ignore the chunk and only write the headers for HEAD requests
        if self.request.method == "HEAD":
            if headers: self.request.write(headers)
            return

        if headers or chunk:
            self.request.write(headers + chunk)

    def get_error_html(self, status_code, **kwargs):
        """Override to implement custom error pages.

        It will send email notification to admins if debug is off when internal 
        server error happening.
        
        """
        code = status_code
        message = http.client.responses[status_code]

        try:
            # add stack trace information
            exception = "%s\n\n%s" % (kwargs["exception"], traceback.format_exc())

            if options.debug:
                template = "%s_debug.html" % code
            else:
                template = "%s.html" % code

                ## comment send email for ec2 smtp limit
                if code == 500:
                    fr = options.email_from
                    to = options.admins

                    subject = "[%s]Internal Server Error" % options.sitename
                    body = self.render_string("500_email.html",
                                          code=code,
                                          message=message,
                                          exception=exception)

                    mail.send_email(fr, to, subject, body)

            return self.render_string(template,
                                      code=code,
                                      message=message,
                                      exception=exception)
        except Exception:
            return super(BaseHandler, self).get_error_html(status_code, **kwargs)

    def _remove_slash(self):
        if self.request.method == "GET":
            if _remove_slash_re.match(self.request.path):
                # remove trail slash in path
                uri = self.request.path.rstrip("/")
                if self.request.query:
                    uri += "?" + self.request.query

                self.redirect(uri)


_remove_slash_re = re.compile(".+/$")
