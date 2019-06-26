"""
Copyright (2017) Raydel Miranda 

This file is part of "VillaFlores Product Creator".

    "VillaFlores Product Creator" is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    "VillaFlores Product Creator" is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with "VillaFlores Product Creator".  If not, see <http://www.gnu.org/licenses/>.
"""

import threading
import shutil

from vf_createproducts_core.compose import *


class CopyWorker(threading.Thread):
    def __init__(self, queue, *args, **kwargs):
        super(CopyWorker, self).__init__(*args, **kwargs)
        self.__queue = queue

    def run(self):
        while True:
            source, dest = self.__queue.get()
            shutil.copyfile(source, dest)
            self.__queue.task_done()


class ConverterWorker(threading.Thread):
    def __init__(self, queue, *args, **kwargs):
        super(ConverterWorker, self).__init__(*args, **kwargs)
        self.__queue = queue

    def run(self):
        while True:
            (images, background, output, verbose) = self.__queue.get()
            compose(images, background, output, verbose)
            self.__queue.task_done()
