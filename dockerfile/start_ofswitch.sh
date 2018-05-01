eth=(eno1 enp2s0 enp3s0)
len=${#eth[@]}

service NetworkManager stop
ovs-ctl start

for (( i=0; i<${len}; i++ ));
do
    ifconfig ${eth[$i]} 0
done
ifconfig ofswitch up

ifconfig ofswitch 192.168.1.33 netmask 255.255.255.0
route add default gw 192.168.1.1 ofswitch
