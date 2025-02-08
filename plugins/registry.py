"""
    implementing a plugin loader i.e can load a function from a file given parameters
"""
import importlib as IL
import importlib.util
import os
import json
import shutil
import pandas as pd

#
# we should have a way to register these functions using rudimentary means
#

REGISTRY_PATH=None
class Registry :

    def __init__(self,folder=None,reader = None) :
        """
        
        """
        self._folder = folder if folder else os.environ.get('REGISTRY_FOLDER',None)
        self._filename = os.sep.join([self._folder,'plugins-registry.json'])
        # self._context = self._folder.split(os.sep)[-1]
        self._reader = reader
        self._data = {}
        self.make(self._folder) #-- making the folder just in case we need to
        # self.make(os.sep.join([self._folder,'code']))
        self.load()
    

    def set(self,filename,names) :
        """
        :filename this is the python file
        :names      names of the functions within the file
        """
        if os.path.exists(filename) and names:
            _file = filename.split(os.sep)[-1].split('.')[0]
            _newlocation = os.sep.join([self._folder,'code',filename.split(os.sep)[-1]])
            self._data[_file] = {"content":names,"path":_newlocation}
            #
            # we need to copy the file to the new location
            #
            shutil.copyfile(filename, _newlocation)
            self.write()
            return 1            
        else:
            return 0
    def stats (self):        
        return pd.DataFrame([{'file':_key,'count': len(self._data[_key]['content']),'example':'@'.join([self._data[_key]['content'][0],_key]),'functions':json.dumps(self._data[_key]['content'])} for _key in self._data])
    def make (self,_folder):
        """
        make registry folder
        """
        
        # _folder = self._folder if not _folder else _folder
        _codepath = os.sep.join([self._folder,'code'])
        if not os.path.exists(_folder) :
            os.makedirs(self._folder)
            self.write()
        if not os.path.exists(_codepath):
            os.makedirs(_codepath)

            #
            # adding
    def load (self):
        if os.path.exists(self._filename) :
            f = open(self._filename) #if _filename else open(_filename)
            #_context = self._context if not _context else _context
            try:
                
                self._data = json.loads(f.read())
            except Exception as e:
                pass
            finally:
                f.close()
    def has (self,_key):
        """
        _key    can be formatted as _name@file with
        """
        if '@' in _key :
            _name,_file = _key.split('@')
        else:
            _name = _key
            _file = None
            if len(self._data.keys()) == 1 :
                _file = list(self._data.keys())[0]
        if _file in self._data :
            return _name in self._data[_file]['content']
        return False    
        
    def write (self):
        #
        # will only write the main
        f = open(self._filename,'w+')
        f.write(json.dumps(self._data))
        f.close()
        pass
