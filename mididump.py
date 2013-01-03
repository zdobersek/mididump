
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
