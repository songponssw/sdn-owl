#list interfaces
len=${#eth[@]}

service NetworkManager stop
ovs-ctl start

#config IP & UP OpenFlow Switch
ifconfig ofswitch ${ip} netmask ${mask}
ifconfig ofswitch up
route add default gw ${gateway} ofswitch

# for (( i=0; i<${len}; i++ ));
# do
#     ifconfig ${eth[$i]} 0
# done
