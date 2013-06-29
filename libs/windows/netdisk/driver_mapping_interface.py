import toollibs
import driver_mapping
import html
import cPickle
import os
import urllib



setting_file = "mappingServerData\\driver_mapping.cpickle"

def gen_body():
  flag = 0
  try:
    if os.path.exists(setting_file):
        f = file(setting_file, 'r')
        conf = cPickle.load(f)
        f.close()
    else:
        conf = {}
  except EOFError:
    os.path.remove(setting_file)

  print "<body>"
  s = driver_mapping.sys_driver_mapping()
  params = os.environ.get('QUERY_STRING','')
  m = s.get_mapping()
  try:
    src = urllib.unquote(params.split('=')[1])
    dest = urllib.unquote(params.split('=')[0])
    #print src
    #print dest
  except:
    flag = 1
  if flag == 0:
    dest = dest.upper()
    
    if os.path.isdir(src):
      #print src
      a = 0
    else:
      src = os.path.dirname(src)
    if os.path.exists(src):
      #print 'base:'+src
      try:
        #print dest
        #print m[dest].upper()
        #print src.upper()
        #print "'%s'"%m[dest]
        #print "'%s'"%src
        if m[dest].upper() == src.upper():
          #print m
          s.delete_driver(dest)
          del m[dest]
          print 'delete driver'
        else:
          s.delete_driver(dest)
          print 'replace driver'
          if s.subst_driver(src, dest):
            m[dest] = src
      except KeyError:
        if s.subst_driver(src, dest):
          #print 'add driver'
          m[dest] = src
      print '''
      <script language="JavaScript" type="text/JavaScript">
      <!--
      if(window.location.href.indexOf('?')!= -1)
    	{
    		base = window.location.href.substr(0, window.location.href.indexOf('?'));
    	}
    	else
    	{
    		base = window.location.href;
    	}
    	window.location.href = base;
    	//-->
    	</script>
    	'''
      return


  print '''
  <input id="driver_letter" type="text" maxLength="1"><input id="map_path" type="text"><input type="button" name="map" value="map" onclick='javascript:map_input()''>
  <STYLE type="text/css">
   tr.mapped {color: red;}
  </STYLE>
  <script language="JavaScript" type="text/JavaScript">
  <!--
  //alert(window.location.href);
  function map_driver(src, dest)
  {
    
  	var base;
  	if(window.location.href.indexOf('?')!= -1)
  	{
  		base = window.location.href.substr(0, window.location.href.indexOf('?'));
  	}
  	else
  	{
  		base = window.location.href;
  	}
  	window.location.href = base+"?"+dest+"="+src;
  }
  function map_input()
  {
    map_driver(document.getElementById('map_path').value, document.getElementById('driver_letter').value);
  }
  function map_row(e)
  {
    //alert("clicked");
    map_driver(e.currentTarget.getElementsByTagName("td")[1].innerHTML, e.currentTarget.getElementsByTagName("td")[0].innerHTML.substr(0,2));
  }
  function map_row_click(e)
  {
    //alert("clicked");
    map_driver(e.currentTarget.parentNode.parentNode.getElementsByTagName("td")[1].innerHTML, e.currentTarget.parentNode.parentNode.getElementsByTagName("td")[0].innerHTML.substr(0,2));
  }
  -->
  </script>
  '''
  print '<table border="1">'
  for i in m:
    print '<tr class="mapped" ondblclick="map_row(event)"><td>'
    print i+":</td><td>"+m[i]+'</td><td>'
    html.gen_button("map_row_click(event)", "disable")
    print '</td></tr>'
    try:
      #Check if the driver mapping is already in conf file
      if conf[i].index(m[i]) == -1:
        conf[i].append(m[i])
    except ValueError:
      conf[i].append(m[i])
    except KeyError:
      conf[i] = []
      conf[i].append(m[i])
      
  #Add umounted drivers
  for i in conf.keys():
    try:
      if m[i] == conf[i]:
        continue
    except:
      for k in conf[i]:
        print '<tr ondblclick="map_row(event)"><td>'
        print i+":</td><td>"+k+'</td><td>'
        html.gen_button("map_row_click(event)", "enable")
        print '</td></tr>'
      
  f = file(setting_file, 'w')
  cPickle.dump(conf, f)
  f.close()

  print '</table>'
  print '</body>'


h = html.html()
h.genHead("map drivers")

gen_body()
