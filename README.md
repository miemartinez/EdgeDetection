# Edge Detection
**This project was developed as part of the spring 2021 elective course Cultural Data Science - Visual Analytics at Aarhus University.**

__Task:__ The project uses computer vision to extract features from a given image. More specifically, the script extracts how many letters and punctuations are in an image with text and saves the image with contours around these. 

In the data folder there is an image of a quote from Jefferson Memorial in Washington D.C. 
The output of the python script is saved in the created out folder. The output folder contains three images. 

The script edge_detection.py is in the src folder and it can be run with only specifying the path to an image with text. 
Furthermore, the script is structured as a class object with three methods. The first method is for making the ROI visualized as a green box and saving this as png. 
The second method crops the original image to the ROI and saves the cropped image as png. 
The third method is for detecting edges using Canny edge detection. 
Additionally, the last method is used for drawing contours around the edges, saving the letter contour superimposed on the original image as png and counting how many contours are in the image (i.e., how many letters have been detected).
To make the script more generalizable, I ensured that the user can define the region of interest from the command line. 
If nothing is specified, the program will use the shape of the image and outline a region that is defined on the basis of the Jefferson Memorial image. <br>

__Dependencies:__ <br>
To ensure dependencies are in accordance with the ones used for the script, you can create the virtual environment ‘edge_environment"’ from the command line by executing the bash script ‘create_edge_venv.sh’. 
```
    $ bash ./create_edge_venv.sh
```
This will install an interactive command-line terminal for Python and Jupyter as well as all packages specified in the ‘requirements.txt’ in a virtual environment. After creating the environment, it will have to be activated before running the edge detection script.
```    
    $ source edge_environment/bin/activate
```
After running these two lines of code, the user can commence running the script. <br>

__Parameters:__ <br>
```
    filepath: str <filepath-to-image>
    output_folder: str <name-of-output-folder>, default = "out"
    x_start: int <start-of-ROI-on-x-axis>
    x_end: int <end-of-ROI-on-x-axis>
    y_start: int <start-of-ROI-on-y-axis>
    y_end: int <end-of-ROI-on-y-axis>

```
    
__Usage:__ <br>
```
    edge_detection.py -f <filepath-to-image> -o <name-of-output-folder> -x_s <start-on-x-axis> -x_e <end-on-x-axis> -y_s <start-on-y-axis> -y_e <end-on-y-axis>
```
    
__Example:__ <br>
```
    $ cd src
    $ python3 edge_detection2.py -f ../data/Jefferson_Memorial.jpg -o out -x_s 1410 -x_e 2840 -y_s 880 -y_e 2800

```

The code has been developed in Jupyter Notebook and tested in the terminal on Jupyter Hub on worker02. I therefore recommend cloning the Github repository to worker02 and running the scripts from there. 

### Results:
For a view of the results when running the script on the Jefferson Memorial image see the out folder.
