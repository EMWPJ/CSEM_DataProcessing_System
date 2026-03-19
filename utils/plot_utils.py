"""绘图工具函数"""

import matplotlib.pyplot as plt


def setup_matplotlib_style():
    """设置matplotlib样式"""
    plt.style.use('seaborn-v0_8-darkgrid' if 'seaborn-v0_8-darkgrid' in plt.style.available else 'ggplot')
    
    plt.rcParams['figure.facecolor'] = 'white'
    plt.rcParams['axes.facecolor'] = 'white'
    plt.rcParams['font.size'] = 10
    plt.rcParams['axes.labelsize'] = 10
    plt.rcParams['axes.titlesize'] = 12
    plt.rcParams['xtick.labelsize'] = 9
    plt.rcParams['ytick.labelsize'] = 9
    plt.rcParams['legend.fontsize'] = 9
    plt.rcParams['figure.titlesize'] = 14


def get_channel_colors(n_channels: int) -> list:
    """获取通道颜色列表
    
    Args:
        n_channels: 通道数量
    
    Returns:
        颜色列表
    """
    base_colors = [
        '#1f77b4',  # 蓝色
        '#ff7f0e',  # 橙色
        '#2ca02c',  # 绿色
        '#d62728',  # 红色
        '#9467bd',  # 紫色
        '#8c564b',  # 棕色
        '#e377c2',  # 粉色
        '#7f7f7f',  # 灰色
        '#bcbd22',  # 黄绿色
        '#17becf',  # 青色
    ]
    
    if n_channels <= len(base_colors):
        return base_colors[:n_channels]
    
    colors = base_colors * (n_channels // len(base_colors) + 1)
    return colors[:n_channels]
