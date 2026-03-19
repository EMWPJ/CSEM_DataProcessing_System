"""主窗口模块"""

from typing import Optional

from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QMainWindow, QWidget, QHBoxLayout, QVBoxLayout,
    QMenuBar, QMenu, QStatusBar, QFileDialog, QMessageBox,
    QTabWidget, QLabel
)
from PySide6.QtGui import QAction

from .widgets.time_series_widget import TimeSeriesWidget
from .widgets.spectrum_widget import SpectrumWidget
from .widgets.impedance_widget import ImpedanceWidget
from .widgets.control_panel import ControlPanel


class MainWindow(QMainWindow):
    """CSEM数据处理系统主窗口"""
    
    def __init__(self, parent: Optional[QWidget] = None):
        super().__init__(parent)
        
        self.setWindowTitle('CSEM数据处理系统 v1.0')
        self.setMinimumSize(1200, 800)
        
        self._setup_ui()
        self._setup_menu()
        self._setup_status_bar()
    
    def _setup_ui(self):
        """设置UI"""
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        main_layout = QHBoxLayout(central_widget)
        
        self.control_panel = ControlPanel()
        self.control_panel.setFixedWidth(280)
        main_layout.addWidget(self.control_panel)
        
        self.tab_widget = QTabWidget()
        
        self.time_series_widget = TimeSeriesWidget()
        self.tab_widget.addTab(self.time_series_widget, '时间序列')
        
        self.spectrum_widget = SpectrumWidget()
        self.tab_widget.addTab(self.spectrum_widget, '频谱')
        
        self.impedance_widget = ImpedanceWidget()
        self.tab_widget.addTab(self.impedance_widget, '阻抗')
        
        main_layout.addWidget(self.tab_widget, stretch=1)
    
    def _setup_menu(self):
        """设置菜单"""
        menubar = self.menuBar()
        
        file_menu = menubar.addMenu('文件(&F)')
        
        self.action_open = QAction('打开...', self)
        self.action_open.setShortcut('Ctrl+O')
        file_menu.addAction(self.action_open)
        
        self.action_load_sample = QAction('加载示例数据', self)
        file_menu.addAction(self.action_load_sample)
        
        file_menu.addSeparator()
        
        self.action_export = QAction('导出结果...', self)
        self.action_export.setShortcut('Ctrl+E')
        self.action_export.setEnabled(False)
        file_menu.addAction(self.action_export)
        
        file_menu.addSeparator()
        
        self.action_exit = QAction('退出', self)
        self.action_exit.setShortcut('Ctrl+Q')
        file_menu.addAction(self.action_exit)
        
        help_menu = menubar.addMenu('帮助(&H)')
        
        self.action_about = QAction('关于...', self)
        help_menu.addAction(self.action_about)
    
    def _setup_status_bar(self):
        """设置状态栏"""
        self.statusBar = QStatusBar()
        self.setStatusBar(self.statusBar)
        
        self.status_label = QLabel('准备就绪')
        self.statusBar.addWidget(self.status_label)
        
        self.step_label = QLabel('步骤: -')
        self.statusBar.addPermanentWidget(self.step_label)
    
    def set_status(self, message: str):
        """设置状态栏消息"""
        self.status_label.setText(message)
    
    def set_step(self, step: int, total: int):
        """设置步骤显示"""
        self.step_label.setText(f'步骤: {step}/{total}')
    
    def show_error(self, title: str, message: str):
        """显示错误对话框"""
        QMessageBox.critical(self, title, message)
    
    def show_info(self, title: str, message: str):
        """显示信息对话框"""
        QMessageBox.information(self, title, message)
    
    def show_about(self):
        """显示关于对话框"""
        QMessageBox.about(
            self,
            '关于 CSEM数据处理系统',
            'CSEM数据处理系统 v1.0\n\n'
            '可控源电磁法(CSEM)数据处理教学演示系统\n\n'
            '功能：从原始时间序列到阻抗的全流程计算\n\n'
            '作者: 自动生成\n'
            '日期: 2026-03-19'
        )
    
    def get_open_file_name(self) -> Optional[str]:
        """获取打开文件路径"""
        filepath, _ = QFileDialog.getOpenFileName(
            self,
            '打开数据文件',
            '',
            'CSV文件 (*.csv);;二进制文件 (*.bin);;所有文件 (*.*)'
        )
        return filepath if filepath else None
    
    def get_save_file_name(self, default_ext: str = '.csv') -> Optional[str]:
        """获取保存文件路径"""
        filepath, _ = QFileDialog.getSaveFileName(
            self,
            '保存结果',
            '',
            f'CSV文件 (*{default_ext});;所有文件 (*.*)'
        )
        return filepath if filepath else None
