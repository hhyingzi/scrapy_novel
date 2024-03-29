import random

# 卦值-卦像字典
search_name = {
    0: "坤卦",
    1: "山地剥",
    2: "水地比",
    3: "风地观",
    4: "雷地豫",
    5: "火地晋",
    6: "泽地萃",
    7: "天地否",
    8: "地山谦",
    9: "艮卦",
    10: "水山蹇",
    11: "风山渐",
    12: "雷山小过",
    13: "火山旅",
    14: "泽山咸",
    15: "天山逐",
    16: "地水师",
    17: "山水蒙",
    18: "坎卦",
    19: "风水涣",
    20: "雷水解",
    21: "火水未济",
    22: "泽水困",
    23: "天水讼",
    24: "地风升",
    25: "山风蛊",
    26: "水风井",
    27: "巽卦",
    28: "雷风恒",
    29: "火风鼎",
    30: "泽风大过",
    31: "天风垢",
    32: "地雷复",
    33: "山雷颐",
    34: "水雷屯",
    35: "风雷益",
    36: "震卦",
    37: "火雷噬嗑",
    38: "随卦",
    39: "无妄卦",
    40: "地火明夷",
    41: "山火贲",
    42: "水火既济",
    43: "风火家人",
    44: "雷火丰",
    45: "",
    46: "",
    47: "",
    48: "",
    49: "",
    50: "",
    51: "",
    52: "",
    53: "火泽睽",
    54: "兑卦",
    55: "天泽履",
    56: "地天泰",
    57: "山天大畜",
    58: "水天需",
    59: "风天小畜",
    60: "雷天大壮",
    61: "火天大有",
    62: "泽天夬",
    63: "乾卦",
}

search_story = {
    0: "",
    1: "",
    2: "",
    3: "",
    4: "",
    5: "",
    6: "",
    7: "",
    8: "",
    9: "",
    10: "",
    11: "",
    12: "",
    13: "",
    14: "",
    15: "",
    16: "",
    17: "",
    18: "",
    19: "",
    20: "",
    21: "",
    22: "",
    23: "",
    24: "",
    25: "",
    26: "",
    27: "",
    28: "",
    29: "",
    30: "",
    31: "",
    32: "",
    33: "",
    34: "",
    35: "",
    36: "",
    37: "",
    38: "",
    39: "",
    40: "",
    41: "",
    42: "",
    43: "",
    44: "",
    45: "",
    46: "",
    47: "",
    48: "",
    49: "",
    50: "",
    51: "",
    52: "",
    53: "",
    54: "",
    55: "",
    56: "",
    57: "",
    58: "",
    59: "",
    60: "",
    61: "",
    62: "",
    63: "",
}

# 生成初始爻
def generate_yao():
    # 大衍之数五十，其用四十九
    universe = 50  # 道（大衍之数）
    usage = 49  # 用

    # 蓍草卜筮法。
    for i in range(3):
        # 拨草分为两堆，用于初始化：天地人
        sky = random.randint(1, usage - 2)  # 天
        # print("用：", usage)
        # print("Init 天=: ", sky)

        earth = usage - sky  # 地
        human = 1  # 人
        earth = earth - human
        # 计算
        if int(sky % 4) == 0:
            sky = sky - 4
        else:
            sky = sky - sky % 4
        if int(earth % 4) == 0:
            earth = earth - 4
        else:
            earth = earth - earth % 4
        # 汇总为“用”
        usage = sky + earth + human

    return int(usage / 4)  # 返回爻区间为 [6,7,8,9]


# 变爻
def transfor_yao(yao):
    if yao == 6:
        return 9
    elif yao == 9:
        return 6
    else:
        return yao


# 编码，阴（奇数）为0，阳（偶数）为1
def encode(yao_list):
    for i in range(len(yao_list)):
        yao_list[i] = yao_list[i] % 2


# 计算卦值
def calculate(yao_list):
    sg = 32 * yao_list[0] + 16 * yao_list[1] + 8 * yao_list[2] + 4 * yao_list[3] + 2 * yao_list[4] + yao_list[5]
    return sg


if __name__ == '__main__':
    oyao = []
    tyao = []
    # 起卦
    for i in range(6):
        yao = generate_yao()
        oyao.append(yao)  # 本卦
        tyao.append(transfor_yao(yao))  # 变卦
    print("本卦：", oyao)
    print("变卦：", tyao)

    # 编码
    encode(oyao)
    encode(tyao)
    print("本卦编码：", oyao)
    print("变卦编码：", tyao)

    # 计算卦值
    sg = calculate(tyao)
    print("变卦为:", sg, "-", search_name.get(sg))


