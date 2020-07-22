# Sorting Visualiser
Visualise the sorting of randomised colour gradients.


<p align="center">
  <img src="https://github.com/JPDye/sorting-visualiser/blob/master/img/example/merge_sort_1.gif" />
</p>


<p align="center">
  <img src="https://github.com/JPDye/sorting-visualiser/blob/master/img/example/sn_mid_radix.gif" />
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


### Input:
- viridis
- plasma
- magma
- inferno
- custom
- image

For custom gradient set COLOUR_1, COLOUR_2 and COLOUR_SPACE variables. DIRECTION variable changes direction of interpolation.
For an image, place an image in the /img/input folder, set USE_IMAGE flag to True and the IMAGE_NAME vairable to name of image.

### To Do
- Create CLI or command line argumnets for variables within main.py that control visualisation attributes.
- Add ColCon and GradientCreator to GitHub. Program relies on these tools to create perceptually unfirom gradients.
- Provide matplotlib gradients, so that users dont have to rely on my modules. Virdis is priority for colour blind support.
- Change QuickSort to iterative QuickSort. 
