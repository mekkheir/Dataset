#!/usr/bin/python

from mininet.net import Mininet
from mininet.node import Controller, OVSKernelSwitch
from mininet.cli import CLI
from mininet.link import TCLink, Intf
from mininet.log import setLogLevel, info
from mn_wifi.net import Mininet_wifi
from mn_wifi.cli import CLI
from mn_wifi.link import wmediumd
from mn_wifi.wmediumdConnector import interference
from mn_wifi.v2g import EV, SE
from subprocess import call


def myNetwork():

    net = Mininet_wifi(topo=None,
                       build=False,
                       ipBase='10.0.0.0/8')

    info( '*** Adding controller\n' )
    c0 = net.addController(name='c0',
                           controller=Controller,
                           protocol='tcp',
                           port=6633)

    info( '*** Add switches/APs\n')
    s1 = net.addSwitch('s1', cls=OVSKernelSwitch)

    info( '*** Add hosts/stations/EVs/SEs\n')
    se1 = net.addHost('se1', cls=SE, ip='10.0.0.1', defaultRoute=None)
    ev1 = net.addHost('ev1', cls=EV, ip='10.0.0.2', defaultRoute=None)
    ev2 = net.addHost('ev2', cls=EV, ip='10.0.0.3', defaultRoute=None)

    info( '*** Add links\n')
    net.addLink(se1, s1)
    net.addLink(s1, ev1)
    net.addLink(s1, ev2)

    info( '*** Starting network\n')
    net.build()
    info( '*** Starting controllers\n')
    for controller in net.controllers:
        controller.start()

    info( '*** Starting switches/APs\n')
    net.get('s1').start([c0])

    info( '*** Post configure nodes\n')

    CLI(net)
    net.stop()


if __name__ == '__main__':
    setLogLevel( 'info' )
    myNetwork()

