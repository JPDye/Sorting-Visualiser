from viz import algorithms as algos

from PIL import Image
import numpy as np

class SortingVisualiser:
    def __init__(self, image, randomise=True, reverse=False):
        self.original = np.asarray(image, dtype="uint8")            # Save original image
        self.rows, self.columns, _ = self.original.shape
        self.replaced, self.replace_dict = self.__replace_with_integers() # Replace pixels with consecutive integers for sorting

        if randomise:
            self.__randomise_image()
        if reverse:
            self.__reverse_image()

        self.swaps = []
        self.max_swaps = 0
        self.sorting_methods = {
            "bubble_sort": algos.bubble_sort,
            "selection_sort": algos.selection_sort,
            "insertion_sort": algos.insertion_sort,
            "quick_sort": algos.quick_sort,
            "heap_sort": algos.heap_sort,
            "merge_sort": algos.iterative_merge_sort,
            "radix_sort_lsd": algos.radix_sort_lsd,
        }

    def __replace_with_integers(self):
        replaced = np.zeros((self.rows, self.columns))
        replace_dict = [{}] * self.columns              # Create dict for reverting changes later
        for row in range(self.rows):
            for column in range(self.columns):
                replace_dict[row][column] = self.original[row, column, :]
                replaced[row][column] = column
        return replaced, replace_dict

    def _replace_with_pixels(self):
        pixel_array = np.zeros((self.rows, self.columns, 3), dtype="uint8")
        for row in range(self.rows):
            for column in range(self.columns):
                pixel = self.replace_dict[row][self.replaced[row, column]]
                pixel_array[row, column, :] = pixel
        return pixel_array

    def __reverse_image(self):
        self.replaced = np.flip(self.replaced)

    def __randomise_image(self):
        for i in range(self.rows):
            np.random.shuffle(self.replaced[i, :])

    def __in_place_algo_pixel_swap(self, row, start, end):          # Swap pixels for an in place algorithms
        for i, j in self.swaps[row][start:end]:
            self.replaced[row, i], self.replaced[row, j] = self.replaced[row, j], self.replaced[row, i]

    def __out_place_algo_pixel_swap(self, row, pos, start, step):   # Swap pixels for an out of place algorithm
        pass

    def new_image(self, image, randomise=True):
        self.__init__(image, randomise)

    def sort(self, sorting_method):
        for row_index in range(self.rows):
            row = self.replaced[row_index, :].copy()
            temp_swaps = self.sorting_methods[sorting_method](row)
            self.swaps.append(temp_swaps)
            self.max_swaps = len(self.swaps[-1]) if len(self.swaps[-1]) > self.max_swaps else self.max_swaps

    def visualise(self, num_frames, sort_method="bubble_sort"):
        if not self.swaps:
            self.sort(sort_method)

        num_frames -= 1
        frames = [self._replace_with_pixels()]

        if type(self.swaps[0][0]) is tuple:             # If an in place algorithm was used
            swap_num = 0                                # Track what swap we are on
            swap_step = self.max_swaps // num_frames    # Index needs to be an integer
            remainder = self.max_swaps % num_frames     # Fidn remainder from the int-division

            while swap_num <= self.max_swaps:
                if remainder > 0:       # Check if remainder is left over. Add 1 to indexes is there is.
                    remainder -= 1
                    extra = 1
                else:
                    extra = 0

                for row in range(self.rows):
                    self.__in_place_algo_pixel_swap(row, swap_num, swap_num+swap_step+extra)
                swap_num += swap_step + extra
                frames.append(self._replace_with_pixels())
        else:
            pos = 0
            swap_num = 0
            swap_step = round(self.max_swaps / num_frames)  # Round as index needs to be an integer
            remainder = self.max_swaps % num_frames         # Calculate amount lost from rounding

            while swap_num < self.max_swaps:
                if remainder > 0:       # Check if remainder is left over. Add 1 to indexes is there is.
                    remainder -= 1
                    extra = 1
                else:
                    extra = 0

                # Calculate end positions for swapping
                swap_end = swap_num + swap_step + extra
                pos_end = len(self.swaps[0][swap_num:swap_end]) # Use length of swap list to find end image of index to ensure same lengths.
                pos_end = (pos + pos_end) % self.columns        # If index is greater than length of list. Wrap it around.

                for row in range(self.rows):
                    if pos_end < pos:                           # Check if the index wrapped around
                        swap_amount = self.columns - pos
                        self.replaced[row, pos:] = self.swaps[row][swap_num:swap_num+swap_amount]       # Swap until end of list
                        self.replaced[row, :pos_end] = self.swaps[row][swap_num+swap_amount:swap_end]   # Swap from front to end index
                    else:
                        self.replaced[row, pos:pos_end] = self.swaps[row][swap_num:swap_end]
                swap_num += swap_step + extra
                pos = pos_end
                frames.append(self._replace_with_pixels())
        return frames
