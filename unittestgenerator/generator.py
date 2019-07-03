import os

#Step 1: Ask for a directory, if there's no templates directory under the directory, return error; if yes, create test directory
#Step 2: List all yaml files under template directory
path = '.'

yamlfiles = []
for root, directories, files in os.walk(path):
    for file in files:
        if '.yaml' in file and 'templates' in os.path.basename(root):
            yamlfiles.append(os.path.join(root, file))

for f in yamlfiles:
    print(f)

#Step 4: read yaml file line by line
#Step 5: 

