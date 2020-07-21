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

Program can either create a gradient using two of my own modules - ColCon and GradientCreator - or take an image as input. ColCon and GradientCreator haven't been uploaded yet so only option is to give image as input. Place Image in img/input and set the USE_IMAGE flag to True and the IMAGE_NAME variable to the name of the image.

### To Do
- Create CLI or command line argumnets for variables within main.py that control visualisation attributes.
- Add ColCon and GradientCreator to GitHub. Program relies on these tools to create perceptually unfirom gradients.
- Provide matplotlib gradients, so that users dont have to rely on my modules. Virdis is priority for colour blind support.
