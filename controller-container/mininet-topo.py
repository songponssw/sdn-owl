# Create Mininet Topo for testing controller.py
from mininet.topo import Topo


class MyTopo(Topo):
    def __init__(self):
        # Initialize topology
        Topo.__init__(self)

        # Add hosts and switches
        controller = self.addHost('c0')
        host1 = self.addHost('h1')
        host2 = self.addHost('h2')

        switch1 = self.addSwitch('s1')
        switch2 = self.addSwitch('s2')

        # Add links
        self.addLink(host1, switch1)
        self.addLink(host2, switch2)
        self.addLink(switch1, switch2)
        self.addLink(controller, switch1)


topos = {'mytopo': (lambda: MyTopo())}
