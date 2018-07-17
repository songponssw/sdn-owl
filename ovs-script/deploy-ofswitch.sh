#list information
echo "List interfaces that you would like to add in OF Switch"
echo "ex: eth0 eth1 ...."
read -a eth
len=${#eth[@]}

echo "Enter gateway IP"
read gateway

echo "Enter Switch IP"
read ip

echo "Enter Switch Subnet Mask (ex. 255.255.255.xxx)"
read mask


#checking interface exist 


#create & configure OpenFlow Switch
ovs-vsctl add-br ofswitch -- set bridge ofswitch protocols=OpenFlow10,OpenFlow11,OpenFlow12,OpenFlow13
ovs-vsctl set-controller ofswitch tcp:${ip}:6653
ovs-vsctl set-fail-mode ofswitch secure

#add interface to OpenFlow Switch
for (( i=0; i<${len}; i++ ));
do
  ovs-vsctl add-port ofswitch ${eth[$i]} -- set interface ${eth[$i]} ofport=$[$i+1]
done

#start & off service
service NetworkManager stop
ovs-ctl start

#config IP & UP OpenFlow Switch
ifconfig ofswitch ${ip} netmask ${mask}
ifconfig ofswitch up
route add default gw ${gateway} ofswitch
