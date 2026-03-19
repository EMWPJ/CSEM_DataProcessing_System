"""控制面板组件

提供参数设置、处理控制和步骤导航功能。
"""

from typing import Callable, List, Optional

from PySide6.QtCore import Signal, Qt
from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QGroupBox,
    QLabel, QDoubleSpinBox, QSpinBox, QCheckBox,
    QPushButton, QRadioButton, QButtonGroup,
    QLineEdit, QListWidget, QListWidgetItem
)


class ControlPanel(QWidget):
    """控制面板组件"""
    
    file_open_clicked = Signal()
    load_sample_clicked = Signal()
    step_changed = Signal(int)
    process_clicked = Signal()
    reset_clicked = Signal()
    
    PROCESS_STEPS = [
        '1. 数据读取',
        '2. 预处理',
        '3. 发射提取',
        '4. 频谱分析',
        '5. 阻抗计算',
        '6. 视电阻率',
        '7. 相位计算'
    ]
    
    def __init__(self, parent: Optional[QWidget] = None):
        super().__init__(parent)
        
        self._current_step = 0
        self._setup_ui()
        self._connect_signals()
    
    def _setup_ui(self):
        """设置UI"""
        layout = QVBoxLayout(self)
        
        layout.addWidget(self._create_data_group())
        layout.addWidget(self._create_params_group())
        layout.addWidget(self._create_steps_group())
        layout.addWidget(self._create_control_group())
        
        layout.addStretch()
    
    def _create_data_group(self) -> QGroupBox:
        """创建数据加载组"""
        group = QGroupBox('数据加载')
        layout = QVBoxLayout(group)
        
        self.btn_open_file = QPushButton('选择文件...')
        self.btn_load_sample = QPushButton('加载示例数据')
        
        layout.addWidget(self.btn_open_file)
        layout.addWidget(self.btn_load_sample)
        
        return group
    
    def _create_params_group(self) -> QGroupBox:
        """创建参数设置组"""
        group = QGroupBox('参数设置')
        layout = QVBoxLayout(group)
        
        fs_layout = QHBoxLayout()
        fs_layout.addWidget(QLabel('采样率 (Hz):'))
        self.spin_fs = QDoubleSpinBox()
        self.spin_fs.setRange(0.1, 100000)
        self.spin_fs.setValue(200.0)
        self.spin_fs.setDecimals(1)
        fs_layout.addWidget(self.spin_fs)
        layout.addLayout(fs_layout)
        
        freq_layout = QHBoxLayout()
        freq_layout.addWidget(QLabel('频率范围 (Hz):'))
        self.spin_freq_min = QDoubleSpinBox()
        self.spin_freq_min.setRange(0.001, 1000)
        self.spin_freq_min.setValue(0.1)
        freq_layout.addWidget(self.spin_freq_min)
        freq_layout.addWidget(QLabel(' - '))
        self.spin_freq_max = QDoubleSpinBox()
        self.spin_freq_max.setRange(0.001, 10000)
        self.spin_freq_max.setValue(100.0)
        freq_layout.addWidget(self.spin_freq_max)
        layout.addLayout(freq_layout)
        
        self.cb_remove_dc = QCheckBox('去除直流')
        self.cb_remove_dc.setChecked(True)
        layout.addWidget(self.cb_remove_dc)
        
        self.cb_notch_filter = QCheckBox('工频陷波 (50Hz)')
        self.cb_notch_filter.setChecked(True)
        layout.addWidget(self.cb_notch_filter)
        
        notch_layout = QHBoxLayout()
        notch_layout.addWidget(QLabel('Q值:'))
        self.spin_notch_q = QDoubleSpinBox()
        self.spin_notch_q.setRange(1, 1000)
        self.spin_notch_q.setValue(30.0)
        notch_layout.addWidget(self.spin_notch_q)
        notch_layout.addWidget(QLabel('谐波数:'))
        self.spin_harmonics = QSpinBox()
        self.spin_harmonics.setRange(1, 10)
        self.spin_harmonics.setValue(3)
        notch_layout.addWidget(self.spin_harmonics)
        layout.addLayout(notch_layout)
        
        self.cb_bandpass = QCheckBox('带通滤波')
        layout.addWidget(self.cb_bandpass)
        
        bp_layout = QHBoxLayout()
        bp_layout.addWidget(QLabel('带宽 (Hz):'))
        self.spin_bp_low = QDoubleSpinBox()
        self.spin_bp_low.setRange(0.001, 1000)
        self.spin_bp_low.setValue(0.01)
        bp_layout.addWidget(self.spin_bp_low)
        bp_layout.addWidget(QLabel(' - '))
        self.spin_bp_high = QDoubleSpinBox()
        self.spin_bp_high.setRange(0.001, 10000)
        self.spin_bp_high.setValue(100.0)
        bp_layout.addWidget(self.spin_bp_high)
        layout.addLayout(bp_layout)
        
        layout.addWidget(QLabel('目标频率列表 (逗号分隔):'))
        self.edit_target_freqs = QLineEdit('0.1, 0.5, 1.0, 2.0')
        layout.addWidget(self.edit_target_freqs)
        
        return group
    
    def _create_steps_group(self) -> QGroupBox:
        """创建处理步骤组"""
        group = QGroupBox('处理步骤')
        layout = QVBoxLayout(group)
        
        self.step_buttons = []
        self.step_group = QButtonGroup()
        
        for i, step in enumerate(self.PROCESS_STEPS):
            rb = QRadioButton(step)
            rb.setCheckable(True)
            self.step_group.addButton(rb, i)
            self.step_buttons.append(rb)
            layout.addWidget(rb)
        
        self.step_buttons[0].setChecked(True)
        
        return group
    
    def _create_control_group(self) -> QGroupBox:
        """创建控制按钮组"""
        group = QGroupBox('处理控制')
        layout = QVBoxLayout(group)
        
        btn_layout = QHBoxLayout()
        self.btn_prev = QPushButton('◀ 上一步')
        self.btn_next = QPushButton('下一步 ▶')
        btn_layout.addWidget(self.btn_prev)
        btn_layout.addWidget(self.btn_next)
        layout.addLayout(btn_layout)
        
        self.btn_process = QPushButton('▶ 全流程处理')
        self.btn_process.setStyleSheet('QPushButton { font-weight: bold; }')
        layout.addWidget(self.btn_process)
        
        self.btn_reset = QPushButton('重置')
        layout.addWidget(self.btn_reset)
        
        return group
    
    def _connect_signals(self):
        """连接信号"""
        self.btn_open_file.clicked.connect(self.file_open_clicked.emit)
        self.btn_load_sample.clicked.connect(self.load_sample_clicked.emit)
        self.btn_prev.clicked.connect(self._on_prev_step)
        self.btn_next.clicked.connect(self._on_next_step)
        self.btn_process.clicked.connect(self.process_clicked.emit)
        self.btn_reset.clicked.connect(self.reset_clicked.emit)
        
        self.step_group.buttonClicked.connect(self._on_step_button_clicked)
    
    def _on_prev_step(self):
        """上一步"""
        if self._current_step > 0:
            self._current_step -= 1
            self.step_buttons[self._current_step].setChecked(True)
            self.step_changed.emit(self._current_step)
    
    def _on_next_step(self):
        """下一步"""
        if self._current_step < len(self.PROCESS_STEPS) - 1:
            self._current_step += 1
            self.step_buttons[self._current_step].setChecked(True)
            self.step_changed.emit(self._current_step)
    
    def _on_step_button_clicked(self, button: QRadioButton):
        """步骤按钮点击"""
        step_id = self.step_group.id(button)
        if step_id != self._current_step:
            self._current_step = step_id
            self.step_changed.emit(self._current_step)
    
    def get_current_step(self) -> int:
        """获取当前步骤"""
        return self._current_step
    
    def set_current_step(self, step: int):
        """设置当前步骤"""
        if 0 <= step < len(self.step_buttons):
            self._current_step = step
            self.step_buttons[step].setChecked(True)
    
    def get_params(self) -> dict:
        """获取参数"""
        target_freqs_str = self.edit_target_freqs.text()
        try:
            target_freqs = [float(f.strip()) for f in target_freqs_str.split(',')]
        except ValueError:
            target_freqs = [0.1, 0.5, 1.0, 2.0]
        
        return {
            'sample_rate': self.spin_fs.value(),
            'freq_min': self.spin_freq_min.value(),
            'freq_max': self.spin_freq_max.value(),
            'remove_dc': self.cb_remove_dc.isChecked(),
            'notch_filter': self.cb_notch_filter.isChecked(),
            'notch_q': self.spin_notch_q.value(),
            'harmonics': self.spin_harmonics.value(),
            'bandpass': self.cb_bandpass.isChecked(),
            'bp_low': self.spin_bp_low.value(),
            'bp_high': self.spin_bp_high.value(),
            'target_frequencies': target_freqs,
        }
