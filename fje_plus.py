import argparse
from node_creator import JsonFileNodesCreator
from visitor import TreePrinter,RectanglePrinter
import json

class FunnyJsonExploer:
    def _load(self, file_path: str) -> dict:
        with open(file_path, 'r') as file:
            data = json.load(file)
        return data

    def show(self, printer_type: str, icons_type: int, data: dict) -> None:
        # 先创建节点
        nodes_creator=JsonFileNodesCreator(icons_type)
        nodes_creator.create_all_nodes(data)
        root_node=nodes_creator.get_root_node()
        max_len=nodes_creator.get_max_len()    

        # 根据输入参数选择创建不同风格的打印机    
        printer = None
        if printer_type == "tree":
            printer=TreePrinter(icons_type,max_len)
        elif printer_type == "rectangle":
            printer = RectanglePrinter(icons_type,max_len)
        else:
            #default style-tree
            printer = TreePrinter(icons_type,max_len)       
        # 再打印输出
        printer.print_kid_nodes(root_node)

def main():
    parser = argparse.ArgumentParser(description="Funny JSON Explorer")
    parser.add_argument("-f", "--file", required=True, help="Path to the JSON file")
    parser.add_argument("-s", "--style", required=True, choices=["tree", "rectangle","new_type"], help="Style to display the JSON")
    parser.add_argument("-i", "--icon", type=int, default=0, choices=[-1,0, 1], help="Icon family to use (-1 or 0 or 1)")

    args = parser.parse_args()

    fje = FunnyJsonExploer()
    data = fje._load(args.file)
    fje.show(args.style, args.icon, data=data)


if __name__ == "__main__":
    main()