"""
    implementing a plugin loader i.e can load a function from a file given parameters
"""
import importlib as IL
import importlib.util
import os
import json
import shutil
import pandas as pd

class Loader :
    """
    This class is intended to load a plugin and make it available and assess the quality of the developed plugin
    """
   
    def __init__(self,**_args):
        """
        """
        # _names = _args['names'] if 'names' in _args else None
        # path = _args['path'] if 'path' in _args else None
        # self._names = _names if type(_names) == list else [_names]
        self._modules = {}
        self._names = []
        self._alias = {} #-- synonyms
        if 'file' in _args :
            self.load(**_args)
        self._registry = _args['registry'] if 'registry' in _args else None

    def load (self,**_args):
        """
        This function loads a plugin from a given location
        :file   location of the file
        """
        self._modules = {}
        self._names = []
        path = _args ['file']
        _decoratorName = None if 'decorator' not in _args else _args['decorator']
        
        if os.path.exists(path) :
            _alias = path.split(os.sep)[-1]
            spec = importlib.util.spec_from_file_location(_alias, path)
            module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(module) #--loads it into sys.modules
            for _name in dir(module) :
                if self.isplugin(module,_name,_decoratorName) :
                    self._modules[_name] = getattr(module,_name)
                    if hasattr(self._modules[_name],'name') :
                        _alt = getattr(self._modules[_name],'name')
                        self._alias[_alt] = _name
        return self._modules is not None
                    # self._names [_name]
    # def format (self,**_args):
    #     uri = _args['alias'],_args['name']
    # def set(self,_pointer) :
    def set(self,_key) :
        """
        This function will set a pointer to the list of modules to be called
        This should be used within the context of using the framework as a library
        """
        if type(_key).__name__ == 'function':
            #
            # The pointer is in the code provided by the user and loaded in memory
            #
            _pointer = _key
            _key = 'inline@'+_key.__name__
            # self._names.append(_key.__name__)
        else:
            _pointer = self._registry.get(_key)

        if _pointer  :
            self._modules[_key] = _pointer
            self._names.append(_key)
        
    def isplugin(self,module,name,attr=None):
        """
        This function determines if a module is a recognized plugin
        :module     module object loaded from importlib
        :name       name of the functiion of interest
        :attr       decorator attribute name (if any)
        """
        
        p = type(getattr(module,name)).__name__ =='function'
        q = True if not attr else hasattr(getattr(module,name),attr)
        #
        # @TODO: add a generated key, and more indepth validation
        return p and q
    
    def has(self,_name):
        """
        This will determine if the module name is loaded or not
        """
        return _name in self._modules or _name in self._alias
    def names (self):
        return list(self._modules.keys())
    def get (self,_name=None):
        """
        This functiion determines how many modules loaded vs unloaded given the list of names
        """
        if _name in self._alias :
            _name = self._alias[_name]
        if _name in self._modules :
            return self._modules[_name]

    def apply(self,_name,**_args):
        _pointer = self.get(_name)
        if _pointer :
            return _pointer (**_args) if _args else _pointer()
    def visitor(self,_args,logger=None) :
        for _name in self._names :
            _pointer = self.get(_name)
            _kwargs = _pointer(_args)
            if (type(_kwargs) == pd.DataFrame and not _kwargs.empty) or _kwargs is not None :
                _args = _kwargs
            # _args = _caller(_pointer,_args)
        return _args
   
