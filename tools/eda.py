from numpy.core.multiarray import ndarray
import neurokit2 as nk
from tools.biodatacut import *
from biosppy.plotting import *


def eda_signal_cut_and_save(file_path, subject, exp_time, start_time, channel=2, show=True):
    """
    切分皮电数据，输入文件路径，第几位受试者，第几次实验，实验开始截取数据的时间点，数据所在的通道；自动保存切分后的文件到输入文件所在的路径

    :param file_path: 原始文件路径
    :param subject: 受试者位次
    :param exp_time: 实验位次
    :param start_time: 开始切分时间点
    :param channel: eda信号所在通道
    :param show: 是否绘图
    :return: 分段后的信号，数据保存路径
    """
    exp = [60, 40, 34, 30]

    # filepath = r"C:\Python Files\BiosignalProcessing\data\exper1.mat"

    save_as_filename = file_path[:-5] + "_" + str(subject) + "_" + str(exp_time) + "_eda.txt"

    stop_time = start_time + exp[exp_time - 1]

    eda_signal = biosignal_cut(file_path, start_time, stop_time, channel=channel, save_filepath=save_as_filename)

    if show is True:
        plt.plot(eda_signal)
        plt.show()

    return eda_signal, save_as_filename


def eda_process(raw_signal, exper, path=None):
    """
    皮电信号处理，输入未处理的皮电信号，输出scr监测后的图像。

    :param raw_signal: 未处理的皮电信号
    :param exper: 第几次实验
    :param path: 文件保存的地址
    :return: 无
    """

    # 降采样
    downsize_rate = 100
    down_size = 2000 / downsize_rate
    # raw_signal = np.loadtxt(filepath)
    raw_signal = raw_signal[::int(down_size)]
    # sampling_rate = int(2000 / down_size)
    # plt.plot(raw_signal)
    # plt.show()

    # 带通滤波与平滑处理
    eda_cleaned = nk.eda_clean(raw_signal, sampling_rate=downsize_rate, method="biosppy")

    # 相位成分提取
    # eda = nk.eda_phasic(eda_cleaned, sampling_rate=sampling_rate, method='median')
    # eda_phasic = eda["EDA_Phasic"].values
    # plt.plot(eda_phasic)
    # plt.show()

    # 微分与卷积处理
    info = nk.eda_findpeaks(eda_cleaned, sampling_rate=downsize_rate, method="qz")
    features = [info["SCR_Onsets"], info["SCR_Offsets"], info['SCR_Peaks'], info['eda_phasic_diffandsmoothed']]

    # 时间轴
    length = len(eda_cleaned)
    T = (length - 1) / downsize_rate
    ts = np.linspace(0, T, length, endpoint=True)

    # 绘图
    # bplt.plot_eda_qz(ts=ts, raw=raw_signal, filtered=eda_cleaned, onsets=features[0],
    #                  offsets=features[1], peaks=features[2], eda_phasic_diffandsmoothed=features[3], show=True,
    #                  path=filepath, stimulus=False)

    # 保存文件名

    # scr监测与绘图输出保存
    if path is not None:
        plot_scr_v2(ts=ts, sampling_rate=downsize_rate, filtered=eda_cleaned, onsets=features[0], offsets=features[1],
                    exper=exper, show=False, path=path)
    else:
        plot_scr_v2(ts=ts, sampling_rate=downsize_rate, filtered=eda_cleaned, onsets=features[0], offsets=features[1],
                    exper=exper, show=False)


def plot_scr_v2(ts: ndarray = None,
                sampling_rate: int = 2000,
                filtered: ndarray = None,
                onsets: ndarray = None,
                offsets: ndarray = None,
                path: str = None,
                exper: int = None,
                show: bool = False):
    """绘制SCR到图像_v2

        Parameters
        ----------
        :param sampling_rate:采样频率
        :param show:是否显示
        :param path:文件保存路径
        :param offsets:scr结束时间点
        :param onsets:scr开始时间点
        :param ts:时间轴
        :param filtered:处理后的数据
        :param exper: 实验位次，第几次实验。

        """

    plt.rcParams['font.sans-serif'] = ['Microsoft YaHei']  # 用来正常显示中文标签
    plt.rcParams['axes.unicode_minus'] = False  # 用来正常显示负号

    fig = plt.figure()

    if path is not None:
        fig.suptitle('皮肤电活动\n' + path, fontsize=7)
    else:
        fig.suptitle('皮肤电活动', fontsize=7)

    # filtered signal with onsets, peaks, SCR
    ax1 = fig.add_subplot(311)

    # 给子图设置标题
    # ax1.set_title(path)

    # 设置x轴刻度
    xmjorLocator = MultipleLocator(2)
    ax1.xaxis.set_major_locator(xmjorLocator)

    ax1.tick_params(labelsize=6)

    # 设置x轴刻度范围
    ax1.set_xlim(-1, 60)

    ymin = np.min(filtered)
    ymax = np.max(filtered)
    alpha = 0.1 * (ymax - ymin)
    ymax += alpha
    ymin -= alpha

    ax1.plot(ts, filtered, label='EDA-Filtered')

    # 绘制onsets, offsets点到图像
    # ax1.scatter(ts[onsets], filtered[onsets], marker='o', color='b', label='SCR-Onsets')
    # ax1.scatter(ts[offsets], filtered[offsets], marker='x', color='green', label='SCR-Offsets')

    # SCR反应区域标记上颜色
    for i in range(0, len(ts[onsets]) - 1):
        ax1.axvspan(xmin=ts[onsets][i], xmax=ts[offsets][i], facecolor='gray', alpha=0.4)
    ax1.axvspan(xmin=ts[onsets][-1], xmax=ts[offsets][-1], facecolor='gray', alpha=0.4, label='SCR')

    # 绘制实验开始，进入场景，轮椅启动，距离障碍物最近，轮椅停止位置
    ax1.vlines(ts[0], ymin, ymax, color='y', linestyles="--", linewidth=MINOR_LW, label='进入场景')
    ax1.vlines(ts[15 * sampling_rate], ymin, ymax, color='g', linestyles="--", linewidth=MINOR_LW, label='轮椅启动')
    obs_distance_time = [45, 30, 26, 24]  # 距离障碍物最近时的时间点
    ax1.vlines(ts[obs_distance_time[exper - 1] * sampling_rate], ymin, ymax, color='r', linestyles="--",
               linewidth=MINOR_LW, label='距离最近')
    wheelchair_stop_time = [55, 36, 30, 27]
    ax1.vlines(ts[wheelchair_stop_time[exper - 1] * sampling_rate], ymin, ymax, color='b', linestyles="--",
               linewidth=MINOR_LW, label='轮椅停止')

    ax1.set_ylabel('uS')
    ax1.set_xlabel('Time(s)')
    ax1.legend(loc="upper right", fontsize=5)
    ax1.grid()

    # make layout tight
    # fig.tight_layout()

    # save to file
    if path is not None:
        path = utils.normpath(path)
        root, ext = os.path.splitext(path)
        ext = ext.lower()
        if ext not in ['png', 'jpg']:
            path = root + '_scr.png'

        fig.savefig(path, dpi=300, bbox_inches='tight')
        print("plot_scr()处理后的图像已经保存到文件路径{}".format(path))

    # show
    if show:
        plt.show()
    else:
        # close
        plt.close(fig)


# def plot_eda(ts: ndarray = None,
#              raw: ndarray = None,
#              filtered: ndarray = None,
#              onsets: ndarray = None,
#              offsets: ndarray = None,
#              peaks: ndarray = None,
#              eda_phasic_diffandsmoothed: ndarray = None,
#              path: str = None,
#              show: bool = False,
#              stimulus: bool = False):
#     """Create a summary plot from the output of signals.eda.eda.
#
#     Parameters
#     ----------
#     ts : array
#         Signal time axis reference (seconds).
#     raw : array
#         Raw EDA signal.
#     filtered : array
#         Filtered EDA signal.
#     onsets : array
#         Indices of SCR pulse onsets.
#     offsets : array
#         Indices of SCR pulse offsets.
#     peaks : array
#         Indices of the SCR peaks.
#     eda_phasic_diffandsmoothed : array (modified by qz).
#         eda_phasic_diffandsmoothed.
#     path : str, optional
#         If provided, the plot will be saved to the specified file.
#     show : bool, optional
#         If True, show the plot immediately.
#     stimulus : bool, optional
#         If True, show the stimulus.
#         绘制预测到的刺激发生时间, 以零点开始的刺激延时作为后续刺激的校准，默认不绘制。
#     modified by qz at 2020-10-28
#
#     """
#
#     plt.rcParams['font.sans-serif'] = ['Microsoft YaHei']  # 用来正常显示中文标签
#     plt.rcParams['axes.unicode_minus'] = False  # 用来正常显示负号
#
#     fig = plt.figure()
#     fig.suptitle('EDA信号处理及SCR检测\n' + path)
#
#     # raw signal
#     ax1 = fig.add_subplot(311)
#
#     # ax1.plot(ts, raw, linewidth=MAJOR_LW, label='raw')
#     ax1.plot(ts, raw, label='raw EDA')
#
#     ax1.set_ylabel('Amplitude(uS)')
#     ax1.legend(loc="upper left", fontsize=6)
#     ax1.grid()
#
#     # 设置x轴刻度
#     xmjorLocator = MultipleLocator(1)
#     ax1.xaxis.set_major_locator(xmjorLocator)
#
#     # filtered signal with onsets, peaks
#     ax2 = fig.add_subplot(312, sharex=ax1)
#
#     ymin = np.min(filtered)
#     ymax = np.max(filtered)
#     alpha = 0.1 * (ymax - ymin)
#     ymax += alpha
#     ymin -= alpha
#
#     ax2.plot(ts, filtered, label='EDA-Filtered')
#
#     # 绘制onsets, peaks, offsets点到图像
#     ax2.scatter(ts[onsets], filtered[onsets], marker='o', color='b', label='SCR-Onsets')
#     # ax2.scatter(ts[peaks], filtered[peaks], marker='^', label='SCR-Peaks')
#     ax2.scatter(ts[offsets], filtered[offsets], marker='x', color='green', label='SCR-Offsets')
#
#     # SCR反应区域标记上颜色
#     i: int
#
#     for i in range(0, len(ts[onsets]) - 1):
#         ax2.axvspan(xmin=ts[onsets][i], xmax=ts[offsets][i], facecolor='gray', alpha=0.4)
#     ax2.axvspan(xmin=ts[onsets][-1], xmax=ts[offsets][-1], facecolor='gray', alpha=0.4, label='SCR')
#
#     # 预测刺激开始的时间，用红色竖线表示
#     if stimulus:
#         stimulus_list = onsets - onsets[0]
#         ax2.vlines(ts[stimulus_list], ymin, ymax,
#                    color='r',
#                    linewidth=MINOR_LW,
#                    label='Stimulus')
#
#     ax2.set_ylabel('Amplitude(uS)')
#     ax2.legend(loc="upper right", fontsize=5)
#     ax2.grid()
#
#     # eda_phasic_diffandsmoothed
#     ax3 = fig.add_subplot(313, sharex=ax1)
#     ax3.plot(ts[:len(eda_phasic_diffandsmoothed)], eda_phasic_diffandsmoothed, label='EDA-processed')
#
#     # ax3.hlines(0, 0, ts[-1], colors='r', linestyles='dashed')
#     ax3.axhline(color='orange', ls='dashed')
#
#     ax3.scatter(ts[onsets], eda_phasic_diffandsmoothed[onsets], marker='o', color='b', label='SCR-Onsets')
#     ax3.scatter(ts[peaks], eda_phasic_diffandsmoothed[peaks], marker='^', color='orange', label='SCR-Peaks')
#     ax3.scatter(ts[offsets], eda_phasic_diffandsmoothed[offsets], marker='x', color='green', label='SCR-Offsets')
#
#     # SCR反应区域标记上颜色
#     for i in range(0, len(ts[onsets]) - 1):
#         ax3.axvspan(xmin=ts[onsets][i], xmax=ts[offsets][i], facecolor='gray', alpha=0.4)
#     ax3.axvspan(xmin=ts[onsets][-1], xmax=ts[offsets][-1], facecolor='gray', alpha=0.4, label='SCR')
#
#     ax3.set_xlabel('Time(s)')
#     ax3.set_ylabel('Amplitude(uS)')
#     ax3.legend(loc="upper right", fontsize=5)
#     ax3.grid()
#
#     # make layout tight
#     fig.tight_layout()
#
#     # save to file
#     if path is not None:
#         path = utils.normpath(path)
#         root, ext = os.path.splitext(path)
#         ext = ext.lower()
#         if ext not in ['png', 'jpg']:
#             path = root + '.png'
#
#         fig.savefig(path, dpi=300, bbox_inches='tight')
#
#     # show
#     if show:
#         plt.show()
#     else:
#         # close
#         plt.close(fig)
#
#
# def plot_scr(ts: ndarray = None,
#              filtered: ndarray = None,
#              onsets: ndarray = None,
#              offsets: ndarray = None,
#              path: str = None,
#              show: bool = False,
#              stimulus: object = False):
#     """绘制SCR到图像
#
#         Parameters
#         ----------
#         ts : array
#             Signal time axis reference (seconds).
#         filtered : array
#             Filtered EDA signal.
#         onsets : array
#             Indices of SCR pulse onsets.
#         offsets : array
#             Indices of SCR pulse offsets.
#         path : str, optional
#             If provided, the plot will be saved to the specified file.
#         show : bool, optional
#             If True, show the plot immediately.
#         stimulus : bool, optional
#             If True, show the stimulus.
#             绘制预测到的刺激发生时间, 以零点开始的刺激延时作为后续刺激的校准，默认不绘制。
#         modified by qz at 2020-10-28
#
#         """
#
#     plt.rcParams['font.sans-serif'] = ['Microsoft YaHei']  # 用来正常显示中文标签
#     plt.rcParams['axes.unicode_minus'] = False  # 用来正常显示负号
#
#     fig = plt.figure()
#     fig.suptitle('EDA处理及SCR检测\n')
#
#     # filtered signal with onsets, peaks, SCR
#     ax1 = fig.add_subplot(311)
#
#     # 给子图设置标题
#     ax1.set_title(path)
#
#     # 设置x轴刻度
#     xmjorLocator = MultipleLocator(2)
#     ax1.xaxis.set_major_locator(xmjorLocator)
#
#     # 设置x轴刻度范围
#     ax1.set_xlim(0, 60)
#
#     ymin = np.min(filtered)
#     ymax = np.max(filtered)
#     alpha = 0.1 * (ymax - ymin)
#     ymax += alpha
#     ymin -= alpha
#
#     ax1.plot(ts, filtered, label='EDA-Filtered')
#
#     # 绘制onsets, offsets点到图像
#     # ax1.scatter(ts[onsets], filtered[onsets], marker='o', color='b', label='SCR-Onsets')
#     # ax1.scatter(ts[offsets], filtered[offsets], marker='x', color='green', label='SCR-Offsets')
#
#     # SCR反应区域标记上颜色
#     for i in range(0, len(ts[onsets]) - 1):
#         ax1.axvspan(xmin=ts[onsets][i], xmax=ts[offsets][i], facecolor='gray', alpha=0.4)
#     ax1.axvspan(xmin=ts[onsets][-1], xmax=ts[offsets][-1], facecolor='gray', alpha=0.4, label='SCR')
#
#     # 预测刺激开始的时间，用红色竖线表示
#     if stimulus:
#         stimulus_list = onsets - onsets[0]
#         ax1.vlines(ts[stimulus_list], ymin, ymax,
#                    color='r',
#                    linewidth=MINOR_LW,
#                    label='Stimulus')
#
#     ax1.set_ylabel('Amplitude(uS)')
#     ax1.legend(loc="upper left", fontsize=4)
#     ax1.grid()
#
#     # make layout tight
#     fig.tight_layout()
#
#     # save to file
#     if path is not None:
#         path = utils.normpath(path)
#         root, ext = os.path.splitext(path)
#         ext = ext.lower()
#         if ext not in ['png', 'jpg']:
#             path = root + '_scr.png'
#
#         fig.savefig(path, dpi=300, bbox_inches='tight')
#
#     # show
#     if show:
#         plt.show()
#     else:
#         # close
#         plt.close(fig)
