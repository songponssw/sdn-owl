#list information
echo "List interfaces that you would like to add in OF Switch"
echo "ex: eth0 eth1 ...."
read -a eth
len=${#eth[@]}

eth_out=""
for (( i=0;i<len;i++))
do
    eth_out="$eth_out${eth[$i]} "
done

echo "Enter gateway IP"
read gateway

echo "Enter Controller IP"
read controller

echo "Enter Switch IP"
read ip

echo "Enter Switch Subnet Mask (ex. 255.255.255.xxx)"
read mask

#echo to file 
printf "eth=%s\ngateway=%s\nip=%s\nmask=%s\nlen=%s\nctrl=%s\n" "$eth_out" "$gateway" "$ip" "$mask" "$len" "$controller" > run.sh

#checking interface exist 

cat ovs-start.sh >> run.sh

