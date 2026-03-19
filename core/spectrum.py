"""频谱分析模块

提供FFT、Welch PSD、交叉谱等频谱分析功能。
"""

from __future__ import annotations

from typing import Optional, Tuple

import numpy as np
from scipy import signal


class SpectrumAnalyzer:
    """频谱分析器"""
    
    def __init__(self, fs: float):
        """初始化频谱分析器
        
        Args:
            fs: 采样率 (Hz)
        """
        self.fs = fs
    
    def compute_psd(self, data: np.ndarray,
                   nperseg: Optional[int] = None,
                   noverlap: Optional[int] = None,
                   window: str = 'hann') -> Tuple[np.ndarray, np.ndarray]:
        """Welch方法功率谱密度估计
        
        Args:
            data: 输入数据 (N,) 或 (N, n_channels)
            nperseg: FFT分段长度，None则使用1024
            noverlap: 分段重叠点数，None则使用nperseg/2
            window: 窗函数类型
        
        Returns:
            (freqs, psd): 频率数组，功率谱密度
                freqs: (K,) 频率轴
                psd: (K,) 或 (K, n_channels) 功率谱密度
        """
        data = np.asarray(data, dtype=float)
        
        if nperseg is None:
            nperseg = min(1024, len(data))
        if noverlap is None:
            noverlap = nperseg // 2
        
        if data.ndim == 1:
            freqs, psd = signal.welch(data, fs=self.fs, nperseg=nperseg,
                                      noverlap=noverlap, window=window)
            return freqs, psd
        else:
            psd_list = []
            for i in range(data.shape[1]):
                _, psd_i = signal.welch(data[:, i], fs=self.fs, nperseg=nperseg,
                                       noverlap=noverlap, window=window)
                psd_list.append(psd_i)
            freqs = np.fft.rfftfreq(nperseg, 1.0 / self.fs)
            return freqs, np.column_stack(psd_list)
    
    def compute_csd(self, signal1: np.ndarray, signal2: np.ndarray,
                   nperseg: Optional[int] = None,
                   noverlap: Optional[int] = None) -> Tuple[np.ndarray, np.ndarray]:
        """交叉谱密度计算
        
        Args:
            signal1, signal2: 输入信号 (N,)
            nperseg: 分段长度
            noverlap: 分段重叠点数
        
        Returns:
            (freqs, csd): 频率数组，交叉谱密度
        """
        if nperseg is None:
            nperseg = min(1024, len(signal1))
        if noverlap is None:
            noverlap = nperseg // 2
        
        freqs, csd = signal.csd(signal1, signal2, fs=self.fs,
                               nperseg=nperseg, noverlap=noverlap)
        return freqs, csd
    
    def compute_fft(self, data: np.ndarray,
                   window: str = 'hann',
                   detrend: bool = True) -> Tuple[np.ndarray, np.ndarray]:
        """FFT频谱计算
        
        Args:
            data: 输入数据 (N,) 或 (N, n_channels)
            window: 窗函数类型
            detrend: 是否去趋势
        
        Returns:
            (freqs, spectrum): 频率数组，频谱（复数）
        """
        data = np.asarray(data, dtype=float)
        n = data.shape[0]
        win = signal.get_window(window, n)
        
        if data.ndim == 1:
            x = data.copy()
            if detrend:
                x = signal.detrend(x, type='constant')
            x = x * win
            X = np.fft.rfft(x)
            freqs = np.fft.rfftfreq(n, 1.0 / self.fs)
            return freqs, X
        else:
            spectra = []
            for i in range(data.shape[1]):
                x = data[:, i].copy()
                if detrend:
                    x = signal.detrend(x, type='constant')
                x = x * win
                X = np.fft.rfft(x)
                spectra.append(X)
            freqs = np.fft.rfftfreq(n, 1.0 / self.fs)
            return freqs, np.column_stack(spectra)
    
    def compute_amplitude_phase(self, data: np.ndarray) -> Tuple[np.ndarray, np.ndarray]:
        """从复数频谱计算幅度和相位
        
        Args:
            data: 复数频谱数据
        
        Returns:
            (amplitude, phase): 幅度谱，相位谱（弧度）
        """
        amplitude = np.abs(data)
        phase = np.angle(data)
        return amplitude, phase
    
    def compute_psd_welch_multichannel(self, data: np.ndarray,
                                      nperseg: int = 1024,
                                      noverlap: Optional[int] = None) -> Tuple[np.ndarray, np.ndarray]:
        """多通道Welch功率谱计算
        
        使用与单通道相同的长度和重叠进行分段平均。
        
        Args:
            data: 数据矩阵 (N, n_channels)
            nperseg: 分段长度
            noverlap: 重叠点数
        
        Returns:
            (freqs, psd_matrix): freqs (K,), psd (K, n_channels)
        """
        data = np.asarray(data, dtype=float)
        if data.ndim == 1:
            data = data.reshape(-1, 1)
        
        if noverlap is None:
            noverlap = nperseg // 2
        
        n_channels = data.shape[1]
        psd_matrix = np.zeros((nperseg // 2 + 1, n_channels))
        
        for i in range(n_channels):
            freqs, psd_matrix[:, i] = signal.welch(
                data[:, i], fs=self.fs, nperseg=nperseg,
                noverlap=noverlap
            )
        
        return freqs, psd_matrix
