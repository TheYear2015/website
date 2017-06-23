# -*- coding: utf-8 -*-

import scorpiom.handlers.help as help
import scorpiom.handlers.index as index

handlers = []
sub_handlers = []
ui_modules = {}

handlers.extend(help.handlers)
handlers.extend(index.handlers)