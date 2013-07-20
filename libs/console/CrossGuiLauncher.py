import traceback
import libsys
import libs.utils.filetools as fileTools
import libs.logsys.logDir as logDir
from ConsoleOutputCollector import ConsoleOutputCollector
import os
import beanstalkc
from libs.services.svc_base.beanstalkd_interface import gBeanstalkdServerHost, gBeanstalkdServerPort
#from libs.services.beanstalkdServices.beanstalkServiceBaseV2 import gBeanstalkdServerHost, gBeanstalkdServerPort
from libs.services.svc_base.gui_service import GuiService
from msg_handler import GuiServiceMsgHandler
import webbrowser
from configuration import g_config_dict
import sys
import time
from libs.services.svc_base.msg import Msg
from libs.services.svc_base.msg_based_service_mgr import gMsgBasedServiceManagerMsgQName
from libs.services.svc_base.msg_service import MsgQ


class CrossGuiLauncher(object):
    def __init__(self, gui_factory):
        '''
        * Create taskbar menu
        '''
        self.gui_factory = gui_factory
        self.session_id = time.time()
        self.taskbar_icon_app = self.gui_factory.create_taskbar_icon_app()
        self.app_list_ui = self.gui_factory.get_app_list()
        self.taskbar_icon_app["Open Main Page"] = self.open_main
        self.taskbar_icon_app["Show/Hide"] = self.app_list_ui.app_list.toggle
        self.taskbar_icon_app["Exit"] = self.on_quit_clicked

        super(CrossGuiLauncher, self).__init__()
        self.app_name_to_task_dict = {}
        #self.basic_app_name_to_task_dict = {}
        self.wnd_to_console_dict = {}
        self.task_to_menu_item_dict = {}
        self.wnd2str = {}
        self.start_basic_service()
        self.msg_handler = GuiServiceMsgHandler(gui_factory)
        #self.drop_handler = None
        self.beanstalkd_launcher = None

    def open_main(self):
        webbrowser.open("http://127.0.0.1:" + str(g_config_dict["ufs_web_server_port"]) + "/objsys/manager/", new=1)

    def start_msg_loop(self):
        self.gui_factory.start_msg_loop()

    def on_app_item_selected(self, app_id):
        #print 'selected: ', app_id
        minimized = self.on_menu_clicked(app_id)
        self.app_list_ui[app_id] = {"checked": not minimized, "action": self.on_app_item_selected}

    #####################################
    # Event handlers
    #####################################
    def on_menu_clicked(self, menu_text):
        return self.app_name_to_task_dict[menu_text].toggle()

    def on_child_closed(self, child_wnd):
        self.app_list_ui[self.wnd2str[child_wnd]] = {"checked": False, "action": self.on_app_item_selected}


    def on_quit_clicked(self):
        #self.window.hide()
        #self.icon.set_visible(False)
        print 'on_quit_clicked'
        for log_collector in self.task_to_menu_item_dict.keys():
            if log_collector == self.beanstalkd_app:
                continue
            log_collector.send_stop_signal()
        stop_msg = Msg()
        stop_msg.add_cmd("stop")
        stop_msg["session_id"] = self.session_id
        MsgQ(gMsgBasedServiceManagerMsgQName).send_cmd(stop_msg)

        print 'wait for 10 seconds'
        #self.timer_id = gobject.timeout_add(50000, self.final_quit)#Here time value are milliseconds
        self.gui_factory.timeout(5000, self.final_quit)

    '''
    def on_console_wnd_close_clicked(self, console_wnd):
        self.wnd_to_console_dict[console_wnd].send_stop_signal()
        #self.timer_id = gobject.timeout_add(5000, self.kill_console_process_tree)#Here time value are milliseconds
    '''
    ###############################
    # Internal functions
    ###############################

    def final_quit(self):
        print 'start to killing apps'
        #Kill Beanstalkd Launcher service
        if not (self.beanstalkd_launcher is None):
            self.beanstalkd_launcher.kill_console_process_tree()

        if not (self.msg_based_service_mgr is None):
            self.msg_based_service_mgr.kill_console_process_tree()

        for log_collector in self.task_to_menu_item_dict.keys():
            if log_collector == self.beanstalkd_app:
                continue
            log_collector.kill_console_process_tree()

        if not (self.beanstalkd_app is None):
            self.beanstalkd_app.kill_console_process_tree()
        print "before factory exit"
        self.gui_factory.exit()
        print 'all application killed, after main_quit'
        print 'stopping postgresql'
        stop_script_path = fileTools.findAppInProduct('postgresql_stop')
        os.system(stop_script_path)
        sys.exit(0)

    def start_services(self, app_list):
        """Start GUI service by start thread that retrieve msg from beanstalkd.
        """
        for i in app_list:
            self.start_app_by_name_with_session_id(i)
        try:
            #Prevent impact to normal apps
            self.gui_factory.set_msg_callback(self.handle_msg)
            self.pyqt_service = GuiService(self.gui_factory)
            self.pyqt_service.start()
            self.gui_factory.msg("App starting")
        except:
            traceback.print_exc()

    def handle_msg(self, data):
        #print "msg_handler:", data
        if data["command"] == "Launch":
            param = [data["path"]]
            param.extend(data["param"])
            print 'launching: ', param
            self.create_console_wnd_for_app(param)
        elif data["command"] == "LaunchApp":
            self.start_app_by_name_with_session_id(data["app_name"], data["param"])
        else:
            self.msg_handler.handle_msg(data)

    def start_basic_service(self):
        self.beanstalkd_app = self.start_app_by_name_with_session_id('startBeanstalkd.bat')
        if self.beanstalkd_app is None:
            return None
            #Check if beanstalkd started correctly
        retry_cnt = 0
        while True:
            try:
                self.beanstalk = beanstalkc.Connection(host=gBeanstalkdServerHost, port=gBeanstalkdServerPort)
                break
            except beanstalkc.SocketError:
                retry_cnt += 1
                if retry_cnt > 100:
                    print "beanstalkd start failed"
                    break
        if retry_cnt > 100:
            raise "Beanstalkd can not be started"

        ###########################
        # Start beanstalkd service manager
        ###########################
        #This service will manage services (services who want to receive notification of quitting must register to this service)
        #self.beanstalkd_launcher = self.start_basic_app("BeanstalkdLauncherService")
        self.msg_based_service_mgr = self.start_app_by_name_with_session_id("msg_based_service_mgr")
        ######
        ##TODO: check BeanstalkdLauncherService is working? No, retry to register in services
        #import time
        #time.sleep(20)

    def create_console_wnd_for_app(self, param):
        """
        Start an app with full path and parameters passed in a list
        param: [appFullPath, param1, param2, ...]
        """
        l = logDir.logDir(os.path.basename(param[0]) + str(param[1:]))
        child_wnd = self.gui_factory.create_console_output_wnd(self, l.getLogFilePath())
        collector = ConsoleOutputCollector()
        cwd = libsys.get_root_dir()
        collector.runConsoleApp(child_wnd, cwd, param)
        self.wnd_to_console_dict[child_wnd] = collector
        child_wnd.set_title(param[0])

        cnt = 1
        app_name = os.path.basename(param[0])
        app_path = os.path.dirname(param[0])
        app_path_and_param_gen_str = "%s(%s) params: %s" % (app_name, app_path, str(param[1:]))
        if self.app_name_to_task_dict.has_key(app_path_and_param_gen_str):
            while self.app_name_to_task_dict.has_key(app_path_and_param_gen_str + '-' + str(cnt)):
                cnt += 1
            app_path_and_param_gen_str = app_path_and_param_gen_str + '-' + str(cnt)

        self.app_name_to_task_dict[app_path_and_param_gen_str] = child_wnd
        self.wnd2str[child_wnd] = app_path_and_param_gen_str
        #self.app_name_to_collector[app_path_and_param_gen_str] = collector
        self.task_to_menu_item_dict[collector] = child_wnd
        #self.taskbar_icon_app[app_path_and_param_gen_str] = self.on_app_item_selected
        self.app_list_ui[app_path_and_param_gen_str] = {"checked": False, "action": self.on_app_item_selected}
        return collector

    def start_app_by_name_with_session_id(self, app_name, param=[]):
        full_path = fileTools.findFileInProduct(app_name)
        if full_path is None:
            full_path = fileTools.findAppInProduct(app_name)
            if full_path is None:
                print app_name, 'not found ---- !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!'
                return None
        all_param = [full_path, '--session_id', "%f" % self.session_id]
        all_param.extend(param)
        return self.create_console_wnd_for_app(all_param)


def start_cross_gui_launcher(app_list=[]):
    from libs.qtconsole.PyQtGuiFactory import PyQtGuiFactory

    g = CrossGuiLauncher(PyQtGuiFactory())
    try:
        g.start_services(app_list)
    except:
        pass
    g.start_msg_loop()


def main():
    start_cross_gui_launcher()


if __name__ == '__main__':
    main()