import matplotlib.pyplot as plt
import numpy as np
import os
import pandas as pd

from matplotlib.figure import Figure

def bands(bands_df:pd.DataFrame, k_points_positions:list[float], k_points_root:list[str], spin:bool=False, k_points_each:int=None, bands_spin_df:pd.DataFrame=None, ylim:list[int] = [], Fermi:float=0, console:bool=False, k_range:list[int] = None, size=[4,5], XLocs = [], spin_max = 0.5, spin_min = -0.5):
    """
    バンド図を描画する処理

    Parameters
    -----------------

    bands_df : DataFrame
        列ごとに異なるバンドのデータ
    k_points_positions : DataFrame
        バンド図のK点の位置。要素の数だけ取得しているので細かい部分は適当
    k_points_each : Int
        それぞれのK点間のサンプル数を入力
    k_points_root : list[str]
        設定したK点のルートを配列で入力する
    spin : Bool
        スピン期待値を表示するか否か指定する
    bands_spin_df : DataFrame
        列ごとに各バンドのスピン期待値のデータ
    save ; Bool
        保存するか否かを指定する
    ylim : list[int]
        y軸の範囲を指定する
    Fermi : Float
        フェルミエネルギーを入力すると0eVに固定される
    k_range1 : list[int]
        k点の選択範囲ののインデックス

    Returns
    --------------------
    fig : Figure
        バンド図
    """
    # 各K点の位置を等間隔の値に変換
    # k_points_positions = range(len(k_points_df))

    plt.rcParams["font.family"] = "Times New Roman"
    plt.rcParams["mathtext.fontset"] = "stix"
    plt.rcParams["font.size"] = 14
    plt.rcParams["xtick.labelsize"] = 12
    plt.rcParams["ytick.labelsize"] = 12
    plt.rcParams['xtick.direction'] = 'in' # x axis in
    plt.rcParams['ytick.direction'] = 'in' # y axis in

    K_points_num = len(k_points_positions)
    # k_points_each = 30
    # k_points_root = [r"$\Gamma$", "K", "M", r"$\Gamma$"]

    # プロットの準備
    # fig = plt.figure(figsize=(size[0], size[1]), dpi=100)
    fig = Figure(figsize=(size[0], size[1]), dpi=150)
    ax1 = fig.add_axes(
        # (left, bottom, width, height)
        (0.14, 0.1, 0.83, 0.88),
    )

    ax1.tick_params(
        right = True,
        left = True,
        top = True,
        bottom = True,
    )

    # それぞれのバンドをプロット
    cbar_flg = False
    for col in bands_df.columns:
        ax1.plot(k_points_positions, list(map(lambda y: float(y) - Fermi, bands_df[col])), color='black', lw=0.5)
        if spin:
            # sc = ax1.pcolormesh(np.arange(0, K_points_num, 1), list(map(lambda y:float(y) - Fermi, bands_df[col])), list(map(float, bands_spin_df[col])), cmap='jet', vmin=spin_min, vmax=spin_max)
            sc = ax1.scatter(np.arange(0, K_points_num, 1), list(map(lambda y:float(y) - Fermi, bands_df[col])), c=list(map(float, bands_spin_df[col])), cmap='jet', vmin=spin_min, vmax=spin_max, s=10, marker="_")
            if not cbar_flg:
                cbar = fig.colorbar(sc, ax=ax1)
                cbar_flg = True
            # cbar.set_label('Spin Expectation Value', fontsize=12)

    # 軸ラベルやタイトルを追加
    ax1.set_xlabel('K-point')
    ax1.set_ylabel('Energy (eV)')
    # ax1.set_title('Band Structure')
    ax1.grid(axis="x", c="black", lw=0.5)
    if k_points_each:
        ax1.set_xticks(np.arange(0, K_points_num, k_points_each))
    elif XLocs != []:
        ax1.set_xticks(XLocs)
    ax1.set_xticklabels(k_points_root)

    # x軸の範囲を設定
    if XLocs == []:
        if k_range:
            ax1.set_xlim(k_points_each*k_range[0], k_points_each*k_range[1])
        else:
            ax1.set_xlim(0, K_points_num-1)
    else:
        ax1.set_xlim(0, XLocs[-1])

    # y軸の範囲を設定
    if ylim:
        ax1.set_ylim(ylim[0], ylim[1])

    return fig

def save(fig:plt.Figure, file_path:str):
    """
    画像を保存する処理

    すでに指定した名前のファイルが存在していれば、インデックスを加算して保存する

    Parameters
    ------------------

    fig : Figure
        保存する画像
    file_path : String
        保存先のパスを指定する

    Returns
    ------------------
    None
    """
    base, ext = os.path.splitext(file_path)  # ファイル名と拡張子を分ける
    counter = 1
    
    # 同じ名前のファイルが存在する限り、番号をインクリメント
    new_filepath = file_path
    while os.path.exists(new_filepath):
        new_filepath = f"{base}_{counter}{ext}"
        counter += 1

    # ファイルを保存
    fig.savefig(new_filepath)
    print(f"Saved figure as: {new_filepath}")

def bands_compare(bands_df_1:pd.DataFrame, bands_df_2:pd.DataFrame, k_points_positions_1:list[float], k_points_positions_2:list[float], k_points_root:list[str], spin:bool=False, k_points_each:int=None, bands_spin_df:pd.DataFrame=None, file_name:str = None, ylim:list[int] = [], Fermi:float=0, console:bool=False, k_range:list[int] = None, size=[4,5], XLocs = [], labels:list[str] = ["band1", "band2"]):
    """
    バンド図を描画する処理

    Parameters
    -----------------

    bands_df : DataFrame
        列ごとに異なるバンドのデータ
    k_points_positions : DataFrame
        バンド図のK点の位置。要素の数だけ取得しているので細かい部分は適当
    k_points_each : Int
        それぞれのK点間のサンプル数を入力
    k_points_root : list[str]
        設定したK点のルートを配列で入力する
    spin : Bool
        スピン期待値を表示するか否か指定する
    bands_spin_df : DataFrame
        列ごとに各バンドのスピン期待値のデータ
    save ; Bool
        保存するか否かを指定する
    file_name : String
        保存する際のファイル名を指定する
    ylim : list[int]
        y軸の範囲を指定する
    Fermi : Float
        フェルミエネルギーを入力すると0eVに固定される
    k_range1 : list[int]
        k点の選択範囲ののインデックス

    Returns
    --------------------
    fig : Figure
        バンド図
    """
    # 各K点の位置を等間隔の値に変換
    # k_points_positions = range(len(k_points_df))

    plt.rcParams["font.family"] = "Times New Roman"
    plt.rcParams["mathtext.fontset"] = "stix"
    plt.rcParams["font.size"] = 14
    plt.rcParams["xtick.labelsize"] = 12
    plt.rcParams["ytick.labelsize"] = 12
    plt.rcParams['xtick.direction'] = 'in' # x axis in
    plt.rcParams['ytick.direction'] = 'in' # y axis in

    K_points_num = 0
    if XLocs == []:
        K_points_num = len(k_points_positions_1)
    # k_points_each = 30
    # k_points_root = [r"$\Gamma$", "K", "M", r"$\Gamma$"]

    # プロットの準備
    fig = plt.figure(figsize=(size[0], size[1]), dpi=150)
    ax1 = fig.add_axes(
        # (left, bottom, width, height)
        (0.14, 0.1, 0.83, 0.88),
    )

    ax1.tick_params(
        right = True,
        left = True,
        top = True,
        bottom = True,
    )

    # それぞれのバンドをプロット
    label_flg = False
    cbar_flg = False
    for col in bands_df_1.columns:
        if label_flg:
            # ax1.plot(k_points_positions_1, list(map(lambda y: float(y) - Fermi, bands_df_1[col])), color='black', lw=0.5)
            ax1.scatter(k_points_positions_1, list(map(lambda y: float(y) - Fermi, bands_df_1[col])), color='black', s=0.5)
        else:
            # ax1.plot(k_points_positions_1, list(map(lambda y: float(y) - Fermi, bands_df_1[col])), color='black', lw=0.5, label=labels[0])
            ax1.scatter(k_points_positions_1, list(map(lambda y: float(y) - Fermi, bands_df_1[col])), color='black', s=0.5, label=labels[0])
            label_flg = True
        if spin:
            sc = ax1.scatter(np.arange(0, K_points_num, 1), list(map(lambda y:float(y) - Fermi, bands_df[col])), c=list(map(float, bands_spin_df[col])), cmap='jet', vmin=-0.5, vmax=0.5, s=10)
            if not cbar_flg:
                cbar = fig.colorbar(sc, ax=ax1)
                cbar_flg = True
            # cbar.set_label('Spin Expectation Value', fontsize=12)
            
    label_flg = False
    for col in bands_df_2.columns:
        if label_flg:
            # ax1.plot(k_points_positions_1, list(map(lambda y: float(y) - Fermi, bands_df_1[col])), color='red', lw=0.5)
            ax1.scatter(k_points_positions_2, list(map(lambda y: float(y) - Fermi, bands_df_2[col])), color='red', s=0.5)
        else:
            # ax1.plot(k_points_positions_1, list(map(lambda y: float(y) - Fermi, bands_df_1[col])), color='red', lw=0.5, label=labels[1])
            ax1.scatter(k_points_positions_2, list(map(lambda y: float(y) - Fermi, bands_df_2[col])), color='red', s=0.5, label=labels[1])
            label_flg = True

    # 軸ラベルやタイトルを追加
    ax1.set_xlabel('K-point')
    ax1.set_ylabel('Energy (eV)')
    # ax1.set_title('Band Structure')
    ax1.grid(axis="x", c="black", lw=0.5)
    if k_points_each:
        ax1.set_xticks(np.arange(0, K_points_num, k_points_each))
    elif XLocs != []:
        ax1.set_xticks(XLocs)
    ax1.set_xticklabels(k_points_root)

    # x軸の範囲を設定
    if XLocs == []:
        if k_range:
            ax1.set_xlim(k_points_each*k_range[0], k_points_each*k_range[1])
        else:
            ax1.set_xlim(0, K_points_num-1)
    else:
        ax1.set_xlim(0, XLocs[-1])

    # y軸の範囲を設定
    if ylim:
        ax1.set_ylim(ylim[0], ylim[1])

    ax1.legend()

    if file_name:
        save(fig, "./../fig/" + file_name + ".png")
    return fig

def pdos(pdos_data, E_data, label, xlim=[], ylim=[], file_name=None, Fermi:float=0):

    plt.rcParams["font.family"] = "Times New Roman"
    plt.rcParams["mathtext.fontset"] = "stix"
    plt.rcParams["font.size"] = 14
    plt.rcParams["xtick.labelsize"] = 12
    plt.rcParams["ytick.labelsize"] = 12
    plt.rcParams['xtick.direction'] = 'in' # x axis in
    plt.rcParams['ytick.direction'] = 'in' # y axis in

    # プロットの準備
    fig = plt.figure(figsize=(4, 5), dpi=150)
    ax1 = fig.add_axes(
            (0.14, 0.1, 0.83, 0.88),
    )

    ax1.tick_params(
        right = True,
        left = True,
        top = True,
        bottom = True,
    )

    colourList = ["black", "blue", "red", "green", "purple"]

    if xlim:
        ax1.set_xlim(xlim[0], xlim[1])
    if ylim:
        ax1.set_ylim(ylim[0], ylim[1])

    for index, ele in enumerate(pdos_data):
        ax1.plot(ele, list(map(lambda y: float(y) - Fermi, E_data[0])), c=colourList[index], label=convert_to_fraction(label[index]), lw=0.5)

    # 軸ラベルやタイトルを追加
    ax1.set_xlabel('DOS')
    ax1.set_ylabel('Energy (eV)')
    ax1.legend()
    if file_name:
        save(fig, "./../fig/pdos/" + file_name + ".png")

    return fig

def convert_to_fraction(notation):
    """
    Convert notations like s05, p15 to s1/2, p3/2.

    Parameters:
        notation (str): The input string (e.g., "s05", "p15").

    Returns:
        str: The converted string (e.g., "s1/2", "p3/2").
    """
    import re

    # Regular expression to match the format
    match = re.match(r"([a-zA-Z]+)(\d+)", notation)
    if not match:
        return notation

    letter = match.group(1)  # Alphabetical part (e.g., "s", "p")
    # print(match.group(2))
    number1 = int(match.group(2)[0])
    number2 = int(match.group(2)[1]) # always 5

    # Convert the number to n/2 format
    numerator = number1 * 2 + 1
    denominator = 2
    fraction = f"{numerator}/{denominator}"

    # Combine the letter and the fraction
    return f"{letter}{fraction}"

def spin_split(bands_df, index1, index2, k_points_each:int, k_points_root:list[str], k_points_num, rangeX=-1):

    plt.rcParams["font.family"] = "Times New Roman"
    plt.rcParams["mathtext.fontset"] = "stix"
    plt.rcParams["font.size"] = 14
    plt.rcParams["xtick.labelsize"] = 12
    plt.rcParams["ytick.labelsize"] = 12
    plt.rcParams['xtick.direction'] = 'in' # x axis in
    plt.rcParams['ytick.direction'] = 'in' # y axis in

    fig = plt.figure(figsize=(4, 5), dpi=150)
    ax1 = fig.add_axes(
        # (left, bottom, width, height)
        (0.14, 0.1, 0.83, 0.88),
    )

    ax1.tick_params(
        right = True,
        left = True,
        top = True,
        bottom = True,
    )

    column1 = bands_df.columns[index1]
    column2 = bands_df.columns[index2]
    list1 = list(map(lambda x: float(x), bands_df[column1]))
    list2 = list(map(lambda x: float(x), bands_df[column2]))
    ax1.plot(np.arange(0, k_points_num, 1), list(map(lambda y1, y2: (y2 - y1)*1E+3, list1, list2)), color='black')

    # 軸ラベルやタイトルを追加
    ax1.set_xlabel('K-point')
    ax1.set_ylabel('spin split (meV)')
    # ax1.set_title('Band Structure')
    ax1.grid(axis="x", c="black", lw=0.5)
    ax1.set_xticks(np.arange(0, k_points_num, k_points_each))
    ax1.set_xticklabels(k_points_root)

    # x軸の範囲を設定
    if rangeX >= 0:
        ax1.set_xlim(10*(rangeX-1), 10*rangeX)
        print(rangeX)
    else:
        ax1.set_xlim(0, k_points_num-1)

    ax1.set_ylim(0, 100)

def spin(spin_df, index1, k_points_each:int, k_points_root:list[str], k_points_num):

    plt.rcParams["font.family"] = "Times New Roman"
    plt.rcParams["mathtext.fontset"] = "stix"
    plt.rcParams["font.size"] = 14
    plt.rcParams["xtick.labelsize"] = 12
    plt.rcParams["ytick.labelsize"] = 12
    plt.rcParams['xtick.direction'] = 'in' # x axis in
    plt.rcParams['ytick.direction'] = 'in' # y axis in

    fig = plt.figure(figsize=(4, 5), dpi=150)
    ax1 = fig.add_axes(
        # (left, bottom, width, height)
        (0.14, 0.1, 0.83, 0.88),
    )

    ax1.tick_params(
        right = True,
        left = True,
        top = True,
        bottom = True,
    )

    column1 = spin_df.columns[index1]
    list1 = list(map(lambda x: float(x), spin_df[column1]))
    ax1.plot(np.arange(0, k_points_num, 1), list1, color='black')
    
    # x軸の範囲を設定
    ax1.set_xlim(0, k_points_num-1)

    ax1.set_ylim(-0.5, 0.5)

    # 軸ラベルやタイトルを追加
    ax1.set_xlabel('K-point')
    ax1.set_ylabel('spin split (eV)')
    # ax1.set_title('Band Structure')
    ax1.grid(axis="x", c="black", lw=0.5)
    ax1.set_xticks(np.arange(0, k_points_num, k_points_each))
    ax1.set_xticklabels(k_points_root)