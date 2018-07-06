len=${#eth[@]}

service NetworkManager stop
ovs-ctl start

for (( i=0; i<${len}; i++ ));
do
    ifconfig ${eth[$i]} 0
done
ifconfig ofswitch up

ifconfig ofswitch ${ip} netmask ${mask}
route add default gw ${gateway} ofswitch