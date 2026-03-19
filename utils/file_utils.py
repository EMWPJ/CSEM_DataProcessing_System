"""文件工具函数"""

import os
from pathlib import Path


def ensure_dir_exists(filepath: str) -> str:
    """确保目录存在
    
    Args:
        filepath: 文件路径
    
    Returns:
        原始文件路径
    """
    dir_path = os.path.dirname(filepath)
    if dir_path:
        Path(dir_path).mkdir(parents=True, exist_ok=True)
    return filepath


def get_file_extension(filepath: str) -> str:
    """获取文件扩展名
    
    Args:
        filepath: 文件路径
    
    Returns:
        扩展名（包含点号），如 '.csv'
    """
    return os.path.splitext(filepath)[1].lower()


def is_csv_file(filepath: str) -> bool:
    """判断是否为CSV文件"""
    return get_file_extension(filepath) == '.csv'


def is_binary_file(filepath: str) -> bool:
    """判断是否为二进制文件"""
    ext = get_file_extension(filepath)
    return ext in ['.bin', '.dat', '.raw']
