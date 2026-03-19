"""CSEM数据处理系统 - 主程序入口"""

import sys
from typing import Optional, Dict, List

import numpy as np

sys.path.insert(0, '.')

from PySide6.QtWidgets import QApplication

from gui.main_window import MainWindow
from core.data_reader import DataReader
from core.preprocessing import Preprocessor
from core.spectrum import SpectrumAnalyzer
from core.impedance import ImpedanceCalculator, ImpedanceResult
from core.resistivity import compute_apparent_resistivity
from core.emission_extractor import EmissionExtractor


class CSEMApplication:
    """CSEM数据处理应用程序"""
    
    def __init__(self):
        self.app = QApplication(sys.argv)
        self.window = MainWindow()
        
        self._times: Optional[np.ndarray] = None
        self._raw_data: Optional[np.ndarray] = None
        self._processed_data: Optional[np.ndarray] = None
        self._channel_names: list = []
        self._sample_rate: float = 200.0
        
        self._freqs: Optional[np.ndarray] = None
        self._psd: Optional[np.ndarray] = None
        self._impedance_results: Dict[float, ImpedanceResult] = {}
        self._apparent_resistivity: Optional[np.ndarray] = None
        
        self._connect_signals()
    
    def _connect_signals(self):
        """连接信号"""
        self.window.control_panel.file_open_clicked.connect(self._on_open_file)
        self.window.control_panel.load_sample_clicked.connect(self._on_load_sample)
        self.window.control_panel.step_changed.connect(self._on_step_changed)
        self.window.control_panel.process_clicked.connect(self._on_process)
        self.window.control_panel.reset_clicked.connect(self._on_reset)
        
        self.window.action_open.triggered.connect(self._on_open_file)
        self.window.action_load_sample.triggered.connect(self._on_load_sample)
        self.window.action_exit.triggered.connect(self._on_exit)
        self.window.action_about.triggered.connect(self._on_about)
    
    def _on_open_file(self):
        """打开文件"""
        filepath = self.window.get_open_file_name()
        if filepath is None:
            return
        
        try:
            self.window.set_status(f'正在读取文件: {filepath}')
            
            data_format = DataReader.auto_detect_format(filepath)
            
            if data_format == 'csv':
                times, data, channel_names = DataReader.read_csv(filepath)
            else:
                self.window.show_error('错误', '暂不支持该数据格式，请提供CSV格式或联系开发者')
                self.window.set_status('读取失败')
                return
            
            self._times = times
            self._raw_data = data
            self._channel_names = channel_names
            
            if len(times) > 1:
                dt = times[1] - times[0]
                self._sample_rate = 1.0 / dt
                self.window.control_panel.spin_fs.setValue(self._sample_rate)
            
            self._processed_data = data.copy()
            
            self.window.time_series_widget.set_data(times, data, channel_names)
            self.window.set_status(f'已加载: {len(times)} 样本, {data.shape[1] if data.ndim > 1 else 1} 通道')
            self.window.action_export.setEnabled(True)
            
        except Exception as e:
            self.window.show_error('读取错误', f'无法读取文件:\n{str(e)}')
            self.window.set_status('读取失败')
    
    def _on_load_sample(self):
        """加载示例数据"""
        self.window.set_status('正在生成示例数据...')
        
        fs = 200.0
        duration = 10.0
        n_samples = int(fs * duration)
        times = np.arange(n_samples) / fs
        
        freqs = [0.1, 0.5, 1.0, 2.0]
        n_channels = 5
        data = np.zeros((n_samples, n_channels))
        
        for f in freqs:
            for i in range(n_samples):
                t = times[i]
                data[i, 0] += np.sin(2 * np.pi * f * t)
                data[i, 1] += 0.8 * np.sin(2 * np.pi * f * t + 0.3)
                data[i, 2] += 0.1 * np.sin(2 * np.pi * f * t + 1.2)
                data[i, 3] += 0.05 * np.sin(2 * np.pi * f * t + 0.8)
                data[i, 4] += np.sin(2 * np.pi * f * t)
        
        noise = np.random.randn(n_samples, n_channels) * 0.05
        data += noise
        
        channel_names = ['Ex', 'Ey', 'Hx', 'Hy', 'Current']
        
        self._times = times
        self._raw_data = data
        self._channel_names = channel_names
        self._sample_rate = fs
        self._processed_data = data.copy()
        
        self.window.control_panel.spin_fs.setValue(fs)
        self.window.time_series_widget.set_data(times, data, channel_names)
        self.window.set_status(f'已加载示例数据: {n_samples} 样本, {n_channels} 通道')
        self.window.action_export.setEnabled(True)
    
    def _on_step_changed(self, step: int):
        """步骤改变"""
        self.window.set_step(step + 1, 7)
    
    def _on_process(self):
        """全流程处理"""
        if self._raw_data is None:
            self.window.show_error('错误', '请先加载数据')
            return
        
        params = self.window.control_panel.get_params()
        fs = params['sample_rate']
        
        self.window.set_status('步骤1/7: 预处理...')
        self.window.set_step(1, 7)
        
        preprocessor = Preprocessor(fs)
        self._processed_data = preprocessor.process(
            self._raw_data,
            remove_dc=params['remove_dc'],
            remove_trend=True,
            notch=params['notch_filter'],
            fline=50.0,
            bandpass=params['bandpass'],
            low_freq=params['bp_low'],
            high_freq=params['bp_high']
        )
        
        self.window.time_series_widget.set_data(self._times, self._processed_data, self._channel_names)
        
        self.window.set_status('步骤2/7: 发射时段提取...')
        self.window.set_step(2, 7)
        
        extractor = EmissionExtractor(fs, params['target_frequencies'])
        
        self.window.set_status('步骤3/7: 频谱分析...')
        self.window.set_step(3, 7)
        
        analyzer = SpectrumAnalyzer(fs)
        if self._processed_data.ndim == 1:
            self._freqs, self._psd = analyzer.compute_psd(self._processed_data)
            self.window.spectrum_widget.set_data(self._freqs, self._psd, self._channel_names[:1])
        else:
            self._freqs, self._psd = analyzer.compute_psd(self._processed_data[:, :4])
            self.window.spectrum_widget.set_data(self._freqs, self._psd, self._channel_names[:4])
        
        self.window.set_status('步骤4/7: 阻抗计算...')
        self.window.set_step(4, 7)
        
        if self._processed_data.ndim == 2 and self._processed_data.shape[1] >= 4:
            data_dict = {
                'Ex': self._processed_data[:, 0],
                'Ey': self._processed_data[:, 1],
                'Hx': self._processed_data[:, 2],
                'Hy': self._processed_data[:, 3]
            }
            
            impedance_calc = ImpedanceCalculator(fs)
            target_freqs = params['target_frequencies']
            
            zxy_mag_list = []
            zxy_phase_list = []
            zyx_mag_list = []
            zyx_phase_list = []
            rho_list = []
            
            for freq in target_freqs:
                result = impedance_calc.compute_impedance(
                    data_dict['Ex'], data_dict['Ey'],
                    data_dict['Hx'], data_dict['Hy'],
                    freq=freq,
                    method='robust'
                )
                self._impedance_results[freq] = result
                
                zxy_mag_list.append(result.zxy_magnitude)
                zxy_phase_list.append(result.zxy_phase)
                zyx_mag_list.append(result.zyx_magnitude)
                zyx_phase_list.append(result.zyx_phase)
                
                rho = compute_apparent_resistivity(result.zxy, freq)
                rho_list.append(rho)
            
            self.window.set_status('步骤5/7: 显示结果...')
            self.window.set_step(5, 7)
            
            freq_array = np.array(target_freqs)
            zxy_mag_array = np.array(zxy_mag_list)
            zxy_phase_array = np.array(zxy_phase_list)
            zyx_mag_array = np.array(zyx_mag_list)
            zyx_phase_array = np.array(zyx_phase_list)
            rho_array = np.array(rho_list)
            
            self._apparent_resistivity = rho_array
            
            self.window.impedance_widget.set_data(
                freq_array,
                zxy_magnitude=zxy_mag_array,
                zxy_phase=zxy_phase_array,
                zyx_magnitude=zyx_mag_array,
                zyx_phase=zyx_phase_array,
                apparent_resistivity=rho_array
            )
        
        self.window.set_status('处理完成')
        self.window.set_step(7, 7)
    
    def _on_reset(self):
        """重置"""
        self._times = None
        self._raw_data = None
        self._processed_data = None
        self._channel_names = []
        self._sample_rate = 200.0
        self._freqs = None
        self._psd = None
        self._impedance_results = {}
        self._apparent_resistivity = None
        
        self.window.time_series_widget.clear()
        self.window.spectrum_widget.clear()
        self.window.impedance_widget.clear()
        
        self.window.control_panel.set_current_step(0)
        self.window.set_status('已重置')
        self.window.set_step(0, 7)
    
    def _on_exit(self):
        """退出"""
        self.app.quit()
    
    def _on_about(self):
        """关于"""
        self.window.show_about()
    
    def run(self):
        """运行应用程序"""
        self.window.show()
        return self.app.exec()


def main():
    """主函数"""
    app = CSEMApplication()
    sys.exit(app.run())


if __name__ == '__main__':
    main()
