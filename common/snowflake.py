import time
import random
import threading

class _Snowflake:
    UNUSED_BITS = 1
    EPOCH_BITS = 41
    NODE_ID_BITS = 10
    SEQUENCE_BITS = 12

    max_node_id = (1 << NODE_ID_BITS) - 1
    max_sequence = (1 << SEQUENCE_BITS) - 1
    start_time_millis = 1704067200000

    def __init__(self):
        self.node_id = random.randint(0, self.max_node_id)
        self.last_time_millis = self.start_time_millis
        self.sequence = 0
        self.lock = threading.Lock()

    def next_id(self):
        with self.lock:
            current_time_millis = int(time.time() * 1000)

            if current_time_millis < self.last_time_millis:
                raise Exception("Invalid Time")

            if current_time_millis == self.last_time_millis:
                self.sequence = (self.sequence + 1) & self.max_sequence
                if self.sequence == 0:
                    current_time_millis = self._wait_next_millis(current_time_millis)
            else:
                self.sequence = 0

            self.last_time_millis = current_time_millis

            return ((current_time_millis - self.start_time_millis) << (self.NODE_ID_BITS + self.SEQUENCE_BITS)) | \
                   (self.node_id << self.SEQUENCE_BITS) | \
                   self.sequence

    def _wait_next_millis(self, current_timestamp):
        while current_timestamp <= self.last_time_millis:
            current_timestamp = int(time.time() * 1000)
        return current_timestamp

_snowflake_instance = _Snowflake()

def generate_id():
    return _snowflake_instance.next_id()
