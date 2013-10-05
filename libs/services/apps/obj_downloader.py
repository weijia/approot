import json
import os
import urlparse
import sys
import argparse

#Generate target path
#approot/../exported/hostname/year/month/timestamp.txt: include data and all server timestamps
#approot/../exported/hostname/2013/09/1234234234.12.txt: include data and all server timestamps
#Every dump file contains dumped duration for a server. App create a map for those durations and only dump
#the durations that is not in the dump folder.


#Find the latest dump file
import datetime
import jsonpickle
from timeslice.TimeSlice import TimeSlice, TimeSet
from libs.datetime_storage.datetime_folders import DateTimeFolder
from libs.folder_update_checker import FolderUpdateChecker
from libs.utils.misc import ensure_dir
from libs.utils.obj_tools import getHostName, get_ufs_obj_from_ufs_url, JsonDecoderForUfsObj, get_ufs_obj_from_json
from ui_framework.objsys.models import UfsObj, ObjRelation


class NewStyleObjectTimeSlice(TimeSlice, object):
    pass


class NewStyleObjectTimeSet(TimeSet, object):
    pass

def main():

    dump_file_format = {"exported": [{"name1": "data1"}], "server_timestamps":
        {"server1-timestamp": 1000000, "server2-timestamp": 20000000}}
    #Check the latest timestamp for a server

    parser = argparse.ArgumentParser()
    #print self.param_dict
    ############################
    parser.add_argument("--server", help="server name to download from")

    print sys.argv
    #print parser
    args = vars(parser.parse_args())

    print args['server']
    p = urlparse.urlparse(args['server'])
    print p.netloc

    g_dump_root_folder = "d:/tmp/dumproot/"
    ensure_dir(g_dump_root_folder)
    g_dump_state_folder = "d:/tmp/dumpstate/"
    ensure_dir(g_dump_state_folder)

    root = DateTimeFolder(g_dump_root_folder)

    offset = 0



        
    ##################################
    # Load import state file
    ##################################
        
    sync_state = {"laptop1": {"downloaded_timeset": NewStyleObjectTimeSet()}}
        
    ##################################
    # Import existing data from file
    ##################################
    #Get hostname
    self_host_name = getHostName()
    file_timestamp_keeper = []
    #Scan other host's data directories.
    for hostname_as_folder in os.listdir(g_dump_root_folder):
        if hostname_as_folder == self_host_name:
            continue
        host_name_as_folder_full_path = os.path.join(g_dump_root_folder,  hostname_as_folder)
        '''
        {"server":"allbookmarks.duapp.com", "downloaded":[
        {"meta": {"limit": 20, "next": "/objsys/api/ufsobj/ufsobj/?offset=20&limit=20&format=json",
        "offset": 0, "previous": null, "total_count": 184}, "objects": [{"description": "",
        "full_path": "", "head_md5": "", "id": 2, "resource_uri": "/objsys/api/ufsobj/ufsobj/2/",
        "size": null, "tags": ["all_history"], "timestamp": "2013-08-18T04:54:59", "total_md5": "",
        "ufs_url": "http://blog.csdn.net/id19870510/article/details/8489486", "uuid":
        "09006587-787a-4814-8133-1a716d8b5968", "valid": true}]}
        ]}
       '''
        if os.path.isdir(host_name_as_folder_full_path):
            checker = FolderUpdateChecker(host_name_as_folder_full_path, file_timestamp_keeper)
            for updated_item_full_path in checker.enum_new_file():
                fp = open(updated_item_full_path, "r")
                info = json.load(fp)
                fp.close()
                server = info["server"]
                for downloaded_item in info["downloaded"]:
                    for item in ["objects"]:
                        referencer_url = server + item["resource_uri"]
                        referencer_obj, created = UfsObj.get_or_create(referencer_url, valid=True)
                        referenced_obj = get_ufs_obj_from_json(item)
                        referenced_obj.tags = ','.join(item["tags"])
                        ObjRelation.get_or_create(from_obj=referencer_obj, to_obj=referenced_obj,
                                                  relation="Referencing", valid=True)


    ###################################
    # Load current state file from folder
    ###################################
    state_file_path = os.path.join(g_dump_state_folder, "state.txt")

    if os.path.exists(state_file_path):
        state_file = open(state_file_path, "r")
        slices = jsonpickle.decode(state_file.read())
        state_file.close()


    def get_last_timestamp_for_server(server_loc):
        for last_dump_file_path in root.enumerate_from_latest():
            item = json.load(last_dump_file_path)
            try:
                return item["server_timestamps"][server_loc]
            except KeyError:
                pass

    for folder_for_host in os.listdir(g_dump_root_folder):
        host_dump_folder_full_path = os.path.join(g_dump_root_folder, folder_for_host)


    time_set = NewStyleObjectTimeSet()


    def dump_data_for_time_slice(time_slice):
        pass


    #Check if the first item on server is dumped
    if 0 == len(time_set):
        start = datetime.datetime(datetime.MINYEAR, 1, 1)


    if (0 == len(time_set)) or (time_set[0].start.year != datetime.MINYEAR):
        dump_data_for_time_slice()


    for index in range(0, len(time_set)):
        time_slice = time_set[index]



    get_last_timestamp_for_server(p.netloc)
    #http://mycampus.duapp.com/objsys/api/ufsobj/ufsobj/?format=json
    first_url = "https://%s/objsys/api/ufsobj/ufsobj/?offset=%d&limit=%d&format=json" % (p.netloc, offset, 20)
