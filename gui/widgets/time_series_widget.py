"""时间序列显示组件

用于显示CSEM时间序列数据（原始和处理后）。
"""

from typing import List, Optional

import numpy as np
from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
from PySide6.QtWidgets import QWidget, QVBoxLayout
from PySide6.QtCore import Signal


class TimeSeriesWidget(QWidget):
    """时间序列显示组件"""
    
    data_changed = Signal()
    
    def __init__(self, parent: Optional[QWidget] = None):
        super().__init__(parent)
        
        self._times: Optional[np.ndarray] = None
        self._data: Optional[np.ndarray] = None
        self._channel_names: List[str] = []
        self._visible_channels: List[int] = []
        
        self._setup_ui()
    
    def _setup_ui(self):
        """设置UI"""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        
        self.figure = Figure(figsize=(8, 6))
        self.canvas = FigureCanvas(self.figure)
        layout.addWidget(self.canvas)
        
        self.axes = self.figure.add_subplot(111)
        self.axes.set_xlabel('Time (s)')
        self.axes.set_ylabel('Amplitude')
        self.axes.grid(True, alpha=0.3)
        
        self.figure.tight_layout()
    
    def set_data(self, times: np.ndarray, data: np.ndarray,
                 channel_names: Optional[List[str]] = None):
        """设置时间序列数据
        
        Args:
            times: 时间数组 (N,)
            data: 数据矩阵 (N,) 或 (N, n_channels)
            channel_names: 通道名称列表
        """
        self._times = times
        self._data = data
        
        if channel_names is not None:
            self._channel_names = channel_names
        elif data.ndim == 2:
            self._channel_names = [f'Ch{i}' for i in range(data.shape[1])]
        else:
            self._channel_names = ['Data']
        
        if data.ndim == 1:
            self._visible_channels = [0]
        else:
            self._visible_channels = list(range(data.shape[1]))
        
        self.plot()
        self.data_changed.emit()
    
    def plot(self):
        """绘制时间序列"""
        if self._times is None or self._data is None:
            return
        
        self.axes.clear()
        
        data = self._data
        if data.ndim == 1:
            data = data.reshape(-1, 1)
        
        for i in self._visible_channels:
            if i < data.shape[1]:
                label = self._channel_names[i] if i < len(self._channel_names) else f'Ch{i}'
                self.axes.plot(self._times, data[:, i], label=label, alpha=0.8)
        
        self.axes.set_xlabel('Time (s)')
        self.axes.set_ylabel('Amplitude')
        self.axes.grid(True, alpha=0.3)
        self.axes.legend(loc='upper right', fontsize=8)
        
        self.figure.tight_layout()
        self.canvas.draw()
    
    def set_visible_channels(self, channels: List[int]):
        """设置可见通道
        
        Args:
            channels: 通道索引列表
        """
        self._visible_channels = channels
        self.plot()
    
    def clear(self):
        """清除显示"""
        self._times = None
        self._data = None
        self._channel_names = []
        self._visible_channels = []
        self.axes.clear()
        self.axes.set_xlabel('Time (s)')
        self.axes.set_ylabel('Amplitude')
        self.canvas.draw()
