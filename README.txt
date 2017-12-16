* PURPOSE
This program extract MINST data file to JSON files.
MINST is a format used to train a network neuron nest.
Here are the data for number recognition : http://yann.lecun.com/exdb/mnist/
For more general information : https://www.nist.gov/itl/iad/image-group/emnist-dataset
* EXAMPLES
 - to extract raw data into JSON, first uncompress the archive
   then, run this command : minstdatasetextractor.py EXTRACT -l <LABELS_FILE> -i <IMAGES_FILE> -o <OUTPUT_FOLDER> -p <PATTERN>
 - to display extracted JSON data, run this command : minstdatasetextractor.py DISPLAY -f <DISPLAY_FILES#0> <DISPLAY_FILES#1> ... <DISPLAY_FILES#N>
