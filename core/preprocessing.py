"""预处理模块

提供CSEM数据的预处理功能：去直流、去趋势、滤波等。
"""

from __future__ import annotations

from typing import Optional

import numpy as np
from scipy import signal


class Preprocessor:
    """CSEM数据预处理器"""
    
    def __init__(self, fs: float):
        """初始化预处理器
        
        Args:
            fs: 采样率 (Hz)
        """
        self.fs = fs
    
    def remove_dc(self, data: np.ndarray) -> np.ndarray:
        """去除直流分量（去均值）
        
        Args:
            data: 输入数据 (N,) 或 (N, M)
        
        Returns:
            去直流后的数据，形状与输入相同
        """
        data = np.asarray(data, dtype=float)
        if data.ndim == 1:
            return data - np.mean(data)
        else:
            result = data.copy()
            for i in range(data.shape[1]):
                result[:, i] = data[:, i] - np.mean(data[:, i])
            return result
    
    def remove_trend(self, data: np.ndarray, order: int = 1) -> np.ndarray:
        """去除趋势
        
        Args:
            data: 输入数据 (N,) 或 (N, M)
            order: 多项式阶数，1=线性，2=二次
        
        Returns:
            去趋势后的数据
        """
        data = np.asarray(data, dtype=float)
        if data.ndim == 1:
            return signal.detrend(data, type='linear')
        else:
            result = data.copy()
            for i in range(data.shape[1]):
                result[:, i] = signal.detrend(data[:, i], type='linear')
            return result
    
    def notch_filter(self, data: np.ndarray,
                    fline: float = 50.0,
                    quality: float = 30.0,
                    harmonics: int = 3) -> np.ndarray:
        """工频陷波滤波
        
        Args:
            data: 输入信号 (N,) 或 (N, M)
            fline: 工频频率 (Hz)，50或60
            quality: 品质因子，Q越大陷波越窄
            harmonics: 处理的谐波数（包含基频）
        
        Returns:
            滤波后的信号
        """
        data = np.asarray(data, dtype=float)
        nyq = self.fs / 2.0
        
        def _filter_single(x: np.ndarray) -> np.ndarray:
            y = x.copy()
            for h in range(1, harmonics + 1):
                f0 = fline * h
                if f0 >= nyq:
                    break
                b, a = signal.iirnotch(w0=f0 / nyq, Q=quality)
                y = signal.filtfilt(b, a, y)
            return y
        
        if data.ndim == 1:
            return _filter_single(data)
        else:
            result = np.zeros_like(data)
            for i in range(data.shape[1]):
                result[:, i] = _filter_single(data[:, i])
            return result
    
    def bandpass_filter(self, data: np.ndarray,
                       low_freq: float,
                       high_freq: float,
                       order: int = 4) -> np.ndarray:
        """带通滤波
        
        Args:
            data: 输入数据 (N,) 或 (N, M)
            low_freq: 通带下限频率 (Hz)
            high_freq: 通带上限频率 (Hz)
            order: 滤波器阶数
        
        Returns:
            滤波后的数据
        """
        data = np.asarray(data, dtype=float)
        nyq = self.fs / 2.0
        low = low_freq / nyq
        high = high_freq / nyq
        
        b, a = signal.butter(N=order, Wn=[low, high], btype='band')
        
        if data.ndim == 1:
            return signal.filtfilt(b, a, data)
        else:
            result = np.zeros_like(data)
            for i in range(data.shape[1]):
                result[:, i] = signal.filtfilt(b, a, data[:, i])
            return result
    
    def process(self, data: np.ndarray,
                remove_dc: bool = True,
                remove_trend: bool = True,
                notch: bool = True,
                fline: float = 50.0,
                bandpass: bool = False,
                low_freq: float = 0.01,
                high_freq: float = 100.0) -> np.ndarray:
        """综合预处理流程
        
        Args:
            data: 输入数据
            remove_dc: 是否去直流
            remove_trend: 是否去趋势
            notch: 是否做工频陷波
            fline: 工频频率
            bandpass: 是否做带通滤波
            low_freq: 带通下限
            high_freq: 带通上限
        
        Returns:
            预处理后的数据
        """
        result = data.copy()
        
        if remove_dc:
            result = self.remove_dc(result)
        
        if remove_trend:
            result = self.remove_trend(result)
        
        if notch:
            result = self.notch_filter(result, fline=fline)
        
        if bandpass:
            result = self.bandpass_filter(result, low_freq, high_freq)
        
        return result
