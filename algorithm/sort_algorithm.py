#! /usr/bin/python
#coding=utf-8

import utils

@utils.time_wrapper
def sort_maopao(array_like:list):
    """冒泡排序
    """
    n = len(array_like)
    for i in range(0, n - 1):
        for j in range(0, n - i - 1):
            if array_like[j] > array_like[j + 1]:
                array_like[j], array_like[j + 1] = array_like[j + 1], array_like[j] 

    return array_like


@utils.time_wrapper
def sort_chose(array_like:list):
    """选择排序
    每次选择最大或者最小的数进行插入
    """
    for i in range(0, len(array_like)):
        min_vale = array_like[i]
        min_idx = i
        for j in range(i + 1, len(array_like)):
            if (array_like[j] < min_vale):
                min_vale = array_like[j]
                min_idx = j

        array_like[i], array_like[min_idx] = array_like[min_idx], array_like[i]


    return array_like


@utils.time_wrapper
def sort_insert(array_like:list):
    """插入排序
    分成有序和无序两部分，逐步插入
    """

    for i in range(0, len(array_like)):
        tmp_val = array_like[i]
        for j in range(i - 1, -1,  -1):
            if tmp_val < array_like[j]:
                array_like[j + 1] = array_like[j]
            else:
                array_like[j + 1] = tmp_val
                break


    return array_like


@utils.time_wrapper
def sort_hill(array_like:list, k = 5):
    """希尔排序，主要是分治分思想
    """
    for tmp_k in range(k, 0, -1):
        for i in range(0, tmp_k):
            array_like[i::tmp_k] = sort_insert(array_like[i::tmp_k])

    return array_like


@utils.time_wrapper
def sort_merge(array_like, k = 2):
    """归并排序，主要是递归的思想
    送进去k个，返回来1个
    """
    n = len(array_like)
    def __sort_merge(array, i, j):
        """递归程序
        """
        #递归终止条件
        if (j - i == 1 or j - i == 0):
            return  array[i:j]
        else: # 处理递归
            array1 = __sort_merge(array, i, int(i + (j - i) / k))
            array2 = __sort_merge(array, int(i + (j - i) / k), j)

            idx_1 = 0
            idx_2 = 0
            res = []
            while(idx_1 < len(array1) or idx_2 < len(array2)):
                if (idx_1 == len(array1)):
                    res.append(array2[idx_2])
                    idx_2 += 1
                elif (idx_2 == len(array2)):
                    res.append(array1[idx_1])
                    idx_1 += 1
                elif array2[idx_2] < array1[idx_1]:
                    res.append(array2[idx_2])
                    idx_2 += 1
                else :
                    res.append(array1[idx_1])
                    idx_1 += 1

            return  res

    return __sort_merge(array_like, 0, n)

@utils.time_wrapper
def sort_quick(array_like:list):
    """快速排序
    递归+ 分治的思想
    """
    def __sort_quick(array_like, i, j, k):
        r_i = i
        r_j = j
        if (j < i):
            return []
        elif (j - i == 0):
            return array_like[i:j]
        elif (j - i == 1):
            if array_like[i] > array_like[j]:
                array_like[i], array_like[j] = array_like[j], array_like[i]
            return array_like[i:j]
        else:
            while(i < j): #搜索从前到后，写复杂了
                if(i == k):
                    if array_like[k] > array_like[j]:
                        array_like[k], array_like[j] = array_like[j], array_like[k]
                        k = j
                    else:
                        j -= 1
                elif j == k:
                    if array_like[k] < array_like[i]:
                        array_like[k], array_like[i] = array_like[i], array_like[k]
                        k = i
                    else:
                        i += 1
                else:
                    if(array_like[i] > array_like[k] and array_like[j] < array_like[k]):
                        array_like[i], array_like[j] = array_like[j], array_like[i]
                        i += 1
                        j -= 1
                    if (array_like[i] <= array_like[k]):
                        i += 1
                    if (array_like[j] >= array_like[k]):
                        j -= 1

            array1 = __sort_quick(array_like, r_i, k - 1, r_i)
            array2 = __sort_quick(array_like, k + 1, r_j, k + 1)

            #print(array1 + [array_like[k]] + array2)
            return array1+ [array_like[k]] + array2

    n = len(array_like)
    k = 0
    return __sort_quick(array_like, 0, n - 1, k)


@utils.time_wrapper
def sort_heap(array_like:list):
    """堆排序, 小根
    i 的孩子节点为 (i + 1) * 2 - 1, 和 (i + 1) * 2
    """
    def __adjust_heap(array_like, i):
        n = len(array_like)
        idx_par = i
        idx_child_1 = (i) * 2 + 1
        idx_child_2 = (i) * 2 + 2

        if idx_child_1 < n and array_like[idx_par] > array_like[idx_child_1]:
            array_like[idx_par], array_like[idx_child_1] = array_like[idx_child_1], array_like[idx_par]
            array_like = __adjust_heap(array_like, idx_child_1)

        if idx_child_2 < n and array_like[idx_par] > array_like[idx_child_2]:
            array_like[idx_par], array_like[idx_child_2] = array_like[idx_child_2], array_like[idx_par]
            array_like = __adjust_heap(array_like, idx_child_2)

        return array_like
    
    # 初始化堆
    n = len(array_like)
    for i in range(int((n + 1) / 2  - 1), -1, -1):
        array_like = __adjust_heap(array_like, i)

    ans = [array_like[0]]
    array_like[0], array_like[n - 1] = array_like[n - 1], array_like[0]
    for i in range(1, len(array_like)):
        array_like[0: n - i] = __adjust_heap(array_like[0: n - i], 0)
        ans.append(array_like[0])
        array_like[0], array_like[n - i - 1] = array_like[n - i - 1], array_like[0]

    return ans
    
@utils.time_wrapper
def sort_count(array_like):
    """记数排序
    """
    min_val = min(array_like)
    max_val = max(array_like)

    num = max_val - min_val + 1
    count_place = [0] * num
    for i in range(0, len(array_like)):
        count_place[array_like[i] - min_val] += 1

    j = 0
    for i in range(0, len(count_place)):
        for _ in range(0, count_place[i]):
            array_like[j] = min_val + i
            j += 1

    return array_like


if __name__ == "__main__":
    array = utils.generate_random_array(100, -100, 100)
    maopao_array = sort_maopao(array)
    assert utils.is_sorted(maopao_array)

    array = utils.generate_random_array(100, -100, 100)
    chose_array = sort_chose(array)
    assert utils.is_sorted(chose_array)

    array = utils.generate_random_array(100, -100, 100)
    insert_array = sort_insert(array)
    assert utils.is_sorted(insert_array)

    array = utils.generate_random_array(100, -100, 100)
    hill_array = sort_hill(array)
    assert utils.is_sorted(hill_array)

    array = utils.generate_random_array(100, -100, 100)
    merge_array = sort_merge(array)
    assert utils.is_sorted(merge_array)

    array = utils.generate_random_array(100, -100, 100)
    quick_array = sort_quick(array)
    assert utils.is_sorted(quick_array)

    array = utils.generate_random_array(10, -100, 100)
    heap_array = sort_heap(array)
    assert utils.is_sorted(heap_array)

    array = utils.generate_random_array(10, -100, 100)
    count_array = sort_count(array)
    assert utils.is_sorted(count_array)
