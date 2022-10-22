from typing import Optional

MAX_BUFFER_LENGTH = 100


class Memento:
    _state = None

    def __init__(self, state) -> None:
        self._state = state

    def get_state(self):
        return self._state


class EditorHistory:
    buffer: [Memento] = []
    current_state_index: int = -1

    def delete(self, start_index: int) -> None:
        """
        Delete objects from current_state_index to max_length.
        If buffer is full, delete old states.
        """
        del self.buffer[start_index:]

    def push(self, m: Memento) -> None:
        """
        Add new state to the end of buffer.
        """
        if self.current_state_index < len(self.buffer) - 1:
            self.delete(self.current_state_index)
        self.buffer.append(m)
        self.current_state_index += 1
        print("push", self.buffer)

    def undo(self) -> Optional[Memento]:
        """
        Return state from history at index current_state_index - 1.
        """
        print("undo", self.current_state_index, self.buffer)
        if self.current_state_index >= 0 and len(self.buffer) > 0:
            self.current_state_index -= 1
            return self.buffer[self.current_state_index]
        else:
            return None

    def shift_undo(self) -> Optional[Memento]:
        """
        Return state from history at index current_state_index + 1.
        """
        print("shift undo", self.current_state_index)
        if self.current_state_index < MAX_BUFFER_LENGTH and \
                len(self.buffer) > self.current_state_index + 1:
            self.current_state_index += 1
            return self.buffer[self.current_state_index]
        else:
            return None
