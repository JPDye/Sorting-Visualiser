# Sorting Visualiser
Visualise the sorting of randomised colour gradients.

![Alt Text](https://github.com/JPDye/sorting-visualiser/blob/master/img/example/merge_sort_1.gif)




## Usage
```shell
python ./main <algo_name>
```
Replace <algo_name> with one of the following:
- bubble_sort
- selection_sort
- insertion_sort
- quick_sort
- heap_sort
- merge_sort (set NUM_COLOURS to power of 2 for best results)
- radix_sort_lsd (set NUM_COLOURS to multiple of 100 for best results)

Two required modules - ColCon and GradientCreator - have not been uploaded to GitHub yet. Project is still usable. Just comment out lines 91-116 in main.py and feed a numpy array of pixels in the visualiser on line 112 in place of the pixels variable.

### To Do
- Create CLI or command line argumnets for variables within main.py that control visualisation attributes.
- Add ColCon and GradientCreator to GitHub. Program relies on these tools to create perceptually unfirom gradients. Cleaning code up first.
- Rewrite '__replace_with_integers()' function to allow passing images as well as gradients.
