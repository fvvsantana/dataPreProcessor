#!/bin/bash
#convert all the .xlsx files to .csv file
echo "Converting all the xlsx files..."
for filename in *.xlsx; do
	python3 ../dataProcessor.py --convert -i "$filename" -o $(basename "$filename" .xlsx).csv
done

#concatenate all the .csv files
echo "Concatenating all the csv files..."
python3 ../dataProcessor.py --concatenate --ignoreFirstLine -o concatenated.csv *.csv

#select only the relevant columns
echo "Selecting the relevant columns..."
python3 ../dataProcessor.py --select [1,2,3,5] -i concatenated.csv -o selectedColumns.csv

#python3 ../dataProcessor.py --calculate -i relevantData.csv -o calculateExample.csv acceleration[0,1,2]
echo "Summarizing the data..."
python3 ../dataProcessor.py --summarize --nlines 32 -i selectedColumns.csv -o finalData.csv mean median stdev

echo "Done"

#!/bin/bash
#for filename in /Data/*.txt; do
#    for ((i=0; i<=3; i++)); do
#        ./MyProgram.exe "$filename" "Logs/$(basename "$filename" .txt)_Log$i.txt"
#    done
#done
