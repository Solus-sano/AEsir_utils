import torch
import numpy as np
from typing import Union, List, Tuple
import json
import os
# from safetensors.torch import load_file



def print_json_structure(data, indent='', level=0):
    """
    Recursively prints the structure of a JSON-like data object.

    This function prints the keys and types of values in a dictionary, the length
    and an example element for lists, and the shape for numpy arrays and torch tensors.
    Other data types are printed with their type name and value.

    Args:
        data: The data object to be analyzed. Can be a dictionary, list, numpy array,
              torch tensor, string(json file), or other data type.
        indent (str): The indentation string used for formatting the output.
        level (int): The current level of recursion, used for formatting the output.
    """
    if isinstance(data, str):
        assert data.endswith('.json'), "Only support json file"
        data = json.load(open(data))
    
    if isinstance(data, dict):
        for key, value in data.items():
            print(f"{indent}|-- \033[31m{key}\033[0m:")
            print_json_structure(value, indent + "    ", level + 1)
    
    # 处理列表
    elif isinstance(data, list):
        print(f"{indent}\033[33mList of length {len(data)}\033[0m")
        if len(data) > 0:
            print(f"\033[33m{indent}(Example element):\033[0m")
            print_json_structure(data[-1], indent, level + 1)
    
    # 处理 NumPy 数组
    elif isinstance(data, np.ndarray):
        print(f"{indent}\033[32mnp.ndarray with shape\033[0m {data.shape}")
    
    # 处理 PyTorch 张量
    elif isinstance(data, torch.Tensor):
        print(f"{indent}\033[32mtorch.Tensor with shape\033[0m {data.shape}")
    
    # 处理其他类型
    else:
        print(f"\033[32m{indent}({type(data).__name__})\033[0m{data}")


def get_ckpt_structure(data):
    """
    Loads a checkpoint file and returns a string representation of its structure. 

    Args:
        file (str): Path to the checkpoint file. The file can be a '.safetensors' 
                    file or any other format compatible with torch.load.

    Returns:
        str: A string containing the keys, shapes, and data types of the tensors
             in the checkpoint.
    """
    if isinstance(data, str):
        if data.endswith('.safetensors'):
            from safetensors.torch import load_file
            ckpt = load_file(data)
        else:
            ckpt = torch.load(data)
    elif isinstance(data, dict):
        ckpt = data
    else:
        raise ValueError(f"Unsupported data type: {type(data)}")        
        
    # if save_path is None:
    #     for k,v in ckpt.items():
    #         print(k,":   ",v.shape, "   ",v.dtype)
    # else:
    #     with open(save_path,'w') as f:
    #         for k,v in ckpt.items():
    #             f.write(k + ": " + str(v.shape) + "   " + str(v.dtype) + '\n')
    op_txt = ""
    for k,v in ckpt.items():
        op_txt += f"\033[33m{k}\033[0m" + ": " + str(v.shape) + "   " + str(v.dtype) + '\n'
    return op_txt

def print_nnmodel_state_dict(model):
    print_json_structure(model.state_dict())
    
def tree_to_string(directory, prefix="", level=-1, show_hidden=False, current_level=1, ignore_dirs=[]):
    """
    递归地可视化文件目录结构，并返回其字符串表示形式。

    参数:
        directory (str): 要可视化的目录路径。
        prefix (str): 用于构建树形结构的前缀字符串。
        level (int): 可视化的最大深度。-1 表示没有限制。
        show_hidden (bool): 是否显示隐藏文件和目录。
        current_level (int): 当前的递归深度。
        ignore_dirs (list): 一个列表，包含要忽略的目录名(例如 ".git")。

    返回:
        str: 目录结构的字符串表示，如果出错则返回错误信息字符串。
    """
    if not os.path.isdir(directory):
        return f"错误: '{directory}' 不是一个有效的目录。"

    output_lines = []

    if level != -1 and current_level > level:
        return "" # 如果超过级别限制，返回空字符串，避免添加不必要的内容

    files = []
    dirs = []
    base_name = os.path.basename(directory) # 获取当前目录的名称

    try:
        entries = os.listdir(directory)
        if not show_hidden:
            entries = [entry for entry in entries if not entry.startswith('.')]
        entries.sort() # 对条目进行排序以便一致地显示
    except PermissionError:
        # 如果是顶层目录权限不足，则在主调用中处理。
        # 如果是子目录权限不足，则在此处添加一行。
        if current_level == 0: # 检查是否是初始调用
             return f"错误: 权限不足，无法访问 '{directory}'。"
        else:
            return f"{prefix}├── [权限不足: {base_name}]\n"
    except FileNotFoundError:
        return f"错误: 目录 '{directory}' 未找到。"

    # 将当前目录（如果是初始调用且非"."）添加到输出中
    # 这个逻辑稍微复杂，因为我们不想重复打印初始目录名，除非它是递归的一部分
    # 对于原始的tree命令，它会打印 "." 或给定的目录名作为根

    # 将条目分类为目录和文件
    for entry in entries:
        path = os.path.join(directory, entry)
        if os.path.isdir(path):
            if entry in ignore_dirs:
                continue
            dirs.append(entry)
        else:
            files.append(entry)

    # 处理目录
    for i, dir_name in enumerate(dirs):
        is_last_entry_in_current_level = (i == len(dirs) - 1) and (len(files) == 0)
        connector = "└── " if is_last_entry_in_current_level else "├── "
        output_lines.append(f"{prefix}{connector}{dir_name}")

        new_prefix = prefix + ("    " if is_last_entry_in_current_level else "│   ")
        # 递归调用，并将其结果添加到输出行
        # 确保递归调用返回的是字符串，然后按行分割并添加到列表中
        # 或者，如果递归函数也返回列表，则直接 extend
        recursive_output = tree_to_string(os.path.join(directory, dir_name), new_prefix, level, show_hidden, current_level + 1, ignore_dirs)
        if recursive_output: # 确保不是空字符串或错误消息
            if isinstance(recursive_output, str) and not recursive_output.startswith("错误:"):
                 # 如果递归返回的是一个多行字符串，则按行分割
                 # 但我们设计的递归函数本身会处理好前缀，所以这里直接添加
                output_lines.append(recursive_output.rstrip('\n')) # 去掉末尾可能的多余换行符
            elif isinstance(recursive_output, list): # 以防万一将来修改为返回列表
                output_lines.extend(recursive_output)
            elif recursive_output.startswith("错误:") or recursive_output.startswith(prefix + "├── [权限不足:"): # 如果是错误信息或权限不足信息
                output_lines.append(recursive_output.rstrip('\n'))


    # 处理文件
    for i, file_name in enumerate(files):
        is_last_file = (i == len(files) - 1)
        connector = "└── " if is_last_file else "├── "
        output_lines.append(f"{prefix}{connector}{file_name}")

    # 对于初始调用，我们可能想要添加根目录本身
    # 这个逻辑可以放在调用函数的地方，或者在这里有条件地添加
    if current_level == 0 and directory != ".":
        # 如果我们想在最前面加上根目录名
        # return f"{base_name}\n" + "\n".join(output_lines)
        # 或者让调用者自己决定是否打印根目录名
        pass


    return "\n".join(output_lines)


def display_tree(directory_path, level=-1, show_hidden=False):
    """
    一个包装函数，用于打印由 tree_to_string 生成的目录树。
    它会首先打印目标目录的名称，然后打印其内容树。
    """
    if not os.path.isdir(directory_path):
        print(f"错误: '{directory_path}' 不是一个有效的目录。")
        return

    # 打印根目录的名称
    print(directory_path)

    # 获取并打印树形结构
    # 对于 tree_to_string 的初始调用，prefix 通常是空的
    # current_level 也从0开始
    tree_str = tree_to_string(directory_path, prefix="", level=level, show_hidden=show_hidden, current_level=0)

    # 如果 tree_to_string 返回了指示顶层目录错误的字符串，则直接打印
    if tree_str.startswith("错误:"):
        print(tree_str)
    elif tree_str: # 确保不是空字符串
        print(tree_str)
    # 如果目录为空且没有错误，则不打印任何内容（除了目录名本身）

        
if __name__ == "__main__":
    display_tree("./")