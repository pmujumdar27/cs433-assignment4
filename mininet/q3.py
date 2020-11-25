from mininet.net import Mininet
from mininet.topo import Topo
from mininet import cli

net = Mininet()

s1 = net.addSwitch( 's1' )
c0 = net.addController( 'c0' )

h1 = net.addHost('h1')
h2 = net.addHost('h2')
h3 = net.addHost('h3')
h4 = net.addHost('h4')
h5 = net.addHost('h5')
h6 = net.addHost('h6')

net.addLink(h1, s1)
net.addLink(h2, s1)
net.addLink(h3, s1)
net.addLink(h4, s1)
net.addLink(h5, s1)
net.addLink(h6, s1)

net.start()

print("Mininet started")
# cli.CLI(net)
print(h1.cmd("nohup sudo python3 ./tcp_server_sc_thread.py &"))
print("server started")
print(h2.cmdPrint("sudo python3 ./tcp_client_sc_thread.py 1 square_root_of_4.txt > out.txt &"))
print(h3.cmdPrint("sudo python3 ./tcp_client_sc_thread.py 1 checkmate.txt > out.txt &"))
print(h4.cmdPrint("sudo python3 ./tcp_client_sc_thread.py 1 pi.txt > out.txt &"))
print(h5.cmdPrint("sudo python3 ./tcp_client_sc_thread.py 1 shakespear.txt > out.txt &"))
print(h6.cmdPrint("sudo python3 ./tcp_client_sc_thread.py 1 war_and_peace.txt > out.txt &"))
print("Done")
cli.CLI(net)
print("Done final")

net.stop()