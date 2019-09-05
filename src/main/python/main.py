import logging
import sys

from fbs_runtime.application_context.PyQt5 import ApplicationContext

from composer import Composer

logging.basicConfig(
    filename='composer.log',
    level=logging.DEBUG,
    format="====================================================================\n"
           "%(asctime)s - %(name)s - %(levelname)s\n"
           "====================================================================\n"
           "%(message)s"
)

if __name__ == '__main__':
    logging.info("Starting composer ...")
    appctxt = ApplicationContext()       # 1. Instantiate ApplicationContext
    composer = Composer()
    composer.show()
    exit_code = appctxt.app.exec_()      # 2. Invoke appctxt.app.exec_()
    logging.info("Closing composer ...")
    sys.exit(exit_code)
