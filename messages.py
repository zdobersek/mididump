
class MIDIMessage:
    _message_length = None

    def __init__(self, data):
        self._data = data
        self._check()

    def _check(self):
        pass

    def __str__(self):
        raise NotImplementedError("Subclasses must implement")


class MIDINoteOffMessage(MIDIMessage):
    def _check(self):
        assert ord(self._data[1]) >> 7 is 0, "Invalid data byte #1"
        assert ord(self._data[2]) >> 7 is 0, "Invalid data byte #2"

    def __str__(self):
        return "Note Off - channel %d - note number %d - note velocity %d" \
               % (ord(self._data[0]) & 0xf + 1, ord(self._data[1]) & 0x7f, ord(self._data[2]) & 0x7f)


class MIDINoteOnMessage(MIDIMessage):
    def _check(self):
        assert ord(self._data[1]) >> 7 is 0, "Invalid data byte #1"
        assert ord(self._data[2]) >> 7 is 0, "Invalid data byte #2"

    def __str__(self):
        return "Note On - channel %d - note number %d - note velocity %d" \
               % (ord(self._data[0]) & 0xf + 1, ord(self._data[1]) & 0x7f, ord(self._data[2]) & 0x7f)


class MIDIPolyphonicAftertouchMessage(MIDIMessage):
    def _check(self):
        assert ord(self._data[1]) >> 7 is 0, "Invalid data byte #1"
        assert ord(self._data[2]) >> 7 is 0, "Invalid data byte #2"

    def __str__(self):
        return "Polyphonic Aftertouch - channel %d - note number %d - pressure %d" \
               % (ord(self._data[0]) & 0xf + 1, ord(self._data[1]) & 0x7f, ord(self._data[2]) & 0x7f)


class MIDIControlModeChangeMessage(MIDIMessage):
    def _check(self):
        assert ord(self._data[1]) >> 7 is 0, "Invalid data byte #1"
        assert ord(self._data[2]) >> 7 is 0, "Invalid data byte #2"

    def __str__(self):
        return "Control/Mode Change - channel %d - controller number %d - controller value %d" \
               % (ord(self._data[0]) & 0xf + 1, ord(self._data[1]) & 0x7f, ord(self._data[2]) & 0x7f)


class MIDIProgramChangeMessage(MIDIMessage):
    def _check(self):
        assert ord(self._data[1]) >> 7 is 0, "Invalid data byte #1"

    def __str__(self):
        return "Program Change - channel %d - program number %d" \
                % (ord(self._data[0]) & 0xf + 1, ord(self._data[1] & 0x7f))


class MIDIChannelAftertouchMessage(MIDIMessage):
    def _check(self):
        assert ord(self._data[1]) >> 7 is 0, "Invalid data byte #1"

    def __str__(self):
        return "Channel Aftertouch - channel %d - pressure value %d" \
               % (ord(self._data[0]) & 0xf + 1, ord(self._data[1] & 0x7f))


class MIDIPitchWheelControlMessage(MIDIMessage):
    def _check(self):
        assert ord(self._data[1]) >> 7 is 0, "Invalid data byte #1"
        assert ord(self._data[2]) >> 7 is 0, "Invalid data byte #2"

    def __str__(self):
        return "Pitch Wheel Control - channel %d - LSB %d - MSB %d" \
               % (ord(self._data[0]) & 0xf + 1, ord(self._data[1]) & 0x7f, ord(self._data[2]) & 0x7f)


class MIDISystemExclusiveMessage(MIDIMessage):
    def __str__(self):
        return "System Exclusive"


class MIDITimeCodeQuarterFrameMessage(MIDIMessage):
    def _check(self):
        assert ord(self._data[1]) >> 7 is 0, "Invalid data byte #1"

    def __str__(self):
        return "Time Code Quarter Frame - message type %d - values %d" \
               % ((ord(self._data[1]) & 0x70) >> 4, ord(self._data[1]) & 0xf)


class MIDISongPositionPointerMessage(MIDIMessage):
    def _check(self):
        assert ord(self._data[1]) >> 7 is 0, "Invalid data byte #1"
        assert ord(self._data[2]) >> 7 is 0, "Invalid data byte #2"

    def __str__(self):
        return "Song Position Pointer - LSB %d - MSB %d" \
               % (ord(self._data[1]) & 0x7f, ord(self._data[2]) & 0x7f)


class MIDISongSelectMessage(MIDIMessage):
    def _check(self):
        assert ord(self._data[1]) >> 7 is 0, "Invalid data byte #1"

    def __str__(self):
        return "Song Select - selected sequence/song %d" \
               % (ord(self._data[1] & 0x7f))


class MIDIUndefinedMessage(MIDIMessage):
    def __str__(self):
        return "Undefined (Reserved)"


class MIDITuneRequestMessage(MIDIMessage):
    def __str__(self):
        return "Tune Request"


class MIDIEndOfSystemExclusiveMessage(MIDIMessage):
    def __str__(self):
        return "End Of System Exclusive"


class MIDITimingClockMessage(MIDIMessage):
    def __str__(self):
        return "Timing Clock"


class MIDIStartMessage(MIDIMessage):
    def __str__(self):
        return "Start"


class MIDIContinueMessage(MIDIMessage):
    def __str__(self):
        return "Continue"


class MIDIStopMessage(MIDIMessage):
    def __str__(self):
        return "Stop"


class MIDIActiveSensingMessage(MIDIMessage):
    def __str__(self):
        return "Active Sensing"


class MIDISystemResetMessage(MIDIMessage):
    def __str__(self):
        return "MIDISystemResetMessage"


_messages_per_status_byte = {
    0x8: MIDINoteOffMessage,
    0x9: MIDINoteOnMessage,
    0xA: MIDIPolyphonicAftertouchMessage,
    0xB: MIDIControlModeChangeMessage,
    0xC: MIDIProgramChangeMessage,
    0xD: MIDIChannelAftertouchMessage,
    0xE: MIDIPitchWheelControlMessage,
    0xF: {
        0x0: MIDISystemExclusiveMessage,
        0x1: MIDITimeCodeQuarterFrameMessage,
        0x2: MIDISongPositionPointerMessage,
        0x3: MIDISongSelectMessage,
        0x4: MIDIUndefinedMessage,
        0x5: MIDIUndefinedMessage,
        0x6: MIDITuneRequestMessage,
        0x7: MIDIEndOfSystemExclusiveMessage,
        0x8: MIDITimingClockMessage,
        0x9: MIDIUndefinedMessage,
        0xA: MIDIStartMessage,
        0xB: MIDIContinueMessage,
        0xC: MIDIStopMessage,
        0xD: MIDIUndefinedMessage,
        0xE: MIDIActiveSensingMessage,
        0xF: MIDISystemResetMessage,
    },
}


class MessageDecoder:
    @staticmethod
    def get(data):
        assert len(data) == 3, "Incorrect data length (expected `3`)"

        status_byte = ord(data[0])
        first_quartet, second_quartet = status_byte >> 4, status_byte & 0x15
        assert first_quartet in _messages_per_status_byte.keys(), "Unknown message based on first quartet of the status byte (`%s` = `%s`)" \
                                                                  % (bin(first_quartet), hex(first_quartet))
        result = _messages_per_status_byte[first_quartet]
        if type(result) is dict:
            assert second_quartet in result, "Unknown message based on second quartet of the status byte (`%s` = `%s`, first quartet `%s`)" \
                                             % (bin(second_quartet), hex(first_quartet), bin(second_quartet), hex(second_quartet))
            return result[second_quartet](data)

        return result(data)