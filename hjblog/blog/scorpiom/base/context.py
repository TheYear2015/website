# -*- coding: utf-8 -*-

import time
from scorpiom.base.utils import storage

options = storage()

class Context(storage):
    """Template context container.
    
    A container which will return empty string silently if the key is not exist
    rather than raise AttributeError when get a item's value.
    
    It will raise TemplateContextError if debug is True and the key 
    does not exist.   
    
    The context item also can be accessed through get attribute. 
    
    """

    def __init__(self):
        self.context = storage()
        self.context.options = options
        self.context.title = ""


    def prepare_time(self):
        if not self.__hasattr__("time"):
            self.time = storage()
        self.time.server_time = time.strftime("%Y-%m-%d %T", time.localtime(time.time()))

    def prepare_request(self, request):
        self.request = request

        