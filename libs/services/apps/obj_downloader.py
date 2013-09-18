


#Generate target path
#approot/../exported/hostname/timestamp.txt: include data and all server timestamps

#Find the latest dump file
{"exported": [{"name1":"data1"}], "server_timestamps":{"server1-timestamp":1000000, "server2-timestamp"}}
#Check the latest timestamp for a server

        parser = argparse.ArgumentParser()
        #print self.param_dict
        ############################
        parser.add_argument("--server", help="server name to download from")

        print sys.argv
        #print parser
        args = vars(parser.parse_args())
        return args

urllib