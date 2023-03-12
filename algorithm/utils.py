#! /usr/bin/python
#coding=utf-8

import random
import time

def time_wrapper(func):
    """记时装饰器
    """
    def wrapper_func(*args, **key_args):
        st = time.perf_counter()
        res = func(*args, **key_args)
        cost_time = time.perf_counter() - st

        print(f"{func.__name__}, Time cost: {cost_time}")
        return res
    return wrapper_func

def generate_random_array(n, min, max):
    """产生随机序列
    """
    return [random.randint(min, max) for _ in range(n)]


def is_sorted(array_like):
    """检查是否升序
    """
    for i in range(0, len(array_like) - 1):
        if array_like[i] > array_like[i + 1]:
            return False
    print("Input array is sorted.")
    return True

if __name__ == "__main__":

    random_array = generate_random_array(100, 0, 100)
