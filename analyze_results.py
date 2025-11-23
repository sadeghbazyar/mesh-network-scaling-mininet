import matplotlib.pyplot as plt
import re
import os

def extract_ping_delay_and_loss(filename):
    if not os.path.exists(filename):
        print(f"[!] File not found: {filename}")
        return None, None
    try:
        with open(filename) as f:
            text = f.read()
        delay_match = re.search(r'rtt\s+min/avg/max/mdev\s+=\s+\d+\.\d+/(\d+\.\d+)/\d+\.\d+/\d+\.\d+', text)
        delay = float(delay_match.group(1)) if delay_match else None
        loss_match = re.search(r'(\d+)% packet loss', text)
        loss = float(loss_match.group(1)) if loss_match else None
        return delay, loss
    except Exception as e:
        print(f"[!] Error reading {filename}: {e}")
        return None, None

def extract_throughput(filename):
    if not os.path.exists(filename):
        print(f"[!] File not found: {filename}")
        return None
    try:
        with open(filename) as f:
            text = f.read()
        # اولویت با گزارش سرور برای UDP
        udp_server_match = re.search(r'Server Report:\s*\[.*?\].*?(\d+\.\d+)\s+Mbits/sec', text)
        if udp_server_match:
            return float(udp_server_match.group(1))
        # استخراج توان عملیاتی از بخش کلی
        match = re.search(r'\[.*?\]\s+0\.00-\d+\.\d+\s+sec\s+.*?(\d+\.\d+)\s+Mbits/sec', text)
        return float(match.group(1)) if match else None
    except Exception as e:
        print(f"[!] Error reading {filename}: {e}")
        return None

nodes = [5, 10, 15]

delays = []
losses = []
tcp_throughputs = []
udp_throughputs = []

for n in nodes:
    delay, loss = extract_ping_delay_and_loss(f'results/ping_output_{n}.txt')
    delays.append(delay)
    losses.append(loss)
    tcp_throughputs.append(extract_throughput(f'results/tcp_result_{n}.txt'))
    udp_throughputs.append(extract_throughput(f'results/udp_result_{n}.txt'))

print("Delays (ms):", delays)
print("Packet Loss (%):", losses)
print("TCP Throughput (Mbps):", tcp_throughputs)
print("UDP Throughput (Mbps):", udp_throughputs)

plt.figure(figsize=(16, 4))

plt.subplot(1, 4, 1)
plt.plot(nodes, delays, marker='o', color='orange')
plt.title('Average Delay (ms)')
plt.xlabel('Number of Nodes')
plt.ylabel('Delay (ms)')
plt.grid(True)

plt.subplot(1, 4, 2)
plt.plot(nodes, losses, marker='o', color='red')
plt.title('Packet Loss (%)')
plt.xlabel('Number of Nodes')
plt.ylabel('Loss (%)')
plt.grid(True)

plt.subplot(1, 4, 3)
plt.plot(nodes, tcp_throughputs, marker='o', color='blue')
plt.title('TCP Throughput (Mbps)')
plt.xlabel('Number of Nodes')
plt.ylabel('Throughput (Mbps)')
plt.grid(True)

plt.subplot(1, 4, 4)
plt.plot(nodes, udp_throughputs, marker='o', color='green')
plt.title('UDP Throughput (Mbps)')
plt.xlabel('Number of Nodes')
plt.ylabel('Throughput (Mbps)')
plt.grid(True)

plt.tight_layout()
plt.show()