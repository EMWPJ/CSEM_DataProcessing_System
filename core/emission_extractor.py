"""发射时段提取模块

从连续CSEM数据中提取各频率的发射时段。
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, List, Optional

import numpy as np


@dataclass
class EmissionWindow:
    """发射时段数据容器"""
    times: np.ndarray
    data: np.ndarray
    current: np.ndarray
    frequency: float
    start_index: int
    end_index: int
    
    @property
    def duration(self) -> float:
        """时段长度（秒）"""
        return self.times[-1] - self.times[0] if len(self.times) > 0 else 0.0
    
    @property
    def n_samples(self) -> int:
        """采样点数"""
        return len(self.times)


class EmissionExtractor:
    """发射时段提取器
    
    Note:
        具体提取逻辑（相关检测、模板匹配、噪声门限等）待实现
    """
    
    def __init__(self, fs: float, target_frequencies: Optional[List[float]] = None):
        """初始化发射时段提取器
        
        Args:
            fs: 采样率 (Hz)
            target_frequencies: 目标频率列表 (Hz)
        """
        self.fs = fs
        self.target_frequencies = target_frequencies or []
    
    def extract_windows(self,
                       times: np.ndarray,
                       data: np.ndarray,
                       current: np.ndarray,
                       window_length: Optional[float] = None,
                       overlap: float = 0.5) -> Dict[float, EmissionWindow]:
        """提取发射时段
        
        从连续数据中提取包含目标频率发射信号的时段。
        
        Args:
            times: 时间数组 (N,)
            data: E场数据 (N, n_e_channels)
            current: 发射电流数据 (N,)
            window_length: 窗口长度（秒），None则自动根据最低频率计算
            overlap: 相邻窗口重叠率 [0, 1)
        
        Returns:
            {frequency: EmissionWindow} 字典
        
        Raises:
            NotImplementedError: 具体提取逻辑待实现
        
        Note:
            具体实现需要考虑：
            1. 如何根据电流信号检测发射时段
            2. 如何处理多频率叠加的发射信号
            3. 窗口长度和重叠率的确定方法
        """
        raise NotImplementedError(
            "发射时段提取逻辑待实现。"
            "需要用户提供：\n"
            "1. 具体的提取算法（如相关检测、噪声门限等）\n"
            "2. 二进制数据格式信息\n"
            "3. 发射信号的特征参数"
        )
    
    def extract_windows_simple(self,
                              times: np.ndarray,
                              data: np.ndarray,
                              current: np.ndarray,
                              target_freq: float,
                              n_cycles: int = 10) -> EmissionWindow:
        """简化版发射时段提取
        
        基于信号长度和目标频率计算窗口长度。
        作为占位实现，返回整个数据作为发射时段。
        
        Args:
            times: 时间数组
            data: E场数据
            current: 发射电流数据
            target_freq: 目标频率
            n_cycles: 包含的周期数
        
        Returns:
            EmissionWindow对象
        """
        period = 1.0 / target_freq
        window_length = period * n_cycles
        
        n_samples = int(window_length * self.fs)
        n_samples = min(n_samples, len(times))
        
        return EmissionWindow(
            times=times[:n_samples],
            data=data[:n_samples],
            current=current[:n_samples],
            frequency=target_freq,
            start_index=0,
            end_index=n_samples - 1
        )
