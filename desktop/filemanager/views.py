# Create your views here.
    
    
# -*- coding: utf-8 -*-
from __future__ import with_statement # This isn't required in Python 2.6     
__metaclass__ = type


from contextlib import closing, contextmanager 
import os, sys, traceback
import os.path

#from mod_python import apache, util
#from util import parse_qs
import urlparse
from urlparse import parse_qs
import time


#today = time.today

ver = sys.version_info

if ver[0]<2 and ver[1]<5:
    #raise EnvironmentError('Must have Python version 2.5 or higher.')
    pass


try:
    import json
except ImportError:
    #raise EnvironmentError('Must have the json module.  (It is included in Python 2.6 or can be installed on version 2.5.)')
    pass


try:
    from PIL import Image
except ImportError:
    #raise EnvironmentError('Must have the PIL (Python Imaging Library).')
    pass

path_exists = os.path.exists
normalize_path = os.path.normpath
absolute_path = os.path.abspath 
make_url = urlparse.urljoin
split_path = os.path.split
split_ext = os.path.splitext
import urllib

euncode_urlpath = urllib.quote_plus

#encode_json = json.JSONEcoder().encode
def encode_json(res):
    res = json.dumps(res)
    print res
    return res

def encodeURLsafeBase64(data):
    return base64.urlsafe_b64encode(data).replace('=','').replace(r'\x0A','')
       
def image(*args):
    #raise NotImplementedError 
    pass


class FakeApacheReqForDjango(object):
    def __init__(self):
        self.filename = "noname"
        self.content = ""
        self.content_list = []
    def content_type(self, type, **kwargs):
        pass
    def write(self, str):
        self.content_list.append(str)
    def sendfile(self, **kwargs):
        pass
        
        
class Filemanager:
    
    """Replacement for FCKEditor's built-in file manager."""
    
    def __init__(self, fileroot= '/'):
        self.fileroot = fileroot
        self.patherror = encode_json(
                {
                    'Error' : 'No permission to operate on specified path.',
                    'Code' : -1
                }
            )
    
    def isvalidrequest(self, path = None, req = None, **kwargs):
        """Returns an error if the given path is not within the specified root path."""
        if path is None:
            path = kwargs['path']
        if req is None:
            req = kwargs['req']
        #assert split_path(path)[0]==self.fileroot
        assert not req is None
        return True


    def getinfo(self, path=None, getsize=True, req=None, **kwargs):
        """Returns a JSON object containing information about the given file."""

        if not self.isvalidrequest(path,req):
            return (self.patherror, None, 'application/json')

        thefile = {
            'Filename' : split_path(path)[-1],
            'File Type' : '',
            'Preview' : path if split_path(path)[-1] else 'images/fileicons/_Open.png',
            'Path' : path,
            'Error' : '',
            'Code' : 0,
            'Properties' : {
                    'Date Created' : '',
                    'Date Modified' : '',
                    'Width' : '',
                    'Height' : '',
                    'Size' : ''
                }
            }
            
        imagetypes = ['gif','jpg','jpeg','png']
        
    
        if not path_exists(path):
            print 'path not exists'
            thefile['Error'] = 'File does not exist.'
            return (encode_json(thefile), None, 'application/json')
        
        
        if os.path.isdir(path):
            thefile['File Type'] = 'dir'
        else:
            thefile['File Type'], ext = os.path.splitext(path)
            
            if ext in imagetypes:
                img = Image(path).size()
                thefile['Properties']['Width'] = img[0]
                thefile['Properties']['Height'] = img[1]
                
            else:
                previewPath = 'images/fileicons/' + ext.upper() + '.png'
                thefile['Preview'] = previewPath if path_exists('../../' + previewPath) else 'images/fileicons/default.png'

        if not os.path.isdir(path):
            thefile['Preview'] = "/filemanager/preview/"+path.replace(":", "__")

        thefile['Properties']['Date Created'] = os.path.getctime(path) 
        thefile['Properties']['Date Modified'] = os.path.getmtime(path) 
        thefile['Properties']['Size'] = os.path.getsize(path)

        req.content_type('application/json')
        req.write(encode_json(thefile))


    def getfolder(self, path=None, getsizes=True, req=None, **kwargs):
        print '-----------------------------getfolder called'
        if not self.isvalidrequest(path, req):
            return (self.patherror, None, 'application/json')

        result = []         
        filelist = os.listdir(path)

        for i in filelist:
            #print i, path
            #if i[0]=='.':
            #result.append(self.getinfo(path + i, getsize=getsizes, req = req))
            self.getinfo(os.path.join(path, i), getsize=getsizes, req = req)
        
        #print result
        req.content_type('application/json')
        #req.write(encode_json(result))
        #print req.content
    
    
    def rename(self, old=None, new=None, req=None):
                
        if not self.isvalidrequest(path=new,req=req):
            return (self.patherror, None, 'application/json')
        
        if old[-1]=='/':
            old=old[:-1]
            
        oldname = split_path(path)[-1]
        path = string(old)
        path = split_path(path)[0]
        
        if not path[-1]=='/':
            path += '/'
        
        newname = encode_urlpath(new)
        newpath = path + newname
        
        os.path.rename(old, newpath)
        
        result = {
            'Old Path' : old,
            'Old Name' : oldname,
            'New Path' : newpath,
            'New Name' : newname,
            'Error' : 'There was an error renaming the file.' # todo: get the actual error
        }
        
        req.content_type('application/json')
        req.write(encode_json(result))
    

    def delete(self, path=None, req=None):
    
        if not self.isvalidrequest(path,req):
            return (self.patherror, None, 'application/json')

        os.path.remove(path)
        
        result = {
            'Path' : path,
            'Error' : 'There was an error renaming the file.' # todo: get the actual error
        }
        
        req.content_type('application/json')
        req.write(encode_json(result))
    
    
    def add(self, path=None, req=None):     

        if not self.isvalidrequest(path,req):
            return (self.patherror, None, 'application/json')
        
    
        try:
            thefile = util.FieldStorage(req)['file'] #TODO get the correct param name for the field holding the file            
            newName = thefile.filename
            
            with open(newName, 'rb') as f:
                            f.write(thefile.value) 
            
        except:

            result = {
                'Path' : path,
                'Name' : newName,
                'Error' : file_currenterror
            }
            
        else:
            result = {
                'Path' : path,
                'Name' : newName,
                'Error' : 'No file was uploaded.'
            }
    
        req.content_type('text/html')
        req.write(('<textarea>' + encode_json(result) + '</textarea>'))
        
    
    def addfolder(self, path, name):        

        if not self.isvalidrequest(path,req):
            return (self.patherror, None, 'application/json')

        newName = encode_urlpath(name)
        newPath = path + newName + '/'
        
        if not path_exists(newPath):
            try:
                os.mkdir(newPath)
            except:
            
                result = {
                    'Path' : path,
                    'Name' : newName,
                    'Error' : 'There was an error creating the directory.' # TODO grab the actual traceback.
                }
        
    def download(self, path=None, req=None):
    
        if not self.isvalidrequest(path,req):
            return (self.patherror, None, 'application/json')
            
        name = path.split('/')[-1]
                  
        req.content_type('application/x-download')
        req.filename=name
        req.sendfile(path)

    



#myFilemanager = Filemanager(fileroot='/var/www/html/dev/fmtest/UserFiles/') #modify fileroot as a needed

from django.template import Context, loader
from django.shortcuts import render_to_response
from django.http import HttpResponse

def handler(request): 
    #req.content_type = 'text/plain' 
    #req.write("Hello World!") 
    req = FakeApacheReqForDjango()
    readRes = request.read()

    kwargs = parse_qs(readRes)

    kwargs = dict(request.REQUEST)
    #elif request.method == 'GET': 
    #    kwargs = parse_qs(req.args)
    if kwargs.has_key('path'):
        kwargs['path'] = urllib.unquote(kwargs['path'])
    #oldid = os.getuid()
    #os.setuid(501)

    
    if True:#try:
        method=str(kwargs['mode'])
        del kwargs['mode']
        methodKWargs=kwargs
        methodKWargs['req']=req
        myFilemanager = Filemanager(fileroot='/') #modify fileroot as a needed
        getattr(myFilemanager, method)(**methodKWargs)
        #return apache.OK 


    else:#except KeyError:
        #return apache.HTTP_BAD_REQUEST
        pass

    #except Exception, (errno, strerror):
        #apache.log_error(strerror, apache.APLOG_CRIT)
        #return apache.HTTP_INTERNAL_SERVER_ERROR
        pass

    #os.setuid(oldid)
    if len(req.content_list) > 1:
        return HttpResponse('['+','.join(req.content_list)+']', mimetype="application/json")
    else:
        return HttpResponse(','.join(req.content_list), mimetype="application/json")



def handler2(request):
    return HttpResponse('{"Code": 0, "File Type": "D:/$RECYCLE", "Error": "", "Filename": "$RECYCLE.BIN", "Path": "D:/$RECYCLE.BIN", "Preview": "images/fileicons/default.png", "Properties": {"Date Created": 1317474344.9274843, "Width": "", "Size": 0, "Date Modified": 1317474344.9743593, "Height": ""},}', mimetype="application/json")
    '''
    return render_to_response('class_scheduling/collapsible_panes.html', {'classroom_id': 1, 'class_duration_in_min': 60, 
            'columns':[[{"title":"Pending to schedule", "id":"class_need_to_schedule_panel"}, {"title":"Classroom List", "id":"classroom_list_panel"}, 
            {"title":"Teacher List", "id":"teacher_list_panel"}, {"title":"Conflict List", "id":"conflict_list_panel"}]]})
    '''

def index(request):

    t = loader.get_template('filemanager/index.html')
    c = Context()
    return HttpResponse(t.render(c))
    '''
    return render_to_response('class_scheduling/collapsible_panes.html', {'classroom_id': 1, 'class_duration_in_min': 60, 
            'columns':[[{"title":"Pending to schedule", "id":"class_need_to_schedule_panel"}, {"title":"Classroom List", "id":"classroom_list_panel"}, 
            {"title":"Teacher List", "id":"teacher_list_panel"}, {"title":"Conflict List", "id":"conflict_list_panel"}]]})
    '''
from django.core.servers.basehttp import FileWrapper
import mimetypes
def preview(request):
    print '--------------preview called'
    print request.path
    path = request.path
    path = path.replace('/filemanager/preview/','')
    path = path.replace('__', ":")
    wrapper = FileWrapper(open(path, 'rb'))
    content_type = mimetypes.guess_type(path)[0]
    response = HttpResponse(wrapper, content_type=content_type)
    response['Content-Length'] = os.path.getsize(path)
    return response