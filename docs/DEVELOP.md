# CSEM数据处理系统 - 开发文档

## 1. 项目概述

### 1.1 项目背景

可控源电磁法（Controlled-Source Electromagnetic Method, CSEM）是一种重要的地球物理勘探方法，广泛应用于油气资源探测、地下水调查、地热能勘探等领域。CSEM数据处理涉及从原始时间序列到最终电磁阻抗的完整计算流程，需要专业的信号处理和地球物理知识。

本系统旨在为CSEM数据处理提供一个**教学演示**平台，完整展示从原始数据到阻抗计算的全过程，帮助学生和研究人员理解CSEM数据处理的原理和方法。

### 1.2 系统目标

1. **教学演示**：完整展示CSEM数据处理流程，每步骤都有可视化输出
2. **流程控制**：支持步骤导航（前进/后退），便于观察中间结果
3. **参数可调**：提供交互式参数调整，实时观察参数变化对结果的影响
4. **结果展示**：清晰展示频谱、阻抗、视电阻率、相位等关键结果

### 1.3 系统特点

- **Python + PySide6**：利用Python丰富的科学计算生态，结合现代化的Qt图形界面
- **模块化设计**：核心处理逻辑与界面分离，便于维护和扩展
- **完整流程**：从原始时间序列到阻抗的8个处理步骤，流程完整
- **可视化驱动**：每个步骤都有图形化输出，便于理解处理原理

---

## 2. 系统架构

### 2.1 整体架构

```
┌─────────────────────────────────────────────────────────────────┐
│                        CSEM数据处理系统                          │
├─────────────────────────────────────────────────────────────────┤
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────────────────┐ │
│  │   主窗口    │  │  控制面板   │  │      可视化区域          │ │
│  │ (MainWindow)│  │  (Control) │  │   (Matplotlib Widgets)   │ │
│  └─────────────┘  └─────────────┘  └─────────────────────────┘ │
├─────────────────────────────────────────────────────────────────┤
│                      核心处理层 (Core)                           │
│  ┌──────────┐ ┌──────────┐ ┌──────────┐ ┌──────────┐ ┌───────┐ │
│  │数据读取器 │ │ 预处理   │ │发射提取器 │ │ 频谱分析 │ │阻抗计算│ │
│  └──────────┘ └──────────┘ └──────────┘ └──────────┘ └───────┘ │
├─────────────────────────────────────────────────────────────────┤
│                      数据层 (Data)                              │
│         时间序列数据 / 处理结果 / 配置参数 / 示例数据             │
└─────────────────────────────────────────────────────────────────┘
```

### 2.2 项目目录结构

```
CSEM_DataProcessing_System/
├── CSEMProcesss.py          # 现有处理模块（复用）
├── core/                    # 核心处理模块
│   ├── __init__.py
│   ├── data_reader.py       # 数据读取器
│   ├── preprocessing.py     # 预处理
│   ├── spectrum.py          # 频谱分析
│   ├── emission_extractor.py# 发射时段提取（接口）
│   ├── impedance.py         # 阻抗计算
│   ├── resistivity.py       # 视电阻率
│   └── phase.py            # 相位计算
├── gui/                     # GUI模块
│   ├── __init__.py
│   ├── main_window.py       # 主窗口
│   ├── styles.py            # 样式主题
│   ├── widgets/
│   │   ├── __init__.py
│   │   ├── time_series_widget.py  # 时间序列组件
│   │   ├── spectrum_widget.py     # 频谱组件
│   │   ├── impedance_widget.py    # 阻抗组件
│   │   └── control_panel.py       # 控制面板
│   └── dialogs/
│       ├── __init__.py
│       ├── file_dialog.py        # 文件选择对话框
│       └── about_dialog.py       # 关于对话框
├── utils/
│   ├── __init__.py
│   ├── plot_utils.py        # 绘图工具
│   ├── file_utils.py        # 文件工具
│   └── config_manager.py     # 配置管理
├── data/                    # 示例数据目录
│   └── sample.bin           # 示例二进制数据
├── tests/                   # 单元测试
│   └── test_core.py
├── docs/                    # 文档
│   ├── README.md           # 项目说明
│   ├── DEVELOP.md          # 开发文档（本文件）
│   └── ARCHITECTURE.md     # 架构设计
├── requirements.txt         # 依赖列表
├── main.py                 # 程序入口
└── SPEC.md                 # 需求规格说明
```

---

## 3. 功能模块设计

### 3.1 处理流程总览

CSEM数据处理系统按照以下流程进行处理：

```
┌─────────┐    ┌─────────┐    ┌─────────────┐    ┌─────────┐
│数据读取 │ -> │ 预处理  │ -> │发射时段提取 │ -> │ 频谱分析│
└─────────┘    └─────────┘    └─────────────┘    └─────────┘
                                                    │
                                                    ▼
┌─────────┐    ┌─────────┐    ┌─────────┐    ┌─────────┐
│ 结果导出 │ <- │ 绘图输出│ <- │ 相位计算│ <- │阻抗计算 │
└─────────┘    └─────────┘    └─────────┘    └─────────┘
```

### 3.2 模块详细设计

#### 3.2.1 数据读取模块 (data_reader)

**职责**：读取原始时间序列数据

**功能**：
- 支持CSV/ASCII文本格式读取
- 支持二进制原始数据读取（预留接口）
- 自动识别数据格式
- 返回时间数组和数据矩阵

**接口**：

```python
class DataReader:
    @staticmethod
    def read_csv(filepath: str, **kwargs) -> Tuple[np.ndarray, np.ndarray]:
        """读取CSV格式数据"""
        
    @staticmethod
    def read_binary(filepath: str, header_info: dict) -> Tuple[np.ndarray, np.ndarray]:
        """读取二进制格式数据
        
        Args:
            filepath: 文件路径
            header_info: 包含以下字段的字典
                - n_channels: 通道数
                - sample_rate: 采样率 Hz
                - data_type: 'int16'|'int32'|'float32'
                - byte_order: 'little'|'big'
                - header_bytes: 文件头字节数
                - gain: 增益系数列表
        
        Returns:
            (times, data): 时间数组 (N,)，数据矩阵 (N, n_channels)
        """
        raise NotImplementedError("二进制读取接口，具体实现待定")
```

**输出数据传输**：
- 时间数组：`times` shape=(N,)
- 数据矩阵：`data` shape=(N, n_channels)

---

#### 3.2.2 预处理模块 (preprocessing)

**职责**：对原始数据进行基础预处理

**功能**：
- 直流移除（去均值）
- 趋势移除（线性/多项式）
- 工频陷波滤波（50Hz/60Hz及谐波）
- 带通滤波（保留有效频段）
- 异常值处理

**接口**：

```python
class Preprocessor:
    def __init__(self, fs: float):
        self.fs = fs
    
    def remove_dc(self, data: np.ndarray) -> np.ndarray:
        """去除直流分量（均值）"""
        
    def remove_trend(self, data: np.ndarray, order: int = 1) -> np.ndarray:
        """去除趋势
        
        Args:
            data: 输入数据
            order: 多项式阶数，1=线性，2=二次
        
        Returns:
            去趋势后的数据
        """
    
    def notch_filter(self, data: np.ndarray, fline: float = 50.0, 
                     quality: float = 30.0, harmonics: int = 3) -> np.ndarray:
        """工频陷波滤波"""
    
    def bandpass_filter(self, data: np.ndarray, 
                       low_freq: float, high_freq: float,
                       order: int = 4) -> np.ndarray:
        """带通滤波
        
        Args:
            low_freq: 通带下限频率 (Hz)
            high_freq: 通带上限频率 (Hz)
            order: 滤波器阶数
        """
```

---

#### 3.2.3 发射时段提取模块 (emission_extractor)

**职责**：从连续数据中提取各频率的发射时段

**功能**：
- 接收电流信号作为参考
- 提取不同目标频率对应的发射时段
- 返回各频率段的数据窗口

**接口**：

```python
class EmissionExtractor:
    def __init__(self, fs: float, target_frequencies: List[float]):
        self.fs = fs
        self.target_frequencies = target_frequencies
    
    def extract_windows(self, 
                       times: np.ndarray,
                       data: np.ndarray,
                       current: np.ndarray,
                       window_length: Optional[float] = None,
                       overlap: float = 0.5) -> Dict[float, EmissionWindow]:
        """提取发射时段
        
        Args:
            times: 时间数组 (N,)
            data: E场数据 (N, n_e_channels)
            current: 发射电流数据 (N,)
            window_length: 窗口长度（秒），None则自动根据最低频率计算
            overlap: 相邻窗口重叠率 [0, 1)
        
        Returns:
            {frequency: EmissionWindow} 字典
                - times: 窗口内时间
                - data: 窗口内E场数据
                - current: 窗口内电流数据
        
        Note:
            具体提取逻辑（相关检测、模板匹配、噪声门限等）待实现
        """
        raise NotImplementedError("发射时段提取逻辑待实现")


@dataclass
class EmissionWindow:
    times: np.ndarray
    data: np.ndarray  # (N_window, n_channels)
    current: np.ndarray  # (N_window,)
    frequency: float
    start_index: int
    end_index: int
```

---

#### 3.2.4 频谱分析模块 (spectrum)

**职责**：计算信号的频谱特性

**功能**：
- FFT频谱计算
- Welch功率谱密度估计
- 交叉谱计算（用于相位）
- 幅度谱/相位谱分离

**接口**：

```python
class SpectrumAnalyzer:
    def __init__(self, fs: float):
        self.fs = fs
    
    def compute_psd(self, data: np.ndarray, 
                    nperseg: Optional[int] = None,
                    noverlap: Optional[int] = None,
                    window: str = 'hann') -> Tuple[np.ndarray, np.ndarray]:
        """Welch方法功率谱密度估计
        
        Args:
            data: 输入数据 (N,) 或 (N, n_channels)
            nperseg: FFT分段长度
            noverlap: 分段重叠点数
            window: 窗函数类型
        
        Returns:
            (freqs, psd): 频率数组，功率谱密度
        """
    
    def compute_cross_spectrum(self, signal1: np.ndarray, signal2: np.ndarray,
                              nperseg: Optional[int] = None) -> Tuple[np.ndarray, np.ndarray]:
        """交叉谱计算
        
        Returns:
            (freqs, csd): 频率数组，交叉功率谱密度
        """
    
    def compute_amplitude_phase(self, data: np.ndarray) -> Tuple[np.ndarray, np.ndarray]:
        """计算幅度谱和相位谱
        
        Returns:
            (amplitude, phase): 幅度谱，相位谱（弧度）
        """
```

---

#### 3.2.5 阻抗计算模块 (impedance)

**职责**：计算电磁阻抗

**功能**：
- 单点阻抗计算 Z = E/H
- 张量阻抗计算
- 阻抗幅值和相位提取

**接口**：

```python
class ImpedanceCalculator:
    def __init__(self, fs: float):
        self.fs = fs
    
    def compute_impedance(self, 
                         ex: np.ndarray, ey: np.ndarray,
                         hx: np.ndarray, hy: np.ndarray,
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
            ImpedanceResult包含：
                - zxx, zxy, zyx, zyy: 张量阻抗分量
                - zxx_err, zxy_err, zyx_err, zyy_err: 估计误差
                - zxy_phase, zyx_phase: 阻抗相位
        """
    
    def compute_tensor_impedance(self, data_dict: Dict[str, np.ndarray], 
                                 freq: float) -> np.ndarray:
        """计算张量阻抗矩阵
        
        Returns:
            Z: 2x2 复数阻抗矩阵 [[Zxx, Zxy], [Zyx, Zyy]]
        """


@dataclass
class ImpedanceResult:
    zxx: complex
    zxy: complex
    zyx: complex
    zyy: complex
    zxx_err: float = 0.0
    zxy_err: float = 0.0
    zyx_err: float = 0.0
    zyy_err: float = 0.0
```

---

#### 3.2.6 视电阻率模块 (resistivity)

**职责**：计算视电阻率

**接口**：

```python
def compute_apparent_resistivity(z: complex, freq: float, 
                                 geometry_factor: float = 1.0,
                                 mu0: float = 4e-7 * np.pi) -> float:
    """计算视电阻率
    
    Formula: ρa = (1/μ0ω) * |Z|² = (|Z|²) / (2πμ0f)
    
    Args:
        z: 复数阻抗
        freq: 频率 (Hz)
        geometry_factor: 几何因子K
        mu0: 真空磁导率
    
    Returns:
        视电阻率 (Ω·m)
    """
    return geometry_factor * (np.abs(z) ** 2) / (2 * np.pi * mu0 * freq)
```

---

#### 3.2.7 相位计算模块 (phase)

**职责**：计算阻抗相位

**接口**：

```python
def compute_impedance_phase(z: complex) -> float:
    """计算阻抗相位
    
    Args:
        z: 复数阻抗
    
    Returns:
        相位角 (度)
    """
    return np.angle(z, deg=True)
```

---

## 4. 数据流设计

### 4.1 核心数据结构

```python
@dataclass
class CSEMData:
    """CSEM处理数据容器"""
    # 原始数据
    times: np.ndarray
    raw_data: np.ndarray  # (N, n_channels)
    
    # 通道信息
    channel_names: List[str]  # ['Ex', 'Ey', 'Hx', 'Hy', 'Current']
    sample_rate: float  # Hz
    
    # 处理后数据
    processed_data: Optional[np.ndarray] = None
    emission_windows: Optional[Dict[float, EmissionWindow]] = None
    
    # 处理结果
    spectrum_result: Optional[Dict[str, np.ndarray]] = None
    impedance_result: Optional[ImpedanceResult] = None
    apparent_resistivity: Optional[float] = None
    impedance_phase: Optional[float] = None
    
    # 元数据
    station_name: str = ""
    survey_date: str = ""
    file_path: str = ""


@dataclass
class ProcessingConfig:
    """处理配置参数"""
    # 采样率
    sample_rate: float = 200.0  # Hz
    
    # 预处理参数
    remove_dc: bool = True
    remove_trend: bool = True
    trend_order: int = 1
    notch_filter: bool = True
    notch_frequency: float = 50.0  # Hz
    notch_quality: float = 30.0
    notch_harmonics: int = 3
    
    # 频谱分析参数
    fft_length: Optional[int] = None  # None=自动
    nperseg: Optional[int] = 1024
    noverlap: Optional[int] = 512
    
    # 发射提取参数
    target_frequencies: List[float] = field(default_factory=lambda: [0.1, 0.5, 1.0, 2.0])
    window_length: Optional[float] = None  # None=自动
    overlap_ratio: float = 0.5
    
    # 几何因子
    geometry_factor: float = 1.0
```

### 4.2 数据处理管道

```
                    ┌──────────────┐
                    │  原始数据    │
                    │  (文件)      │
                    └──────┬───────┘
                           │
                           ▼
┌─────────────────────────────────────────────────────────────┐
│                    DataReader.read()                         │
│                    读取原始数据                               │
└─────────────────────────────────────────────────────────────┘
                           │
                           ▼
                    ┌──────────────┐
                    │  CSEMData    │
                    │  (原始)      │
                    └──────┬───────┘
                           │
                           ▼
┌─────────────────────────────────────────────────────────────┐
│                   Preprocessor.process()                     │
│  去除直流 → 去趋势 → 陷波滤波 → 带通滤波                     │
└─────────────────────────────────────────────────────────────┘
                           │
                           ▼
                    ┌──────────────┐
                    │  CSEMData    │
                    │  (预处理后)  │
                    └──────┬───────┘
                           │
                           ▼
┌─────────────────────────────────────────────────────────────┐
│               EmissionExtractor.extract()                    │
│  相关检测 → 窗口截取 → 分频段存储                            │
└─────────────────────────────────────────────────────────────┘
                           │
                           ▼
                    ┌──────────────┐
                    │  CSEMData    │
                    │  (发射时段)   │
                    └──────┬───────┘
                           │
                           ▼
┌─────────────────────────────────────────────────────────────┐
│                 SpectrumAnalyzer.analyze()                   │
│  分段 → 加窗 → FFT → 平均 → PSD/CSD                         │
└─────────────────────────────────────────────────────────────┘
                           │
                           ▼
                    ┌──────────────┐
                    │  CSEMData    │
                    │  (频谱)       │
                    └──────┬───────┘
                           │
                           ▼
┌─────────────────────────────────────────────────────────────┐
│                ImpedanceCalculator.compute()                │
│  Ex/Hx, Ey/Hy, Ey/Hx, Ex/Hy → 张量阻抗                      │
└─────────────────────────────────────────────────────────────┘
                           │
                           ▼
                    ┌──────────────┐
                    │  结果数据    │
                    │  Zxy, ρa, φ  │
                    └──────────────┘
```

---

## 5. 界面设计

### 5.1 主窗口布局

```
┌────────────────────────────────────────────────────────────────────┐
│ CSEM数据处理系统 v1.0          [文件(F)] [帮助(H)]                  │
├────────────────────────────────────────────────────────────────────┤
│ ┌──────────────┐  ┌────────────────────────────────────────────┐  │
│ │  控制面板     │  │                                            │  │
│ │              │  │         时间序列/频谱/阻抗显示区域            │  │
│ │ ▼ 数据加载   │  │         (Matplotlib Figure Canvas)         │  │
│ │  [选择文件]  │  │                                            │  │
│ │  [加载示例]  │  │                                            │  │
│ │              │  │                                            │  │
│ │ ▼ 参数设置   │  │                                            │  │
│ │  采样率[Hz]  │  │                                            │  │
│ │  频率范围    │  │                                            │  │
│ │  滤波参数    │  │                                            │  │
│ │              │  │                                            │  │
│ │ ▼ 处理步骤   │  │                                            │  │
│ │  ○ 数据读取  │  │                                            │  │
│ │  ○ 预处理   │  │                                            │  │
│ │  ○ 发射提取  │  │                                            │  │
│ │  ● 频谱分析  │  │                                            │  │
│ │  ○ 阻抗计算  │  │                                            │  │
│ │              │  │                                            │  │
│ │ [◀ 上一步]   │  │                                            │  │
│ │ [下一步 ▶]  │  │                                            │  │
│ │ [▶ 全流程]  │  │                                            │  │
│ │ [重置]      │  │                                            │  │
│ └──────────────┘  └────────────────────────────────────────────┘  │
├────────────────────────────────────────────────────────────────────┤
│ 状态: 就绪                                    处理步骤: 4/7        │
└────────────────────────────────────────────────────────────────────┘
```

### 5.2 组件规格

#### 5.2.1 时间序列组件 (TimeSeriesWidget)

**功能**：显示原始和处理后的时间序列

**显示内容**：
- 多通道时间序列（垂直堆叠或叠加显示可切换）
- 通道选择复选框
- 十字光标，显示点击位置的坐标
- 可选：发射时段标记

**交互**：
- 缩放（鼠标滚轮）
- 平移（鼠标拖拽）
- 通道显示/隐藏切换

#### 5.2.2 频谱组件 (SpectrumWidget)

**功能**：显示功率谱密度和相位谱

**显示内容**：
- 双Y轴：左侧功率谱(dB)，右侧相位(度)
- 可切换线性/对数频率轴
- 多通道叠加显示
- 峰值标记

**交互**：
- 频率范围选择
- 通道选择
- 坐标单位切换

#### 5.2.3 阻抗组件 (ImpedanceWidget)

**功能**：显示阻抗曲线

**显示内容**：
- 子图1：|Zxy|, |Zyx| 幅度 vs 频率
- 子图2：相位φxy, φyx vs 频率
- 子图3：视电阻率ρa vs 频率
- 子图4：张量阻抗椭圆（可选）

**交互**：
- 频率对数/线性切换
- 数据点提示
- 导出图片

#### 5.2.4 控制面板 (ControlPanel)

**功能**：参数设置和处理控制

**组成**：
- 数据加载区：文件选择按钮、示例数据按钮
- 参数设置区：QSpinBox/QDoubleSpinBox输入
- 步骤指示器：QRadioButton列表
- 处理控制按钮：上一步/下一步/全流程/重置

---

## 6. 接口规范

### 6.1 核心模块接口

所有核心处理模块遵循统一接口规范：

```python
from abc import ABC, abstractmethod
from typing import TypeVar, Generic

T_in = TypeVar('T_in')
T_out = TypeVar('T_out')

class Processor(ABC, Generic[T_in, T_out]):
    """处理基类"""
    
    @abstractmethod
    def process(self, data: T_in, config: Optional[ProcessingConfig] = None) -> T_out:
        """执行处理"""
        pass
    
    @abstractmethod
    def validate_input(self, data: T_in) -> bool:
        """验证输入数据"""
        pass
    
    def get_config_widget(self) -> Optional[QWidget]:
        """返回配置面板（可选）"""
        return None
```

### 6.2 信号与槽规范

```python
# 处理状态信号
class ProcessingSignals(QObject):
    started = Signal(str)           # 处理开始 (step_name)
    progress = Signal(int, int)     # 进度更新 (current, total)
    finished = Signal(str, object)   # 处理完成 (step_name, result)
    error = Signal(str, str)         # 错误 (step_name, message)
    
# 数据更新信号
class DataSignals(QObject):
    data_updated = Signal(str)       # 数据更新 (data_key)
    config_changed = Signal(dict)    # 配置变更
```

### 6.3 异常处理规范

```python
class CSEMError(Exception):
    """CSEM处理基础异常"""
    pass

class DataReadError(CSEMError):
    """数据读取异常"""
    pass

class ProcessingError(CSEMError):
    """数据处理异常"""
    pass

class ValidationError(CSEMError):
    """数据验证异常"""
    pass
```

---

## 7. 错误处理

### 7.1 异常分类

| 异常类型 | 说明 | 处理方式 |
|---------|------|---------|
| DataReadError | 无法读取文件 | 弹出文件选择对话框让用户重新选择 |
| InvalidFormatError | 数据格式不正确 | 提示用户并显示期望格式 |
| InsufficientDataError | 数据长度不足 | 提示并建议增加数据长度 |
| ProcessingError | 处理计算错误 | 记录日志，尝试跳过该步骤 |
| ConfigError | 配置参数错误 | 高亮错误参数，提示有效范围 |

### 7.2 日志规范

```python
import logging

logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('csem_processing.log'),
        logging.StreamHandler()
    ]
)
```

---

## 8. 性能考虑

### 8.1 大数据处理

- 对于长时间序列（>100MB），采用分块处理
- 使用NumPy向量化运算，避免Python循环
- 必要时使用numba JIT编译加速

### 8.2 GUI响应性

- 长时间处理操作在单独线程执行
- 使用QProgressDialog显示进度
- 处理完成后通过信号更新GUI

### 8.3 内存管理

- 及时释放中间结果内存
- 使用生成器处理大数据文件
- 避免不必要的数据复制

---

## 9. 测试策略

### 9.1 单元测试

```python
# tests/test_core.py
import unittest
import numpy as np
from core.preprocessing import Preprocessor
from core.spectrum import SpectrumAnalyzer

class TestPreprocessor(unittest.TestCase):
    def test_remove_dc(self):
        data = np.array([1, 2, 3, 4, 5])
        result = Preprocessor.remove_dc(data)
        self.assertAlmostEqual(np.mean(result), 0, places=10)
    
    def test_notch_filter(self):
        # 生成测试信号并验证陷波效果
        pass

class TestSpectrumAnalyzer(unittest.TestCase):
    def test_psd_shape(self):
        fs = 100
        data = np.random.randn(1000)
        freqs, psd = SpectrumAnalyzer(fs).compute_psd(data)
        self.assertEqual(len(freqs), len(psd))
```

### 9.2 集成测试

- 使用示例数据验证完整处理流程
- 对比输出与参考值（如果提供）

---

## 10. 开发计划

### Phase 1: 框架搭建（第1周）
- [ ] 创建项目目录结构
- [ ] 实现PySide6主窗口框架
- [ ] 实现基础控件类
- [ ] 集成现有CSEMProcesss.py模块

### Phase 2: 核心功能（第2周）
- [ ] DataReader数据读取器
- [ ] Preprocessor预处理
- [ ] EmissionExtractor接口（空实现）
- [ ] SpectrumAnalyzer频谱分析

### Phase 3: 阻抗计算（第3周）
- [ ] ImpedanceCalculator阻抗计算
- [ ] 视电阻率和相位计算
- [ ] 阻抗显示组件

### Phase 4: 完善与测试（第4周）
- [ ] 参数配置保存/加载
- [ ] 结果导出功能
- [ ] 帮助文档
- [ ] 集成测试

---

## 11. 编码规范

### 11.1 命名规范

| 类型 | 规范 | 示例 |
|-----|------|------|
| 类名 | PascalCase | `TimeSeriesWidget` |
| 函数/方法 | snake_case | `compute_impedance` |
| 常量 | UPPER_SNAKE | `DEFAULT_SAMPLE_RATE` |
| 实例变量 | snake_case | `sample_rate` |
| 私有变量 | _前缀 | `_internal_data` |
| 类型变量 | PascalCase | `T_in`, `T_out` |

### 11.2 文档规范

```python
def compute_impedance(voltage: np.ndarray, current: np.ndarray, 
                     fs: float, freq: Optional[float] = None) -> complex:
    """计算阻抗 Z = V / I.
    
    基于FFT频域比值计算复数阻抗，包含幅度和相位信息。
    
    Args:
        voltage: 电压时域数据 (N,)
        current: 电流时域数据 (N,)，必须与电压同长度
        fs: 采样率 (Hz)
        freq: 目标频率 (Hz)，None则使用电压谱峰值频率
    
    Returns:
        复数阻抗 (幅值 = |Z|, 相位 = arg(Z) in radians)
    
    Raises:
        ValueError: 当voltage和current长度不一致时
    
    Example:
        >>> import numpy as np
        >>> t = np.linspace(0, 1, 1000)
        >>> V = np.sin(2*np.pi*10*t)
        >>> I = np.sin(2*np.pi*10*t + 0.5)
        >>> Z = compute_impedance(V, I, 1000, 10)
        >>> print(f"|Z| = {np.abs(Z):.3f}, arg(Z) = {np.angle(Z):.3f}")
    """
```

### 11.3 类型注解

- 所有公共函数必须包含类型注解
- 使用 `Optional[X]` 表示可选参数
- 使用 `List[X]`, `Dict[K, V]` 等容器类型

---

## 12. 依赖管理

### requirements.txt

```
PySide6>=6.6.0
numpy>=1.24.0
scipy>=1.11.0
matplotlib>=3.7.0
pandas>=2.0.0
PyYAML>=6.0
```

---

## 13. 附录

### A. 术语表

| 术语 | 说明 |
|-----|------|
| CSEM | Controlled-Source Electromagnetic Method，可控源电磁法 |
| FFT | Fast Fourier Transform，快速傅里叶变换 |
| PSD | Power Spectral Density，功率谱密度 |
| CSD | Cross Spectral Density，交叉功率谱密度 |
| 阻抗 | Impedance，电磁响应特性 |
| 视电阻率 | Apparent Resistivity，等效电阻率 |
| 张量阻抗 | Tensor Impedance，多分量测量时的阻抗矩阵 |

### B. 参考资料

1. CSEM原理：《地球物理电磁法》教科书
2. PySide6文档：https://doc.qt.io/qtforpython/
3. SciPy信号处理：https://docs.scipy.org/doc/scipy/reference/signal.html
4. Matplotlib绑定：https://matplotlib.org/stable/gallery/user_interfaces/

---

*文档版本：v1.0*
*最后更新：2026-03-19*
