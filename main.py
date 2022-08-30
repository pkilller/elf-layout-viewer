# encoding: utf-8

import other


# 工程说明: 根据map_view.cfg中提供的so(elf)文件的内存布局信息, 来绘制出分布图, 帮助直观了解elf格式在内存中的分布.
#           方便脱壳还原elf.

class Sec:
    def __init__(self):
        self.inside = []
        self.same = []
        pass
    name = ""
    begin = 0
    end = 0
    comment = ""

    inside = [] # 包含的
    same = []   # 相同边界的

# return
def pre_cfg(str_map_view):
    # clean comment
    index = 0
    is_first = True
    while (index != -1):
        if is_first is False:
            end_index = str_map_view[index:].find("\r\n")
            if (end_index == -1):
                end_index = len(str_map_view)
            else:
                end_index = index+end_index+2 #计入换行, 防止将前面的注释截断, 造成后续无法替换
            str_map_view = str_map_view.replace(str_map_view[index:end_index],"\r\n")
        index = str_map_view.find("#")
        is_first = False

    # clear space
    while (str_map_view.find(" ") != -1):
        str_map_view = str_map_view.replace(" ", "")

    while (str_map_view.find("\r\n\r\n") != -1):
        str_map_view = str_map_view.replace("\r\n\r\n", "\r\n")
    return str_map_view


def _str2int(str_number):
    str_number = str_number.lower()
    if len(str_number) > 2 and str_number[:2] == "0x":
        return int(str_number, 16)
    elif len(str_number) > 1 and str_number[-1:] == "h":
        str_hex = "0x"+str_number[:-1]
        return int(str_hex, 16)
    else:
        return int(str_number)


# return : obj_sec
def str_to_sec(str_sec):
    obj_sec = Sec()

    name = other.regex_search("n\=(\S+)", str_sec)
    sec = other.regex_search("s\=(\S+)", str_sec)
    comment = other.regex_search("c\=(\S+)", str_sec)

    # sec
    if sec.find(",") != -1:
        tmp_ret = sec.split(",")
        obj_sec.begin = _str2int(tmp_ret[0])
        obj_sec.end = obj_sec.begin + _str2int(tmp_ret[1]) - 1
    elif sec.find("-") != -1:
        tmp_ret = sec.split("-")
        obj_sec.begin = _str2int(tmp_ret[0])
        obj_sec.end = _str2int(tmp_ret[1])
    else:
        return None
    pass
    obj_sec.name = name
    obj_sec.comment = comment
    return obj_sec


# return : list_secs[obj_sec, ...]
def cfg_to_objs(str_map_view):
    list_objs = []
    str_map_view = pre_cfg(str_map_view)
    list_secs = other.regex_search_all("\{[\s\S]*?\}", str_map_view)

    for str_sec in list_secs:
        obj_sec = str_to_sec(str_sec)
        list_objs.append(obj_sec)
    return list_objs


def __do_levels(list_secs):
    secs_count = len(list_secs)

    # 合并同区域
    for i in range(secs_count-1, -1, -1):
        if list_secs[i] is None:
            continue
        for _i in range(secs_count-1, -1, -1):
            if i == _i or list_secs[_i] is None:
                continue
            if list_secs[i].begin == list_secs[_i].begin and list_secs[_i].end == list_secs[i].end:
                list_secs[i].same.append(list_secs[_i])
                list_secs[_i] = None    # 标记,

    # 移入被包含关系
    for i in range(secs_count-1, -1, -1):
        if list_secs[i] is None:
            continue
        for _i in range(secs_count-1, -1, -1):
            if i == _i or list_secs[_i] is None:
                continue
            # 若被包含, 则移入
            elif list_secs[i].begin <= list_secs[_i].begin and list_secs[_i].end <= list_secs[i].end:
                list_secs[i].inside.append(list_secs[_i])
                list_secs[_i] = None    # 标记,

    # 清除None项
    for i in range(secs_count-1, -1, -1):
        if list_secs[i] is None:
            del list_secs[i]

    # 冒泡排序
    is_over = False
    if len(list_secs) >= 2:
        while is_over is False:
            is_over = True
            for i in range(1, len(list_secs)):
                if (list_secs[i-1].begin > list_secs[i].begin):
                    tmp_sec = list_secs[i-1]
                    list_secs[i-1] = list_secs[i]
                    list_secs[i] = tmp_sec
                    is_over = False


    # 递归整理
    for i in range(len(list_secs)-1, -1, -1):
        __do_levels(list_secs[i].inside)

    pass


def do_levels(list_secs):
    __do_levels(list_secs)


def _sec_view(obj_sec, level_count):
    # header
    header = "{ ["+hex(obj_sec.begin)+"h]" + obj_sec.name
    for obj_sec_same in obj_sec.same:
        header += " / " + obj_sec_same.name
    header = "  "*level_count + header

    # foot
    foot = "} ["+hex(obj_sec.end)+"h]" + obj_sec.name
    for obj_sec_same in obj_sec.same:
        foot += " / " + obj_sec_same.name
    foot = "  "*level_count + foot

    # inside
    inside = ""
    last_addr = obj_sec.end
    for obj_sec_inside in obj_sec.inside:
        # 若非紧密连接, 则输出空隙长度
        if (last_addr+1 < obj_sec_inside.begin):
            inside += "  "*(level_count+1)
            inside += "/* gap size: %xh  */" % (obj_sec_inside.begin-(last_addr+1))
            inside += "\r\n"
        inside_view = _sec_view(obj_sec_inside, level_count+1)
        inside += inside_view + "\r\n\r\n"
        last_addr = obj_sec_inside.end

    if inside[-4:] == "\r\n\r\n":
        inside = inside[:-2]

    if inside != "":
        return header + "\r\n" + inside + "" + foot
    else:
        return header + "\r\n" + foot

def do_output_view(list_secs):
    obj_sec = Sec()
    obj_sec.name = "elf(.so)"
    obj_sec.begin = 0
    obj_sec.end = list_secs[len(list_secs)-1].end
    obj_sec.inside = list_secs
    return _sec_view(obj_sec, 0)


def main():
    list_secs = cfg_to_objs(other.read_file_data("map_view.cfg").decode('utf-8'))
    do_levels(list_secs)
    str_output_map_view = do_output_view(list_secs)
    other.write_file_data("output_map_view.txt", str_output_map_view.encode("utf-8"))
    pass



main()