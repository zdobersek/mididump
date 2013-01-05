# This file is part of mididump.
#
# mididump is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# mididump is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with mididump.  If not, see <http://www.gnu.org/licenses/>.


import os.path
import polling
import sys


def get_device_file(args):
    assert len(args) > 0, "The MIDI device was not specified through arguments."
    device_file = args[0]
    assert os.path.exists(device_file), "The MIDI device specified through arguments does not exist."
    return device_file

def main(args):
    try:
        device_file = get_device_file(args)
        polling.MIDIPoll(device_file).poll()
    except AssertionError, e:
        print "!!Error:", str(e)
        return 1

    return 0


if __name__=="__main__":
    sys.exit(main(sys.argv[1:]))
