# coding=utf-8
__author__ = 'lxn3032'


import os
import time
import numbers
import warnings

from poco import Poco
from poco.exceptions import InvalidOperationException
from rpc import AndroidRpcClient

from airtest.core.android import Android, ADB
from airtest.core.android.ime_helper import YosemiteIme
from poco.vendor.android.utils.installation import install


this_dir = os.path.dirname(os.path.realpath(__file__))
PocoServicePackage = 'com.netease.open.pocoservice'
PocoServicePackageTest = 'com.netease.open.pocoservice.test'


class AndroidUiautomationPoco(Poco):
    def __init__(self, serial=None):
        # TODO: 临时用着airtest的方案
        self.android = Android(serial, init_display=False, minicap=False, minicap_stream=False, minitouch=False, shell_ime=False)
        self.adb_client = self.android.adb
        if not serial:
            devices = self.adb_client.devices("device")
            if len(devices) == 0:
                raise RuntimeError('No available device connected. Please check your adb connection.')
            elif len(devices) > 1:
                raise RuntimeError('Too much devices connected. Please specified one by serialno.')
            self.adb_client.set_serialno(devices[0][0])

        # install ime
        self.ime = YosemiteIme(self.android)
        self.ime.start()

        # install
        updated = install(self.adb_client, os.path.join(this_dir, 'lib', 'pocoservice-debug.apk'))
        install(self.adb_client, os.path.join(this_dir, 'lib', 'pocoservice-debug-androidTest.apk'), updated)

        # forward
        try:
            self.adb_client.forward("tcp:10081", "tcp:10081")  # TODO： 处理本地端口被占用的情况
        except:
            pass

        # start
        if updated or not self._is_running(PocoServicePackage):
            if self._is_running('com.github.uiautomator'):
                warnings.warn('{} should not run together with "uiautomator". "uiautomator" will be killed.'
                              .format(self.__class__.__name__))
                self.adb_client.shell(['am', 'force-stop', 'com.github.uiautomator'])

            self.adb_client.shell(['am', 'force-stop', PocoServicePackage])
            self.instrument_proc = self.adb_client.shell([
                'am', 'instrument', '-w', '-e', 'class',
                '{}.InstrumentedTestAsLauncher#launch'.format(PocoServicePackage),
                '{}.test/android.support.test.runner.AndroidJUnitRunner'.format(PocoServicePackage)],
                not_wait=True)
            time.sleep(3.5)  # TODO： 通过shell的输出判断要等多久，或者用ping检测

        endpoint = "http://127.0.0.1:10081"
        rpc_client = AndroidRpcClient(endpoint, self.ime)
        super(AndroidUiautomationPoco, self).__init__(rpc_client)

    def _is_running(self, package_name):
        processes = self.adb_client.shell(['ps']).splitlines()
        for ps in processes:
            ps = ps.strip()
            if ps.endswith(package_name):
                return True
        return False

    def click(self, pos):
        if not (0 <= pos[0] <= 1) or not (0 <= pos[1] <= 1):
            raise InvalidOperationException('Click position out of screen. {}'.format(pos))
        self.rpc.click(*pos)

    def swipe(self, p1, p2=None, direction=None, duration=1.0):
        if not (0 <= p1[0] <= 1) or not (0 <= p1[1] <= 1):
            raise InvalidOperationException('Swipe origin out of screen. {}'.format(p1))
        if p2:
            sp2 = p2
        elif direction:
            sp2 = [p1[0] + direction[0], p1[1] + direction[1]]
        else:
            raise RuntimeError("p2 and direction cannot be None at the same time.")
        self.rpc.swipe(p1[0], p1[1], sp2[0], sp2[1], duration)

    def long_click(self, pos, duration=3.0):
        if not (0 <= pos[0] <= 1) or not (0 <= pos[1] <= 1):
            raise InvalidOperationException('Click position out of screen. {}'.format(pos))
        self.rpc.long_click(pos[0], pos[1], duration)

    def snapshot(self, width=720):
        # snapshot接口暂时还补统一
        if not isinstance(width, numbers.Number):
            return None

        return self.rpc.get_screen(int(width))
