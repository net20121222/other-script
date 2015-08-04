#encoding utf-8

from suds.client import Client
from suds.xsd.doctor import ImportDoctor,Import
from multiprocessing import Pool,Manager
import time,paramiko,os,sys,logging,socket,re
#socket.setdefaulttimeout(1)
logging.basicConfig(level=logging.CRITICAL,
                format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',
                datefmt='%a, %d %b %Y %H:%M:%S',
                filename='dport.log',
                filemode='w')

def get_ip_address():
    ip = os.popen("/sbin/ifconfig | grep 'inet addr' | awk '{print $2}'").read()
    ip = ip[ip.find(':')+1:ip.find('\n')]
    return ip

def checkip(ip):
    p = re.compile('^(([01]?\d\d?|2[0-4]\d|25[0-5])\.){3}([01]?\d\d?|2[0-4]\d|25[0-5])$')
    if p.match(ip):
        return True
    else:
        return False 

def get_interwork(ip_list,ip):
    url='http://service.exclouds.com:44100/IpInfoWebService.cis?wsdl'
    imp = Import('http://bean.cdn.excloud.com')
    imp.filter.add('http://services.spring.excloud.com')
    d = ImportDoctor(imp)
    client = Client(url,doctor=d,timeout=20)
    ip_obj = client.service.findlabIps(ip)
    for ip_obj in ip_obj.IpInfo:
        ip_list.append(ip_obj.ipf_ip)
    if ip_list:
        return True
    else:
        return False

def work(queue,portlist):
    while(1):
        ip_list = get_work(queue)
        if not ip_list:
            break
        for ip in ip_list:
            do_work(ip,portlist)
    
def do_work(ip,portlist):
    scanner(ip,portlist)

def scanner(ip,portlist):
    alarmports = []
    for port in range(65535):
        try:
            s=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            _port = str(port)
            if _port not in portlist:
                a = s.connect((ip, port))
                alarmports.append(port)
            s.close()
        except Exception,e:
            s.close()
            continue
    errormsg = ''
    if len(alarmports) != 0:
	logging.critical('%s:%s'%(ip,alarmports))
    
def put_work(queue,ip_list):
    for ip in ip_list:
       queue.put(ip)
       
def get_work(queue):
    ip_list= []
    num_ip = 1
    if queue.empty():
        return ip_list
    if queue.qsize() < 1 :
        num_ip = queue.size()
    for i in range(num_ip):
        value = queue.get(False)
        ip_list.append(value)
    return  ip_list

def get_portlist():
    passwd_list = []
    passwd_finename = "./safeport.conf"
    if not os.path.exists(passwd_finename):
        return passwd_list
    else:
        try:
            with open(passwd_finename) as passwd_fd:
                for lineinfo in passwd_fd:
                    passwd_list.append(lineinfo.strip("\n").strip("\r\n"))
                return passwd_list
        except:
            return passwd_list
    
if __name__ == '__main__':
    print "Start work..."
    logging.critical("=======================Start Check=======================")
    time1 = time.time()
    ip_list = []
    manager = Manager()
    queue = manager.Queue()
    local_ip = get_ip_address()
    if not checkip(local_ip):
        logging.critical("local_ip is error")
        sys.exit()
    get_interwork(ip_list,local_ip)
    portlist = get_portlist()
    if not ip_list:
        logging.critical("service.exclouds.com get no IP,Please call Chenyilin!!")
        sys.exit()
    #ip_list = ["222.219.187.107","222.219.187.108","118.122.36.207","118.122.36.209","118.122.36.211"]
    put_work(queue,ip_list)
    progress = Pool()
    for num_progress in range(5):
        progress.apply_async(work, args=(queue,portlist,))
    progress.close()
    progress.join()
    time2 = time.time()
    lasttime =  int(time2-time1)
    end_msg = "=======================End Check(%ds)=======================" %(lasttime)
    logging.critical(end_msg)
    print "ALL down"
    







