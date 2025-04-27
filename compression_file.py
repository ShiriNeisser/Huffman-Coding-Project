from typing import List, Dict
import heapq
import sys
import os

# Text file doesn't contain any numbers, which means that all non-leaf nodes can have a number as a unique value.
# We will us counting up like in the example.
class UniqueValue:
    count_up = 0

    def __init__(self, depth: int, path: str) -> None:
        self.depth: int = depth
        self.path: str = path
        self.char: str = None
        self.number: int = None
    
    def __str__(self) -> str:
        # tmp = f"d{self.depth}p{self.path}c"
        # if self.char is not None:
        #     tmp += self.char
        # return tmp
        if self.char is not None:
            return self.char
        elif self.number is not None:
            return str(self.number)
        else:
            return "yet to be assigned"
        
    def update_number(self) -> None:
        self.number = self.get_increase_count()

    @classmethod
    def get_increase_count(cls) -> int:
        tmp = cls.count_up
        cls.count_up += 1
        return tmp

class HT_Node:
    def __init__(self, freq: int, char: str=None, smaller_child: "HT_Node"=None, bigger_child: "HT_Node"=None) -> None:
        self.char = char
        self.freq: int = freq
        self.smaller_child: "HT_Node" = smaller_child
        self.bigger_child: "HT_Node" = bigger_child
        self.is_leaf: bool = self.char is not None
        self.unique_value: UniqueValue = None
        self.check_attributes()

    def __lt__(self, other: "HT_Node") -> bool:
        return self.freq < other.freq
    
    def __add__(self, other: "HT_Node") -> "HT_Node":
        return HT_Node(char=None, freq=self.freq + other.freq, smaller_child=self, bigger_child=other)

    def __repr__(self) -> str:
        return f"HT_Node(char={self.char}, freq={self.freq}, unique_value={self.unique_value})"

    def check_attributes(self):
        if self.is_leaf is True: # node is a leaf
            if len(self.char) != 1: # self.char is not a single char
                print(f"self.char isn't a single character, len(self.char) = {self.char}")
                exit(1)
        if self.freq <= 0:
            print(f"frequency doesn't make sense, self.freq = {self.freq}")
            exit(1)

    def assign_children_unique_values(self):        
        if self.is_leaf is True:
            self.unique_value.char = self.char
            # print(f"assigned leaf = {self}")
        else:
            self.unique_value.update_number()
            self.smaller_child.unique_value = UniqueValue(depth=self.unique_value.depth + 1, 
                                                          path=self.unique_value.path + "0")
            # print(f"smaller_child = {self.smaller_child}")
            self.smaller_child.assign_children_unique_values()

            self.bigger_child.unique_value = UniqueValue(depth=self.unique_value.depth + 1, 
                                                          path=self.unique_value.path + "1")
            # print(f"bigger_child = {self.bigger_child}")
            self.bigger_child.assign_children_unique_values()
        # print(self)

    def list_nodes_in_order(self) -> List["HT_Node"]:
        if self.is_leaf is True:
            return [self]
        return self.smaller_child.list_nodes_in_order() + [self] + self.bigger_child.list_nodes_in_order()
    
    def list_nodes_pre_order(self) -> List["HT_Node"]:
        if self.is_leaf is True:
            return [self]
        return [self] + self.smaller_child.list_nodes_pre_order() + self.bigger_child.list_nodes_pre_order()

    def fill_encode_dict(self, encoding_dict: "HT_Node"):
        if self.is_leaf is True:
            encoding_dict[self.char] = self
            return
        self.smaller_child.fill_encode_dict(encoding_dict)
        self.bigger_child.fill_encode_dict(encoding_dict)

class HuffmanTree:
    def __init__(self, text_file_path: str) -> None:
        self.text_file_path: str = text_file_path
        self.char_historgram: Dict[str, int] = dict()   # created by: create_histogram()
        self.node_min_heap: List[HT_Node]               # created by: historgram_to_min_heap()
        self.root: HT_Node                              # created by: build_tree()

        self.create_histogram()
        self.historgram_to_min_heap()
        # print(self)
        self.build_tree()
        # print(f"HuffmanTree's root = {self.root}")
        self.assign_unique_values()

        self.in_order_unique_values = ','.join([node.unique_value.__str__() for node in self.root.list_nodes_in_order()])
        # print(f"\nInorder={{{self.in_order_unique_values}}}")
        self.pre_order_unique_values = ','.join([node.unique_value.__str__() for node in self.root.list_nodes_pre_order()])
        # print(f"\nPreorder={{{self.pre_order_unique_values}}}")

    def __repr__(self) -> str:
        repr_str: str = ""
        attr_list: List[str] = list()
        
        attr_list.append(f"text_file_path   = {self.text_file_path}")
        attr_list.append(f"char_historgram  = {self.char_historgram}")
        attr_list.append(f"node_min_heap    = {self.node_min_heap}")
        attr_list.append(f"sorted_node_list = {sorted(self.node_min_heap)}")

        repr_str += "HuffmanTree(\n\t"
        repr_str += ',\n\n\t'.join(attr_list)
        repr_str += "\n\t)"
        return repr_str

    def create_histogram(self) -> "HuffmanTree":
        with open(file=self.text_file_path, mode='r', encoding='utf-8') as fd:
            for line in fd:
                for char in line:
                    if char not in self.char_historgram:
                        self.char_historgram[char] = 1
                    else:
                        self.char_historgram[char] += 1

    def historgram_to_min_heap(self) -> None:
        self.node_min_heap = [HT_Node(char=char, freq=freq) for char, freq in self.char_historgram.items()]
        heapq.heapify(self.node_min_heap)

    def build_tree(self) -> HT_Node:
        while(len(self.node_min_heap) > 1):
            smaller_node = heapq.heappop(self.node_min_heap)
            bigger_node = heapq.heappop(self.node_min_heap)
            papa_node = smaller_node + bigger_node # The order matters
            heapq.heappush(self.node_min_heap, papa_node)
        self.root = self.node_min_heap[0]

    def assign_unique_values(self) -> None:
        self.root.unique_value = UniqueValue(depth=0, path="")
        # print(f"\nroot = {self.root}")
        # if there is only one type of char in the file, make sure to convert it to '0' bits.
        if self.root.is_leaf is True:
            self.root.unique_value.path = "0"
        # print("\n * Starting unique value assignments:")
        self.root.assign_children_unique_values()

class Order:
    # Expects str_form to look as follows: "{a,b,c,2,3,...,h}" (which means even index characters are to be extracted)
    def __init__(self, str_form: str) -> None:
        self.str_form: str = str_form
        self.xls_form: str = f"{self.str_form[1:-1]},"
        self.list_form: List[str] = list()  # created by build_list_form()
        self.build_list_form()
        
    def build_list_form(self, i: int= 0) -> None:
        if not (i < len(self.xls_form)):
            return
        found_ind = self.xls_form.find(',', i+1)
        if found_ind == -1:
            print(f"build_list_form({i = }) can't find ','! exiting...")
            exit(1)
        self.list_form.append(self.xls_form[i : found_ind])
        if(self.list_form[-1] == ""):
            print(f"{self.list_form[-3] = }")
            print(f"{self.list_form[-2] = }")
            print(f"{self.list_form[-1] = }")
            exit(1)
        self.build_list_form(found_ind+1)
    
class TreeNode:
    def __init__(self, val: str, depth: int, path: str):
        self.val: str = val
        self.left: "TreeNode" = None
        self.right: "TreeNode" = None
        self.is_leaf = False
        self.depth: int = depth
        self.path: str = path

    def __repr__(self) -> str:
        return f"Preorder scan:\n{self}"

    def __str__(self) -> str:
        left = ""
        right = ""
        if self.left is not None:
            left = f"\n{self.left}"
        if self.right is not None:
            right = f"\n{self.right}"
        if self.val == '\n':
            val = r'\n'
        else:
            val = self.val
        return f"{self.depth * '-'}val: '{val}', {self.depth = }, {self.path = }{left}{right}"

    @classmethod
    def buildTree(cls, preorder: List[str], inorder: List[str], depth: int = 0, path: str = "") -> "TreeNode":
        if not inorder or not preorder:
            return None
        # The first element in preorder is the root
        root_value:str = preorder.pop(0)
        root: TreeNode = TreeNode(root_value, depth, path)

        # Find the index of the root in inorder list to split left and right subtrees
        inorder_index: int = inorder.index(root_value)

        # Recursively build the left and right subtrees
        root.left = cls.buildTree(preorder, inorder[:inorder_index], depth + 1, path+'0')
        root.right = cls.buildTree(preorder, inorder[inorder_index + 1:], depth + 1, path+'1')
        if (root.left is None) and (root.right is None): 
            root.is_leaf = True
        return root

class HuffmanEncoder:
    # ASCII Control Characters are: (0x00 to 0x1F, 0x7F)
    # apart from the ASCII control characters (0x00 to 0x1F and 0x7F), 
    # all other characters in the ASCII table (0x20 to 0x7E, 0xFF) are printable 
    # and can be normally written into a text file as characters.
    control_characters: List[str] = [f"{bin(num)[2:]:>08}" for num in list(range(0x00, 0x1F+1)) + [0x7F]]
    backslash_code: str = f"{bin(0x5C)[2:]:>08}"

    def __init__(self, hf_tree: HuffmanTree, compressed_file: str) -> None:
        self.hf_tree: HuffmanTree = hf_tree
        self.compressed_file:str = compressed_file
        self.char2node_encoding_dict: Dict[str, HT_Node] = dict()   # created by: tree_to_encoding_dict()
        self.char2path_encoding_dict: Dict[str, str]                # created by: tree_to_encoding_dict()
        self.buffer = ""
        self.tree_to_encoding_dict()
        # print(f"\nencoding_dict = {self.char2path_encoding_dict}")
        self.write2file()

    def tree_to_encoding_dict(self) -> None:
        self.hf_tree.root.fill_encode_dict(self.char2node_encoding_dict)
        self.char2path_encoding_dict = {char:node.unique_value.path for char, node in self.char2node_encoding_dict.items()}

    @staticmethod
    def str_bin_2_char(str_bin: str) -> str:
        return chr(int(str_bin, 2))
    
    @classmethod
    def str_bin_encoder(cls, str_bin: str) -> str:
        if str_bin not in cls.control_characters and str_bin != cls.backslash_code:
            return cls.str_bin_2_char(str_bin)
        # Backslash is used to show that the next char should be treated as a problematic char or backslash when encoding.
        # Since all problematic chars and backslash have '0' in their leftmost bit, we just flip it.
        return "\\" + cls.str_bin_2_char('1' + str_bin[1:8])
    
    def write2file(self):
        source_path = self.hf_tree.text_file_path
        # Check if the target file exists
        if not os.path.exists(self.compressed_file):
            # If it doesn't exist, create the file by opening it in write mode and then closing it
            open(file=self.compressed_file, mode='w', encoding='utf-8').close()
            print(f"Created the file, ", end='')
        
        # If it exists, open the target file in write mode and the source file in read mode
        with open(file=self.compressed_file, mode='w', encoding='utf-8') as compressed_file, open(file=source_path, mode='r', encoding='utf-8') as source_file:
            # Move lines from the source file to the target file
            for line in source_file:
                for char in line:
                    self.buffer += self.char2path_encoding_dict[char]
                    while len(self.buffer)>=8:
                        tmp = self.str_bin_encoder(self.buffer[:8])
                        compressed_file.write(tmp)
                        self.buffer = self.buffer[8:]
            left_over_len_in_buffer = len(self.buffer)
            tmp = self.str_bin_encoder(f"{self.buffer:<08}")
            compressed_file.write(tmp)
            compressed_file.write(str(left_over_len_in_buffer))
            compressed_file.write(f"\nInorder={{{self.hf_tree.in_order_unique_values}}}")
            compressed_file.write(f"\nPreorder={{{self.hf_tree.pre_order_unique_values}}}")

class Huffman:
    def __init__(self, text_file_path: str) -> None:
        ID1:str = "209323658"
        ID2:str = "315932608"
        self.text_file_path: str = text_file_path
        self.compressed_file_path: str = self.get_file_path(file_name=f"{ID1}_{ID2}_compressed.txt")
        self.huffman_tree: HuffmanTree = HuffmanTree(text_file_path=text_file_path)
        self.huffman_encoder: HuffmanEncoder = HuffmanEncoder(hf_tree=self.huffman_tree, compressed_file=self.compressed_file_path)
        print(f"Compressed file path: {self.compressed_file_path}")
        print()
        with open(file=self.text_file_path, mode='r', encoding='utf-8') as fd:
            content = fd.read()
            print(f"Original file len = {len(content)}")
        with open(file=self.compressed_file_path, mode='r', encoding='utf-8') as fd:
            for line in fd:
                print(f"Compressed file - compressed text len = {len(line)}")
                break
        with open(file=self.compressed_file_path, mode='r', encoding='utf-8') as fd:
            content = fd.read()
            print(f"Compressed file len = {len(content)}")

    @staticmethod
    def get_file_path(file_name: str) -> str:
        return os.path.join(os.path.dirname(os.path.abspath(__file__)), file_name)

def main() -> None:
    first_argument: str = get_first_arg()
    Huffman(text_file_path=first_argument)

def get_first_arg() -> str:
    if len(sys.argv) > 1:
        first_argument = sys.argv[1]
        print(f"The first argument is: {first_argument}")
        return first_argument
    else:
        print("No arguments were passed.")
        exit(1)

if __name__ == "__main__":
    main()