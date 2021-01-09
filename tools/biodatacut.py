from pandas import read_csv
from scipy.io import loadmat, savemat  # 别删
import numpy as np  # 别删
import os

global signal_data


def biosignal_cut(biodata_file, start_time=None, stop_time=None, sampling_rate=2000, channel='all', save_filepath=None):
    """
    信号切分函数，输入原始大段生理信号数据，切分时间段，输出对应信号分段

    :param biodata_file: biopac导出的mat格式文件路径，或脑血流csv数据
    :param start_time: 开始切分的时间点，单位秒
    :param stop_time: 停止切分时间点，单位秒
    :param sampling_rate: 数据的采样频率，单位hz
    :param channel: 数据在mat格式文件中的列，一般有三列，从0开始数；填all时，剪脑血流数据
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
    signal_data_cut = signal_data[int(start_time_cut): int(stop_time_cut)]

    # 数据保存到文件
    if save_filepath is not None:
        if channel == "all":
            with open(save_filepath, "w+", newline="") as file:
                signal_data_cut.to_csv(file, index=0, columns=["CH4", "CH5", "CH6", "CH7", "CH8", "CH9", "CH10", "CH11",
                                                               "CH12", "CH13", "CH14", "CH15", "CH16", "CH17", "CH18",
                                                               "CH19"])
                file.close()
            print("脑血流数据所有通道，{}-{}秒数据已经保存到文件路径{}".format(start_time, stop_time, save_filepath))

        elif channel in [0, 1, 2]:
            with open(save_filepath, "w+", newline="") as file:
                np.savetxt(file, signal_data_cut)
                file.close()
            print("第{}通道中，{}-{}秒数据已经保存到文件路径{}".format(channel, start_time, stop_time, save_filepath))

        return signal_data_cut


def signal_cut(signal, segment, start_time, stop_time, path):

    signal_cuted = signal[start_time: stop_time]

    save_path = path[:-4] + "_" + str(segment+1) + ".txt"

    with open(save_path, "w+", newline="") as file:
        np.savetxt(file, signal_cuted)
        file.close()
    print("第{}个片段，{}~{}数据已保存到路径{}".format(segment+1, start_time, stop_time, save_path))


def get_biofile_path(data_path):
    """
    将数据集文件夹中的文件路径保存到4个列表中；标签保存到labels列表中。
    example：./data/-1A/1/exper4_ecg_3010.txt
            数据集路径/类别路径/样本路径/样本生理信号文件路径
            data_path/class_path/biofile_path/biofile
    数据集文件架构：
                data
                  |- -1A
                  |- 1A
                  |- 1B
                     |- 1
                     |- 2
                     |- 3
                     ....
                     |- 20
                         |- ecg.txt
                         |- eda.txt
                         |- emg.txt
                         |- fnirs.txt
    :param data_path: 数据集路径
    :return: 4个包含生理数据txt文件路径字符串的列表，一个标签列表
    """

    ecg_path = []
    eda_path = []
    emg_path = []
    fnirs_path = []
    labels = []

    # 获得类别文件夹路径
    class_path = [data_path + "/" + i for i in os.listdir(data_path)]

    for k in range(len(class_path)):
        # 获得样本路径
        biofile_path = os.listdir(class_path[k])
        _biofile_path = biofile_path
        # 样本路径按文件名排序
        for j, n in enumerate(biofile_path):
            _biofile_path[j] = int(n)
        _biofile_path.sort()
        biofile_path = [str(i) for i in _biofile_path]
        biofile_path = [class_path[k] + "/" + i for i in biofile_path]
        # print(biofile_path)
        # 获得样本内的生理数据txt文件路径，一种数据保存到一个列表，4种数据，4个列表。
        for m in range(len(biofile_path)):
            labels.append(k)  # 数据集标签保存到列表，分三个类别，用数字0， 1， 2代表三种不同的情绪状态。
            bio_path = [biofile_path[m] + "/" + i for i in os.listdir(biofile_path[m])]
            # print(bio_path)
            # 检查文件名，保存到不同的列表。
            for p in bio_path:
                if "ecg" in p:
                    ecg_path.append(p)
                if "eda" in p:
                    eda_path.append(p)
                if "emg" in p:
                    emg_path.append(p)
                if "fnirs" in p:
                    fnirs_path.append(p)

    return ecg_path, eda_path, emg_path, fnirs_path, labels


def channel_formatting():
    a = loadmat(r"C:\Python Files\BiosignalProcess_V2\data\exper_12.26\11\exper11.mat")["exper11"][:, 0].reshape(-1, 1)
    b = loadmat(r"C:\Python Files\BiosignalProcess_V2\data\exper_12.26\11\exper11.mat")["exper11"][:, 1].reshape(-1, 1)
    c = loadmat(r"C:\Python Files\BiosignalProcess_V2\data\exper_12.26\11\exper11.mat")["exper11"][:, 2].reshape(-1, 1)
    e = np.concatenate((b, c, a), axis=1)
    savemat("./exper11.mat", {"data": e})


if __name__ == "__main__":

    ecg_path, eda_path, emg_path, fnirs_path, labels = get_biofile_path("../segment/exper_12.26v2")
    print(len(ecg_path))
