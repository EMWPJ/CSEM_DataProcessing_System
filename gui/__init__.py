"""GUI模块"""

from .main_window import MainWindow
from .widgets.time_series_widget import TimeSeriesWidget
from .widgets.spectrum_widget import SpectrumWidget
from .widgets.impedance_widget import ImpedanceWidget
from .widgets.control_panel import ControlPanel

__all__ = [
    'MainWindow',
    'TimeSeriesWidget',
    'SpectrumWidget',
    'ImpedanceWidget',
    'ControlPanel',
]
