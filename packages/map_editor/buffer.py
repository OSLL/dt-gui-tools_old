# TODO add types

class Buffer:
    _objects = None

    def save_buffer(self, buffer) -> None:
        self._objects = buffer

    def get_buffer(self):
        return self._objects
