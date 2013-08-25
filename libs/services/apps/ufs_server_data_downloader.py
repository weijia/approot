# -*- coding: gbk -*-
"""
This example is based on folder_expand_service
"""
#import os
import os
import time
from libs.utils.misc import ensure_dir
import libsys
#from libs.logsys.logSys import cl, info
#from libs.services.svc_base.msg import Msg
from libs.services.svc_base.simple_service_v2 import SimpleService
from libs.services.svc_base.service_base import ThreadedService
import libs.utils.transform as transform
from django.conf import settings

import httplib2 as http
import json

try:
    from urlparse import urlparse
except ImportError:
    from urllib.parse import urlparse


class UfsServerDataDownloader(ThreadedService):
    def run(self):
        root_dir = libsys.get_root_dir()
        url = 'http://1.mycampus.duapp.com/objsys/api/ufsobj/ufsobj/?format=json'
        url += '&username=%s&password=%s' % (settings.UFS_SERVER_ADMIN_NAME,
                                             settings.UFS_SERVER_ADMIN_PASSWORD)
        while not self.is_quitting():
            headers = {
                'Accept': 'application/json',
                'Content-Type': 'application/json; charset=UTF-8'
            }

            target = urlparse(url)
            method = 'GET'
            body = ''

            h = http.Http()

            # If you need authentication some example:
            #if auth:
            #    h.add_credentials(auth.user, auth.password)

            response, content = h.request(
                target.geturl(),
                method,
                body,
                headers)

            # assume that content is a json reply
            # parse content with the json module
            data = json.loads(content)
            if data["meta"]["total_count"] > 0:

                dump_root = os.path.join(root_dir, "../ufs_server_dump/")
                ensure_dir(dump_root)

                dump_filename = os.path.join(dump_root, str(time.time())+".json")
                f = open(dump_filename, "w")
                f.write(json.dumps(data, indent=4))
                f.close()

            if not (data["meta"]["next"] is None):
                url = data["meta"]["next"]
                continue
            break


if __name__ == "__main__":
    s = SimpleService({},
        worker_thread_class=UfsServerDataDownloader)
    s.run()