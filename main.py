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

    filepath = [r"./exper_11.16/data/1/exper1.mat",
                r"./exper_11.16/data/2/exper2.mat",
                r"./exper_11.16/data/3/exper3.mat",
                r"./exper_11.16/data/4/exper4.mat",
                r"./exper_11.16/data/5/exper5.mat"]
    cut_time = [[778, 924, 1019, 1189],
                [388, 579, 823, 901],
                [578, 714, 879, 989],
                [283, 475, 630, 739],
                [447, 483, 623, 712]]

    for k in range(5):
        file = filepath[k]
        for i in range(4):
            # EDA处理
            eda, eda_saveasfilename = eda_signal_cut_and_save(file, k + 1, i + 1, cut_time[k][i], show=False)
            eda_process(eda, i + 1, eda_saveasfilename)
            # ECG处理
            ecg, ecg_saveasfilename = ecg_signal_cut_and_save(file, k + 1, i + 1, cut_time[k][i], show=False)
            ecg_process(ecg, i + 1, ecg_saveasfilename)
            # EMG处理
            emg, emg_saveasfilename = emg_signal_cut_and_save(file, k + 1, i + 1, cut_time[k][i], show=False)
            emg_process(emg, i + 1, emg_saveasfilename)

    fnirs_filepath = [r"./exper_11.16/data/1/fnirs/exper1.csv",
                      r"./exper_11.16/data/2/fnirs/exper2.csv",
                      r"./exper_11.16/data/3/fnirs/exper3.csv",
                      r"./exper_11.16/data/4/fnirs/exper4.csv",
                      r"./exper_11.16/data/5/fnirs/exper5.csv"]
    fnirs_cut_time = [[447, 596, 724, 859],
                      [26, 166, 269, 347],
                      [218, 353, 515, 627],
                      [147, 340, 494, 567],
                      [39, 135, 214, 304]]

    # 第4个人的第4组脑血流数据不能用，会报错
    for k in range(5):
        fnirs_file = fnirs_filepath[k]
        for i in range(4):
            fnirs, fnirs_saveasfilename = fnirs_signal_cut_and_save(fnirs_file, k + 1, i + 1, fnirs_cut_time[k][i],
                                                                    show_CHx=None)
            fnirs_CHx_process(fnirs, "all", fnirs_saveasfilename, show=False)


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

    picture = [5725, 3010, 4130, 5760, 3019, 4008, 5780, 5168,
               4658, 5780.1, 4810, 5825, 3266, 4672, 5831, 3195, 4652]

    for k in range(11):
        file1 = filepath1[k]
        file2 = filepath2[k]
        for i in range(17):
            print("正在处理{}-->{}".format(k + 1, i + 1))
            try:
                # ECG
                _file1 = file1[:-4] + "_ecg_" + str(picture[i]) + ".txt"
                # print("{}--{}".format(StartTime1[k]+i*45, StartTime1[k]+i*45+20))
                biosignal_cut(file1, start_time=StartTime1[k] + i * 45, stop_time=StartTime1[k] + i * 45 + 20,
                              sampling_rate=2000,
                              channel=0, save_filepath=_file1)
                # EMG
                _file2 = file1[:-4] + "_emg_" + str(picture[i]) + ".txt"
                biosignal_cut(file1, start_time=StartTime1[k] + i * 45, stop_time=StartTime1[k] + i * 45 + 20,
                              sampling_rate=2000,
                              channel=1, save_filepath=_file2)
                # EDA
                _file3 = file1[:-4] + "_eda_" + str(picture[i]) + ".txt"
                biosignal_cut(file1, start_time=StartTime1[k] + i * 45, stop_time=StartTime1[k] + i * 45 + 20,
                              sampling_rate=2000,
                              channel=2, save_filepath=_file3)
                # fnirs
                _file4 = file2[:-4] + "_fnirs_" + str(picture[i]) + ".csv"
                biosignal_cut(file2, start_time=StartTime2[k] + i * 45, stop_time=StartTime2[k] + i * 45 + 20,
                              sampling_rate=5,
                              channel="all", save_filepath=_file4)
                fnirs_interpolate_process(_file4, CH="CH11")

            except ValueError as ex:
                print("处理{}-->{}时，发生错误{}".format(k + 1, i + 1, ex))
                continue


if __name__ == "__main__":

    time1 = time.time()
    exper12_26()
    time2 = time.time()
    print("用时{}".format(time2-time1))
