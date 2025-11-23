from mininet.net import Mininet
from mininet.node import Controller
from mininet.link import TCLink
from mininet.log import setLogLevel, info
from mininet.topo import Topo
import time
import os

class Mesh15Topo(Topo):
    def build(self):
        hosts = [self.addHost(f'h{i+1}') for i in range(15)]
        for i in range(len(hosts)):
            for j in range(i+1, len(hosts)):
                self.addLink(hosts[i], hosts[j], cls=TCLink, bw=10, delay='5ms')

def run_simulation():
    os.makedirs('results', exist_ok=True)

    topo = Mesh15Topo()
    net = Mininet(topo=topo, controller=Controller, link=TCLink)
    net.start()

    h1, h2 = net.get('h1'), net.get('h2')

    info('\n*** Starting traffic capture with tcpdump\n')
    h1.cmd('tcpdump -i h1-eth0 -w results/mesh15_capture.pcap &')
    time.sleep(1)

    info('\n*** Starting ping connectivity test between h1 and h2\n')
    ping_result = h1.cmd(f'ping -c 5 {h2.IP()}')
    with open('results/ping_output_15.txt', 'w') as f:
        f.write(ping_result)

    info('\n*** Running TCP test using iperf\n')
    h1.cmd('iperf -s > results/tcp_server_15.txt &')
    time.sleep(2)
    h2.cmd(f'iperf -c {h1.IP()} -t 10 > results/tcp_result_15.txt')

    info('\n*** Running UDP test using iperf\n')
    h1.cmd('iperf -u -s > results/udp_server_15.txt &')
    time.sleep(2)
    h2.cmd(f'iperf -u -c {h1.IP()} -b 1M -t 10 > results/udp_result_15.txt')

    info('\n*** Stopping tcpdump traffic capture\n')
    h1.cmd('pkill -f tcpdump')

    info('\n*** Simulation completed\n')
    net.stop()

if __name__ == '__main__':
    setLogLevel('info')
    run_simulation()
