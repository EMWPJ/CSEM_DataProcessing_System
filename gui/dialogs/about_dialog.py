"""关于对话框"""

from PySide6.QtWidgets import QDialog, QVBoxLayout, QLabel, QPushButton


class AboutDialog(QDialog):
    """关于对话框"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle('关于')
        self.setModal(True)
        self.resize(400, 300)
        self._setup_ui()
    
    def _setup_ui(self):
        layout = QVBoxLayout(self)
        
        layout.addWidget(QLabel('<h2>CSEM数据处理系统</h2>'))
        layout.addWidget(QLabel('版本: v1.0'))
        layout.addWidget(QLabel(''))
        layout.addWidget(QLabel('可控源电磁法(CSEM)数据处理教学演示系统'))
        layout.addWidget(QLabel(''))
        layout.addWidget(QLabel('功能：从原始时间序列到阻抗的全流程计算'))
        layout.addWidget(QLabel(''))
        layout.addWidget(QLabel('作者: 自动生成'))
        layout.addWidget(QLabel('日期: 2026-03-19'))
        
        layout.addStretch()
        
        self.btn_close = QPushButton('关闭')
        self.btn_close.clicked.connect(self.accept)
        layout.addWidget(self.btn_close)
