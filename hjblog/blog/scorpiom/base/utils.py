# -*- coding: utf-8 -*-

class storage(dict):
    """Template context container.
    
    A container which will return empty string silently if the key is not exist
    rather than raise AttributeError when get a item's value.
    
    It will raise TemplateContextError if debug is True and the key 
    does not exist.   
    
    The context item also can be accessed through get attribute. 
    
    """
    def __setattr__(self, key, value):
        self[key] = value

    def __str__(self):
        return str(self)

    def __iter__(self):
        return iter(self.items())

    def __getattr__(self, key):
        """Get a context attribute.
        
        Raise TemplateContextError if the attribute not be set to
        avoid confused AttributeError exception when debug is True, or return ""
        
        """
        if key in self:
            return self[key]
        else:
            self._getattr_error(key)

    def __hasattr__(self, key):
        if key in self:
            return True
        else:
            return False

    def _getattr_error(self, key):
        raise
    
    def parse_config_file(self, path):
        """Rewrite tornado default parse_config_file.
    
        Parses and loads the Python config file at the given path.
    
        This version allow customize new options which are not defined before
        from a configuration file.
        """
        with open(path,'r') as f:
            exec(f.read(), self)