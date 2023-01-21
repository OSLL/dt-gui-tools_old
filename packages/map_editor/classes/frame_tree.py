from typing import Optional, List

from classes.basic.tree import Tree


class FrameTree:

    def __init__(self):
        self.__tree = Tree[str]()

    def add(self, frame_name: str, parent: Optional[str] = None) -> None:
        if parent:
            self.__tree.add(successor=frame_name,
                            predecessor=parent)
        else:
            parent_frame_name = "/".join(frame_name.split("/")[:-1])
            self.__tree.add(successor=frame_name,
                            predecessor=parent_frame_name)

    def remove(self, frame_name: str):
        self.__tree.remove(frame_name)

    def predecessor(self, frame_name: str) -> str:
        return list(self.__tree.predecessors(frame_name))[0]

    def all_successors(self, frame_name: str) -> List[str]:
        frame_names = self.__tree.successors(frame_name)
        for frame_nm in frame_names:
            frame_names += self.all_successors(frame_nm)
        return frame_names
