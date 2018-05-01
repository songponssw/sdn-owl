ovs-ctl start
eth=(enp1s0 enp5s1 enp5s2)
len=${#eth[@]}

ovs-vsctl add-br ofswitch -- set bridge ofswitch protocols=OpenFlow10,OpenFlow11,OpenFlow12,OpenFlow13
for (( i=0; i<${len}; i++ ));
do
  ovs-vsctl add-port ofswitch ${eth[$i]} -- set interface ${eth[$i]} ofport=$[$i+1]
done

ovs-vsctl set-controller ofswitch tcp:192.168.1.31:6653
ovs-vsctl set-fail-mode ofswitch secure


