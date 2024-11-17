import torch
import numpy as np
from typing import Union, List, Tuple
# from safetensors.torch import load_file



def print_json_structure(data, indent='', level=0):
    """
    Recursively prints the structure of a JSON-like data object.

    This function prints the keys and types of values in a dictionary, the length
    and an example element for lists, and the shape for numpy arrays and torch tensors.
    Other data types are printed with their type name and value.

    Args:
        data: The data object to be analyzed. Can be a dictionary, list, numpy array,
              torch tensor, or other data type.
        indent (str): The indentation string used for formatting the output.
        level (int): The current level of recursion, used for formatting the output.
    """
    if isinstance(data, dict):
        for key, value in data.items():
            print(f"{indent}|-- {key}:")
            print_json_structure(value, indent + "    ", level + 1)
    
    # 处理列表
    elif isinstance(data, list):
        print(f"{indent}|-- List of length {len(data)}")
        if len(data) > 0:
            print(f"{indent}    |-- Example element:")
            print_json_structure(data[0], indent + "    ", level + 1)
    
    # 处理 NumPy 数组
    elif isinstance(data, np.ndarray):
        print(f"{indent}|-- np.ndarray with shape {data.shape}")
    
    # 处理 PyTorch 张量
    elif isinstance(data, torch.Tensor):
        print(f"{indent}|-- torch.Tensor with shape {data.shape}")
    
    # 处理其他类型
    else:
        print(f"{indent}|-- {type(data).__name__}: {data}")


def get_ckpt_structure(file = '/data2/liangzhijia/ckpt/sdxl/Kohaku-XL_beta/sdxl_vae.safetensors'):
    """
    Loads a checkpoint file and returns a string representation of its structure. 

    Args:
        file (str): Path to the checkpoint file. The file can be a '.safetensors' 
                    file or any other format compatible with torch.load.

    Returns:
        str: A string containing the keys, shapes, and data types of the tensors
             in the checkpoint.
    """
    if file.endswith('.safetensors'):
        from safetensors.torch import load_file
        ckpt = load_file(file)
    else:
        ckpt = torch.load(file)
    # if save_path is None:
    #     for k,v in ckpt.items():
    #         print(k,":   ",v.shape, "   ",v.dtype)
    # else:
    #     with open(save_path,'w') as f:
    #         for k,v in ckpt.items():
    #             f.write(k + ": " + str(v.shape) + "   " + str(v.dtype) + '\n')
    op_txt = ""
    for k,v in ckpt.items():
        op_txt += k + ": " + str(v.shape) + "   " + str(v.dtype) + '\n'
    return op_txt