"""视电阻率计算模块"""

import numpy as np


MU0 = 4e-7 * np.pi


def compute_apparent_resistivity(z: complex,
                                 frequency: float,
                                 geometry_factor: float = 1.0,
                                 mu0: float = MU0) -> float:
    """计算视电阻率
    
    Formula: ρa = (|Z|²) / (2πμ0f)
    
    Args:
        z: 复数阻抗
        frequency: 频率 (Hz)
        geometry_factor: 几何因子K
        mu0: 真空磁导率，默认4π×10^-7 H/m
    
    Returns:
        视电阻率 (Ω·m)
    """
    if frequency <= 0:
        raise ValueError(f"频率必须为正数，得到: {frequency}")
    
    return geometry_factor * (np.abs(z) ** 2) / (2 * np.pi * mu0 * frequency)


def compute_apparent_resistivity_from_components(zxx: complex, zxy: complex,
                                                zyx: complex, zyy: complex,
                                                frequency: float,
                                                geometry_factor: float = 1.0) -> dict:
    """从阻抗分量计算各分量对应的视电阻率
    
    Returns:
        dict with keys 'rho_xx', 'rho_xy', 'rho_yx', 'rho_yy'
    """
    return {
        'rho_xx': compute_apparent_resistivity(zxx, frequency, geometry_factor),
        'rho_xy': compute_apparent_resistivity(zxy, frequency, geometry_factor),
        'rho_yx': compute_apparent_resistivity(zyx, frequency, geometry_factor),
        'rho_yy': compute_apparent_resistivity(zyy, frequency, geometry_factor),
    }
