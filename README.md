# Sorting Visualiser

Create colour gradients in different colour spaces and then feed them into a sorting visualiser.
<p align="center">
  <img src="https://github.com/JPDye/sorting-visualiser/blob/custom_gradients/img/example/viridis_1.gif" />
</p>

<p align="center">
  <img src="https://github.com/JPDye/sorting-visualiser/blob/custom_gradients/img/gradients/all_colour_spaces.png" />
</p>




## Usage
```shell
python ./main <algo_name>
```
### Algorithms:
- bubble_sort
- selection_sort
- insertion_sort
- quick_sort
- heap_sort
- merge_sort
- radix_sort_lsd

For best results use merge_sort with the NUM_COLOURS variable set to a power of 2.

For best results use radix_sort_lsd with the NUM_COLOURS variable set to a multiple of 100


### Gradients:
- viridis
- plasma
- magma
- inferno
- custom
- image

Set COLOUR_MAP to one of these to feed a gradient into the visualiser.

For custom gradient set COLOUR_1, COLOUR_2 and COLOUR_SPACE variables. DIRECTION variable changes direction of interpolation.

For an image, place an image in the /img/input folder, set USE_IMAGE flag to True and the IMAGE_NAME vairable to name of image.

### To Do
- Create CLI.
- Change QuickSort to iterative QuickSort. 
- Add BogoSort, CocktailSort, TimSort and more...
