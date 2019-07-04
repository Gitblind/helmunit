import os,re,shutil

def find_nth(string, substring, n):
   if (n == 1):
       return string.find(substring)
   else:
       return string.find(substring, find_nth(string, substring, n - 1) + 1)

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

# Create _test.yaml file for each template yaml file
def create_test_file_for(filename):
    try:
        testfilename = re.search('templates/(.+?).yaml', filename).group(1)+"_test.yaml"
    except AttributeError:
        print("Error, can not find the yaml file")
    
    print("Create a new test file:" + testpath + testfilename)
    testfile = open(testpath + testfilename, 'w') 
    return testfile

# List all yaml files under template directory
for filename in yamlfiles:
    
    testfile = create_test_file_for(filename)

    #read yaml file line by line
    lines = [line.rstrip('\n') for line in open(filename)]
    parentlevel = 0
    levelspacenumber = 2
    prefix = ''

    for line in lines:
        if (line.find(":") > -1):
            line = line.replace("-", " ")
            level = (len(line)-len(line.lstrip(' ')))/levelspacenumber

            if level == 0:
                pathindicator = line[:line.index(":")].lstrip(' ')
                prefix = line[:line.index(":")].lstrip(' ') + "."
            elif level > parentlevel :
                pathindicator = prefix + line[:line.index(":")].lstrip(' ')
                prefix = prefix + line[:line.index(":")].lstrip(' ') + "."
            elif level <= parentlevel :
                pathindicator = prefix + line[:line.index(":")].lstrip(' ')
                prefix = prefix[0:find_nth(prefix, ".", level)+1]

            parentlevel = level
            testfile.write(pathindicator + "\n")
