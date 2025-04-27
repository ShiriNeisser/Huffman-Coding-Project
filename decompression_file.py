from typing import List, Dict
import sys
import os

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

class HuffmanDecoder:
    # ASCII Control Characters are: (0x00 to 0x1F, 0x7F)
    # apart from the ASCII control characters (0x00 to 0x1F and 0x7F), 
    # all other characters in the ASCII table (0x20 to 0x7E, 0xFF) are printable 
    # and can be normally written into a text file as characters.
    control_characters: List[str] = [f"{bin(num)[2:]:>08}" for num in list(range(0x00, 0x1F+1)) + [0x7F]]
    backslash_code: str = f"{bin(0x5C)[2:]:>08}"
    encoded_forms: List[str] = [f"1{str_bin[1:]}" for str_bin in control_characters + [backslash_code]]

    def __init__(self, compressed_file: str, decompressed_file: str) -> None:
        self.compressed_file: str = compressed_file
        self.decompressed_file: str = decompressed_file
        self.inorder: Order     # created by: extract_ordered_lists()
        self.preorder: Order    # created by: extract_ordered_lists()
        self.root: TreeNode     # created by: spawn_huffman_tree()
        self.path2char_decoding_dict: Dict[str, str] = dict()    # created by: tree_to_encoding_dict()
        #
        self.extract_ordered_lists()
        self.spawn_huffman_tree()
        self.tree_to_decoding_dict(self.root)
        self.write2file()

        # print(f"{self.root = }")
        # print(f"{self.path2char_decoding_dict = }")

    @staticmethod
    def char_2_str_bin(char: str) -> str:
         # Convert the character to its ASCII value
        ascii_value = ord(char)
        # Convert the ASCII value to a binary string, remove the '0b' prefix, and ensure it's 8 bits long
        binary_representation = bin(ascii_value)[2:].zfill(8)
        return binary_representation
    
    @classmethod
    def char_decoder(cls, encoded_char: str, special: bool) -> str: # returns a binary string of 1s and 0s
        ascii_bin = cls.char_2_str_bin(encoded_char)
        if special is False:
            return ascii_bin
        # Backslash is used to show that the next char should be treated as a problematic char or backslash when encoding.
        # Since all problematic chars and backslash have '0' in their leftmost bit, we just flip it.
        return '0' + ascii_bin[1:8]

    def tree_to_decoding_dict(self, node: TreeNode) -> None:
        if node.is_leaf is True:
            self.path2char_decoding_dict[node.path] = node.val
            return
        self.tree_to_decoding_dict(node.left)
        self.tree_to_decoding_dict(node.right)

    def spawn_huffman_tree(self) -> None:
        self.root = TreeNode.buildTree(self.preorder.list_form, self.inorder.list_form)
        if self.root.is_leaf is True:
            self.root.path = '0'

    def extract_ordered_lists(self) -> None:
        lines: List[str]
        with open(file=self.compressed_file, mode='r') as fd:
            lines = fd.readlines()
        content: str = ''.join(lines[1:])
        # Initialize variables to hold the content of each section
        inorder_str = ""
        preorder_str = ""

        # Check if the 'Inorder=' and 'Preorder=' tags exist in the content
        if 'Inorder=' in content and 'Preorder=' in content:
            # Split the content at 'Preorder=' to separate the sections
            inorder_str, preorder_str = content.split('Preorder=')
            # Remove 'Inorder=' from the Inorder section
            inorder_str = inorder_str.replace('Inorder=', '').strip()
        
        self.inorder = Order(inorder_str)
        self.preorder = Order(preorder_str)

    def write2file(self) -> None:
        # Check if the target file exists
        if not os.path.exists(self.compressed_file):
            print(f"compressed file path is wrong = {self.compressed_file}, exiting...")
            exit(1)
        if not os.path.exists(self.decompressed_file):
            # If it doesn't exist, create the file by opening it in write mode and then closing it
            open(file=self.decompressed_file, mode='w', encoding='utf-8').close()
            print(f"Created the file, ", end='')
        
        # If it exists, open the target file in write mode and the source file in read mode
        with open(file=self.compressed_file, mode='r', encoding='utf-8') as compressed_fd, open(file=self.decompressed_file, mode='w', encoding='utf-8') as decompressed_fd:
            lines = compressed_fd.readlines()
            last_char_relevant_bits = eval(lines[0][-2])
            # print(f"\n{last_char_relevant_bits = }")
            # Move lines from the source file to the target file
            special = False
            curr_node: TreeNode = self.root
            for l, char in enumerate(lines[0][:-2]):
                if char == '\\':
                    special = True
                    continue
                path = self.char_decoder(char, special)
                if l == len(lines[0])-3:
                    path = path[:last_char_relevant_bits]
                special = False
                i:int = 0
                while i < len(path):
                    if curr_node.is_leaf is True:
                        decompressed_fd.write(curr_node.val)
                        if curr_node == self.root:
                            i+=1
                        else:
                            curr_node = self.root
                    else:
                        tree_step = path[i]
                        i+=1
                        if tree_step == '0':
                            curr_node = curr_node.left
                        else:
                            curr_node = curr_node.right
            if self.root.is_leaf is not True:
                decompressed_fd.write(curr_node.val)

class Huffman:
    def __init__(self, text_file_path: str) -> None:
        ID1:str = "209323658"
        ID2:str = "315932608"
        self.compressed_file_path: str = text_file_path
        self.decompressed_file_path: str = self.get_file_path(file_name=f"{ID1}_{ID2}_decompressed.txt")
        self.huffman_decoder: HuffmanDecoder = HuffmanDecoder(compressed_file=self.compressed_file_path, decompressed_file=self.decompressed_file_path)

        print()
        print(f"Decompressed file path: {self.decompressed_file_path}")
        with open(file=self.compressed_file_path, mode='r', encoding='utf-8') as fd:
            content = fd.read()
            print(f"Compressed file len = {len(content)}")
        with open(file=self.decompressed_file_path, mode='r', encoding='utf-8') as fd:
            content = fd.read()
            print(f"Decompressed file len = {len(content)}")

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