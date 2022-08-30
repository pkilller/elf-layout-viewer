#encoding=utf-8
# -*- coding: utf-8 -*-

import inspect
import base64
import json
import random
import subprocess
import re
import requests
import urllib
import hashlib
import time
import datetime

def str_to_json(str_json):
    try:
        '''
        fstream = tempfile.NamedTemporaryFile(mode='w+')
        fstream.write(str_json)
        fstream.flush()
        fstream.seek(0)
        result_json = json.load(fstream)
        '''
        result_json = json.loads(str_json)
        return result_json
    except Exception as e:
        raise e
        return None


# ensure_ascii: True.将非ascii字符转义为\uxxx\uxxx表示方式,  False.不转义,按原值显示.
def json_to_str(obj_json, ensure_ascii=True):
    try:
        return json.dumps(obj_json, ensure_ascii=ensure_ascii)
    except Exception as e:
        return None


def base64_encode(buff):
    return base64.b64encode(buff)


def base64_decode(buff):
    return base64.b64decode(buff)


# 生成随机bytes
# byte值的取值区间为: begin_byte_val - end_byte_val, 如果省略默认为"0x00-0xFF"
def get_req_bytes(bytes_len, begin_byte_val=None, end_byte_val=None):
    r_bytes = ""
    # 区间为NULL, 或不合法时使用默认
    if (None == begin_byte_val or
        None == end_byte_val or
        begin_byte_val > end_byte_val):
        begin_byte_val  = 0x00
        end_byte_val    = 0xFF

    for i in range(bytes_len):
        r_int = int(random.uniform(begin_byte_val, end_byte_val))
        r_bytes += chr(r_int)
    return r_bytes


def byte_2_hex(by):
    HEX_VAL = "0123456789abcdef"

    low_val = ord(by) & 0x0F
    hig_val = ord(by) & 0xF0
    hig_val = hig_val >> 4
    low = HEX_VAL[low_val:low_val+1]
    hig = HEX_VAL[hig_val:hig_val+1]
    return hig+low


# 将bytes转为hex文本
# byte_prefix:每个byte的hex的前缀.例子: "0x"
# byte_seg: 每个byte之间的分隔符.例子:", "
def bytes_2_hexs(in_bytes, byte_prefix=None, byte_seg=None):
    str_hexs    = ""
    index       = 0
    bytes_len   = len(in_bytes)

    if (None == byte_prefix):
        byte_prefix = ""
    if (None == byte_seg):
        byte_seg = ""

    for by in in_bytes:
        index += 1
        hex_str = byte_2_hex(by)
        # 尾部不加分隔符
        if(index != bytes_len):
            str_hexs += byte_prefix + hex_str + byte_seg
        else:
            str_hexs += byte_prefix + hex_str

    return str_hexs


# 从路径中提出 文件名
def get_filename_frompath(file_path):
    # 从路径中提取出文件名
    nMarkIndex = file_path.rfind("\\")
    if(nMarkIndex == -1):
        return file_path
    return file_path[nMarkIndex+1:]


def regex_search_all(pattern, string):
    list_result = []
    Math = re.search(pattern, string)
    try:
        reCompile   = re.compile(pattern)
        list_result = reCompile.findall(string)
    except:
        list_result = None
    return list_result


def regex_search(pattern, string):
    result = None
    try:
        Math = re.search(pattern, string)
        result = Math.groups()[0]
    except Exception as e:
        result = None
    return result


################################################################################
# - Fun     :   检查一个字符串是否完全匹配于正则表达式.
# - Params  :
#               -    strExpress    : 正则表达式.
#               -    strString     : 要检查的字符串.
# - Return  :    匹配: True, 不匹配: False
# - Note    :
#
#
################################################################################
def regex_compare(strExpress, strString):
    reExpress   = None
    Match       = None
    try:
        reExpress = re.compile(strExpress)
        Match = reExpress.match(strString) #字符串是否匹配完全匹配于正则表达式
    except:
        return False

    if(None == Match):
        return False
    else:
        return True
    return False


# 返回: 成功: 数据  失败: None
def read_file_data(file_path):
    try:
        file = open(file_path, "rb")
        data = file.read()
        file.close()
    except Exception as e:
        return None
    return data


# 返回: 成功: True  失败: False
def write_file_data(file_path, data):
    try:
        file = open(file_path, "wb")
        file.write(data)
        file.close()
    except:
        return False
    return True


################################################################################
# - Fun     :   执行控制台Shell
# - Params  :
#               - strCmdline            :    命令行
# - Return  :   元组: (exitcode, strOutStrings) , 当bWaitEnd=True时返回值才有效可靠.
#               - exitcode         : 退出码.
#               - strOutStrings    : 命令台输出的文本.
#
# - Note    :   阻塞模式调用
#
#
################################################################################
def ConsoleShell(strCmdline):
    strTmpOutput    = ""
    listOutput      = []
    SubPs = subprocess.Popen(strCmdline, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, shell=True)
    # 读取执行过程中的输出信息
    while (SubPs.poll() == None):
        strTmpOutput    = str(SubPs.stdout.readline())   #读取一行
        if (strTmpOutput != None):
            listOutput.append(strTmpOutput)
    SubPs.wait(); #等待进程关闭.
    # 读取缓存中的剩余,并拼接为一整条字符串.
    strTmpOutput  = str(SubPs.stdout.read())
    listOutput.append(strTmpOutput)
    strOutput     = "".join(listOutput)
    #取出退出码
    nExitCode = SubPs.returncode

    #关闭流, 防止内存泄露.
    if (SubPs.stdout):
        SubPs.stdout.close()
    if (SubPs.stdin):
        SubPs.stdin.close()
    if (SubPs.stderr):
        SubPs.stderr.close()
    SubPs.kill()
    return (nExitCode, strOutput)


# url编码
def url_encode_utf8(value):
    tmp = value.decode('gbk', 'replace')
    tmp = tmp.encode('utf-8', 'replace')
    return urllib.quote(tmp)


def url_decode_utf8(value):
    tmp = urllib.unquote(value)
    tmp = tmp.decode('utf-8', 'replace')
    return tmp.encode('gbk', 'replace')


def url_encode_gbk(value):
    tmp = value.decode('gbk', 'replace')
    tmp = tmp.encode('gbk', 'replace')
    return urllib.quote(tmp)


def url_decode_gbk(value):
    tmp = urllib.unquote(value)
    tmp = tmp.decode('gbk', 'replace')
    return tmp.encode('gbk', 'replace')


def url_encode(value):
    return urllib.quote(value)


def url_decode(value):
    return urllib.unquote(value)


# get
# sample: tongcheng_request(url="http://xxx.com/", type="get", post_data=None);
# return: (status_code, response_data)
def http_get(session, url, params=None, headers=None, cookies=None, proxies=None, timeout=20):
    try:
        if(session):
            response = session.get(url=url, params=params, headers=headers, cookies=cookies, proxies=proxies, timeout=timeout)
        else:
            response = requests.get(url=url, params=params, headers=headers, cookies=cookies, proxies=proxies, timeout=timeout)
        # response
        response_code = response.status_code

        if(hasattr(response, 'data')):
            responst_data = response.data   # 原始bin数据
        elif(hasattr(response, 'content')):
            responst_data = response.content    # 文本数据, requests库已经将其转为了与当前环境相配的编码.
        elif(hasattr(response, 'text')):
            responst_data = response.text   # 文本数据, 强转编码? 有些页面的内容在此属性会损坏, 无法还原成可读文本.
        else:
            responst_data = None
        #print responst_data
        return (response_code, responst_data)
    except Exception as e:
        return (None,None)


# post
# 返回元组:response_body
# return: (status_code, response_data)
def http_post(session, url, post_data=None, files=None, headers=None, cookies=None, proxies=None, timeout=20):
    try:

        # 若files有效, 则暂存并删除headers::Content-Type, 因为bin上传方式, 需要借助Content-Type来存放分割识别符. 请求完再恢复
        # 如下:
        '''
            POST / HTTP/1.1
            Host: 127.0.0.1
            Accept-Encoding: identity
            Cookie: id=eyJlbmMiOiJBMjU2R0NNIiwiYWxnIjoiZGlyIn0..WfiY3nh4hTfZ6ww4.MNKt5Q-5Vr7F4xCwAp3FvE3ACeuG4DLGM9v5ZKuQQrk9UklohvPj8ODmyy4pTAQRRr3ABRwKOMjQ_JplPwawoDig8oWCgDWNbAmZn9T4GfA6S3wDA2YTJFI4JMK94Rosqru71sRIQCkulgB_.joWeZn99YX1upIDzu9bklA
            Content-Length: 74719
            Content-Type: multipart/form-data; boundary=cbcae3352357437da1cde228f6f044e8

            --cbcae3352357437da1cde228f6f044e8
            Content-Disposition: form-data; name="transient"

            true
            --cbcae3352357437da1cde228f6f044e8
            Content-Disposition: form-data; name="localId"

            1445932840180
            --cbcae3352357437da1cde228f6f044e8
            Content-Disposition: form-data; name="asGroupOwner"

            false
            --cbcae3352357437da1cde228f6f044e8
            Content-Disposition: form-data; name="chatId"
        '''
        if(session):
            # backup 'Content-Type'
            orig_contentType = None
            if(files):
                orig_contentType = session.headers.pop('Content-Type', None)

            response = session.post(url=url, data=post_data, files=files, headers=headers, cookies=cookies, proxies=proxies, timeout=timeout)

            # restore 'Content-Type'
            if(None != orig_contentType):
                session.headers.update({'Content-Type': orig_contentType})

        else:
            response = requests.post(url=url, data=post_data, files=files, headers=headers, cookies=cookies, proxies=proxies, timeout=timeout)
        # response
        response_code = response.status_code

        if(hasattr(response, 'data')):
            responst_data = response.data   # 原始bin数据
        elif(hasattr(response, 'content')):
            responst_data = response.content    # 文本数据, requests库已经将其转为了与当前环境相配的编码.
        elif(hasattr(response, 'text')):
            responst_data = response.text   # 文本数据, 强转编码? 有些页面的内容在此属性会损坏, 无法还原成可读文本.
        else:
            responst_data = None
        # print responst_data
        return (response_code, responst_data)
    except Exception as e:
        return (None,None)


def clac_md5(data):
    md5_obj = hashlib.md5()
    md5_obj.update(data)
    return md5_obj.hexdigest()


def cur_time_str():
    #获得当前时间时间戳
    timeStamp = int(time.time())
    #转换为其他日期格式,如:"%Y-%m-%d %H:%M:%S"
    timeArray = time.localtime(timeStamp)
    otherStyleTime = time.strftime("%Y-%m-%d %H:%M:%S", timeArray)
    return otherStyleTime


def seconds_to_time(v_seconds):
    hour = int(v_seconds/60/60)
    v_seconds -= hour*60*60
    min = int(v_seconds/60)
    v_seconds -= min*60
    return datetime.time(hour, min, int(v_seconds))


# fmt:  0. date+time 1. date  2. time
def timestamp_to_fmtime(v_timestamp, fmt=0):
    timeArray = timestamp_to_structtime(v_timestamp=v_timestamp)
    otherStyleTime = ""
    if fmt == 0:
        otherStyleTime = time.strftime("%Y-%m-%d %H:%M:%S", timeArray)
    elif fmt == 1:
        otherStyleTime = time.strftime("%Y-%m-%d", timeArray)
    elif fmt == 2:
        otherStyleTime = time.strftime("%H:%M:%S", timeArray)
    return otherStyleTime

# fmt:  0. date+time 1. date  2. time
def fmtime_to_timestamp(v_fmtime, fmt=0):
    v_time = None
    if fmt == 0:
        v_datetime = datetime.datetime.strptime(v_fmtime, "%Y-%m-%d %H:%M:%S")
    elif fmt == 1:
        v_datetime = datetime.datetime.strptime(v_fmtime, "%Y-%m-%d")
    elif fmt == 2:
        v_datetime = datetime.datetime.strptime(v_fmtime, "%H:%M:%S")
    v_structtime = datetime_to_structtime(v_datetime=v_datetime)
    return structtime_to_timestamp(v_structtime=v_structtime)

# fmt:  0. date+time 1. date  2. time
def datetime_to_fmtime(v_datetime, fmt=0):
    otherStyleTime = ""
    if fmt == 0:
        otherStyleTime = v_datetime.strftime("%Y-%m-%d %H:%M:%S")
    elif fmt == 1:
        otherStyleTime = v_datetime.strftime("%Y-%m-%d")
    elif fmt == 2:
        otherStyleTime = v_datetime.strftime("%H:%M:%S")
    return otherStyleTime

# fmt:  0. date+time 1. date  2. time
def fmtime_to_datetime(v_fmtime, fmt=0):
    v_time = None
    if fmt == 0:
        v_time = datetime.datetime.strptime(v_fmtime, "%Y-%m-%d %H:%M:%S")
    elif fmt == 1:
        v_time = datetime.datetime.strptime(v_fmtime, "%Y-%m-%d")
    elif fmt == 2:
        v_time = datetime.datetime.strptime(v_fmtime, "%H:%M:%S")

    return v_time


def timestamp_to_structtime(v_timestamp):
    timeArray = time.localtime(v_timestamp)
    return timeArray


def structtime_to_timestamp(v_structtime):
    timestamp=time.mktime(v_structtime)
    return timestamp


def time_to_dayseconds(v_time):
    day_seconds = 0
    if isinstance(v_time, datetime.time):
        day_seconds = v_time.hour*60*60 + v_time.minute*60 + v_time.second
    else:
        return None
    return day_seconds


def structtime_to_dayseconds(v_structtime):
    day_seconds = 0
    if isinstance(v_structtime, time.struct_time):
        day_seconds = v_structtime.tm_hour*60*60 + v_structtime.tm_min*60 + v_structtime.tm_sec
    else:
        return None
    return day_seconds


# [time.time] to [datetime.date]
def structtime_to_date(v_structtime):
    if isinstance(v_structtime, time.struct_time):
        year = v_structtime.tm_year
        mon = v_structtime.tm_mon
        day = v_structtime.tm_mday
    else:
        return None
    v_date = datetime.date(year, mon, day)
    return v_date


def structtime_to_time(v_structtime):
    if isinstance(v_structtime, time.struct_time):
        year = v_structtime.tm_year
        mon = v_structtime.tm_mon
        day = v_structtime.tm_mday
    else:
        return None
    v_date = datetime.date(year, mon, day)
    return v_date


def structtime_to_datetime(v_structtime):
    if isinstance(v_structtime, time.struct_time):
        year = v_structtime.tm_year
        mon = v_structtime.tm_mon
        day = v_structtime.tm_mday
        hour = v_structtime.tm_hour
        min = v_structtime.tm_min
        sec = v_structtime.tm_sec
    else:
        return None
    v_datetime = datetime.datetime(year, mon, day, hour, min, sec)
    return v_datetime


def date_to_structtime(v_date):
    if isinstance(v_date, datetime.date):
        year = v_date.year
        month = v_date.month
        day = v_date.day
    else:
        return None
    v_timestamp = time.mktime((year, month, day, 0, 0, 0, 0, 0, 0))
    v_time = timestamp_to_structtime(v_timestamp=v_timestamp)
    return v_time


def datetime_to_structtime(v_datetime):
    if isinstance(v_datetime, datetime.date):
        year = v_datetime.year
        month = v_datetime.month
        day = v_datetime.day
        hour = v_datetime.hour
        minute = v_datetime.minute
        second = v_datetime.second
    else:
        return None
    v_timestamp = time.mktime((year, month, day, hour, minute, second, 0, 0, 0))
    v_structtime = timestamp_to_structtime(v_timestamp=v_timestamp)
    return v_structtime


def get_caller_function_name():
    # tmp = inspect.stack()
    return inspect.stack()[2][3]


def get_current_function_name():
    # tmp = inspect.stack()
    return inspect.stack()[1][3]