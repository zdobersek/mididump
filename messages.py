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


class MIDIMessage:
    LENGTH = 3

    def __init__(self, data):
        self._data = data
        self._check()

    def _check(self):
        pass

    def __str__(self):
        raise NotImplementedError("Subclasses must implement")


class MIDINoteOffMessage(MIDIMessage):
    def _check(self):
        assert self._data[1] >> 7 is 0, "Invalid data byte #1"
        assert self._data[2] >> 7 is 0, "Invalid data byte #2"

    def __str__(self):
        return "Note Off - channel %d - note number %d - note velocity %d" \
               % (self._data[0] & 0xf + 1, self._data[1] & 0x7f, self._data[2] & 0x7f)


class MIDINoteOnMessage(MIDIMessage):
    def _check(self):
        assert self._data[1] >> 7 is 0, "Invalid data byte #1"
        assert self._data[2] >> 7 is 0, "Invalid data byte #2"

    def __str__(self):
        return "Note On - channel %d - note number %d - note velocity %d" \
               % (self._data[0] & 0xf + 1, self._data[1] & 0x7f, self._data[2] & 0x7f)


class MIDIPolyphonicAftertouchMessage(MIDIMessage):
    def _check(self):
        assert self._data[1] >> 7 is 0, "Invalid data byte #1"
        assert self._data[2] >> 7 is 0, "Invalid data byte #2"

    def __str__(self):
        return "Polyphonic Aftertouch - channel %d - note number %d - pressure %d" \
               % (self._data[0] & 0xf + 1, self._data[1] & 0x7f, self._data[2] & 0x7f)


class MIDIControlModeChangeMessage(MIDIMessage):
    def _check(self):
        assert self._data[1] >> 7 is 0, "Invalid data byte #1"
        assert self._data[2] >> 7 is 0, "Invalid data byte #2"

    def __str__(self):
        return "Control/Mode Change - channel %d - control number %d - control value %d" \
               % (self._data[0] & 0xf + 1, self._data[1] & 0x7f, self._data[2] & 0x7f)


class MIDIProgramChangeMessage(MIDIMessage):
    LENGTH = 2

    def _check(self):
        assert self._data[1] >> 7 is 0, "Invalid data byte #1"

    def __str__(self):
        return "Program Change - channel %d - program number %d" \
                % (self._data[0] & 0xf + 1, ord(self._data[1] & 0x7f))


class MIDIChannelAftertouchMessage(MIDIMessage):
    LENGTH = 2

    def _check(self):
        assert self._data[1] >> 7 is 0, "Invalid data byte #1"

    def __str__(self):
        return "Channel Aftertouch - channel %d - pressure value %d" \
               % (self._data[0] & 0xf + 1, ord(self._data[1] & 0x7f))


class MIDIPitchWheelControlMessage(MIDIMessage):
    def _check(self):
        assert self._data[1] >> 7 is 0, "Invalid data byte #1"
        assert self._data[2] >> 7 is 0, "Invalid data byte #2"

    def __str__(self):
        return "Pitch Wheel Control - channel %d - LSB %d - MSB %d" \
               % (self._data[0] & 0xf + 1, self._data[1] & 0x7f, self._data[2] & 0x7f)


class MIDISystemExclusiveMessage(MIDIMessage):
    def __str__(self):
        return "System Exclusive"


class MIDITimeCodeQuarterFrameMessage(MIDIMessage):
    def _check(self):
        assert self._data[1] >> 7 is 0, "Invalid data byte #1"

    def __str__(self):
        return "Time Code Quarter Frame - message type %d - values %d" \
               % ((self._data[1] & 0x70) >> 4, self._data[1] & 0xf)


class MIDISongPositionPointerMessage(MIDIMessage):
    def _check(self):
        assert self._data[1] >> 7 is 0, "Invalid data byte #1"
        assert self._data[2] >> 7 is 0, "Invalid data byte #2"

    def __str__(self):
        return "Song Position Pointer - LSB %d - MSB %d" \
               % (self._data[1] & 0x7f, self._data[2] & 0x7f)


class MIDISongSelectMessage(MIDIMessage):
    LENGTH = 2

    def _check(self):
        assert self._data[1] >> 7 is 0, "Invalid data byte #1"

    def __str__(self):
        return "Song Select - selected sequence/song %d" \
               % (ord(self._data[1] & 0x7f))


class MIDIUndefinedMessage(MIDIMessage):
    def __str__(self):
        return "Undefined (Reserved)"


class MIDITuneRequestMessage(MIDIMessage):
    LENGTH = 1

    def __str__(self):
        return "Tune Request"


class MIDIEndOfSystemExclusiveMessage(MIDIMessage):
    LENGTH = 1

    def __str__(self):
        return "End Of System Exclusive"


class MIDITimingClockMessage(MIDIMessage):
    LENGTH = 1

    def __str__(self):
        return "Timing Clock"


class MIDIStartMessage(MIDIMessage):
    LENGTH = 1

    def __str__(self):
        return "Start"


class MIDIContinueMessage(MIDIMessage):
    LENGTH = 1

    def __str__(self):
        return "Continue"


class MIDIStopMessage(MIDIMessage):
    LENGTH = 1

    def __str__(self):
        return "Stop"


class MIDIActiveSensingMessage(MIDIMessage):
    LENGTH = 1

    def __str__(self):
        return "Active Sensing"


class MIDISystemResetMessage(MIDIMessage):
    LENGTH = 1

    def __str__(self):
        return "MIDISystemResetMessage"


_messages_per_status_byte = {
    0b1000: MIDINoteOffMessage,
    0b1001: MIDINoteOnMessage,
    0b1010: MIDIPolyphonicAftertouchMessage,
    0b1011: MIDIControlModeChangeMessage,
    0b1100: MIDIProgramChangeMessage,
    0b1101: MIDIChannelAftertouchMessage,
    0b1110: MIDIPitchWheelControlMessage,
    0b1111: {
        0b0000: MIDISystemExclusiveMessage,
        0b0001: MIDITimeCodeQuarterFrameMessage,
        0b0010: MIDISongPositionPointerMessage,
        0b0011: MIDISongSelectMessage,
        0b0100: MIDIUndefinedMessage,
        0b0101: MIDIUndefinedMessage,
        0b0110: MIDITuneRequestMessage,
        0b0111: MIDIEndOfSystemExclusiveMessage,
        0b1000: MIDITimingClockMessage,
        0b1001: MIDIUndefinedMessage,
        0b1010: MIDIStartMessage,
        0b1011: MIDIContinueMessage,
        0b1100: MIDIStopMessage,
        0b1101: MIDIUndefinedMessage,
        0b1110: MIDIActiveSensingMessage,
        0b1111: MIDISystemResetMessage,
    },
}


class MessageDecoder:
    @staticmethod
    def get(buf):
        status_byte = buf[0]
        first_quartet, second_quartet = status_byte >> 4, status_byte & 0x15
        assert first_quartet in _messages_per_status_byte.keys(), "Unknown message based on first quartet of the status byte (`%s` = `%s`)" \
                                                                  % (bin(first_quartet), hex(first_quartet))
        entry = _messages_per_status_byte[first_quartet]
        if type(entry) is dict:
            assert second_quartet in entry, "Unknown message based on second quartet of the status byte (`%s` = `%s`, first quartet `%s`)" \
                                             % (bin(second_quartet), hex(first_quartet), bin(second_quartet), hex(second_quartet))
            return entry[second_quartet](buf[:entry.LENGTH])

        return entry(buf[:entry.LENGTH])
