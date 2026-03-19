"""相位计算模块"""

import numpy as np
from scipy import signal
from typing import Optional


def compute_phase(signal_x: np.ndarray,
                 signal_y: np.ndarray,
                 fs: float,
                 freq: Optional[float] = None,
                 nperseg: Optional[int] = None) -> float:
    """计算两个信号的相位差
    
    基于互功率谱(CSD)计算相角: arg(S_xy)
    
    Args:
        signal_x: 参考信号 (N,)
        signal_y: 待对比信号 (N,)
        fs: 采样率 (Hz)
        freq: 目标频率 (Hz)，None则使用CSD峰值频率
        nperseg: 分段长度
    
    Returns:
        相位差（度）
    """
    signal_x = np.asarray(signal_x, dtype=float)
    signal_y = np.asarray(signal_y, dtype=float)
    
    if nperseg is None:
        nperseg = min(1024, len(signal_x))
    
    f, Pxy = signal.csd(signal_x, signal_y, fs=fs, nperseg=nperseg)
    
    if freq is None:
        freq = f[np.argmax(np.abs(Pxy))]
    
    idx = np.argmin(np.abs(f - freq))
    phase_rad = np.angle(Pxy[idx])
    return np.degrees(phase_rad)


def compute_impedance_phase(z: complex) -> float:
    """计算阻抗相位
    
    Args:
        z: 复数阻抗
    
    Returns:
        相位角（度），范围 [-180, 180]
    """
    return np.degrees(np.angle(z))


def unwrap_phase(phase_deg: np.ndarray) -> np.ndarray:
    """相位解缠绕
    
    将相位从 [-180, 180] 展开为连续相位
    
    Args:
        phase_deg: 相位数组（度）
    
    Returns:
        解缠绕后的相位数组
    """
    phase_rad = np.radians(phase_deg)
    phase_unwrap_rad = np.unwrap(phase_rad)
    return np.degrees(phase_unwrap_rad)
