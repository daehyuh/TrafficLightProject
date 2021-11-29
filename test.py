import pandas as pd

import requests
import time
from time import sleep


def get_hex():
    target_url = "http://49.50.163.17:8933/get_hex"

    response = requests.post(target_url)

    return response.text


def hex_to_step(hex_data):
    step = hex_data[14:15]
    return step


def hex_to_time():
    step = get_hex()[13:15]
    return step


def get_int_fulltime():
    return int(get_hex()[33:35], 16)


def get_int_time():
    return int(get_hex()[31:33], 16)


def get_int_step():
    return int(get_hex()[14], 16)

print(get_int_time())


# df = pd.DataFrame(
#     {'STEP': [0, 1, 2, 3, 4, 5, 6, 7], 'RED': [1, 1, 1, 1, 1, 1, 1, 1], 'YELLOW': [0, 0, 0, 1, 0, 0, 0, 0],
#      'LEFT': [1, 1, 1, 0, 0, 0, 0, 0], 'GREEN': [0, 0, 0, 0, 0, 0, 0, 0]})
# df = df.set_index('STEP')
# df.to_csv("test.csv")
#
# df2 = pd.read_csv("test.csv")
# print(df2)
#
# hex_data = get_hex()
# step = hex_to_step(hex_data)
# print(step)
#
# inform_dict = {"RED": 0, "YELLOW": 0, "LEFT": 0, "GREEN": 0}
# inform_by_step = df2[df2['STEP'] == int(step)]
#
#
# keys = inform_dict.keys()
# print(keys)
#
# for k in inform_dict.keys():
#     if k in inform_by_step:
#         inform_dict[k] = int(inform_by_step[k])
#
# print(inform_dict)
#
# print(inform_by_step)






