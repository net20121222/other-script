def get_running_progress(dirc_run,szProName):
    list_run = os.listdir("/proc")
    list_run = filter(lambda x:x.isdigit(),list_run)
    for i in xrange(len(list_run)):
        szPidTmpName = "/proc/%s/exe" %list_run[i]
        if not os.path.exists(szPidTmpName):
            continue         
        szProTmpName = os.readlink(szPidTmpName)        
        if not cmp(szProName,szProTmpName):
            dirc_run[list_run[i]] = szProTmpName
    return 0   
	
def RunningStatus():
    iPid = os.getpid()
    print "%d======" %(iPid)
    szPidName = "/proc/%d/exe" %iPid
    szProName = os.readlink(szPidName)
    dirc_run = {}
    get_running_progress(dirc_run,szProName)
    if len(dirc_run) > 1:
        print "The progress is working,please close it"
        for key,value in dirc_run.iteritems():
            if iPid == key.atoi():
                continue
            else:
                print "Progress ID:%s    Progress Name:%s" %(key,value)
        return False
    else:
        print "Progress start"
        return True
		
