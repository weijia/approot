#coding:utf-8
#author: leanse

import sys
sys.path.append("..")

import unittest
from client import KuaipanAPI
from session import KuaipanSession

class TestKupanAPI(unittest.TestCase):

    def setUp(self):
       sess = KuaipanSession("", "", "app_folder")
       sess.set_access_token("", "")
       self.api = KuaipanAPI(sess)

    
    def test_acc_info(self):
        print "================acc_info===================="
        ret = self.api.account_info()
        assert int(ret['user_id']) == 3261479

    def test_metadata(self):
        print "================meta_data==================="
        self.api.create_folder(u"/metadata文件")
        self.api.upload_file("/metadata文件/1.txt", "hello", True)
        self.api.upload_file("/metadata文件/2.txt", "world", True)
        ret = self.api.metadata(u"/metadata文件")
        assert ret['files'].__len__() == 2
        ret = self.api.metadata(u"/metadata文件/1.txt")
        assert ret['name'] == u"1.txt"

    def test_shares(self):
        print "================shares======================"
        ret = self.api.create_folder(u"/文件share/")
        assert ret['msg'] == 'ok'
        ret = self.api.upload_file(u"/文件share/1.txt", "hello world!", True)
        self.api.shares(u"/文件share/1.txt")
        try:
            print self.api.shares(u"/文件share")
        except Exception, e:
            assert e.code == 404
        else:
            assert False

    def test_create_folder(self):
        print "===============create_folder=================="
        ret = self.api.create_folder(u"/test新建文件夹")
        assert ret['msg'] == 'ok'
        ret = self.api.create_folder(u"/test新建文件夹/folder")
        assert ret['msg'] == 'ok'
        ret = self.api.create_folder(u"/noExistFolder/folder")
        assert ret['msg'] == 'ok'

        path = u"/noExistFolder/" + "a" * 255
        try:
            ret = self.api.create_folder(path = path)
        except Exception, e:
            assert e.code == 400
        else:
            assert False

        not_allow = ("\\", ":", "?", "<", ">", "\"", "|")
        for s in not_allow:
            try:
                path = "/test新建文件夹/test_not_allow" + s
                ret = self.api.create_folder(path)
            except Exception, e:
                assert e.code == 400
            else:
                print s
                assert False
        path = u"/test新建文件夹/.aaaaaaa"
        ret = self.api.create_folder(path)
        assert ret['msg'] == 'ok'


    def test_delete(self):
        print "=================test_delete======================="
        ret = self.api.create_folder("/delete/delete")
        assert ret['msg'] == 'ok'
        ret = self.api.delete("/delete/delete")
        assert ret['msg'] == 'ok'

        ret = self.api.metadata("/delete")
        assert len(ret['files']) == 0
        try:
            ret = self.api.delete("/delete/delete")
        except Exception, e:
            assert e.code == 404
        else:
            assert False


    def test_move(self):
        print "==================test_move========================"
        ret = self.api.create_folder(u"/test_move文件夹/to_folder")
        assert ret['msg'] == "ok"
        ret = self.api.upload_file(u"/test_move文件夹/from.txt", "hello world!", True)
        try:
            ret = self.api.move(u"/test_move文件夹/from.txt", u"/test_move文件夹/to_folder/from.txt")
            assert ret['msg'] == 'ok'
        except Exception, e:
            assert e.code == 403
        ret = self.api.upload_file(u"/test_move文件夹/from1.txt", "xxxxxxxxxxxxxxxxxxxxxx", True)
        try:
            ret = self.api.move(u"/test_move文件夹/from1.txt", u"/test_move文件夹/to_folder/to.txt")
            assert ret['msg'] == 'ok'
        except Exception, e:
            assert e.code == 403

    def test_copy(self):
        print "==============test_copy==========================="
        ret = self.api.create_folder(u"/test_copy/to_folder")
        assert ret['msg'] == 'ok'
        ret = self.api.upload_file(u"/test_copy/from.txt", "aaaaaaaaaaaaaaaaaaaaa", True)
        try:
            ret = self.api.copy(u"/test_copy/from.txt", "/test_copy/to_folder/from.txt")
            assert ret['msg'] == 'ok'
        except Exception, e:
            assert e.code == 403

        try:
            ret = self.api.copy("/test_copy/from.txt", u"/test_copy/to_folder/to.txt")
            assert ret['msg'] == "ok"
        except Exception, e:
            assert e.code == 403
    
    def test_upload_file(self):
        print "==============test_upload========================"
        ret = self.api.create_folder(u"/上传文件/")
        assert ret['msg'] == "ok"
        
        ret = self.api.upload_file(u"/上传文件/hello.txt", "hello world!\nhello world！", True)

        f = open("./testcase.py", "rb")
        ret = self.api.upload_file(u"/上传文件/test.py", f, True)
        try: 
            ret = self.api.upload_file(u"/上传文件", f, False)
        except Exception, e:
            assert e.code == 405
        try:
            ret = self.api.upload_file(u"/not_exists_folder/a.txt", "abcdefghijklmnopqrst", True)
        except Exception, e:
            assert e.code == 405

    def test_download_file(self):
        print "==============test_download======================"
        ret = self.api.create_folder("/test_download")
        assert ret['msg'] == "ok"

        ret = self.api.upload_file("/test_download/download.txt", "hello", True)
        rs = self.api.download_file("/test_download/download.txt")
        result = rs.read()
        print result
        assert result == "hello"
    
    def test_thumbnail(self):
        print "=============test_thumbnail====================="
        ret = self.api.create_folder("/test_thumbnail/")
        assert ret['msg'] == "ok"

        f = open("./thumbnail.jpg", "rb")
        ret = self.api.upload_file("/test_thumbnail/a.jpg", f, True)

        ret = self.api.thumbnail("/test_thumbnail/a.jpg", 800, 600)

        f = open("./test_thumb.jpg", "wb")
        f.write(ret)
        f.close()

    def test_document_view(self):
        print "============test_document_view================="
        ret = self.api.create_folder("/test_document_view/")
        ret = self.api.upload_file("/test_document_view/d.txt", "hello", True)
        ret = self.api.document_view('/test_document_view/d.txt', 'normal', 'txt', zip = 0)
        print ret

if __name__ == "__main__":
    unittest.main()
