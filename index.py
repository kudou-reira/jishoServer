from flask import Flask, abort, request, jsonify, render_template
import json, chardet
import os, csv
import pandas as pd

app = Flask(__name__)

scriptDir = os.path.dirname(os.path.abspath(__file__))
csvDir = os.path.join(scriptDir, 'outputCSV')

try:
	os.makedirs(csvDir)
except OSError:
	pass # already exists

@app.route('/processBook', methods=['POST'])
def main(): 
	# print(request.data)

	print(type(request.data))
	received = request.data.decode("utf-8")
	data = json.loads(received)
	# print(received)
	
	for book in data:
			tempFilename = book["title"] + "(" + book["creators"] + ")" + ".csv"
			# print(tempFilename)
			outputCSVFile = os.path.join(csvDir, tempFilename)
			with open(outputCSVFile, 'w', newline='', encoding='utf-8-sig') as f:
				fieldnames = ['searchedWord', 'pronounciations', 'englishDefinition', 'partOfSpeech', 'tags', 'seeAlso', 'info']
				writer = csv.DictWriter(f, fieldnames=fieldnames)
				writer.writeheader()
				
				for word in book["bookWords"]:
					# print(word["searchedWord"])
					counter = 0
					entryCounter = 1
					for entry in word["entries"]:
							formatPronounciations = ', '.join("{!s}={!r}".format(k,v) for (k,v) in entry["pronounciations"].items())

							etymologiesLength = len(entry["etymologies"])
							# etymologies is a list of etymology objects
							etymologies = entry["etymologies"]
							if counter == 0:
									# counter controls the searchedWord
									writer.writerow({'searchedWord' : word["searchedWord"]})
									# after writerow, goes to next row, so always a gap line?
							else:
									writer.writerow({'searchedWord' : ''})

							writer.writerow({'searchedWord' : str(entryCounter), 'pronounciations': formatPronounciations, 'englishDefinition': ', '.join(etymologies[0]["englishDefinition"]), 'partOfSpeech': ', '.join(etymologies[0]["partOfSpeech"]), 'tags': ', '.join(etymologies[0]["tags"]), 'seeAlso': ', '.join(etymologies[0]["seeAlso"])})
							for i in range(1, etymologiesLength, 1):
									writer.writerow({'englishDefinition': ', '.join(etymologies[i]["englishDefinition"])})
							
							counter += 1
							entryCounter += 1
			
			# should be done writing to csv
			# now render it to a template

	links = []
	linkStr = '/outputBooks/'

	directory = os.fsencode(csvDir)
	for file in os.listdir(directory):
		filename = os.fsdecode(file)
		if filename.endswith(".csv"): 
			# create a list of csv filenames, these will have csv replaced with html(?)
			# returns a web link
			# ex. "your files have been created, click here to view them (served) or to download"
			# print(os.path.join(directory, filename))
			
			links.append(request.base_url.replace('/processBook', '') + linkStr + filename.replace('.csv', ''))

	# return a list of rendered views (links, or whatever)
	print(links)
	return jsonify({'result' : 'success', 'links': links})

# https://stackoverflow.com/questions/34009980/return-a-download-and-rendered-page-in-one-flask-response
# https://python-forum.io/Thread-show-csv-file-in-flask-template-html

@app.route('/test')
def index(): 
	return "this is the test page"

@app.route('/outputBooks')
def processedLinks():
	return 'outputBooks'

@app.route('/outputBooks/<filename>')
def output_download(filename):
    # error is file does not exist
	columns = ["searchedWord", "pronounciations", "englishDefinition", "partOfSpeech", "tags", "seeAlso", "info"]
	directoryPath = csvDir + "\\" + filename + ".csv"
	df = pd.read_csv(directoryPath, engine='python')
	tempHTML = df.to_html()
	return render_template('index.html', table=tempHTML)
	# return "this is the filename" + filename + "and this is the directoryPath" + directoryPath


if __name__ == '__main__':
	app.run(host='0.0.0.0', port=3000, debug=True)