from node import ContainerFactory,LeafFactory
import symbols

class JsonFileNodesCreator:
    def __init__(self,_icons_type):
        self.containerCreator = ContainerFactory()
        self.leafCreator=LeafFactory()
        self.root_node = self.containerCreator.create_node()
        self.icons_type=_icons_type#0表示第一套，1表示第二套，-1表示不使用
        self.max_length=0#存储所有节点的行输出串中最大长度
        self.space_each_level=3

    def create_all_nodes(self, data: dict) -> None:
        flag,kids_node=self.create_kid_nodes(data=data)
        if flag==0:
            print("illegal json file input")
            return
        self.root_node.extend_children(kids_node)

    def find_target_icons(self):
        container_icon=" "
        leaf_icon=" "          
        if self.icons_type!=-1:
            #使用icon
            container_icon=symbols.icons[self.icons_type][0]
            leaf_icon=symbols.icons[self.icons_type][1]
        return container_icon,leaf_icon

    def get_node_str_len(self,len_key,flag,content,level):
        length=level*self.space_each_level
        if flag==0 and content!=None:#叶子节点
            length+=len_key+2+len(str(content))#tangerine: cheap & juicy!
        else:
            length+=len_key#gala     
        return length       

    def create_node(self,key,value,level,leaf_icon,container_icon):
        #当前节点和子节点有相同的祖先,标记level为1的尾结点所在的子树中的所有节点
        flag,content=self.create_kid_nodes(data=value,level=level+1,parent_key=key)
        length=self.get_node_str_len(len(key),flag,content,level)
        if flag==0:
            #没有子节点的情况
            node=self.leafCreator.create_node(_icon=leaf_icon,_name=key,_level=level,_value=content)
        else:
            #有子节点
            node=self.containerCreator.create_node(_icon=container_icon,_name=key,_level=level)
            node.extend_children(content)   
        return length,node
        
    #返回由data创建的所有节点列表,level表示将要创建的节点的level,parent_key专门用于数组类型
    def create_kid_nodes(self,data,level=1,parent_key=""):
        items=[]
        max_len=0
        container_icon,leaf_icon=self.find_target_icons()
        if isinstance(data, dict):
            for key, value in data.items():                
                length,node=self.create_node(key,value,level,leaf_icon,container_icon)
                max_len=max(max_len,length)
                items.append(node)
        elif isinstance(data, list):
            #遍历列表中的所有元素
            for i, value in enumerate(data):
                full_key = f"{parent_key}[{i}]"
                length,node=self.create_node(full_key,value,level,leaf_icon,container_icon)
                max_len=max(max_len,length)
                items.append(node)
        else:
            #如果传入的value，不是字典也不是列表，那就是普通的值,返回0，表示返回的不是节点
            return 0,data
        max_len+=1#包括value后面的空格符,max_length只在rectangle形式输出中使用
        self.max_length=max(self.max_length,max_len)
        return 1,items        
    
    def get_root_node(self):
        return self.root_node
    
    def get_max_len(self):
        return self.max_length