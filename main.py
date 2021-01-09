from tools.eda import *
from tools.ecg import *
from tools.emg import *
from tools.fnirs import *
import time


def exper11_16():
    """
        ************************************************************************************************

        2020-11-16 轮椅与VR同步实验数据处理
            实验人员5人：刘腾、王虹杰、牛冠学、邵尉、柳富强。
            实验流程：进入场景15秒后，轮椅分别以0.2、0.4、0.6、0.8米每秒前进8米后停止。
            实验时长：60秒、40秒、34秒、30秒。

        ************************************************************************************************
        """

    filepath = [r"./data/exper_11.16/1/exper1.mat",
                r"./data/exper_11.16/2/exper2.mat",
                r"./data/exper_11.16/3/exper3.mat",
                r"./data/exper_11.16/4/exper4.mat",
                r"./data/exper_11.16/5/exper5.mat"]
    cut_time = [[778, 924, 1019, 1189],
                [388, 579, 823, 901],
                [578, 714, 879, 989],
                [283, 475, 630, 739],
                [447, 483, 623, 712]]

    for k in range(5):
        file = filepath[k]
        for i in range(4):
            print("正在处理{}-->{}".format(k + 1, i + 1))
            try:
                # EDA处理
                eda, eda_txt_name, eda_png_name = eda_signal_cut_and_save(file, k + 1, i + 1, cut_time[k][i],
                                                                          show=False)
                eda_process(eda, i + 1, eda_png_name)
                # ECG处理
                ecg, ecg_txt_name, ecg_png_name = ecg_signal_cut_and_save(file, k + 1, i + 1, cut_time[k][i],
                                                                          show=False)
                ecg_process(ecg, i + 1, ecg_png_name)
                # EMG处理
                emg, emg_txt_name, emg_png_name = emg_signal_cut_and_save(file, k + 1, i + 1, cut_time[k][i],
                                                                          show=False)
                emg_process(emg, i + 1, emg_png_name)
            except ValueError as ex:
                print("处理{}-->{}时，发生错误{}".format(k + 1, i + 1, ex))
                continue

    fnirs_filepath = [r"./data/exper_11.16/1/fnirs/exper1.csv",
                      r"./data/exper_11.16/2/fnirs/exper2.csv",
                      r"./data/exper_11.16/3/fnirs/exper3.csv",
                      r"./data/exper_11.16/4/fnirs/exper4.csv",
                      r"./data/exper_11.16/5/fnirs/exper5.csv"]
    fnirs_cut_time = [[447, 596, 724, 859],
                      [26, 166, 269, 347],
                      [218, 353, 515, 627],
                      [147, 340, 494, 567],
                      [39, 135, 214, 304]]

    # 第4个人的第4组脑血流数据不能用，会报错
    for k in range(5):
        fnirs_file = fnirs_filepath[k]
        for i in range(4):
            print("正在处理{}-->{}".format(k + 1, i + 1))
            try:
                fnirs, fnirs_csv_name, fnirs_png_name = fnirs_signal_cut_and_save(fnirs_file, k + 1, i + 1,
                                                                                  fnirs_cut_time[k][i],
                                                                                  show_CHx=None)
                fnirs_CHx_process(fnirs, "all", fnirs_png_name, show=False)
            except ValueError as ex:
                print("！！！处理{}-->{}时，发生错误{}".format(k + 1, i + 1, ex))
                continue


def exper12_26():
    """
    ************************************************************************************************
    2020-12-26日实验：IAPS国际情感图片库实验
    实验人员：共11人
    ************************************************************************************************
    """

    filepath1 = [r"./data/exper_12.26/1/exper1.mat",
                 r"./data/exper_12.26/2/exper2.mat",
                 r"./data/exper_12.26/3/exper3.mat",
                 r"./data/exper_12.26/4/exper4.mat",
                 r"./data/exper_12.26/5/exper5.mat",
                 r"./data/exper_12.26/6/exper6.mat",
                 r"./data/exper_12.26/7/exper7.mat",
                 r"./data/exper_12.26/8/exper8.mat",
                 r"./data/exper_12.26/9/exper9.mat",
                 r"./data/exper_12.26/10/exper10.mat",
                 r"./data/exper_12.26/11/exper11.mat"]

    filepath2 = [r"./data/exper_12.26/1/fnirs/exper1.csv",
                 r"./data/exper_12.26/2/fnirs/exper2.csv",
                 r"./data/exper_12.26/3/fnirs/exper3.csv",
                 r"./data/exper_12.26/4/fnirs/exper4.csv",
                 r"./data/exper_12.26/5/fnirs/exper5.csv",
                 r"./data/exper_12.26/6/fnirs/exper6.csv",
                 r"./data/exper_12.26/7/fnirs/exper7.csv",
                 r"./data/exper_12.26/8/fnirs/exper8.csv",
                 r"./data/exper_12.26/9/fnirs/exper9.csv",
                 r"./data/exper_12.26/10/fnirs/exper10.csv",
                 r"./data/exper_12.26/11/fnirs/exper11.csv"]

    StartTime1 = [226, 207, 207, 116, 87, 147, 34, 175, 292, 113, 244]
    StartTime2 = [50.4, 53.2, 62.4, 27.8, 34.8, 36.4, 54.2, 38.4, 290.8, 203, 45.8]

    picture = [5725, 3010, 4130, 5760, 3019, 4008, 5780, 3168,
               4658, 5780.1, 4810, 5825, 3266, 4672, 5831, 3195, 4652]

    errors = []

    for k in range(11):
        file1 = filepath1[k]
        file2 = filepath2[k]
        for i in range(17):
            print("正在处理{}-->{}".format(k + 1, i + 1))
            try:
                # ECG
                _file1 = file1[:-4] + "_ecg_" + str(picture[i]) + ".txt"
                # print("{}--{}".format(StartTime1[k]+i*45, StartTime1[k]+i*45+20))
                ecg = biosignal_cut(file1, start_time=StartTime1[k] + i * 45, stop_time=StartTime1[k] + i * 45 + 20,
                                    sampling_rate=2000,
                                    channel=0, save_filepath=_file1)
                ecg_process(ecg, i + 1, _file1)
                # EMG
                _file2 = file1[:-4] + "_emg_" + str(picture[i]) + ".txt"
                emg = biosignal_cut(file1, start_time=StartTime1[k] + i * 45, stop_time=StartTime1[k] + i * 45 + 20,
                                    sampling_rate=2000,
                                    channel=1, save_filepath=_file2)
                emg_process(emg, i + 1, _file2)
                # EDA
                try:
                    _file3 = file1[:-4] + "_eda_" + str(picture[i]) + ".txt"
                    eda = biosignal_cut(file1, start_time=StartTime1[k] + i * 45, stop_time=StartTime1[k] + i * 45 + 20,
                                        sampling_rate=2000,
                                        channel=2, save_filepath=_file3)
                    eda_process(eda, i + 1, _file3)
                except IndexError as ex1:
                    print("!!!处理{}-->{}时，发生错误{}".format(k + 1, i + 1, ex1))
                    error = "eda" + str(k + 1) + "_" + str(i + 1) + "_" + str(picture[i])
                    errors.append(error)
                    continue
                # fnirs
                _file4 = file2[:-4] + "_fnirs_" + str(picture[i]) + ".csv"
                fnirs = biosignal_cut(file2, start_time=StartTime2[k] + i * 45, stop_time=StartTime2[k] + i * 45 + 20,
                                      sampling_rate=5,
                                      channel="all", save_filepath=_file4)
                fnirs_CHx_process(fnirs, "CH11", _file4)
                fnirs_interpolate_process(_file4, CH="CH11")

            except ValueError as ex:
                print("!!!处理{}-->{}时，发生错误{}".format(k + 1, i + 1, ex))
                error = "fnirs" + str(k + 1) + "_" + str(i + 1) + "_" + str(picture[i])
                errors.append(error)
                continue
    print("以下文件出现问题：{}".format(errors))


# ['eda1_5_3019', 'eda1_8_5168', 'eda3_5_3019', 'eda4_15_5831', 'eda6_10_5780.1', 'eda6_15_5831', 'eda6_17_652',
# 'fnirs8_15_5831', 'eda9_6_4008', 'fnirs9_17_4652', 'eda10_4_5760', 'eda10_10_5780.1', 'eda10_14_4672',
# 'fnirs10_17_4652', 'eda11_1_5725', 'eda11_3_4130']


def exper12_26v2():
    """
    IAPS图像实验切分生理数据中的SCR反应函数。
    首先对EDA信号进行处理，监测SCR反应，按照SCR反应的开始时间，结束时间切分ECG,EMG,EDA,FNIRS数据并保存到文件。

    Returns
    -------

    """
    errors = []
    ecg_path, eda_path, emg_path, fnirs_path, labels = get_biofile_path("./data/exper_12.26v2")
    for i in range(len(eda_path)):
        try:
            ecg = np.loadtxt(ecg_path[i])
            ecg_info = biosppy_ecg.ecg(signal=ecg, sampling_rate=2000, show=False, plot_method="qz", path=None)
            ecg = ecg_info['filtered']
            eda = np.loadtxt(eda_path[i])
            emg = np.loadtxt(emg_path[i])
            emg = nk_emg.emg_clean(emg, 2000)
            fnirs = pd.read_csv(fnirs_path[i], header=0)
            fnirs = fnirs["CH11"].values
            fnirs, a, b = filter_signal(fnirs, ftype="butter", band="bandpass", order=2,
                                        frequency=[0.02, 0.1], sampling_rate=2000)
            [onsets, offsets, eda] = eda_process(eda, i, path=None)
            for j in range(len(onsets)):
                _ecg_path = "./segment" + ecg_path[i][6:]
                _eda_path = "./segment" + eda_path[i][6:]
                _emg_path = "./segment" + emg_path[i][6:]
                _fnirs_path = "./segment" + fnirs_path[i][6:]
                # _ecg_path = _ecg_path[:-4] + "_" + str(j+1) + ".txt"
                signal_cut(ecg, j, onsets[j], offsets[j], _ecg_path)
                signal_cut(eda, j, onsets[j], offsets[j], _eda_path)
                signal_cut(emg, j, onsets[j], offsets[j], _emg_path)
                signal_cut(fnirs, j, onsets[j], offsets[j], _fnirs_path)

        except :
            errors.append(i)
            print("！！！处理第{}个数据时出错".format(i))

    print("\n出错文件：{}".format(errors))


if __name__ == "__main__":
    time1 = time.time()
    # exper12_26()
    # exper11_16()
    exper12_26v2()
    time2 = time.time()
    print("----------用时{}秒！！---------".format(time2 - time1))
