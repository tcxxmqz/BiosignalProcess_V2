from tools.eda import *
from tools.ecg import *
from tools.emg import *
from tools.fnirs import *


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
            # EDA处理
            eda, eda_saveasfilename = eda_signal_cut_and_save(file, k + 1, i + 1, cut_time[k][i], show=False)
            eda_process(eda, i + 1, eda_saveasfilename)
            # ECG处理
            ecg, ecg_saveasfilename = ecg_signal_cut_and_save(file, k + 1, i + 1, cut_time[k][i], show=False)
            ecg_process(ecg, i + 1, ecg_saveasfilename)
            # EMG处理
            emg, emg_saveasfilename = emg_signal_cut_and_save(file, k + 1, i + 1, cut_time[k][i], show=False)
            emg_process(emg, i + 1, emg_saveasfilename)

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
    for k in range(1):
        fnirs_file = fnirs_filepath[k]
        for i in range(4):
            fnirs, fnirs_saveasfilename = fnirs_signal_cut_and_save(fnirs_file, k + 1, i + 1, fnirs_cut_time[k][i],
                                                                    show_CHx=None)
            fnirs_CHx_process(fnirs, "all", fnirs_saveasfilename, show=False)


if __name__ == "__main__":
    exper11_16()
