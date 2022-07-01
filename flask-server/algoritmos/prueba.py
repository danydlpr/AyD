import pyphi
import numpy as np

tpm = np.array([
        [0.0, 0.0, 0.0],
        [0.0, 0.0, 1.0],
        [1.0, 0.0, 1.0],
        [1.0, 0.0, 0.0],
        [1.0, 0.0, 0.0],
        [1.0, 1.0, 1.0],
        [1.0, 0.0, 1.0],
        [1.0, 1.0, 0.0]
        ])
cm = np.array([
        [0, 1, 1],
        [1, 0, 1],
        [1, 1, 0]
    ])

network = pyphi.Network(tpm, cm=cm, node_labels=['A', 'B', 'C'])


subsystem = pyphi.Subsystem(network, [1, 0, 0], network.node_labels)

import numpy as np
import h5py
f = h5py.File('sample_timeseries.mat','r')
data = f.get('data/variable1')
data = np.array(data) # For converting to a NumPy array