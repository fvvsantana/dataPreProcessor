# Data Pre-processor Script

This code was made in my undergraduate research project in order to pre-process data.
The data were collected from the accelerometer sensor of an smartwatch and the goal was detecting what activity the user was doing.

In the data set present in the 'data' folder, we have: timestamp of the collected measure (Timestamp), acceleration on the 3 axis (Ax, Ay, Az), modulus of the acceleration (Acc) and the executed activity (Activity). Among the activities, there were: going downstairs, upstairs, walking, sitting and standing.

The whole idea was finding relevant features about the data that could result in a good classification. With help of the python script, we could use a shell script to process the data and calculate the desired features.

If you're more interested about the whole process of classification, take a look at the [article](WebMediaArticle.pdf) about my scientific initiation project.

## Prerequisites

This script needs Python 3 and the module xlrd to be executed. The used versions were: Python (3.6.9) and xlrd (1.2.0)
In order to install xlrd on Python3 using pip, run the command:
```
python -m pip install xlrd
```

## Usage
Data Pre-processor Script provides operations to work with xlsx and csv datasets, e.g. data calculation, data summarization and file conversion.

In order to get information on how to use the script, open the [help](help.txt) file or run:

```
python dataProcessor.py --help
```

If you're using linux, running the [example.sh file](example.sh) can quickly give you more understanding about how the commands work.
To execute it, enter the 'data' folder and run:
```
sh example.sh
```
Some .csv files will be generated during the data processing. The final data set will be in the [finalData.csv](finalData.csv) file. In this file are calculated the features: Mean_Ax, Median_Ax, Stdev_Ax, Mean_Ay, Median_Ay, Stdev_Ay, Mean_Az, Median_Az, Stdev_Az. The label Activity will be preserved.

To delete the generated files, still in the 'data' folder, run:
```
rm *.csv
```
