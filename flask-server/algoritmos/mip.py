
import pyphi
network = pyphi.network.from_json('C:/Users/PC RYZEN/Documents/UdC/Analisis/network2.json')
networkRG4L = pyphi.Network(network.get('tpm'), cm=network.get('cm'), node_labels=network.get('labels'))

state = (0, 0, 0, 0)
node_indices = ("A","B","C","D")

subsystem = pyphi.Subsystem(networkRG4L, network.get('state'), network.get('labels'))

A, B, C, D = subsystem.node_indices
print(subsystem.state)
mechanism = (A, B, C, D)
purview = (A, B, C, D)

mip = subsystem.cause_mip(mechanism, purview)

print(mip.partition)
print(subsystem.tpm)



