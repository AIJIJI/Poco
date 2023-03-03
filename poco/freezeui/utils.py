# coding=utf-8

from poco.freezeui.hierarchy import FrozenUIDumper,FrozenUIHierarchy
from poco.freezeui.ImmutableFrozenUIDumper import ImmutableFrozenUIDumper

__all__ = ['create_immutable_hierarchy', 'create_immutable_dumper']


def create_immutable_hierarchy(hierarchy_dict):
    dumper = create_immutable_dumper(hierarchy_dict)
    return FrozenUIHierarchy(dumper)


def create_immutable_dumper(hierarchy_dict):
    return ImmutableFrozenUIDumper(hierarchy_dict)
