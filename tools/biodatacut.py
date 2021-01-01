from pandas import read_csv
from scipy.io import loadmat  # 别删
import numpy as np  # 别删

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


if __name__ == "__main__":
    from scipy.io import loadmat
    from scipy.io import savemat
    import numpy as np

    a = loadmat(r"C:\Python Files\BiosignalProcess_V2\data\exper_12.26\11\exper11.mat")["exper11"][:, 0].reshape(-1, 1)
    b = loadmat(r"C:\Python Files\BiosignalProcess_V2\data\exper_12.26\11\exper11.mat")["exper11"][:, 1].reshape(-1, 1)
    c = loadmat(r"C:\Python Files\BiosignalProcess_V2\data\exper_12.26\11\exper11.mat")["exper11"][:, 2].reshape(-1, 1)
    e = np.concatenate((b, c, a), axis=1)
    savemat("./exper11.mat", {"data": e})

