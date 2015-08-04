#!/bin/sh



if [ $# -ne 2 ];then
	printf "USAGE:	$0 ct:eth0 cnc:eth1 TAG1\n"
	exit 1
elif [ `echo $1|egrep -i "ct|cnc"` ] && [ `echo $2|egrep -i "ct|cnc"` ];then
	if [ `echo $1|cut -f 1 -d :` = "ct" ] || [ `echo $1|cut -f 1 -d :` = "CT" ];then
		CT_DEV=`echo $1|cut -f 2 -d :`
		if [ `echo $2|cut -f 1 -d :` != "cnc" ] && [ `echo $2|cut -f 1 -d :` != "CNC" ];then
			printf "USAGE:	$0 ct:eth0 cnc:eth1 TAG2\n"
			exit 1
		else
			CNC_DEV=`echo $2|cut -f 2 -d :`
		fi
	fi
	if [ `echo $1|cut -f 1 -d :` = "cnc" ] || [ `echo $1|cut -f 1 -d :` = "CNC" ];then
		CNC_DEV=`echo $1|cut -f 2 -d :`
		if [ `echo $2|cut -f 1 -d :` != "ct" ] && [ `echo $2|cut -f 1 -d :` != "CT" ];then
			printf "USAGE:	$0 ct:eth0 cnc:eth1 TAG3\n"
			exit 1
		else
			CT_DEV=`echo $2|cut -f 2 -d :`
		fi
	fi
else
	printf "USAGE:	$0 ct:eth0 cnc:eth1 TAG4\n"
	exit 1
fi

echo "CT_DEV:"$CT_DEV
echo "CNC_DEV:"$CNC_DEV

CT_IP=`/sbin/ifconfig ${CT_DEV}|grep "inet addr"|cut -f 2 -d : |cut -f 1 -d " "`
if [ ! $CT_IP ];then
	echo "Wrong interface $CT_DEV,please check again"
	exit 1
fi

CT_GW=`egrep "GATEWAY" /etc/sysconfig/network-scripts/ifcfg-${CT_DEV}|cut -f 2 -d =`

CNC_IP=`/sbin/ifconfig ${CNC_DEV}|grep "inet addr"|cut -f 2 -d : |cut -f 1 -d " "`
if [ ! $CNC_IP ];then
	echo "Wrong interface $CNC_DEV,please check again"
	exit 1
fi

CNC_GW=`egrep "GATEWAY" /etc/sysconfig/network-scripts/ifcfg-${CNC_DEV}|cut -f 2 -d =`

echo "CT_IP:"$CT_IP
echo "CT_GW:"$CT_GW
echo "CNC_IP:"$CNC_IP
echo "CNC_GW:"$CNC_GW


if [ -z "`egrep "252     tel" /etc/iproute2/rt_tables`" ];then
	echo "252     tel" >> /etc/iproute2/rt_tables
fi
if [ -z "`egrep "251     cnc" /etc/iproute2/rt_tables`" ];then
	echo "251     cnc" >> /etc/iproute2/rt_tables
fi


ip route flush table tel
ip rule add from ${CT_IP} table tel
ip route add default via ${CT_GW} dev ${CT_DEV} src ${CT_IP} table tel

ip route flush table cnc
ip rule add from ${CNC_IP} table cnc
ip route add default via ${CNC_GW} dev ${CNC_DEV} src ${CNC_IP} table cnc
