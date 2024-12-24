from abc import ABC, abstractmethod
from src.ast.NodeType import NodeType


class Node(ABC):
    @abstractmethod
    def type(self) -> NodeType:
        pass

    @abstractmethod
    def json(self) -> dict:
        pass 
