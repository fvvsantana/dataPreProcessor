'''

This script needs Python3 and the module xlrd to be executed.
In order to install xlrd on Python3, run the command:
	python3 -m pip install xlrd

'''

import xlrd
import csv
import sys
import getopt
import math
import statistics

#convert a xlsx file to csv. inputFile and outputFile are both string locations
def xlsxToCsv(inputFile, outputFile):
    workbook = xlrd.open_workbook(inputFile)
    sheet = workbook.sheet_by_index(0)
    csvFile = open(outputFile, 'w')
    csvWriter = csv.writer(csvFile)

    for row in range(sheet.nrows):
        csvWriter.writerow(sheet.row_values(row))

    csvFile.close()

#return a string with the value of the acceleration for the given line of the file
def acceleration(line, axPos, ayPos, azPos):
	del line[-1]
	line = list(map(float, line))
	return str(math.sqrt(line[axPos-1]*line[axPos-1] +  line[ayPos-1]*line[ayPos-1] +  line[azPos-1]*line[azPos-1]))

#calculate the given parameters for the inputFile and store it in the outputFile
def calculateToCsv(inputFile, outputFile, parameters):
	outputLine = ''
	with open(inputFile) as inputFile:
		with open(outputFile, 'w+') as outputFile:
			#read the first line
			inputHeader = inputFile.readline()
			#write the first line
			firstLine = ''
			for parameter in parameters:
				firstLine += parameter.split('[')[0].capitalize() + ','
			outputFile.write(firstLine + inputHeader.split(',')[-1])

			#calculate and write the following lines
			for line in inputFile:
				line = line.split(',')
				label = line[-1]
				for parameter in parameters:
					parameter = parameter.split('[')
					#call the function parameter(line, args), where args are the passed arguments
					outputLine += eval(parameter[0] + '(line.copy(), *(eval("[" + parameter[1])))') + ','

				outputFile.write(outputLine + label)
				outputLine = ''

#for each nLines from inputFile, calculate parameters and store it in outputFile
def summarizeToCsv(inputFile, outputFile, parameters, nLines):
	with open(inputFile) as inputFile:
		with open(outputFile, 'w+') as outputFile:

			#read the first line
			inputHeader = inputFile.readline().split(',')

			#write the first line and setup the linesList
			linesList = []
			firstLine = ''
			for i in range(0, len(inputHeader)-1):
				linesList.append(list())
				for parameter in parameters:
					firstLine += parameter.capitalize() + '_' + inputHeader[i] + ','
			outputFile.write(firstLine + inputHeader[-1])

			outputLine = ''
				#labels.count(labels[0]) == len(labels)
			#store the first label to check when it changes
			#label = inputFile.readline().split(',')[-1]
			label = ''
			for line in inputFile:
				line = line.split(',')

				#check if it's the first time
				if label == '':
					label = line[-1]
				#else, check if the label changed
				elif line[-1] != label:
					#save the label
					label = line[-1]
					#clear the lists and add the elements of the line to these lists
					for column in linesList:
						#clear the sublist
						column.clear()
						#append the element
						column.append(float(line[i]))
					continue

				#add the elements of the line to the lists
				for i in range(0, len(line)-1):
					#append the element
					linesList[i].append(float(line[i]))

				#if linesList is full
				if len(linesList[0]) == nLines:
					#for each list inside linesList
					for column in linesList:
						#for each parameter calculate the value and store in the outputLine
						for parameter in parameters:
							try:
								outputLine += str(eval('statistics.' + parameter + '(column)')) + ','
							except Exception as e:
								pass

					#write to the file
					outputFile.write(outputLine + label)

					#clear the outputLine
					outputLine = ''

					#clear the lists
					for column in linesList:
						#clear the sublist
						column.clear()

#select the columns (passed in columnList) of the inputFile and put it on outputFile
def select(inputFile, outputFile, columnList):
	if not columnList:
		return
	outputLine = ''
	with open(inputFile) as inputFile:
		with open(outputFile, 'w+') as outputFile:
			for line in inputFile:
				line = line.split(',')
				outputLine += line[columnList[0]]
				for i in range(1, len(columnList)):
					outputLine += ',' + line[columnList[i]]
				outputFile.write(outputLine)
				outputLine = ''

#concatenate the files from inputFiles into outputFile.
#if ignoreFirstLine is true, then the first line of each file starting 
# in the second file will be disconsidered
def concatenate(inputFiles, outputFile, ignoreFirstLine):
	with open(outputFile, 'w+') as outputFile:
		for i, inputFile in enumerate(inputFiles):
			with open(inputFile) as inputFile:
				if ignoreFirstLine and i != 0:
					inputFile.readline()
				for line in inputFile:
					outputFile.write(line)

#print the help documentation
def printHelp():
	with open('help.txt') as helpFile:
		print(helpFile.read())
	sys.exit(0)

#print the help usage
def printUsage():
	with open('help.txt') as helpFile:
		line = helpFile.readline()
		while line != '\n':
			print(line, end='')
			line = helpFile.readline()
		print()
	sys.exit(0)

#command handling
def main(argv):

	#get command arguments
	try:
		opts, args = getopt.getopt(argv, 'hucCsS:tn:i:o:', ['help', 'usage', 'convert', 'calculate', 'summarize', 'select=', 'concatenate', 'nlines=', 'input=', 'output=', 'ignoreFirstLine'])
		opts = dict(opts)
		#print('opts: ' + str(opts))
		#print('args: ' + str(args))
	except getopt.GetoptError as error:
		sys.stderr.write('Input error:\n\t' + str(error) + '\n')
		sys.exit(1)

	#operations
	if '-h' in opts or '--help' in opts:
		printHelp()
	elif '-u' in opts or '--usage' in opts:
		printUsage()
	elif '-c' in opts or '--convert' in opts:
		xlsxToCsv(opts.get('-i', opts.get('--input', '')), opts.get('-o', opts.get('--output', '')))
	elif '-C' in opts or '--calculate' in opts:
		calculateToCsv(opts.get('-i', opts.get('--input', '')), opts.get('-o', opts.get('--output', '')), args)
	elif '-s' in opts or '--summarize' in opts:
		summarizeToCsv(opts.get('-i', opts.get('--input', '')), opts.get('-o', opts.get('--output', '')), args, int(opts.get('-n', opts.get('--nlines', 10))))
	elif '-S' in opts or '--select' in opts:
		select(opts.get('-i', opts.get('--input', '')), opts.get('-o', opts.get('--output', '')), eval(opts.get('-S', opts.get('--select', 'list()'))))
	elif '-t' in opts or '--concatenate' in opts:
		concatenate(args, opts.get('-o', opts.get('--output', '')), '--ignoreFirstLine' in opts)


#allow this module to be imported
if __name__ == "__main__":
	main(sys.argv[1:])


