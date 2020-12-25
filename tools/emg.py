import neurokit2.emg as emg
from tools.biodatacut import *
from biosppy.plotting import plot_emg_qz
import matplotlib.pyplot as plt


def emg_signal_cut_and_save(file_path, subject, exp_time, start_time, channel=1, show=True):
    """
    切分肌电数据，输入文件路径，第几位受试者，第几次实验，实验开始截取数据的时间点，数据所在的通道；自动保存切分后的文件到输入文件所在的路径

    :param file_path: 原始文件路径
    :param subject: 受试者位次
    :param exp_time: 实验位次
    :param start_time: 开始切分时间点
    :param channel: eda信号所在通道
    :param show: 是否绘图
    :return: 分段后的信号数据；数据文件保存的路径
    """
    exp = [60, 40, 34, 30]

    # filepath = r"C:\Python Files\BiosignalProcessing\data\exper1.mat"

    save_as_filename = file_path[:-5] + "_" + str(subject) + "_" + str(exp_time) + "_emg.txt"

    stop_time = start_time + exp[exp_time - 1]

    emg_signal = biosignal_cut(file_path, start_time, stop_time, channel=channel, save_filepath=save_as_filename)

    if show is True:
        plt.plot(emg_signal)
        plt.show()

    return emg_signal, save_as_filename


def emg_process(raw_signal, exper, path=None):
    """
    肌电信号处理，简单滤波，绘图

    :param raw_signal: 未处理的肌电信号
    :param exper: 受试者的第几次实验
    :param path: 图像保存的路径
    :return: 无
    """

    print("emg_process()正在处理第{}次实验数据。".format(exper))

    sampling_rate = 2000
    # emg_clean = emg.emg_clean_qz_ellip(raw_signal, sampling_rate=sampling_rate)
    emg_clean = emg.emg_clean(raw_signal, sampling_rate=sampling_rate)

    length = len(emg_clean)
    T = (length - 1) / sampling_rate
    ts = np.linspace(0, T, length, endpoint=True)

    file_path = path[:-4] + ".png"

    plot_emg_qz(ts=ts, emg_cleaned=emg_clean, path=file_path, show=False)
    # emg_amp = emg.emg_amplitude(emg_clean)
    # activity, info = emg.emg_activation(emg_amplitude=emg_amp, emg_cleaned=emg_clean, sampling_rate=sampling_rate,
    #                                     method="biosppy")
    # print("info={}".format(info))
    # fig2 = events_plot([info["EMG_Offsents"], info["EMG_Onsets"]], emg_clean)

    # fig2.savefig(file_path, dpi=300, bbox_inches='tight')
    # plt.show()
