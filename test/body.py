# coding=utf-8


import time

# from tokenid import tokenid, tokenid_g18, tokenid_for_mh
from hunter_cli import Hunter, open_platform
from poco.utils.airtest import AirtestPoco

if __name__ == '__main__':
    tokenid = open_platform.get_api_token('poco-test')
    # hunter = Hunter(tokenid, 'g62', devid='g62_at_408d5c117d0f')
    hunter = Hunter(tokenid, 'g62', devid='g62_at_408d5c117d0f')
    poco = AirtestPoco('g62', hunter)

    # print poco(textMatches='.*入游戏').get_text()
    for n in poco('entry_bg'):
        print n.get_position()

    t0 = time.time()
    with poco.freeze() as pz:
        for n in pz('entry_bg'):
            print n.get_position()
    t1 = time.time()
    print t1 - t0

    # t0 = time.time()
    # for n in poco('entry_bg'):
    #     print n
    # t1 = time.time()
    # print t1 - t0

    # poco = NeteasePoco('g18', hunter)
    # from airtest.core.main import set_serialno
    # set_serialno()
    # ap('HeroIcon').click()
    # ap('Close').click()
    # panels = poco('MainPanel').offspring('Panel').child('Panel')
    # print len(panels.nodes)
    # n = panels.nodes[1]
    # print n
    # # n = panels[1].nodes
    #
    # poco = CocosJsPoco()
    # for p in poco():
    #     print p
