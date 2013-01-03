
import messages
import os
import select


class MIDIPoll:
    def __init__(self, file_path):
        self._file_path = file_path
        self._poll = select.poll()

    def poll(self):
        fd = os.open(self._file_path, os.O_RDONLY)
        self._poll.register(fd, select.POLLIN)

        print "Starting polling device", self._file_path
        while True:
            try:
                events = self._poll.poll()
                for event in events:
                    if event[1] & select.POLLIN:
                        data = os.read(fd, 8)
                        try:
                            message = messages.MessageDecoder.get(data)
                        except AssertionError, e:
                            print "Error while decoding message:", str(e)
                            print "Complete message data:", ','.join([hex(ord(b)) for b in data])

                        print "Message:", str(message)
            except KeyboardInterrupt:
                print
                print "Stopping polling ..."
                break

        self._poll.unregister(fd)
        os.close(fd)
