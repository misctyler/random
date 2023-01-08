import os
import sys
x = []
for subdir, dirs, files in os.walk(sys.argv[1]):
    #print(str(files))
    for file in files:
        path = subdir + os.sep + file
        if path.endswith(".log"):  # FILE SELECTOR
            with open(path) as f:
                for line in f:
                    if sys.argv[2] in line:
                        print(str(path) + ' - ' + str(line))
                        x.append(line)
