import sys
import os
c = os.getcwd()
while c.find('prodRoot') != -1:
  c = os.path.dirname(c)
#print c
sys.path.insert(0, os.path.join(c,'prodRoot'))
