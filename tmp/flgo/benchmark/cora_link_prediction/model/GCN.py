import torch
from torch_geometric.nn import GCNConv
from flgo.utils.fmodule import FModule

class Model(FModule):
    def __init__(self):
        super(Model, self).__init__()
        self.conv1 = GCNConv(1433, 128)
        self.conv2 = GCNConv(128, 64)

    def encode(self, x, edge_index):
        x = self.conv1(x, edge_index)
        x = x.relu()
        return self.conv2(x, edge_index)

    def decode(self, z, edge_label_index):
        return (z[edge_label_index[0]] * z[edge_label_index[1]]).sum(dim=-1)

    def decode_all(self, z):
        prob_adj = z @ z.t()
        return (prob_adj > 0).nonzero(as_tuple=False).t()

def init_local_module(object):
    pass

def init_global_module(object):
    if 'Server' in object.__class__.__name__:
        object.model = Model().to(object.device)