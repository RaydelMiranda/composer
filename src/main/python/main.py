from fbs_runtime.application_context.PyQt5 import ApplicationContext

import sys

from composer import Composer

if __name__ == '__main__':
    appctxt = ApplicationContext()       # 1. Instantiate ApplicationContext
    composer = Composer()
    composer.show()
    exit_code = appctxt.app.exec_()      # 2. Invoke appctxt.app.exec_()
    sys.exit(exit_code)
