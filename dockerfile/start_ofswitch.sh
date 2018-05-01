eth=(enp1s0 enp5s1 enp5s2)
len=${#eth[@]}

service NetworkManager stop
ovs-ctl start

for (( i=0; i<${len}; i++ ));
do
    ifconfig ${eth[$i]} 0
done
ifconfig ofswitch up

ifconfig ofswitch 192.168.1.32 netmask 255.255.255.0
route add default gw 192.168.1.1 ofswitch
