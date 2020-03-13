import datetime
import struct
from datetime import datetime
from pathlib import Path


class Thought:
    def __init__(self, user_id, timestamp, thought):
        self.user_id = user_id
        self.timestamp = timestamp
        self.thought = thought

    def __repr__(self):
        return f"Thought(user_id={self.user_id}, timestamp={repr(self.timestamp)}, thought={repr(self.thought)})"

    def __str__(self):
        # return f"{self.timestamp} user {self.user_id}: {self.thought}"
        return f'[{self.timestamp.strftime("%Y-%m-%d %H:%M:%S")}] user {self.user_id}: {self.thought}'

    def __eq__(self, other):
        if isinstance(other, Thought):
            return self.user_id == other.user_id and self.timestamp == other.timestamp and self.thought == other.thought
        else:
            return False

    def serialize(self):
        thought_b = self.thought.encode('utf-8')
        t_len = len(thought_b)
        return struct.pack("Q", int(self.user_id)) + struct.pack("Q", int(self.timestamp.timestamp())) + struct.pack(
            "I", t_len) + thought_b

    @classmethod
    def deserialize(cls, data):
        user_id, timestamp, thought_size = struct.unpack("QQI", data[:20])
        thought = data[20:].decode("utf-8")
        timestamp = datetime.fromtimestamp(timestamp)
        return Thought(user_id, timestamp, thought)

    @classmethod
    def write_thought(cls, dir, thought):
        prev_thoughts = ''
        time_stamp = str(thought.timestamp).replace(" ", "_").replace(":", "-")
        if Path(f'{dir}/{thought.user_id}/{time_stamp}.txt').exists():
            with open(f'{thought.dir}/{thought.user_id}/{time_stamp}.txt', 'r') as f:
                prev_thoughts = f.readlines()
        with open(f'{dir}/{thought.user_id}/{time_stamp}.txt', 'w+') as f:
            if not prev_thoughts:
                f.write(thought.thought)
            else:
                for t in prev_thoughts:
                    f.write(t + "\n")
                f.write(thought.thought + "\n")
