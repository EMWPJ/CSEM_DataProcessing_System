# CSEM数据处理系统

可控源电磁法（CSEM）数据处理教学演示系统

## 功能特点

- **完整流程**：从原始时间序列到阻抗的全过程计算
- **教学友好**：每个处理步骤都有可视化输出
- **参数可调**：实时调整滤波等参数，观察影响
- **步骤导航**：支持步骤前进/后退，便于理解处理原理

## 处理流程

1. 数据读取 - 读取CSV格式时间序列数据
2. 预处理 - 直流移除、趋势去除、工频陷波
3. 发射时段提取（接口预留）
4. 频谱分析 - FFT、Welch功率谱
5. 阻抗计算 - 张量阻抗
6. 视电阻率计算
7. 相位计算

## 安装

```bash
pip install -r requirements.txt
```

## 运行

```bash
python main.py
```

## 项目结构

```
CSEM_DataProcessing_System/
├── core/                   # 核心处理模块
│   ├── data_reader.py      # 数据读取
│   ├── preprocessing.py    # 预处理
│   ├── spectrum.py         # 频谱分析
│   ├── emission_extractor.py # 发射时段提取（接口）
│   ├── impedance.py        # 阻抗计算
│   ├── resistivity.py      # 视电阻率
│   └── phase.py           # 相位计算
├── gui/                    # PySide6图形界面
│   ├── main_window.py     # 主窗口
│   └── widgets/           # 自定义控件
├── docs/                   # 文档
│   ├── DEVELOP.md         # 开发文档
│   └── SPEC.md            # 需求规格
├── requirements.txt        # 依赖
└── main.py                # 入口
```

## 技术栈

- Python 3.9+
- PySide6 - GUI框架
- NumPy - 数值计算
- SciPy - 信号处理
- Matplotlib - 可视化

## 依赖

```
PySide6>=6.6.0
numpy>=1.24.0
scipy>=1.11.0
matplotlib>=3.7.0
pandas>=2.0.0
PyYAML>=6.0
```

## 文档

- [开发文档](docs/DEVELOP.md) - 详细的系统设计和技术规范
- [需求规格](SPEC.md) - 功能需求和验收标准
