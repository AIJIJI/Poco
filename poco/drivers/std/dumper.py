# coding=utf-8
from poco.freezeui.hierarchy import FrozenUIDumper
from poco.freezeui.hierarchy import Node
from poco.utils.simplerpc.utils import sync_wrapper
from poco.drivers.std.HierarchyTranslator import *
import traceback
import sys

class StdDumper(FrozenUIDumper):
    def __init__(self, rpcclient):
        super(StdDumper, self).__init__()
        self.rpcclient = rpcclient

    @sync_wrapper
    def dumpHierarchy(self, onlyVisibleNode=True):
        return self.rpcclient.call("Dump", onlyVisibleNode)
    def getRoot(self):
        """
        Dump a hierarchy immediately from target runtime and store into a Node (subclass of :py:class:`AbstractNode
        <poco.sdk.AbstractNode>`) object.

        Returns:
            :py:class:`inherit from AbstractNode <Node>`: Each time a new node instance is created by latest hierarchy
             data.
        """
       
        tmp =self.dumpHierarchy()
       	
        dumpResult = translator_agent.Translate(tmp)

        root = Node(dumpResult)

        self._linkParent(root)
        return root