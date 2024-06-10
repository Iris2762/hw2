from abc import ABC, abstractmethod
from iterator import ConcreteIterator
import symbols

# 访问者接口
class Visitor(ABC):
    @abstractmethod
    def visit(self, node):
        pass

# 具体访问者实现
class TreeVisitor(Visitor):
    def __init__(self,last_kid=False,before_str=""):
        self.last_kid=last_kid
        self.before_str=before_str

    #打印输出当前节点的信息
    def visit(self, node):
        if node.level>0:#根节点不打印自身
            output_str=self.before_str
            if self.last_kid:
                output_str+=symbols.left_down_corner
            else:
                output_str+=symbols.left_T
            output_str+=node.draw()
            print(output_str)

class RectangleVisitor(Visitor):
    def __init__(self,first_row=False,may_last_row=True,max_len=0):
        self.first_row=first_row
        self.may_last_row=may_last_row
        self.max_length=max_len
        self.extern_row_len=5

    def create_node_beforestr(self,level,last_row):
        before_str=""
        #生成before_str
        if last_row==False:
            before_str+=(symbols.ver_line+"  ")*(level-1)
        else:
            before_str+=(symbols.left_down_corner+symbols.hor_line)*(level-1)    
        return before_str 

    def create_node_middlestr(self,first_row,last_row,node_draw):
        #生成middle_str
        middle_str=""
        if first_row:
            middle_str+=symbols.left_up_corner+node_draw+" "
        elif last_row:
            middle_str+=symbols.left_down_corner+node_draw+" "
        else:
            middle_str+=symbols.left_T+node_draw+" "
        return middle_str
    
    def create_node_afterstr(self,len_output_str,first_row,last_row):
        #生成last部分,需要控制输出字符串的总长度为max_length+extern_row_len+2,2为每行末尾输出符号的长度
        after_str=(self.max_length-len_output_str+self.extern_row_len)*symbols.hor_line
        if first_row:
            after_str+=symbols.right_up_corner
        elif last_row:
            after_str+=symbols.right_down_corner
        else:
            after_str+=symbols.right_T
        return after_str
    
    #打印输出当前节点的信息
    def visit(self, node):
        last_row=(not (hasattr(node,"children"))) and self.may_last_row
        if node.level>0:
            output_str=self.create_node_beforestr(node.level,last_row)
            output_str+=self.create_node_middlestr(self.first_row,last_row,node.draw())
            output_str+=self.create_node_afterstr(len(output_str),self.first_row,last_row)
            #进行当前节点的输出
            print(output_str)

#第一步：构造出所有节点，以及节点和节点之间的联系
class Printer(ABC):
    def __init__(self,_icons_type=0,max_len=0):
        self.icons_type=_icons_type#0表示第一套，1表示第二套，-1表示不使用
        self.max_length=max_len#存储所有节点的行输出串中最大长度
        self.space_each_level=3 

    @abstractmethod
    def print_kid_nodes(self, node, *args) -> None:
        pass

class TreePrinter(Printer):
    def __init__(self,_icons_type=0,max_len=0):
        super().__init__(_icons_type,max_len)
        self.visitor =TreeVisitor()
        #表示before_str每隔一级level会增长的长度    

    def create_kid_beforestr(self,before_str,node_name,last_kid):
        #构造子节点的before_str
        kid_before_str=before_str
        if node_name!="":#根节点的子节点的before_str为空，不需要构造
            if last_kid:
                kid_before_str+=self.space_each_level*" "
            else:
                kid_before_str+=symbols.ver_line
                kid_before_str+=(self.space_each_level-1)*" "
        return kid_before_str
    
    #打印当前节点的子节点
    #node是当前节点，需要打印其子节点，last_kid表示node是其父节点的最后一个子节点，before_str是node的before_str，需要传递给node的子节点
    def print_kid_nodes(self,node,last_kid=False,before_str=""):
        if hasattr(node,"children") is False:
            #叶子结点，结束
            return
        kid_before_str=self.create_kid_beforestr(before_str,node.name,last_kid)
        #打印子节点
        kids=node.get_children()
        iterator = ConcreteIterator(kids)
        
        while iterator.has_next():
            kid = iterator.next()
            if iterator.has_next():#kid不是最后一个子节点
                self.visitor.last_kid=False
            else:
                self.visitor.last_kid=True
            self.visitor.before_str=kid_before_str
            kid.accept(self.visitor)
            #处理kid的子节点
            self.print_kid_nodes(kid,self.visitor.last_kid,kid_before_str)

    
class RectanglePrinter(Printer):
    def __init__(self,_icons_type=0,max_len=0):
        super().__init__(_icons_type,max_len)
        self.extern_row_len=5
        self.visitor =RectangleVisitor(max_len=self.max_length)

    #first_row标记当前节点node是否为level为1的节点中的第一个，这种信息在node的父节点中决定
    #may_last_row标记当前节点node之前所有的祖先节点是否均为其兄弟节点中最后一个节点
    def print_kid_nodes(self,node,may_last_row=True):
        #打印子节点
        if hasattr(node,"children") is False:
            #叶子结点，结束
            return
        kids=node.get_children()
        iterator = ConcreteIterator(kids)

        while iterator.has_next():
            kid_may_last_row=may_last_row
            if iterator.is_first() and node.level==0:
                kid_first_row=True
            else:
                kid_first_row=False
            kid = iterator.next()    
            if iterator.has_next():
                kid_may_last_row=False
            self.visitor.first_row=kid_first_row
            self.visitor.may_last_row=kid_may_last_row
            #打印kid
            kid.accept(self.visitor)
            #处理kid的子节点
            self.print_kid_nodes(kid,kid_may_last_row)
            