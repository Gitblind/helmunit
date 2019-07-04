import os,re,shutil

# Ask for a directory
path = '.'
# path = input('Enter directory: ')
testpath = ''

# Get all yaml files in templates directory
yamlfiles = []
for root, directories, files in os.walk(path):
    for file in files:
        if '.yaml' in file and 'templates' in os.path.basename(root):
            yamlfiles.append(os.path.join(root, file))
            testpath = os.path.dirname(os.path.abspath(root))+'/tests/'

#If there's yaml file, create test directory
if testpath:
    if os.path.exists(testpath):
        shutil.rmtree(testpath)
    print("Create a tests directory:" + testpath)
    os.mkdir(testpath)
else:
    print("There's no .yaml files in templates directory")
    raise SystemExit

# List all yaml files under template directory
for filename in yamlfiles:
    try:
        # Create _test.yaml file for each template yaml file
        testfilename = re.search('templates/(.+?).yaml', filename).group(1)+"_test.yaml"
    except AttributeError:
        print("Error, can not find the yaml file")
    
    print("Create a new test file:" + testpath + testfilename)
    testfile = open(testpath + testfilename, 'w') 

    #read yaml file line by line
    lines = [line.rstrip('\n') for line in open(filename)]
    currentlevel = 0
    prefix = ''
    levelspacenumber = 2
    for line in lines:
        if (line.find(":") > -1):
            pathindicator = prefix + line[:line.index(":")]
            print(pathindicator)
            # testfile.write(pathindicator + "\n")
            # prefix = prefix + 

            # level = (len(line)-len(line.rstrip(' ')))/2
            # line = line.rstrip(' ')
            # level = level
            
            # prefix = prefix + levelspace
        else:
            prefix = ''


