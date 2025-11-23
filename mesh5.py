from mininet.net import Mininet
from mininet.node import Controller
from mininet.link import TCLink
from mininet.log import setLogLevel, info
from mininet.topo import Topo
import time
import os

class Mesh5Topo(Topo):
    def build(self):
        hosts = [self.addHost(f'h{i+1}') for i in range(5)]
        for i in range(len(hosts)):
            for j in range(i+1, len(hosts)):
                self.addLink(hosts[i], hosts[j], cls=TCLink, bw=10, delay='5ms')

def run():
    os.makedirs("results", exist_ok=True)

    topo = Mesh5Topo()
    net = Mininet(topo=topo, controller=Controller, link=TCLink)
    net.start()

    h1 = net.get('h1')
    h2 = net.get('h2')

    info('*** Starting packet capture with tcpdump\n')
    h1.cmd('tcpdump -i h1-eth0 -w results/mesh5_capture.pcap &')
    time.sleep(1)  # Ensure tcpdump has started

    info('*** Testing connectivity with ping\n')
    ping_result = h1.cmd(f'ping -c 5 {h2.IP()}')
    with open('results/ping_output_5.txt', 'w') as f:
        f.write(ping_result)

    info('*** Running TCP iperf\n')
    h1.cmd('iperf -s > results/tcp_server_5.txt &')
    time.sleep(2)
    h2.cmd(f'iperf -c {h1.IP()} -t 10 > results/tcp_result_5.txt')

    info('*** Running UDP iperf with limited rate\n')
    h1.cmd('iperf -u -s > results/udp_server_5.txt &')
    time.sleep(2)
    h2.cmd(f'iperf -u -c {h1.IP()} -b 1M -t 10 -l 1400 -P 5 > results/udp_result_5.txt')

    info('*** Stopping tcpdump\n')
    h1.cmd('pkill -f tcpdump')

    info('*** Simulation complete\n')
    net.stop()

if __name__ == '__main__':
    setLogLevel('info')
    run()
