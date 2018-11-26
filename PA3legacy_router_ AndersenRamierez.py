#!/usr/bin/python
# Diana Andersen & Jose Ramierez

from mininet.topo import Topo
from mininet.net import Mininet
from mininet.node import Node
from mininet.log import setLogLevel, info
from mininet.cli import CLI

class LinuxRouter( Node ):    # A Node with IP forwarding enabled.

    def config( self, **params ):
        super( LinuxRouter, self).config( **params )
        self.cmd( 'sysctl net.ipv4.ip_forward=1' )  # Enable forwarding on the router

    def terminate( self ):
        self.cmd( 'sysctl net.ipv4.ip_forward=0' )
        super( LinuxRouter, self ).terminate()

class NetworkTopo( Topo ):  # A LinuxRouter connecting three IP subnets

    def build( self, **_opts ):

        defaultIP = '192.168.1.1/24'  # IP address for r0-eth1
        router = self.addNode( 'r0', cls=LinuxRouter, ip=defaultIP )

        # Creating two switches
        s1, s2 = [ self.addSwitch( s ) for s in 's1', 's2' ]

        self.addLink( s1, router, intfName2='r0-eth1',
                      params2={ 'ip' : defaultIP } )  # for clarity
        self.addLink( s2, router, intfName2='r0-eth2',
                      params2={ 'ip' : '172.16.0.1/12' } )

        # Adding hosts h1 and h2
        h1 = self.addHost( 'h1', ip='192.168.1.100/24',
                           defaultRoute='via 192.168.1.1' )
        h2 = self.addHost( 'h2', ip='172.16.0.100/12',
                           defaultRoute='via 172.16.0.1' )

        # Linking the hosts to the subnets
        for h, s in [ (h1, s1), (h2, s2)]:
            self.addLink( h, s )

def run():
    topo = NetworkTopo()
    net = Mininet( topo=topo )  # controller is used by s1-s2
    net.start()

#   For debugging
#   info( '*** Routing Table on Router:\n' )
#   print net[ 'r0' ].cmd( 'route' )

    CLI( net )
    net.stop()

if __name__ == '__main__':
    setLogLevel( 'info' )
    run()
