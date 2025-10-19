# SDN Owl
   SDN Owl is tool for set up the SDN testbed (especially in SDN Switch) using Ansible and Docker. We choose OpenVSwitch to be SDN Switches in testbed. We provide 2 version of OVS Deployments. 
   * Direct version : deploy OVS directly to hosts/hardware.
   * Container version : deploy OVS inside Docker container.

### Deployment
1. Install prerequisite :
```bash
    cd ansible-script 
    ansible-playbook -i hosts run.yml
        - Select 1 for prerequisites installation.
        - Enter 2 for list host/target interfaces that you would like to add in swith
```
2. Generate Deploy script 
```bash
    cd ovs-script
    bash deploy-ofswitch.sh
```
3. Deploy script 
    * Direct version : Go to switch nodes. Then `./deploy_ofswitch.sh`
    * Container version : Go to switch nodes.
        ```bash
            docker pull cyborgcat/sdn-owl_switch
            docker run .......
        ```
4. Start controller 

