"""阻抗显示组件

显示阻抗幅度、相位、视电阻率等结果。
"""

from typing import List, Optional

import numpy as np
from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
from PySide6.QtWidgets import QWidget, QVBoxLayout


class ImpedanceWidget(QWidget):
    """阻抗曲线显示组件"""
    
    def __init__(self, parent: Optional[QWidget] = None):
        super().__init__(parent)
        
        self._frequencies: Optional[np.ndarray] = None
        self._zxy_magnitude: Optional[np.ndarray] = None
        self._zxy_phase: Optional[np.ndarray] = None
        self._zyx_magnitude: Optional[np.ndarray] = None
        self._zyx_phase: Optional[np.ndarray] = None
        self._apparent_resistivity: Optional[np.ndarray] = None
        
        self._setup_ui()
    
    def _setup_ui(self):
        """设置UI"""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        
        self.figure = Figure(figsize=(10, 8))
        self.canvas = FigureCanvas(self.figure)
        layout.addWidget(self.canvas)
        
        self._create_subplots()
        
        self.figure.tight_layout()
    
    def _create_subplots(self):
        """创建子图"""
        self.axes_magnitude = self.figure.add_subplot(2, 2, 1)
        self.axes_phase = self.figure.add_subplot(2, 2, 2)
        self.axes_rho = self.figure.add_subplot(2, 2, 3)
        self.axes_tensor = self.figure.add_subplot(2, 2, 4)
        
        self.axes_magnitude.set_xlabel('Frequency (Hz)')
        self.axes_magnitude.set_ylabel('|Z| (Ω)')
        self.axes_magnitude.set_xscale('log')
        self.axes_magnitude.set_yscale('log')
        self.axes_magnitude.grid(True, alpha=0.3)
        
        self.axes_phase.set_xlabel('Frequency (Hz)')
        self.axes_phase.set_ylabel('Phase (deg)')
        self.axes_phase.set_xscale('log')
        self.axes_phase.grid(True, alpha=0.3)
        
        self.axes_rho.set_xlabel('Frequency (Hz)')
        self.axes_rho.set_ylabel('Apparent Resistivity (Ω·m)')
        self.axes_rho.set_xscale('log')
        self.axes_rho.set_yscale('log')
        self.axes_rho.grid(True, alpha=0.3)
        
        self.axes_tensor.set_xlabel('Real(Z)')
        self.axes_tensor.set_ylabel('Imag(Z)')
        self.axes_tensor.grid(True, alpha=0.3)
        self.axes_tensor.set_aspect('equal')
    
    def set_data(self,
                frequencies: np.ndarray,
                zxy_magnitude: Optional[np.ndarray] = None,
                zxy_phase: Optional[np.ndarray] = None,
                zyx_magnitude: Optional[np.ndarray] = None,
                zyx_phase: Optional[np.ndarray] = None,
                apparent_resistivity: Optional[np.ndarray] = None):
        """设置阻抗数据
        
        Args:
            frequencies: 频率数组
            zxy_magnitude: Zxy幅度 (Ω)
            zxy_phase: Zxy相位 (度)
            zyx_magnitude: Zyx幅度 (Ω)
            zyx_phase: Zyx相位 (度)
            apparent_resistivity: 视电阻率 (Ω·m)
        """
        self._frequencies = frequencies
        self._zxy_magnitude = zxy_magnitude
        self._zxy_phase = zxy_phase
        self._zyx_magnitude = zyx_magnitude
        self._zyx_phase = zyx_phase
        self._apparent_resistivity = apparent_resistivity
        
        self.plot()
    
    def plot(self):
        """绘制阻抗曲线"""
        if self._frequencies is None:
            return
        
        self.axes_magnitude.clear()
        self.axes_phase.clear()
        self.axes_rho.clear()
        self.axes_tensor.clear()
        
        if self._zxy_magnitude is not None:
            self.axes_magnitude.plot(self._frequencies, self._zxy_magnitude,
                                    'b-', label='|Zxy|', linewidth=1.5)
        if self._zyx_magnitude is not None:
            self.axes_magnitude.plot(self._frequencies, self._zyx_magnitude,
                                    'r--', label='|Zyx|', linewidth=1.5)
        self.axes_magnitude.legend()
        self.axes_magnitude.set_xlabel('Frequency (Hz)')
        self.axes_magnitude.set_ylabel('|Z| (Ω)')
        self.axes_magnitude.set_xscale('log')
        self.axes_magnitude.set_yscale('log')
        self.axes_magnitude.grid(True, alpha=0.3)
        
        if self._zxy_phase is not None:
            self.axes_phase.plot(self._frequencies, self._zxy_phase,
                                'b-', label='φxy', linewidth=1.5)
        if self._zyx_phase is not None:
            self.axes_phase.plot(self._frequencies, self._zyx_phase,
                                'r--', label='φyx', linewidth=1.5)
        self.axes_phase.legend()
        self.axes_phase.set_xlabel('Frequency (Hz)')
        self.axes_phase.set_ylabel('Phase (deg)')
        self.axes_phase.set_xscale('log')
        self.axes_phase.grid(True, alpha=0.3)
        
        if self._apparent_resistivity is not None:
            self.axes_rho.plot(self._frequencies, self._apparent_resistivity,
                              'g-', linewidth=1.5)
        self.axes_rho.set_xlabel('Frequency (Hz)')
        self.axes_rho.set_ylabel('Apparent Resistivity (Ω·m)')
        self.axes_rho.set_xscale('log')
        self.axes_rho.set_yscale('log')
        self.axes_rho.grid(True, alpha=0.3)
        
        if self._zxy_magnitude is not None and self._zxy_phase is not None:
            z_complex = self._zxy_magnitude * np.exp(1j * np.radians(self._zxy_phase))
            self.axes_tensor.plot(z_complex.real, z_complex.imag,
                                 'b-', label='Zxy', linewidth=1.5)
        if self._zyx_magnitude is not None and self._zyx_phase is not None:
            z_complex = self._zyx_magnitude * np.exp(1j * np.radians(self._zyx_phase))
            self.axes_tensor.plot(z_complex.real, z_complex.imag,
                                 'r--', label='Zyx', linewidth=1.5)
        self.axes_tensor.legend()
        self.axes_tensor.set_xlabel('Real(Z)')
        self.axes_tensor.set_ylabel('Imag(Z)')
        self.axes_tensor.grid(True, alpha=0.3)
        self.axes_tensor.set_aspect('equal')
        
        self.figure.tight_layout()
        self.canvas.draw()
    
    def clear(self):
        """清除显示"""
        self._frequencies = None
        self._zxy_magnitude = None
        self._zxy_phase = None
        self._zyx_magnitude = None
        self._zyx_phase = None
        self._apparent_resistivity = None
        self.plot()
