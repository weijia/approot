import argparse


class PyroServiceManager(object):
    @staticmethod
    def register(info_dict):
        parser = argparse.ArgumentParser()
        parser.add_argument("--service_name", help="Service Name")
        parser.add_argument("--service_msg_queue", help="Service Message Queue")
