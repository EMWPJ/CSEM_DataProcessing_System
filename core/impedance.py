"""阻抗计算模块

计算CSEM电磁阻抗。
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, Optional

import numpy as np
from scipy import signal


@dataclass
class ImpedanceResult:
    """阻抗计算结果"""
    zxx: complex = 0j
    zxy: complex = 0j
    zyx: complex = 0j
    zyy: complex = 0j
    zxx_err: float = 0.0
    zxy_err: float = 0.0
    zyx_err: float = 0.0
    zyy_err: float = 0.0
    
    @property
    def zxy_magnitude(self) -> float:
        """|Zxy| 阻抗幅度"""
        return np.abs(self.zxy)
    
    @property
    def zxy_phase(self) -> float:
        """φxy 阻抗相位（度）"""
        return np.degrees(np.angle(self.zxy))
    
    @property
    def zyx_magnitude(self) -> float:
        """|Zyx| 阻抗幅度"""
        return np.abs(self.zyx)
    
    @property
    def zyx_phase(self) -> float:
        """φyx 阻抗相位（度）"""
        return np.degrees(np.angle(self.zyx))


class ImpedanceCalculator:
    """阻抗计算器"""
    
    def __init__(self, fs: float):
        """初始化阻抗计算器
        
        Args:
            fs: 采样率 (Hz)
        """
        self.fs = fs
    
    def compute_impedance(self,
                         ex: np.ndarray,
                         ey: np.ndarray,
                         hx: np.ndarray,
                         hy: np.ndarray,
                         freq: float,
                         method: str = 'robust') -> ImpedanceResult:
        """计算指定频率的阻抗
        
        Args:
            ex, ey: 电场分量 (N,)
            hx, hy: 磁场分量 (N,)
            freq: 目标频率 (Hz)
            method: 计算方法
                - 'simple': Z = E/H 简单比值
                - 'robust': 基于交叉谱的稳健估计
        
        Returns:
            ImpedanceResult
        """
        if method == 'simple':
            return self._compute_simple(ex, ey, hx, hy, freq)
        elif method == 'robust':
            return self._compute_robust(ex, ey, hx, hy, freq)
        else:
            raise ValueError(f"不支持的方法: {method}")
    
    def _compute_simple(self, ex: np.ndarray, ey: np.ndarray,
                        hx: np.ndarray, hy: np.ndarray,
                        freq: float) -> ImpedanceResult:
        """简单阻抗计算"""
        n = len(ex)
        win = signal.get_window('hann', n)
        
        ex_win = ex * win
        ey_win = ey * win
        hx_win = hx * win
        hy_win = hy * win
        
        freqs = np.fft.rfftfreq(n, 1.0 / self.fs)
        idx = np.argmin(np.abs(freqs - freq))
        
        Ex = np.fft.rfft(ex_win)[idx]
        Ey = np.fft.rfft(ey_win)[idx]
        Hx = np.fft.rfft(hx_win)[idx]
        Hy = np.fft.rfft(hy_win)[idx]
        
        result = ImpedanceResult()
        if np.abs(Hx) > 1e-10:
            result.zxx = Ex / Hx
        if np.abs(Hy) > 1e-10:
            result.zyx = Ey / Hy
        if np.abs(Hy) > 1e-10:
            result.zxy = Ex / Hy
        if np.abs(Hx) > 1e-10:
            result.zyy = Ey / Hx
        
        return result
    
    def _compute_robust(self, ex: np.ndarray, ey: np.ndarray,
                        hx: np.ndarray, hy: np.ndarray,
                        freq: float) -> ImpedanceResult:
        """基于交叉谱的稳健阻抗估计"""
        nperseg = min(1024, len(ex) // 4)
        noverlap = nperseg // 2
        
        _, ExHx = signal.csd(ex, hx, fs=self.fs, nperseg=nperseg, noverlap=noverlap)
        _, ExHy = signal.csd(ex, hy, fs=self.fs, nperseg=nperseg, noverlap=noverlap)
        _, EyHx = signal.csd(ey, hx, fs=self.fs, nperseg=nperseg, noverlap=noverlap)
        _, EyHy = signal.csd(ey, hy, fs=self.fs, nperseg=nperseg, noverlap=noverlap)
        
        _, HxHx = signal.welch(hx, fs=self.fs, nperseg=nperseg, noverlap=noverlap)
        _, HyHy = signal.welch(hy, fs=self.fs, nperseg=nperseg, noverlap=noverlap)
        
        freqs = np.fft.rfftfreq(nperseg, 1.0 / self.fs)
        idx = np.argmin(np.abs(freqs - freq))
        
        result = ImpedanceResult()
        if np.abs(HxHx[idx]) > 1e-10:
            result.zxx = ExHx[idx] / HxHx[idx]
        if np.abs(HyHy[idx]) > 1e-10:
            result.zyx = EyHy[idx] / HyHy[idx]
        if np.abs(HyHy[idx]) > 1e-10:
            result.zxy = ExHy[idx] / HyHy[idx]
        if np.abs(HxHx[idx]) > 1e-10:
            result.zyy = EyHx[idx] / HxHx[idx]
        
        return result
    
    def compute_tensor_impedance(self,
                                data_dict: Dict[str, np.ndarray],
                                freq: float) -> np.ndarray:
        """计算张量阻抗矩阵
        
        Args:
            data_dict: 包含 'Ex', 'Ey', 'Hx', 'Hy' 的字典
            freq: 目标频率
        
        Returns:
            Z: 2x2 复数阻抗矩阵 [[Zxx, Zxy], [Zyx, Zyy]]
        """
        result = self.compute_impedance(
            data_dict.get('Ex'),
            data_dict.get('Ey'),
            data_dict.get('Hx'),
            data_dict.get('Hy'),
            freq,
            method='robust'
        )
        
        Z = np.array([[result.zxx, result.zxy],
                      [result.zyx, result.zyy]], dtype=complex)
        return Z
