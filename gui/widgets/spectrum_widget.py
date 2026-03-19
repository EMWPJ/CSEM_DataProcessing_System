"""频谱显示组件

用于显示功率谱密度(PSD)和相位谱。
"""

from typing import List, Optional, Tuple

import numpy as np
from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
from PySide6.QtWidgets import QWidget, QVBoxLayout


class SpectrumWidget(QWidget):
    """频谱显示组件"""
    
    def __init__(self, parent: Optional[QWidget] = None):
        super().__init__(parent)
        
        self._freqs: Optional[np.ndarray] = None
        self._psd: Optional[np.ndarray] = None
        self._channel_names: List[str] = []
        
        self._setup_ui()
    
    def _setup_ui(self):
        """设置UI"""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        
        self.figure = Figure(figsize=(8, 6))
        self.canvas = FigureCanvas(self.figure)
        layout.addWidget(self.canvas)
        
        self.axes = self.figure.add_subplot(111)
        self.axes.set_xlabel('Frequency (Hz)')
        self.axes.set_ylabel('Power Spectral Density (V²/Hz)')
        self.axes.set_xscale('log')
        self.axes.set_yscale('log')
        self.axes.grid(True, alpha=0.3)
        
        self.figure.tight_layout()
    
    def set_data(self, freqs: np.ndarray, psd: np.ndarray,
                 channel_names: Optional[List[str]] = None):
        """设置频谱数据
        
        Args:
            freqs: 频率数组 (K,)
            psd: 功率谱密度 (K,) 或 (K, n_channels)
            channel_names: 通道名称列表
        """
        self._freqs = freqs
        self._psd = psd
        
        if channel_names is not None:
            self._channel_names = channel_names
        elif psd.ndim == 2:
            self._channel_names = [f'Ch{i}' for i in range(psd.shape[1])]
        else:
            self._channel_names = ['Data']
        
        self.plot()
    
    def plot(self):
        """绘制频谱"""
        if self._freqs is None or self._psd is None:
            return
        
        self.axes.clear()
        
        psd = self._psd
        if psd.ndim == 1:
            psd = psd.reshape(-1, 1)
        
        colors = ['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', '#9467bd']
        
        for i in range(psd.shape[1]):
            label = self._channel_names[i] if i < len(self._channel_names) else f'Ch{i}'
            color = colors[i % len(colors)]
            self.axes.plot(self._freqs, psd[:, i], label=label, color=color, alpha=0.8)
        
        self.axes.set_xlabel('Frequency (Hz)')
        self.axes.set_ylabel('Power Spectral Density (V²/Hz)')
        self.axes.set_xscale('log')
        self.axes.set_yscale('log')
        self.axes.grid(True, alpha=0.3)
        self.axes.legend(loc='upper right', fontsize=8)
        
        self.figure.tight_layout()
        self.canvas.draw()
    
    def clear(self):
        """清除显示"""
        self._freqs = None
        self._psd = None
        self._channel_names = []
        self.axes.clear()
        self.axes.set_xlabel('Frequency (Hz)')
        self.axes.set_ylabel('Power Spectral Density (V²/Hz)')
        self.canvas.draw()
