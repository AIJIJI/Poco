
from poco.freezeui.hierarchy import FrozenUIHierarchy, FrozenUIDumper

class ImmutableFrozenUIDumper(FrozenUIDumper):
    hierarchy_dict = ""

    def __init__(self, hierarchy_dict):
        super(ImmutableFrozenUIDumper, self).__init__()
        self.hierarchy_dict = hierarchy_dict

    def dumpHierarchy(self, onlyVisibleNode=True):
        return self.hierarchy_dict
