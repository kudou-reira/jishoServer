from flask import Flask, abort, request, jsonify
from collections import namedtuple
import helpers as hl
import json, chardet
import csv

app = Flask(__name__)

@app.route('/processBook', methods=['POST'])
def main(): 
	# print(request.data)
	# print(json.loads(data))
	print(type(request.data))
	received = request.data.decode("utf-8")
	data = json.loads(received)
	# print(received)
	
	for book in data:
			tempFilename = book["title"] + "(" + book["creators"] + ")" + ".csv"
			print(tempFilename)
			with open(tempFilename, 'w', newline='', encoding='utf-8-sig') as f:
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


	return jsonify({'result' : 'success'})


if __name__ == '__main__':
	app.run(host='0.0.0.0', port=3000, debug=True)