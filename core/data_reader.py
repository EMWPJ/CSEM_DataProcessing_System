"""数据读取模块

支持CSV和二进制格式的CSEM时间序列数据读取。
"""

from __future__ import annotations

import struct
from dataclasses import dataclass
from typing import Dict, List, Optional, Sequence, Tuple

import numpy as np


@dataclass
class BinaryHeader:
    """二进制文件头信息"""
    n_channels: int = 5
    sample_rate: float = 200.0
    data_type: str = 'float32'
    byte_order: str = 'little'
    header_bytes: int = 0
    gains: Optional[List[float]] = None


class DataReader:
    """CSEM数据读取器"""
    
    @staticmethod
    def read_csv(filepath: str,
                 time_col: int = 0,
                 data_cols: Optional[Sequence[int]] = None,
                 delimiter: str = ",",
                 skiprows: int = 0,
                 encoding: str = "utf-8") -> Tuple[np.ndarray, np.ndarray, List[str]]:
        """读取CSV格式时间序列数据
        
        Args:
            filepath: 数据文件路径
            time_col: 时间列索引（默认0）
            data_cols: 要读取的数据列索引，None则读取所有非时间列
            delimiter: 分隔符
            skiprows: 跳过的行数（可用于跳过表头）
            encoding: 文件编码
        
        Returns:
            (times, data, channel_names)
                times: 时间数组 (N,)
                data: 数据矩阵 (N, M)
                channel_names: 通道名称列表
        """
        try:
            import pandas as pd
            
            df = pd.read_csv(filepath, delimiter=delimiter, skiprows=skiprows, encoding=encoding)
            
            if data_cols is None:
                data_cols = [i for i in range(len(df.columns)) if i != time_col]
            
            times = df.iloc[:, time_col].to_numpy(dtype=float)
            data = df.iloc[:, list(data_cols)].to_numpy(dtype=float)
            
            channel_names = [str(df.columns[i]) for i in data_cols]
            
            return times, data, channel_names
            
        except Exception as e:
            raise DataReadError(f"读取CSV文件失败: {filepath}, 错误: {e}")
    
    @staticmethod
    def read_binary(filepath: str, header_info: BinaryHeader) -> Tuple[np.ndarray, np.ndarray, List[str]]:
        """读取二进制格式数据
        
        Args:
            filepath: 文件路径
            header_info: 二进制文件头信息
        
        Returns:
            (times, data, channel_names)
        
        Note:
            具体二进制格式需要根据仪器型号实现
            当前为预留接口，抛出NotImplementedError
        """
        raise NotImplementedError(
            "二进制数据读取接口预留，具体实现需要用户提供数据格式信息"
        )
    
    @staticmethod
    def auto_detect_format(filepath: str) -> str:
        """自动检测数据格式
        
        Args:
            filepath: 文件路径
        
        Returns:
            'csv' 或 'binary'
        """
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                f.read(1024)
                return 'csv'
        except UnicodeDecodeError:
            return 'binary'


class DataReadError(Exception):
    """数据读取异常"""
    pass
