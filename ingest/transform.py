import os
import sys

def main(data):
	print("transform")
	newData = {}
	columns = ["Nr", "name", "Title" , "body"]

	for i in range(len(data)):
		row = data[i]
		body = row[columns.index("Title")] + " U.S.C. § " + row[columns.index("Nr")] + " " + row[columns.index("name")] + "\n" + row[columns.index("body")]
		metadata = [row[columns.index("Nr")], row[columns.index("name")], row[columns.index("Title")]]
		newData[i] = body
		#print(body)
	return newData , metadata

if __name__ == '__main__':
	main()