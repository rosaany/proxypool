import sys
import time
import platform
import multiprocessing
from untils.loggings import Logging
from processors.tester import Tester
from processors.server import app
from processors.getter import Getter
from setting import HOST, PORT, GETTER_CYCLE, TESTER_CYCLE, \
    RUN_GETTER, RUN_TESTER, RUN_SERVER

# windows系统时开启，规避不同平台下有概率报错
IS_WINDOWS = platform.system().lower() == 'windows'
if IS_WINDOWS:
    multiprocessing.freeze_support()

tester_process, getter_process, server_process = None, None, None


class Processor:
    def __init__(self):
        self.logger = Logging()

    def run_getter(self):
        if not RUN_GETTER:
            self.logger('Getter module no enabled, exit...')
            return
        getter = Getter()
        loop = 0
        while True:
            getter.run()
            loop += 1
            self.logger.info(f'getter current loop == {loop}')
            time.sleep(GETTER_CYCLE)

    def run_tester(self):
        if not RUN_TESTER:
            self.logger('Tester module no enabled, exit...')
            return
        tester = Tester()
        loop = 0
        while True:
            tester.run()
            loop += 1
            self.logger.info(f'tester current loop == {loop}')
            time.sleep(TESTER_CYCLE)

    def run_server(self):
        if not RUN_SERVER:
            self.logger('Server module no enabled, exit...')
            return
        app.run(host=HOST, port=PORT)

    @property
    def run(self):
        global tester_process, getter_process, server_process
        try:
            if RUN_TESTER:
                tester_process = multiprocessing.Process(target=self.run_tester)
                tester_process.start()
                self.logger.info(f"tester process name {tester_process.name}, pid: {tester_process.pid}")

            if RUN_GETTER:
                getter_process = multiprocessing.Process(target=self.run_getter)
                getter_process.start()
                self.logger.info(f"getter process name {getter_process.name}, pid: {getter_process.pid}")

            if RUN_SERVER:
                server_process = multiprocessing.Process(target=self.run_server)
                server_process.start()
                self.logger.info(f"server process name {server_process.name}, pid: {server_process.pid}")

            tester_process.join()
            getter_process.join()
            server_process.join()
        except KeyboardInterrupt:
            tester_process.terminate()
            getter_process.terminate()
            server_process.terminate()

        finally:
            tester_process.join()
            getter_process.join()
            server_process.join()
            self.logger.info(f"tester process state is {'alive' if tester_process.is_alive() else 'ended'}")
            self.logger.info(f"getter process state is {'alive' if getter_process.is_alive() else 'ended'}")
            self.logger.info(f"server process state is {'alive' if server_process.is_alive() else 'ended'}")


if __name__ == '__main__':
    test = Processor()
    test.run
