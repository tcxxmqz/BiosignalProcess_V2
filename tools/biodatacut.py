from scipy.io import loadmat
import numpy as np
from pandas import read_csv

global signal_data


def biosignal_cut(biodata_file, start_time, stop_time, sampling_rate=2000, channel='all', save_filepath=None):
    """
    信号切分函数，输入原始大段生理信号数据，切分时间段，输出对应信号分段

    :param biodata_file: biopac导出的mat格式文件路径，注意格式
    :param start_time: 开始切分的时间点，单位秒
    :param stop_time: 停止切分时间点，单位秒
    :param sampling_rate: 数据的采样频率，单位hz
    :param channel: 数据在mat格式文件中的列，一般有三列，从0开始数
    :param save_filepath: 切分后数据保存位置
    :return: array，切分后的数据分段
    """

    # 加载文件
    global signal_data
    if channel == 'all':
        signal_data = read_csv(biodata_file)
        # 脑血流数据清洗
        signal_data.replace(r'-.-----', 0, inplace=True)
    elif channel in [0, 1, 2]:
        signal_data = loadmat(biodata_file)["data"][:, channel]
        # signal_data = loadmat(mat_file)["data"]

    # 起始位置计算
    start_time_cut = start_time * sampling_rate
    stop_time_cut = stop_time * sampling_rate

    # 数据切分
    signal_data_cut = signal_data[start_time_cut: stop_time_cut]

    # 数据保存到文件
    if save_filepath is not None:
        if channel == "all":
            with open(save_filepath, "w+") as file:
                signal_data_cut.to_csv(file, index=0, columns=["CH4", "CH5", "CH6", "CH7", "CH8", "CH9", "CH10", "CH11",
                                                               "CH12", "CH13", "CH14", "CH15", "CH16", "CH17", "CH18",
                                                               "CH19"])
                file.close()
            print("脑血流数据所有通道，{}-{}秒数据已经保存到文件路径{}".format(start_time, stop_time, save_filepath))

        elif channel in [0, 1, 2]:
            with open(save_filepath, "w+") as file:
                np.savetxt(file, signal_data_cut)
                file.close()
            print("第{}通道中，{}-{}秒数据已经保存到文件路径{}".format(channel, start_time, stop_time, save_filepath))

        return signal_data_cut
