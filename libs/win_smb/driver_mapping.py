import sys
import os
import string
import re

class sys_driver_mapping:
    def __init__(self):
        self.mapping = {}
        
    def subst_driver(self, src, des, user=None, passwd=None):
        '''
        Substitute the des, so when accessing des, it is just accessing src
        '''
        if src[0] == '\\':
            #use net use
            print des, src
            if (user is None) or (passwd is None):
                cmd_str = 'net use %s: "%s"'%(des, src)
            else:
                cmd_str = 'net use %s: "%s" %s /user:%s'%(des, src, "123456", "richard")                
        else:
            cmd_str = 'subst %s: "%s"'%(des, src)
        print cmd_str
        ret = os.popen(cmd_str)
        #ret = os.popen("dir")
        #print string.join(ret.readlines())
        status = ret.close()#return the exit code
        if status == None:
            #print "success"
            return True
        else:
            #print ret
            #print int(status)
            #print "failed"
            return False
    
    def delete_driver(self, drv):
        cmd_str = 'subst "%s": /d'%drv
        #print cmd_str
        ret = os.popen(cmd_str)
        #print string.join(ret.readlines())
        status = ret.close()#return the exit code
        if status == None:
            #print "success"
            return True
        else:
            #print ret
            #print int(status)
            #print "failed"
            #try to use "net use /delete"
            cmd_str = 'net use /delete %s:'%drv
            cmdout, ret = os.popen2(cmd_str)
            print cmd_str
            l = ret.readline()
            if(re.search('successfully',l)):            
              #print string.join(ret.readlines())
              status = ret.close()#return the exit code
            else:
              cmdout.write('y\r')
              l = ret.readline()
              print l
              status = ret.close()#return the exit code
            #print status
            if status == None:
                #print "success"
                return True
            else:
                #print ret
                #print int(status)
                #print "failed"
                return False
    
    
    def get_mapping(self):
        ret = os.popen("subst")
        p = re.compile('(^UNC)')
        #ret = os.popen("dir")
        dic = {}
        lines = ret.readlines()
        for l in lines:
            #print l
            mat = re.match(' *([A-Z])( *: *\\\ *: *=> *)(.*)$', l)
            g1 = mat.group(1) 
            #print g1
            #print 'to:'
            #print mat.group(2)
            #print mat.group(3)
            #dic[mat.group(1)] = p.sub('\\', mat.group(3))
            if re.match('(^UNC)', mat.group(3)):
                n = p.sub("", mat.group(3))
                print n
                n = '\\' + n
                g2 = n
            else:
                g2 = mat.group(3)
            #print g2
            #print '----------------------------'
            self.mapping[g1] = g2
        status = ret.close()#return the exit code
        self.get_net_use()
        return self.mapping

    def get_net_use(self):
        ret = os.popen("net use")
        #p = re.compile('(^UNC)')
        #ret = os.popen("dir")
        dic = {}
        lines = ret.readlines()
        pending = ''
        lastDriver = '  '#Used to check if the last line contains a driver letter
        resultLine = list()
        for l in lines:
            driverName = l[13:15]
            #print l
            #print "driver:"+driverName
            if len(driverName) < 2:
                driverName = '  '
            if driverName[1] != ':':
                #This line does not contain driver letter
                #Example:
                #Disconnected Z:        \\qtx634-03\shared        Microsoft Windows Network
                if lastDriver[1] == ':':
                    #The last line contain driver letter
                    #print 'driver letter exist'
                    mat = re.match('.+ +([A-Z]): +(\\\\[^ ]+).+$', pending)
                    if mat != None:
                      #print 'group1:',mat.group(1)#Z
                      #print 'group0:',mat.group(0)#all
                      src = mat.group(2).rstrip()
                    #print pending + '<br/>'
                    #print '"%s"'%src
                    #print 'group2:',mat.group(2)#\\qtx634-03\shared
                    self.mapping[mat.group(1)] = src
                else:
                    #ignore the line because neither the previous contains driver letter
                    anop = 1
                lastDriver = '  ' 
            else:
                #This line does contain driver letter, so pend it.
                if lastDriver[1] == ':':
                    #The last line contain driver letter
                    #mat = re.match('(OK)* +([A-Z]): +(\\\\.*)[ ]*$',pending)
                    #print mat.group(3)
                    #print mat.group(2)
                    src = pending[23:48]
                    #print "src:"+src
                    self.mapping[lastDriver[0]] = src
                else:
                    #do not process this line, add it to pending
                    anop = 1

                pending = l
                lastDriver = driverName
                
        status = ret.close()#return the exit code
        return self.mapping
        


def main():
    s = sys_driver_mapping()
    m = s.get_mapping()
    for i in m:
        print i+":"+s.mapping[i]
     
if __name__ == '__main__':
    main()
