# Sorting Visualiser
Visualise the sorting of randomised colour gradients.

# Usage

python ./main <algo_name>

choose from:
  - bubble_sort
  - selection_sort
  - insertion_sort
  - quick_sort
  - heap_sort
  - merge_sort
  - radix_sort_lsd
  

If choosing to use merge_sort set number of colours to a power of 2 for best looking results. 
If using radix_sort set number of colours to multiple of 100 for best looking result
  
Variables within main.py control other attributes of the visualisation. Will create CLI for this at a later date.

Program relies on two other modules of mine - ColCon (Colour Converter) and Gradient (Gradient Creator). These modules have not been uploaded to GitHub yet, I'm cleaning up the code slightly first. 

Project is still usable, you just wont be able to create perceptually uniform gradients for the visualiser. Just comment out lines 89-109 in main.py and feed a numpy array of pixels into the visualiser on line 112 in place of the pixels variable.
