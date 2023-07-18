import os
import sys
sys.path.append(os.path.join(os.path.dirname(__file__), 'ingest'))
from ingest import extract, transform, load

data = extract.main()
filtered = transform.main(data)
results = load.main(filtered)
dir = os.path.dirname(__file__)
parent = os.path.dirname(dir)
for i in range(len(results)):
	with open(dir +'/sqldump/sample-'+str(i)+'.txt', 'a') as f:
		print(dir +'/sqldump/sample-'+str(i)+'.txt')
		f.write(results[i])
