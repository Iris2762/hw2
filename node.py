from abc import ABC, abstractmethod
from typing import List
from visitor import Visitor

#抽象节点类
class Node(ABC):
    def __init__(self,_icon="",_name="",_level=0,_value="") -> None:
        self.icon=_icon#表示当前节点的icon
        self.name=_name
        self.level=_level
        self.value=""
        if _value!=None:
            if isinstance(_value,str):
                self.value=_value
            else:
                self.value=str(_value)

    @abstractmethod
    def draw(self) -> str:
        pass

    @abstractmethod
    def accept(self, visitor: Visitor) -> None:
        pass


#中间节点类，容器
class Container(Node):
    def __init__(self,_icon="",_name="",_level=0,_value=""):
        super().__init__(_icon,_name,_level,_value)
        self.children=[]#存储该中间节点导出的子节点

    def get_children(self)->List[Node]:
        return self.children
    
    def draw(self) -> str:
        # 节点中只输出icon和name：value。且不换行
        output_str = self.icon + self.name
        if self.value != "":
            output_str = output_str + ": " + self.value
        return output_str

    def add_child(self, child: Node) -> None:
        self.children.append(child)

    def extend_children(self, kids: List[Node]) -> None:
        self.children.extend(kids)

    def accept(self, visitor: Visitor) -> None:
        visitor.visit(self)


#叶子节点
class Leaf(Node):
    def __init__(self,_icon="",_name="",_level=0,_value=""):
        super().__init__(_icon,_name,_level,_value)

    def draw(self) -> str:
        # 节点中只输出icon和name：value。且不换行
        output_str = self.icon + self.name
        if self.value != "":
            output_str = output_str + ": " + self.value
        return output_str
    
    def accept(self, visitor: Visitor) -> None:
        visitor.visit(self)

# 节点的抽象工厂类
class NodeFactory(ABC):
    @abstractmethod
    def create_node(self, _icon="", _name="", _level=0, _value="") -> Node:
        pass

#中间节点container的具体工厂
class ContainerFactory(NodeFactory):
    def create_node(self, _icon="", _name="", _level=0, _value="") -> Node:
        return Container(_icon, _name, _level, _value)

#叶子节点leaf的具体工厂
class LeafFactory(NodeFactory):
    def create_node(self, _icon="", _name="", _level=0, _value="") -> Node:
        return Leaf(_icon, _name, _level, _value)
  