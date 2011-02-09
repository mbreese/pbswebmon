#!/usr/bin/python
# Copyright (c) 2009 Stephen Childs, and
# Trinity College Dublin.
#
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
#
# Modified by: Marcus Breese <mbreese@iupui.edu>
#              2011-02-08
#              for pbs_python version 4.1.0
#
#

from PBSQuery import PBSQuery, PBSError
from getopt import getopt
import sys
import datetime
from time import strftime
import os,urllib

import cgitb; cgitb.enable()

NODE_STATES=['down','free','job-exclusive','offline','down,offline','down,job-exclusive','state-unknown','down,busy','job-exclusive,busy']
JOB_STATES=['R','Q','E','C','H','W']
REFRESH_TIME = "30"
JOB_EFFIC={}
USER_EFFIC={}

def user_effic(user):
    effic=0.0

    if user in USER_EFFIC:
        for job in USER_EFFIC[user]:
            effic=effic+job
        effic=(effic/float(len(USER_EFFIC[user]))*100.0)

    return effic
        

def job_effic(myjob):
    effic=0.0
    walltime=0.0
    if 'resources_used' in myjob:
        if 'cput' in myjob['resources_used']:
            cput=convert_time(myjob['resources_used']['cput'][0])
        if 'walltime' in myjob['resources_used']:
            walltime=convert_time(myjob['resources_used']['walltime'][0])        
        

    if walltime != 0.0:
        effic=float(cput)/float(walltime)

    return effic

def get_poolmapping(gridmapdir):

    # find files with more than one link in current directory
    allfiles=os.listdir(gridmapdir)

    maptable=dict()
    inodes=dict()

    # sort the list so the "dn-files" come first
    allfiles.sort()

    for file in allfiles:
        statinfo=os.stat(os.path.join(gridmapdir,file))

        if (file[0] == '%'):
            inodes[statinfo.st_ino]=urllib.unquote(file)
        else:
            if (statinfo.st_nlink == 2):
                maptable[file]=inodes[statinfo.st_ino]

    return maptable

def get_dn (ownershort):
    # user info
    if ownershort in userdnmap:
        ownerdn=userdnmap[ownershort]
    else:
        ownerdn=ownershort

    return ownerdn

def convert_time (timestr):
    
    hours,mins,secs=timestr.split(':')

    seconds=(60*60*int(hours))+(60*int(mins))+int(secs)
    return seconds
    
def convert_to_gb (kbmem):
    idx=kbmem.rfind("kb")
    if (idx!=-1):
        mem=kbmem[0:idx]
        mem=float(mem)
        return mem/(1000.0*1000.0)
    idx=kbmem.rfind("mb")
    if (idx!=-1):
        mem=kbmem[0:idx]
        mem=float(mem)
        return mem/(1000.0)

def fill_user_list (jobs):
    users={}
    for name, atts in jobs.items():
        if 'job_state' in atts:
            job_type=atts['job_state'][0]
        ownershort=atts['Job_Owner'][0].split('@')[0]
        effic=job_effic(atts)
        if not ownershort in USER_EFFIC:
            USER_EFFIC[ownershort]=[]
        USER_EFFIC[ownershort].append(effic)
        if not ownershort in users:
            users[ownershort]={}
            users[ownershort]['jobs']=1
            for state in JOB_STATES:
                if state == job_type:
                    users[ownershort][state]=1
                else:
                    users[ownershort][state]=0
            
                
        else:
            users[ownershort]['jobs']=users[ownershort]['jobs']+1
            users[ownershort][job_type]=users[ownershort][job_type]+1
    return users
           
def print_user_summary(users):
    print "<table class='example table-sorted-desc table-autosort:1 table-stripeclass:alternate user_summary' >"
    print "<caption>Users</caption>"
    print "<thead><tr>",
    print "<th class='table-filterable table-sortable:default' align='left'>User</th>"
#    print "<th class='table-filterable table-sorted-desc table-sortable:numeric'>Jobs</th>"
    totals={}

    for state in JOB_STATES:
        print "<th class='table-filterable table-sorted-desc table-sortable:numeric'>%s</th>" % state
        totals[state]=0
    print "<th class='table-sortable:numeric'>Efficiency</th>"
    print "</tr></thead>"

    total=0
    for user, atts in users.items():
        njobs='0'
        if 'jobs' in atts.keys():
            njobs=atts['jobs']
            total=total+njobs
           

            print "<tr><td onMouseOver='highlight(\"%s\")' onMouseOut='dehighlight(\"%s\")'title='%s'>%s</td>" % (user,user,get_dn(user),user)
            for state in JOB_STATES:
                print "<td>%d</td>" % atts[state]
                totals[state]=totals[state]+atts[state]
            print "<td>%.0f</td>" % user_effic(user)
            print "</tr>"



    print "<tfoot><tr><td><b>Total</b></td>"
    for state in JOB_STATES:
        print "<td>%s</td>" % totals[state]
    print "</tr>"
    print '''</tfoot>'''
    print "</table>"
    
def print_node_summary(nodes):
    print "<table class='example table-sorted-desc table-autosort:1 node_summary'>"
    print "<caption>Nodes</caption>"
    print "<thead><tr>",

    totals={}

    print "<th class='table-filterable table-sortable:default' align='left'>State</th>"
    print "<th class='table-filterable table-sorted-desc table-sortable:numeric'>Count</th>"
    for s in NODE_STATES:
        totals[s]=0


    print "</tr></thead>"
    for name, node in nodes.items():
        if 'state' in node.keys():
	    totals[node['state'][0]]=totals[node['state'][0]]+1

    total=0
    for s in NODE_STATES:
        tdclass=s
        if (s == "down,job-exclusive"):
            tdclass="down"
        print "<tr><td class='%s'>%s</td><td class='%s'>%d</td></tr>" %(tdclass,s,tdclass,totals[s])
        total=total+totals[s]
    print "<tfoot><tr><td><b>Total</b></td><td>%d</td></tr></tfoot>" %total
    print "</table>"


def print_queue_summary(queues):
    print "<table class='example table-sorted-desc table-autosort:1 table-stripeclass:alternate queue_summary'>"
    print "<caption>Queues</caption>"

    print "<thead><tr>"
    headers=['Running','Queued','Held']
    print "<th class='table-filterable table-sortable:default' align='left'>Name</th>"
    totals={}
    for h in headers:
        totals[h]=0
    
    for header in headers:
        print "<th class='table-filterable table-sortable:numeric'>",header,"</th>"
    print "</tr></thead>"
    for queue, atts in queues.items():
        print "<tr>",
        print "<td>",queue, "</td>",

        state=atts['state_count'][0]
        state_counts = state.split()
        statedict={}
        for entry in state_counts:
            type,count=entry.split(":")
            statedict[type]=count


        for s in headers:
            print "<td align='right'>",statedict[s],"</td>",
            totals[s]=totals[s]+int(statedict[s])
            
        print "</tr>"
    print "<tfoot><tr><td><b>Total</b></td>",
    for h in headers:
        print "<td align='right'>%d</td> " %(totals[h])
    print "</tr></tfoot>"
    print "</table>"

def print_key_table():

    print "<table class='key_table'>"
    print "<tr><th>Node color codes</th></tr>"
    allstates=NODE_STATES[:]
    allstates.append('partfull')
    for s in allstates:
        print "<tr><td class='%s'>%s</td></tr>" %(s,s)

    print "</table>"
        


GRID_COLS=4

njobs=-1

# get command line options (unused now?)
optlist, args=getopt(sys.argv[1:], 'j:')
nodelist=[]
for arg in args:
    nodelist.append(arg)

for o,a in optlist:
    if o == '-j':
        njobs=int(a)
        

# get options from config file
import ConfigParser
CONFIG_FILE="/etc/pbswebmon.conf"

try:
    config=ConfigParser.RawConfigParser({'name':None, 'translate_dns':'no', 'gridmap': '/etc/grid-security/gridmapdir'})
    config.readfp(open(CONFIG_FILE))
    serveropts=config.items('server')
    gridopts= config.items('grid')
except:
    print "Error reading config"
    sys.exit(1)

for opt in serveropts:
    if opt[0]=='name':
        server=opt[1] 

for opt in gridopts:
    if opt[0]=='translate_dns':
        translate_dns=opt[1]
    if opt[0]=='gridmap':
        gridmap=opt[1]

print "Content-Type: text/html"     # HTML is following
print 
try:
    p=PBSQuery(server)
    nodes=p.getnodes()
    jobs=p.getjobs()
    queues=p.getqueues()
except PBSError, e:
    print "<h3>Error connecting to PBS server:</h3><tt>",e,"</tt>"
    print "<p>Please check configuration in ",CONFIG_FILE, "</p>"
    sys.exit(1)

    
print '''
<html>
<head>
<title>pbswebmon</title> 
<script src="/pbswebmon/table.js" type="text/javascript"></script>
<script src="/pbswebmon/datasel.js" type="text/javascript"></script>



<script type="text/javascript">

var iTimeout;

/*=window.setTimeout('if (location.reload) location.reload();', %s*1000);*/

function set_refresh(refresh) {

    if (refresh) {
    if (window.setTimeout) {
        iTimeout =
            window.setTimeout('if (location.reload) location.reload();', %s*1000);
    }
    } else {
    if (window.clearTimeout) window.clearTimeout(iTimeout);
    }
}

</script>





<link rel="stylesheet" type="text/css" href="/pbswebmon/table.css" media="all">
<link rel="stylesheet" type="text/css" href="/pbswebmon/local.css" media="all">
</head>
<body>

''' % (REFRESH_TIME, REFRESH_TIME)


users={}

if translate_dns == 'yes':
    userdnmap=get_poolmapping(gridmap)
else:
    userdnmap={}

if len(nodelist) == 0:
    nodelist=nodes.keys()
    nodelist.sort()




print "<div class='summary_box'>"
print "<table class='summary_box_table'><tr class='summary_box_entry'><td>"

print "<b>Cluster status</b><br/>%s<br/>Refreshes every %s seconds." % (strftime("%Y-%m-%d %H:%M:%S"),REFRESH_TIME)

print '''<form class="showdetails">
<INPUT TYPE=CHECKBOX NAME="showdetails" CHECKED  onClick=\"show_hide_data(\'jobdata\',
this.checked)\">\nShow all job details\n
<br>
<INPUT TYPE=CHECKBOX NAME="Fixed header" CHECKED  onClick=\"on_top(\'summary_box\',
this.checked)\">\nHeader always on top\n
<br>
<INPUT TYPE=CHECKBOX NAME="refresh" onClick=\"set_refresh(this.checked)\">\nAuto-refresh\n



</form>'''


print "</td>"

print "<td>"
users=fill_user_list(jobs)
print_user_summary(users)
print "</td><td>"
print_queue_summary(queues)
print "</td><td>"
print_node_summary(nodes)
print "</td></tr></table>"
print "</div>"

print "<br clear='all'>"

print "<table style='margin-top:20px'  class=\" table-autosort:0 node_grid\"><tr>"
count=0
def nsort(l):
    ret = []
    for el in l:
        ret.append((int(el[2:]),el))
    ret.sort()
    return [x[1] for x in ret]

nodelist = nsort(nodelist)
for name in nodelist:
    if name in nodes:
        node=nodes[name]
        attdict={}
        if 'status' in node.keys():
	    attdict = node['status']

#            attrslist=node['status'][0].split(',')

#            for attr in attrslist:
#                attname,attvalue=attr.split('=')
#                attdict[attname]=attvalue
#            print attdict
        
	if 'state' in node.keys():
	    node_state=node['state'][0]

        if True: #'jobs' in node.keys():
            if 'jobs' in node.keys():
                myjobs=node['jobs']
            else:
                myjobs=[]
            nusers='0'
            physmem=0.0

            if 'nusers' in attdict:
                nusers=attdict['nusers'][0]

            if 'physmem' in attdict:
                physmem=convert_to_gb(attdict['physmem'][0])            

            loadave="n/a"
            if 'loadave' in attdict:
                loadave=attdict['loadave'][0]
            
            # if (njobs == -1) or len(myjobs)== njobs:
            if True:
		# define cell bg color based on state
		if (node_state == 'free' and (len(myjobs)>0)):
		    node_state='partfull'
                if (node_state == 'down,job-exclusive'):
		    node_state='down'
                print "<td valign='top'>" 
#                print "<b>%s</b>" %name
                print '''<form class='%s'><b>%s
<INPUT class='job_indiv' TYPE=CHECKBOX NAME="showdetails" CHECKED onClick=\"show_hide_data_id(\'%s\',
this.checked)\"><font size=\'2\'>Show jobs</b>''' % (node_state,name, name)
                print "<br>%d jobs, %s users, %.2f GB, %s load</font></b></form>" % (len(myjobs),nusers,physmem,loadave)
                print "<span class='jobdata' id='"+name+"' style='display:block'>"
                for myjobstr in myjobs:
                    myjobstr=myjobstr.lstrip()
                    cpu,jid=myjobstr.split('/')
                    jidshort=jid.split('.')[0]
                    myjob=jobs[jid]
                    ownershort=myjob['Job_Owner'][0].split('@')[0]
                    if not ownershort in users:
                        users[ownershort]={}
                        users[ownershort]['jobs']=1
                    else:
                        users[ownershort]['jobs']=users[ownershort]['jobs']+1
                    mem=0.0
                    memreq=0.0
                    cput=0.0
                    walltime=1.0
                    effic=0.0
                    if 'resources_used.mem' in myjob.keys():
                        mem=convert_to_gb(myjob['resources_used.mem'])
                    if  'Resource_List.pmem' in myjob.keys():
                        memreq=convert_to_gb(myjob['Resource_List.pmem'])

                    if 'resources_used.cput'  in myjob:
                        cput=convert_time(myjob['resources_used.cput'])

                    if 'resources_used.walltime'  in myjob:
                        walltime=convert_time(myjob['resources_used.walltime'])        
                    if 'queue' in myjob:
                        myqueue=myjob['queue'][0]

                    if walltime != 0.0:
                        effic=float(cput)/float(walltime)

                    wrap=" "

#                        wrap="\n</tr>\n<tr>"
                    print "<span title='"+jidshort+": "+myqueue+"'>"+cpu+ ": "+jidshort+ "</span>",

                    # user info
                    ownerdn=get_dn(ownershort)
                        
                    print "<span class= '%s' title='%s'> %-9s</span>" %(ownershort,ownerdn,ownershort),

                    print "<span title='%s/%s s'>" % (cput, walltime),
                    if effic < .8:
                        print "<font color='gray'>",
                    else:
                        if effic > 1.0:
                            print "<font color='red'>",
                        else:
                            print "<font color='black'>",
                            
                    print "%7.2f%%</font> " % (effic*100.0),
                    print "</span>",
                    
                    
                    if mem > memreq and memreq > 0.0:
                        print "<font color='red'>",
                    else:
                        if mem < 0.5*memreq:
                            print "<font color='gray'>",
                        else:
                            print "<font color='black'>",
                    

                    print "%.2f/%.2f GB</font>" %(mem,memreq)
                print "</span>"
                print "</td>"
            if (count and ((count%GRID_COLS))==GRID_COLS-1):
                print "<!-- ",count,"!-->\n"
                print "</tr>\n<tr>\n"
            count=count+1


print "</table></body></html>"