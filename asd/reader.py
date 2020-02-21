from .asd_pb2 import *
import gzip
import struct
import sh


class Reader:
    def __init__(self, path):

        self._path = path
        self._read_user()

    def _read_user(self):
        with gzip.open(self._path) as f:
            user_msg_size = struct.unpack("I", f.read(4))[0]
            user_msg_bytes = f.read(user_msg_size)
            user = User.FromString(user_msg_bytes)
            self.user_id = user.user_id
            self.username = user.username
            self.birthday = user.birthday
            self.gender = user.gender

    def __iter__(self):
        with gzip.open(self._path) as f:
            user_msg_size = struct.unpack("I", f.read(4))[0]
            _ = f.read(user_msg_size)

            while True:
                buf = f.read(4)
                if len(buf) == 4:
                    msg_size = struct.unpack("I", buf)[0]
                    msg_bytes = f.read(msg_size)
                    snapshot = Snapshot.FromString(msg_bytes)
                else:
                    break

                yield snapshot
