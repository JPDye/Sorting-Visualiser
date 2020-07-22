import math
import random

# --- Bubble Sort Algorithm
def bubble_sort(array):
    swaps = []
    num_swaps = end = -1
    while num_swaps != 0:
        num_swaps = 0
        end += 1
        for i in range(len(array) - end - 1):
            if array[i] > array[i + 1]:
                array[i], array[i + 1] = array[i + 1], array[i]
                swaps.append((i, i + 1))
                num_swaps += 1
    return swaps


# --- Selection Sort Algorithm
def selection_sort(array):
    swaps = []
    for i in range(len(array)):
        idx = i
        for j in range(i + 1, len(array)):
            if array[j] < array[idx]:
                idx = j
        array[i], array[idx] = array[idx], array[i]
        swaps.append((i, idx))
    return swaps


# --- Insertion Sort Algorithm
def insertion_sort(array):
    swaps = []
    for i in range(1, len(array)):
        while array[i] < array[i - 1] and i >= 1:
            array[i], array[i - 1] = array[i - 1], array[i]
            swaps.append((i, i-1))
            i -= 1
    return swaps


# --- Quick Sort Algorithm and Helper


def quick_sort(array):
    return _quick_sort(array, 0, len(array) - 1)

def _quick_sort(array, start, end):
    swaps = []

    if start >= end:
        return swaps

    pivot = array[random.randint(0, len(array)-1)]
    i, j = start, end

    while i <= j:
        while array[i] < pivot: i += 1
        while array[j] > pivot: j -= 1
        if i <= j:
            array[i], array[j] = array[j], array[i]
            swaps.append((i, j))
            i, j, = i + 1, j - 1
    return swaps + _quick_sort(array, start, j) + _quick_sort(array, i, end)


# --- Merge Sort Algorithm and Helper
def merge(l_array, r_array):
    combined = []
    i = j = 0

    while i < len(l_array) and j < len(r_array):
        if l_array[i] < r_array[j]:
            combined.append(l_array[i])
            i += 1
        else:
            combined.append(r_array[j])
            j += 1

    if i == len(l_array):
        combined.extend(r_array[j:])
    else:
        combined.extend(l_array[i:])
    return combined


def iterative_merge_sort(array):
    arr = array.copy()

    pos = 0
    size = 1
    temp_array = []

    swaps = []

    while size < len(arr):
        while pos < len(arr):
            left = arr[pos:pos+size]
            pos += size
            right = arr[pos:pos+size]
            pos += size
            temp_array.extend(merge(left, right))
        swaps.extend(temp_array)
        arr = temp_array
        temp_array = []
        size *= 2
        pos = 0
    return swaps



# --- Radix Sort Algorithm (LSD)
def radix_sort_lsd(array):
    arr = array.copy()
    swaps = []

    max_exp = int(math.log(max(arr), 10))
    exp = 0

    while exp <= max_exp:
        arr = radix_sort_helper(arr, 10 ** exp)
        swaps.extend(arr)
        exp += 1
    return swaps

def radix_sort_helper(array, exp):
    """
    Counting sort impelmentation optimised for helping radix sort.
    """
    n = len(array)
    output = [0] * n
    counter = [0] * 10

    for num in array:
        index = int((num // exp) % 10)
        counter[index] += 1

    for i in range(1, 10):
        counter[i] += counter[i - 1]

    i = n - 1
    while i >= 0:
        index = int((array[i] // exp) % 10)
        output[counter[index] - 1] = array[i]
        counter[index] -= 1
        i -= 1
    return output

# --- Counting sort Algorithm - Helper for Radix Sort
def counting_sort(array, max_val=None):
    if not max_val:
        max_val = max(array)

    output = []
    counter = [0]  * (max_val + 1)

    for num in array:
        counter[num] += 1               # Track how many times each number occurs, using the number as index for the counter

    for num, count in enumerate(counter):
        output.extend([num] * count)    # Append a number onto output list, count number of times.

    return output



# --- Heap Sorting Algorithm and Heap ADT
class Heap:
    # ---------------- Nested Class ---------------- #
    class _Item:
        slots = "_key", "_heap_type"
        def __init__(self, key, heap_type):
            self._key = key
            self._heap_type = heap_type

        def __lt__(self, other):
            if self._heap_type == "min":
                return self._key < other._key
            else:
                return self._key > other._key

        def __str__(self):
            return str(self._key)

        def __repr__(self):
            return str(self)

    # ---------------- Class Methods ---------------- #
    def __init__(self, data=(), heap_type="min"):
        self._data = [self._Item(k, heap_type) for k in data]
        self._heap_type = heap_type
        self._size = len(self._data)
        self._swaps = []
        if self._size > 0:
            self._heapify()

    def __len__(self):
        return self._size

    def _parent(self, i):
        return (i-1) // 2

    def _left(self, i):
        return (i * 2) + 1

    def _right(self, i):
        return  (2 * i) + 2

    def _has_left(self, i):
        return self._left(i) <= len(self) - 1

    def _has_right(self, i):
        return self._right(i) <= len(self) - 1

    def _smallest_child(self, i):
        if self._has_left(i):
            left = self._left(i)
            small_child = left
            if self._has_right(i):
                right = self._right(i)
                if self._data[right] < self._data[left]:
                    small_child = right
            return small_child

    def _swap(self, i, j):
        self._swaps.append((i, j))
        self._data[i], self._data[j] = self._data[j], self._data[i]

    def _sift_up(self, i):
        if i > 0 and self._data[i] < self._data[self._parent(i)]:
            self._swap(i, self._parent(i))
            self._sift_up(self._parent(i))      # recur at position of parent

    def _sift_down(self, i):
        if self._has_left(i):
            small_child = self._smallest_child(i)
            if self._data[small_child] < self._data[i]:
                self._swap(i, small_child)
                self._sift_down(small_child)        # recur at position of small_child

    def _heapify(self):
        start = self._parent(len(self))         # start at deepest non-leaf node
        for i in range(start, -1, -1):
            self._sift_down(i)

    def insert(self, value):
        item = self._Item(value, self._heap_type)
        self._data.append(item)
        self._size += 1
        self._sift_up(len(self))

    def peek(self):
        if len(self) == 0:
            raise IndexError("heap is empty")
        return self._data[1]._key

    def pop(self):
        if len(self) == 0:
            raise IndexError("heap is empty")
        self._swap(0, len(self)-1)
        item = self._data.pop()._key
        self._size -= 1
        self._sift_down(0)
        return item

    def heap_sort(self):
        for i in range(len(self)):
            self._swap(0, len(self)-1)
            self._size -= 1
            self._sift_down(0)
        return self._data, self._swaps


def heap_sort(array):
    heap = Heap(array.copy(), "max")
    return heap.heap_sort()[1]



if __name__ == "__main__":
    import random
    x = [random.randint(0, 100) for i in range(18)]
    print(heap_sort(x))
