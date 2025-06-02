import torch
import numpy as np
from typing import Union, List, Tuple
import json
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