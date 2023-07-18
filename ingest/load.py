import os
import sys

def main(filtered):
    print("load")
    chunkSize = 1000
    allChunks = []
    for i in range(len(filtered)):
        row = filtered[i]
        firstLine = row.split("\n")[0]
        body = row.split("\n")[1]
        ## split body into words into no longer than chunkSize characters long
        words = body.split(" ")
        thisChunks = []
        chunk = ""
        for word in words:
            if len(chunk) + len(word) < chunkSize:
                chunk += word + " "
            else:
                thisChunks.append(firstLine + chunk)
                allChunks.append(firstLine + chunk)
                chunk = word + " "
        thisChunks.append(firstLine + chunk)
        allChunks.append(firstLine + chunk)
        ## write chunks to file 
    print(allChunks)
    return allChunks

if __name__ == '__main__':
    main()