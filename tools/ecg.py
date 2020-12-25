import matplotlib.pyplot as plt
import biosppy.signals.ecg as biosppy_ecg
from tools.biodatacut import *


def ecg_signal_cut_and_save(file_path, subject, exp_time, start_time, channel=0, show=True):
    """
    切分皮电数据，输入文件路径，第几位受试者，第几次实验，实验开始截取数据的时间点，数据所在的通道；自动保存切分后的文件到输入文件所在的路径

    :param file_path: 原始文件路径
    :param subject: 受试者位次
    :param exp_time: 实验位次
    :param start_time: 开始切分时间点
    :param channel: ecg信号所在通道
    :param show: 是否绘图
    :return: 分段后的信号数据；数据保存的路径
    """
    exp = [60, 40, 34, 30]

    # filepath = r"C:\PythonFiles\BiosignalProcessing\data\exper1.mat"

    save_as_filename = file_path[:-5] + "_" + str(subject) + "_" + str(exp_time) + "_ecg.txt"

    stop_time = start_time + exp[exp_time - 1]

    ecg_signal = biosignal_cut(file_path, start_time, stop_time, channel=channel, save_filepath=save_as_filename)

    if show is True:
        plt.plot(ecg_signal)
        plt.show()

    return ecg_signal, save_as_filename


def ecg_process(raw_signal, exper, path=None):
    """
    心电信号处理，输入未处理的心电信号，输出每分钟心跳次数波形。

    :param raw_signal: 未处理的心电信号
    :param exper: 实验位次，第几次实验
    :param path: 文件保存地址
    :return: 无
    """

    file_path = path[:-4]
    print("ecg_process()正在处理第{}次实验数据。".format(exper))
    biosppy_ecg.ecg(signal=raw_signal, sampling_rate=2000, show=False, plot_method="qz", path=file_path)

# # 载入数据
# path = "C:\\Python Files\\biology_signal\\data_set\\1B\\5\\XD.txt"
# raw_signals = np.loadtxt(path)
#
# # 信号处理及绘图 neurokit2
# # signals, info = nk.ecg_process(raw_signals, sampling_rate=2000)
# # fig = nk.ecg_plot(signals, sampling_rate=2000)
#
# # 信号处理及绘图 biosppy
# biosppy_ecg.ecg(signal=raw_signals, sampling_rate=2000, show=True, plot_method='qz', path=path)
#
# plt.show()
