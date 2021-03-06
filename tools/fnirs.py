import neurokit2 as nk
from tools.biodatacut import *
from numpy.core.multiarray import ndarray
from biosppy.plotting import *
from biosppy.signals.tools import filter_signal
import pandas as pd
from scipy.interpolate import interp1d


def fnirs_signal_cut_and_save(file_path, subject, exp_time, start_time, show_CHx: str = None):
    """
    输入脑血流文件路径，返回剪切后的所有通道信号并保存，返回值类型是pandas的Dataframe表格，同时返回保存文件的路径。

    :param file_path:脑血流数据csv文件的路径
    :param subject:第几位受试者
    :param exp_time:此受试者的第几次实验
    :param start_time:此次实验的开始时间点
    :param show_CHx:绘制脑血流图像，输入None不绘制图像；输入通道名称，如CH4，只绘制此通道的数据；输入all，绘制所有通道的数据到一个图
    :return:返回剪切后的数据，为DataFrame类型的变量fnirs_signal；
    返回剪切后的数据csv文件保存位置，为字符串变量
    """

    exp = [60, 40, 34, 30]

    fnirs_csv_name: str = file_path[:-5] + "_" + str(subject) + "_" + str(exp_time) + "_fnirs.csv"
    fnirs_png_name = file_path[:-10] + "png\\" + "exper_" + str(subject) + "_" + str(exp_time) + "_eda.txt"

    stop_time = start_time + exp[exp_time - 1]

    fnirs_signal = biosignal_cut(file_path, start_time, stop_time, sampling_rate=5, channel="all",
                                 save_filepath=fnirs_csv_name)

    if show_CHx is not None:

        if show_CHx == "all":
            sampling_rate = 5
            length = len(fnirs_signal.CH4)
            T = (length - 1) / sampling_rate
            ts = np.linspace(0, T, length, endpoint=True)
            fnirs_allCHx_plot(ts=ts, fnirs_signal=fnirs_signal, show=True)
        else:
            sampling_rate = 5
            length = len(fnirs_signal[show_CHx])
            T = (length - 1) / sampling_rate
            ts = np.linspace(0, T, length, endpoint=True)
            fnirs_CHx_plot(ts=ts, CHx_signal=fnirs_signal[show_CHx].astype('float32'), CH=show_CHx, show=True)

    return fnirs_signal, fnirs_csv_name, fnirs_png_name


def fnirs_CHx_process(raw_signal, CH: str, path=None, show=False):
    """
    脑血流信号处理，输入未处理的信号，要处理的通道名称，保存文件的路径；数据带通滤波后绘制输出。

    :param raw_signal: 未处理的数据，DataFrame类型
    :param CH: 要处理的数据通道，输入一个通道只处理一个并绘图，输入all全部处理输出并绘制到一张图
    :param path: 图像文件保存的路径
    :param show: 是否显示
    :return: 无
    """
    if CH == "all":
        CHx = ["CH4", "CH5", "CH6", "CH7", "CH8", "CH9", "CH10", "CH11", "CH12",
               "CH13", "CH14", "CH15", "CH16", "CH17", "CH18", "CH19"]
        cleaned_signal = pd.DataFrame()
        for ch in CHx:
            cleaned_signal[ch] = nk.signal_filter(raw_signal[ch].astype("float32"), sampling_rate=5, lowcut=0.02,
                                                  highcut=0.1, method="butterworth")

        sampling_rate = 5
        length = len(cleaned_signal["CH4"])
        T = (length - 1) / sampling_rate
        ts = np.linspace(0, T, length, endpoint=True)

        file_path = path[:-4] + "_all"

        fnirs_allCHx_plot(ts=ts, fnirs_signal=cleaned_signal, path=file_path, show=show)

    elif CH in ['CH5', 'CH8', 'CH11', 'CH14', 'CH17', 'CH4', 'CH7', 'CH10',
                'CH13', 'CH16', 'CH19', 'CH6', 'CH9', 'CH12', 'CH15', 'CH18']:
        CHx_signal_cleaned = nk.signal_filter(raw_signal[CH].astype("float32"), sampling_rate=5, lowcut=0.02,
                                              highcut=0.1, method="butterworth")

        sampling_rate = 5
        length = len(CHx_signal_cleaned)
        T = (length - 1) / sampling_rate
        ts = np.linspace(0, T, length, endpoint=True)

        file_path = path[:-4] + CH

        fnirs_CHx_plot(ts=ts, CHx_signal=CHx_signal_cleaned, CH=CH, path=file_path, show=show)
    else:
        print("fnirs_CHx_process()->请输入CH参数！！")


def fnirs_CHx_plot(ts: ndarray = None, CHx_signal: ndarray = None, CH: str = None,
                   path: str = None, show: bool = True):
    """
    绘制一个通道的数据并输出保存

    :param ts: 时间轴
    :param CHx_signal: 某通道数据
    :param CH: 通道名称
    :param path: 图像文件保存的路径
    :param show: 是否显示
    :return: 无
    """

    if CH is None:
        print("请输入处理通道CHx到函数fnirs_CHx_plot()!!")

    plt.rcParams['font.sans-serif'] = ['Microsoft YaHei']  # 用来正常显示中文标签
    plt.rcParams['axes.unicode_minus'] = False  # 用来正常显示负号

    fig = plt.figure()

    if path is not None:
        fig.suptitle('第' + CH + '通道大脑血红蛋白浓度\n' + path)
    else:
        fig.suptitle('第' + CH + '通道大脑血红蛋白浓度')

    ax1 = plt.subplot(311)
    ax1.plot(ts, CHx_signal, label='Total Hb')

    # 设置x, y轴刻度显示范围
    plt.xlim(0, 20)  # 不同实验选择不同刻度显示范围：11.16日实验-> 0~60；12.26日实验：-> 0~20。

    # 设置x轴刻度
    xmjorLocator = MultipleLocator(2)
    ax1.xaxis.set_major_locator(xmjorLocator)

    ax1.tick_params(labelsize=8)

    ax1.set_xlabel('Time(s)')
    ax1.set_ylabel('m(mol/l)*mm')
    ax1.legend(loc='upper right', fontsize=5)
    ax1.grid()

    # save to file
    if path is not None:
        path = utils.normpath(path)
        root, ext = os.path.splitext(path)
        ext = ext.lower()
        if ext not in ['png', 'jpg']:
            path = root + '.png'

        fig.savefig(path, dpi=300, bbox_inches='tight')
        print("fnirs_CHx_plot()处理后的图像已经保存到文件路径{}".format(path))

    # show
    if show:
        plt.show()
    else:
        # close
        plt.close(fig)


def fnirs_allCHx_plot(ts: ndarray = None, fnirs_signal=None, path: str = None, show: bool = True):
    """
    绘制所有通道的数据到一张图

    :param ts: 时间轴
    :param fnirs_signal: 处理或未处理的数据，dataframe格式
    :param path: 图像保存的路径
    :param show: 是否显示
    :return: 无
    """
    CH = ['CH5', 'CH8', 'CH11', 'CH14', 'CH17', 'CH4', 'CH7', 'CH10',
          'CH13', 'CH16', 'CH19', 'CH6', 'CH9', 'CH12', 'CH15', 'CH18']

    plt.rcParams['font.sans-serif'] = ['Microsoft YaHei']  # 用来正常显示中文标签
    plt.rcParams['axes.unicode_minus'] = False  # 用来正常显示负号

    fig, ax = plt.subplots(3, 6)
    fig.set_size_inches(12, 8)

    if path is not None:
        fig.suptitle('前额脑血红蛋白浓度\n' + path, fontsize=7)
    else:
        fig.suptitle('前额脑血红蛋白浓度', fontsize=7)

    for i in range(5):
        ax[0, i].set_title(CH[i], fontsize=7)
        ax[0, i].tick_params(labelsize=4)
        ax[0, i].plot(ts, fnirs_signal[CH[i]].astype('float32'), label='Total Hb')
        ax[0, i].legend(loc='upper right', fontsize=4)

    for i in range(6):
        ax[1, i].set_title(CH[i + 5], fontsize=7)
        ax[1, i].tick_params(labelsize=4)
        ax[1, i].plot(ts, fnirs_signal[CH[i + 5]].astype('float32'), label='Total Hb')
        ax[1, i].legend(loc='upper right', fontsize=4)

    for i in range(1, 6):
        ax[2, i].set_title(CH[i + 10], fontsize=7)
        ax[2, i].tick_params(labelsize=4)
        ax[2, i].plot(ts, fnirs_signal[CH[i + 10]].astype('float32'), label='Total Hb')
        ax[2, i].legend(loc='upper right', fontsize=4)

    plt.subplot(3, 6, 6)
    plt.axis("off")
    plt.subplot(3, 6, 13)
    plt.axis("off")

    # save to file
    if path is not None:
        path = utils.normpath(path)
        root, ext = os.path.splitext(path)
        ext = ext.lower()
        if ext not in ['png', 'jpg']:
            path = root + '.png'

        fig.savefig(path, dpi=300)
        print("fnirs_allCHx_plot()处理后的图像已经保存到文件路径{}".format(path))

    # show
    if show:
        plt.show()
    else:
        # close
        plt.close(fig)


def fnirs_interpolate(fnirs_signal: ndarray, sampling_rate: int = 2000):
    """
    脑血流信号插值函数，输入5Hz的脑血流数据，输出2000Hz脑血流数据。

    Parameters
    ----------
    fnirs_signal 脑血流原始数据
    sampling_rate 插值后的数据采样频率

    Returns 插值后的脑血流数据
    -------

    """

    multiple = int(sampling_rate / 5)
    x = np.arange(0, len(fnirs_signal))
    f1 = interp1d(x, fnirs_signal, kind="quadratic")
    x_new = np.linspace(min(x), max(x), len(fnirs_signal) * multiple)
    fnirs_signal_new = f1(x_new)

    length = len(fnirs_signal_new)
    T = (length - 1) / sampling_rate
    ts = np.linspace(0, T, length, endpoint=True)

    return fnirs_signal_new, ts


def fnirs_interpolate_process(filepath=None, CH="all"):
    """
    脑血流数据插值处理并保存到文件，CH选all，保存所有处理后数据到csv文件，指定一个通道，保存一个通道的数据到csv文件。

    Parameters
    ----------
    filepath 原始脑血流数据文件路径
    CH 要处理的通道

    Returns 无
    -------

    """
    raw_signal = pd.read_csv(filepath)

    if CH == "all":
        CHx = ["CH4", "CH5", "CH6", "CH7", "CH8", "CH9", "CH10", "CH11", "CH12",
               "CH13", "CH14", "CH15", "CH16", "CH17", "CH18", "CH19"]
        interpolated_signal = pd.DataFrame()

        for ch in CHx:
            interpolated_signal[ch], ts = fnirs_interpolate(raw_signal[ch].astype("float32"), sampling_rate=2000)
            interpolated_signal[ch] = interpolated_signal[ch].astype("float32")

        savepath = filepath[:-4] + "_interpolated.csv"
        with open(savepath, "w+", newline="") as file:
            interpolated_signal.to_csv(file, index=True,
                                       columns=["CH4", "CH5", "CH6", "CH7", "CH8", "CH9", "CH10", "CH11",
                                                "CH12", "CH13", "CH14", "CH15", "CH16", "CH17", "CH18",
                                                "CH19"])
            file.close()
            print("脑血流所有通道插值处理后数据已保存到文件{}".format(savepath))

    elif CH in ["CH4", "CH5", "CH6", "CH7", "CH8", "CH9", "CH10", "CH11", "CH12", "CH13", "CH14", "CH15", "CH16",
                "CH17", "CH18", "CH19"]:
        interpolated_signal = pd.DataFrame()
        interpolated_signal[CH], ts = fnirs_interpolate(raw_signal[CH].astype("float32"), sampling_rate=2000)
        interpolated_signal[CH] = interpolated_signal[CH].astype("float32")

        # savepath = filepath[:-4] + CH + "_interpolated.csv"
        savepath = filepath[:-4] + CH + "_interpolated.txt"
        with open(savepath, "w+", newline="") as file:
            interpolated_signal.to_csv(file, index=False, columns=[CH])
        file.close()
        print("脑血流{}通道插值处理后数据已保存到文件{}".format(CH, savepath))


if __name__ == "__main__":
    # path = r"F:\qz\BiosignalProcess_V2\data\exper_12.26\1\fnirs\exper1_fnirs_3010.csv"
    # fnirs_interpolate_process(path, CH="CH11")
    # b = r"F:\qz\BiosignalProcess_V2\data\exper_12.26\1\fnirs\exper1_fnirs_3010CH11_interpolated.txt"
    # a = pd.read_csv(b)
    # c = a.CH11
    # import matplotlib.pyplot as plt
    # plt.plot(c)
    # plt.show()
    import matplotlib.pyplot as plt

    path = "../data/exper_12.26v2/3010/1/exper1_fnirs_3010CH11_interpolated.txt"
    path2 = "../data/exper_12.26v2/3010/1/exper1_fnirs_3010CH11_interpolated.txt"
    # a = np.loadtxt(path)
    fnirs = pd.read_csv(path2, header=0)  # 从第二行开始读，第一行为字符串“CH11”
    # fnirs = z_score(pd.DataFrame(fnirs, dtype="float32"))  # 需要把元素类型为字符串类型的series转成float类型的dataframe
    # fnirs = np.array(fnirs.values, dtype="float32").reshape(-1, 1)
    print(fnirs["CH11"].values)
    fnirs = fnirs["CH11"].values
    b, c, d = filter_signal(fnirs, ftype="butter", band="bandpass", order=2, frequency=[0.02, 0.1], sampling_rate=2000)
    print(len(b))
    plt.plot(b)
    plt.show()
