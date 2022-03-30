'''
author:蔡尚霖
date:2022/3/4
'''
import random
import time
from PySide2.QtWidgets import QApplication, QMessageBox, QTableWidgetItem
from PySide2.QtUiTools import QUiLoader
from PySide2.QtCore import Qt


class Sort_comparison():
    def __init__(self):
        self.sorting_method = [
            ("冒泡排序", self.bubble_sort),
            ("插入排序", self.insert_sort),
            ("选择排序", self.selection_sort),
            ("希尔排序", self.shell_sort),
            ("　堆排序", self.heap_sort),
            ("归并排序", self.merge_sort),
            ("快速排序", self.quick_sort),
            ("基数排序", self.radix_sort)
        ]

        self.ui = QUiLoader().load('ui.ui')

        for i in range(8):
            self.ui.tableWidget.insertRow(i)

        for i in range(8):
            for j in range(4):
                self.__dict__['item' + str(i) + str(j)] = QTableWidgetItem()
                self.__dict__['item' + str(i) + str(j)].setFlags(Qt.ItemIsEnabled)
                self.ui.tableWidget.setItem(i, j, self.__dict__['item' + str(i) + str(j)])
                self.__dict__['item' + str(i) + str(j)].setTextAlignment(Qt.AlignRight)

        self.ui.pushButton.clicked.connect(self.calculate)

    def calculate(self):
        try:
            group = int(self.ui.lineEdit.text())  # 组数
            length = int(self.ui.lineEdit_2.text())  # 表长
            start = int(self.ui.lineEdit_3.text())  # 随机数最小数
            end = int(self.ui.lineEdit_4.text())  # 随机数最大数

            i = 0
            for s, func in self.sorting_method:
                average_compare, average_move, average_runningtime = self.calculation(group, start, end, length, func)
                print("{:<7}{:<19.0f}{:<20.0f}{:<.7f}".format(s, average_compare, average_move, average_runningtime))

                self.ui.tableWidget.item(i, 0).setText(s)
                self.ui.tableWidget.item(i, 1).setText("{:.0f}".format(average_compare))
                self.ui.tableWidget.item(i, 2).setText("{:.0f}".format(average_move))
                self.ui.tableWidget.item(i, 3).setText("{:.7f}".format(average_runningtime))
                i += 1

        except:
            QMessageBox.about(
                self.ui,
                '异常',
                '输入错误'
            )

    def random_list(self, start, stop, length):  # 生成随机列表
        randomlist = []

        for i in range(length):
            randomlist.append(random.randint(start, stop))

        return randomlist

    def bubble_sort(self, nums, length):  # 冒泡排序
        compare = 0
        move = 0

        for i in range(length):
            for j in range(0, length - i - 1):
                compare += 1
                if nums[j] > nums[j + 1]:
                    nums[j], nums[j + 1] = nums[j + 1], nums[j]
                    move += 3

        return compare, move

    def insert_sort(self, nums, length):  # 插入排序
        compare = 0
        move = 0

        for i in range(1, length):
            j = i - 1
            compare += 1
            if nums[i] < nums[j]:
                temp = nums[i]
                nums[i] = nums[j]
                move += 2
                j -= 1
                compare += 1
                while j >= 0 and nums[j] > temp:
                    nums[j + 1] = nums[j]
                    move += 1
                    j -= 1
                nums[j + 1] = temp
                move += 1

        return compare, move

    def selection_sort(self, nums, length):  # 选择排序
        compare = 0
        move = 0

        for i in range(length):
            min_idx = i
            for j in range(i + 1, length):
                compare += 1
                if nums[min_idx] > nums[j]:
                    min_idx = j
            nums[i], nums[min_idx] = nums[min_idx], nums[i]
            move += 3

        return compare, move

    def shell_sort(self, nums, length):  # 希尔排序
        compare = 0
        move = 0

        gap = int(length / 2)
        while gap > 0:
            for i in range(gap, length):
                temp = nums[i]
                move += 1
                j = i
                compare += 1
                while j >= gap and nums[j - gap] > temp:
                    nums[j] = nums[j - gap]
                    j -= gap
                    nums[j] = temp
                    move += 2
            gap = int(gap / 2)

        return compare, move

    def heap_sort(self, nums, length):  # 堆排序
        compare_move = [0, 0]

        def heap_sort_(heap, length, compare_move):
            build_max_heap(heap, length, compare_move)
            for i in range(length - 1, -1, -1):
                heap[0], heap[i] = heap[i], heap[0]
                compare_move[1] += 3
                max_heapify(heap, i, 0, compare_move)
            return heap

        def build_max_heap(heap, length, compare_move):  # 构造最大堆
            heap_size = length
            for i in range((heap_size - 2) // 2, -1, -1):
                max_heapify(heap, heap_size, i, compare_move)

        def max_heapify(heap, heap_size, root, compare_move):
            left = 2 * root + 1
            right = left + 1
            larger = root
            compare_move[0] += 2
            if left < heap_size and heap[larger] < heap[left]:
                larger = left
            if right < heap_size and heap[larger] < heap[right]:
                larger = right
            if larger != root:
                heap[larger], heap[root] = heap[root], heap[larger]
                compare_move[1] += 3
                max_heapify(heap, heap_size, larger, compare_move)

        heap_sort_(nums, length, compare_move)

        return compare_move[0], compare_move[1]

    def merge_sort(self, nums, left, right):  # 归并排序
        compare_move = [0, 0]

        def merge_sort_(nums, left, right, compare_move):
            if left < right:
                mid = int((left + (right - 1)) / 2)
                merge_sort_(nums, left, mid, compare_move)
                merge_sort_(nums, mid + 1, right, compare_move)
                merge(nums, left, mid, right, compare_move)
            return nums

        def merge(nums, left, mid, right, compare_move):
            n1 = mid - left + 1
            n2 = right - mid
            L = [0] * n1
            R = [0] * n2

            for i in range(0, n1):
                L[i] = nums[left + i]
                compare_move[1] += 1
            for i in range(0, n2):
                R[i] = nums[mid + 1 + i]
                compare_move[1] += 1

            i, j, k = 0, 0, left
            while i < n1 and j < n2:
                compare_move[0] += 1
                if L[i] <= R[j]:
                    nums[k] = L[i]
                    compare_move[1] += 1
                    i += 1
                else:
                    nums[k] = R[j]
                    compare_move[1] += 1
                    j += 1
                k += 1

            while i < n1:
                nums[k] = L[i]
                compare_move[1] += 1
                i += 1
                k += 1
            while j < n2:
                nums[k] = R[j]
                compare_move[1] += 1
                j += 1
                k += 1

        merge_sort_(nums, left, right, compare_move)

        return compare_move[0], compare_move[1]

    def quick_sort(self, nums, left, right):  # 快速排序
        compare_move = [0, 0]

        def quick_sort_(nums, left, right, compare_move):
            if left < right:
                pi = partition(nums, left, right, compare_move)
                quick_sort_(nums, left, pi - 1, compare_move)
                quick_sort_(nums, pi + 1, right, compare_move)

        def partition(nums, left, right, compare_move):
            i = left - 1
            pivot = nums[right]

            for j in range(left, right):
                compare_move[0] += 1
                if nums[j] <= pivot:
                    i += 1
                    nums[i], nums[j] = nums[j], nums[i]
                    compare_move[1] += 3

            nums[i + 1], nums[right] = nums[right], nums[i + 1]
            compare_move[1] += 3

            return i + 1

        quick_sort_(nums, left, right, compare_move)

        return compare_move[0], compare_move[1]

    def radix_sort(self, nums):  # 基数排序
        compare = 0
        move = 0

        max_num = max(nums)
        move += 1
        place = 1
        while max_num >= 10 ** place:
            place += 1
        for i in range(place):
            buckets = [[] for _ in range(10)]
            for num in nums:
                radix = int(num / (10 ** i) % 10)
                buckets[radix].append(num)
            j = 0
            for k in range(10):
                for num in buckets[k]:
                    nums[j] = num
                    move += 1
                    j += 1

        return compare, move

    def calculation(self, group, start, end, length, func):  # 计算
        average_compare = 0  # 平均比较次数
        average_move = 0  # 平均移动次数
        average_runningtime = 0  # 平均运行时间

        for i in range(group):
            nums = self.random_list(start, end, length)

            start_time = time.perf_counter()
            if func == self.merge_sort or func == self.quick_sort:  # 判断是否为归并排序或快速排序
                compare, move = func(nums, 0, length - 1)
            elif func == self.radix_sort:
                compare, move = func(nums)
            else:
                compare, move = func(nums, length)
            end_time = time.perf_counter()

            average_compare += compare
            average_move += move
            average_runningtime += (end_time - start_time)
        average_compare /= 5
        average_move /= 5
        average_runningtime /= 5

        return average_compare, average_move, average_runningtime


if __name__ == '__main__':
    app = QApplication([])
    sc = Sort_comparison()
    sc.ui.show()
    app.exec_()
