import pandas as pd
import numpy as np
import os
import re

def bands(file_path):
    # ファイルを行ごとに読み込む
    with open(file_path, 'r') as file:
        lines = file.readlines()

    k_points = []

    band_data = []
    i = 1
    while i < len(lines):
        combined_row = []
        k_points_flg = True
        while k_points_flg:
            if i == len(lines):
                break
            line = lines[i]
            values = line.strip().split()
            if len(values) == 3:
                k_points.append(values)
                k_points_flg = False
                i += 1
            else:
                combined_row += values
                i += 1
        band_data.append(combined_row)

    band_data = np.array(band_data[1:])

    # DataFrameに変換
    k_points_df = pd.DataFrame(k_points, columns=['K_x', 'K_y', 'K_z'])
    bands_df = pd.DataFrame(band_data, columns=[f'Band_{i+1}' for i in range(band_data.shape[1])])

    return bands_df, k_points_df

def pdos(folder_path):

    def readEData(file_path):
        with open(file_path, 'r') as file:
            lines = file.readlines()
        E_column = []
        i = 1
        while i < len(lines):
            values = lines[i].strip().split()
            E_column.append(float(values[0]))
            i += 1

        return E_column

    def readLdosData(file_path):
        with open(file_path, 'r') as file:
            lines = file.readlines()
        ldos_column = []
        i = 1
        while i < len(lines):
            values = lines[i].strip().split()
            ldos_column.append(float(values[1]))
            i += 1

        return ldos_column
    
    file_list = []

    try:
        file_names = os.listdir(folder_path)
        for name in file_names:
            file_list.append(name)
    except FileNotFoundError:
        print(f"指定されたフォルダが見つかりません: {folder_path}")
    except Exception as e:
        print(f"エラーが発生しました: {e}")

    # 抽出結果を格納するリスト
    extracted_data = []

    # 正規表現パターンを定義（元素記号が1～2文字対応）
    pattern = r"atm#\d+\(([A-Z][a-z]?)\)_wfc#(\d+)"

    # 各ファイル名を処理
    for file_name in file_list:
        match = re.search(pattern, file_name)
        if match:
            # 原子記号と #番号を抽出
            atom = match.group(1)  # 原子記号（1～2文字）
            wfc_number = match.group(2)  # wfc 番号
            extracted_data.append((atom, wfc_number, file_name))

    atomList = []
    wfcList = []
    pdos_data = []
    E_data = []

    # 結果を表示
    for atom, wfc_number, file_name in extracted_data:
        # print(f"Atom: {atom}, WFC #: {wfc_number}")
        ldos_data = readLdosData(folder_path + "/" + file_name)
        if atom in atomList:
            atomNum = atomList.index(atom)
            if wfc_number in wfcList[atomNum]:
                wfcNum = wfcList[atomNum].index(wfc_number)
                for i in range(len(pdos_data[atomNum])):
                    pdos_data[atomNum][wfcNum][i] = float(ldos_data[i]) + float(pdos_data[atomNum][wfcNum][i])
            else:
                wfcNum = len(wfcList[atomNum])
                wfcList[atomNum].append(wfc_number)
                pdos_data[atomNum].append(ldos_data)
        else:
            atomNum = len(atomList)
            atomList.append(atom)
            wfcList.append([wfc_number])
            pdos_data.append([ldos_data])
            E_data.append(readEData(folder_path + "/" + file_name))

    # below sorted pdos
    for index, pdos in enumerate(pdos_data):
        sorted_data = []
        for x in range(len(wfcList[index])):
            ele = pdos[wfcList[index].index(str(x+1))]
            sorted_data.append(ele)
        pdos_data[index] = sorted_data
        wfcList[index].sort()

    return pdos_data, E_data, atomList, wfcList

def concat_pdos(pdos_data, indices):
    ans = []
    for index, data in enumerate(pdos_data):
        if not index in indices:
            continue
        concat_pdos = []
        for pdos in data:
            if concat_pdos == []:
                concat_pdos = pdos
            else:
                for x in range(len(pdos)):
                    concat_pdos[x] += pdos[x]
        ans.append(concat_pdos)
    return ans

def pdos2(prefix1, prefix2, prefix_list):
    def readEData(file_path):
        with open(file_path, 'r') as file:
            lines = file.readlines()
        E_column = []
        # pdos_column = []
        i = 1
        while i < len(lines):
            values = lines[i].strip().split()
            E_column.append(float(values[0]))
            i += 1

        return E_column

def pdos2(prefix1, prefix2, prefix_list):
    def readEData(file_path):
        with open(file_path, 'r') as file:
            lines = file.readlines()
        E_column = []
        # pdos_column = []
        i = 1
        while i < len(lines):
            values = lines[i].strip().split()
            E_column.append(float(values[0]))
            i += 1

        return E_column

    def readPdosData(file_path):
        with open(file_path, 'r') as file:
            lines = file.readlines()
        ldos_column = []
        # pdos_column = []
        i = 1
        while i < len(lines):
            values = lines[i].strip().split()
            ldos_column.append(float(values[1]))
            i += 1
        # print(ldos_column)

        return ldos_column


    # 抽出結果を格納するリスト
    E_data = []
    pdos_data = []

    # prefix1 = "./../I_"
    # prefix2 = "_pdos.dat"
    # prefix_list = ["s05", "p05", "p15"]

    for i in prefix_list:
        E_data.append(readEData(prefix1 + i + prefix2))
        pdos_data.append(readPdosData(prefix1 + i + prefix2))
    
    return E_data, pdos_data