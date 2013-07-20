from libs.console.CrossGuiLauncher import start_cross_gui_launcher


################
# It is recommended to start app in ext_svr instead of here. Failure in starting app here will cause unexpected result.
################
autoStartAppList = ["start_ext.bat",
                    #"sftpserver",
                    #"scache.bat",
                    #"tagging"
                    ]



if __name__ == "__main__":
    start_cross_gui_launcher(autoStartAppList)
