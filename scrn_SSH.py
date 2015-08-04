#encoding utf-8

from suds.client import Client
from suds.xsd.doctor import ImportDoctor,Import
from multiprocessing import Pool,Manager
import time,paramiko,os,sys,logging

logging.basicConfig(level=logging.CRITICAL,
                format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',
                datefmt='%a, %d %b %Y %H:%M:%S',
                filename='lowpasswd.log',
                filemode='w')

def get_interwork(ip_list):
    url='http://service.exclouds.com:44100/IpInfoWebService.cis?wsdl'
    imp = Import('http://bean.cdn.excloud.com')
    imp.filter.add('http://services.spring.excloud.com')
    d = ImportDoctor(imp)
    client = Client(url,doctor=d,timeout=20)
    ip_obj = client.service.queryOnlineIp()
    for ip_obj in ip_obj.IpInfo:
        ip_list.append(ip_obj.ipf_ip)
    if ip_list:
        return True
    else:
        return False

def work(queue,passwd_list):
    while(1):
        ip_list = get_work(queue)
        if not ip_list:
            break
        for ip in ip_list:
            do_work(ip,passwd_list)
    
def do_work(ip,passwd_list):
    for passwd in passwd_list:
        sshconnect(ip,str(passwd))
    
def sshconnect(hostname,password = "123456"):
    msg = ''
    try:
        client = paramiko.SSHClient()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        client.connect(hostname,22,'root',password=password)
        client.close()
	msg = '%s login sucess by %s'%(hostname,password)
	logging.critical(msg)
    except Exception as e:
        client.close()
    
def put_work(queue,ip_list):
    for ip in ip_list:
       queue.put(ip)
       
def get_work(queue):
    ip_list= []
    num_ip = 5
    if queue.empty():
        return ip_list
    if queue.qsize() < 5 :
        num_ip = queue.size()
    for i in range(num_ip):
        value = queue.get(False)
        ip_list.append(value)
    return  ip_list

def get_passwdlist():
    passwd_list = []
    passwd_finename = "./passwd.conf"
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
    passwd_list = []
    manager = Manager()
    queue = manager.Queue()
    get_interwork(ip_list)
    passwd_list = get_passwdlist()
    if not passwd_list:
        logging.critical("No passwd.conf or passwd.conf has no passwd at least!!")
        sys.exit()
    if not ip_list:
        logging.critical("service.exclouds.com get no IP,Please call Chenyilin!!")
        sys.exit()
    #ip_list = ["222.219.187.107","222.219.187.108","118.122.36.207","118.122.36.209","118.122.36.211"]
    put_work(queue,ip_list)
    progress = Pool()
    for num_progress in range(5):
        progress.apply_async(work, args=(queue,passwd_list,))
    progress.close()
    progress.join()
    time2 = time.time()
    lasttime =  int(time2-time1)
    end_msg = "=======================End Check(%ds)=======================" %(lasttime)
    logging.critical(end_msg)
    print "ALL down"
    







