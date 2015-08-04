from suds.client import Client
from suds.xsd.doctor import ImportDoctor,Import
#url = 'http://dsc.exclouds.com:8080/mydsc/DomainnameInfoWebService.cis?wsdl'
#url='http://dsc.exclouds.com:8080/mydsc/PlantInfoWebService.cis?wsdl'
#url ='http://127.0.0.1:8080/pushtask/XmlSynchronousWebService.cis?wsdl'

#url ='http://service.exclouds.com:44100/XmlSynchronousWebService.cis?wsdl'
url ='http://118.244.210.10:42123/XmlSynchronousWebService.cis?wsdl'

imp = Import('http://bean.cdn.excloud.com')
imp.filter.add('http://services.spring.excloud.com')
d= ImportDoctor(imp)
client = Client(url,doctor=d,timeout=20)
#print client


#result = client.service.findDeviceByPage('',2,2,'')
#print result

#map ={'plantid':'28','view':'jiangxi'}
#param = client.factory.create(map)
#param.plantid = '28'
#param = client.factory.create('ns0:PortInfo')
#param.view='jiangxi'
#param.port_devid=8
#param.port_name='test22Update'
#param.dev_ipid=12
#param.dev_ip='127.0.0.1'

#client.service.updateById(param)
#client.service.deleteById(1)


result=client.service.getXmlSynchronous()
print result
print len(result)
