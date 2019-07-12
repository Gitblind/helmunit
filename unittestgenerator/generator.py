import os,re,shutil

# Get all yaml files in templates directory
def get_yaml_files(path):
    yamlfiles = []
    for root, directories, files in os.walk(path):
        for file in files:
            if '.yaml' in file and 'templates' in os.path.basename(root):
                yamlfiles.append(os.path.join(root, file))
    return yamlfiles

# Get test dir for template file
def get_test_dir_for(templatefile):
    testpath = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(templatefile))), 'testsdemo')
    return testpath

# If there's yaml file, create test directory
def create_test_dir_for(templatefile):
    testpath = get_test_dir_for(templatefile)

    if os.path.exists(testpath):
        print("Clean up the directory:" + testpath)
        shutil.rmtree(testpath)
    print("Create a tests directory:" + testpath)
    os.mkdir(testpath)
    return testpath

# Create _test.yaml file for each template yaml file
def create_test_file_for(filename):
    try:
        testfilename = re.search('templates(.+?).yaml', filename).group(1)+"_test.yaml"
    except AttributeError:
        print("Error, can not find the yaml file")
        raise SystemExit
    
    print("Create a new test file:" + testpath + testfilename)
    testfile = open(testpath + testfilename, 'w') 
    return testfile

def write_new_line(file):
    file.write("\n")

def write_n_space(file, n):
    while n > 0:
        file.write(" ")
        n = n -1 

# Create Test File Header
def create_test_file_header(templatefile, testfile):
    testfile.write("suite: test " + templatefile)
    write_new_line(testfile)
    testfile.write("templates:")
    write_new_line(testfile)
    write_n_space(testfile, 2)
    testfile.write("- " + os.path.basename(filename))
    write_new_line(testfile)
    testfile.write("tests:")
    write_new_line(testfile)
    write_n_space(testfile, 2)
    testfile.write("- it: should pass")
    write_new_line(testfile)
    write_n_space(testfile, 4)
    testfile.write("release:")
    write_new_line(testfile)
    write_n_space(testfile, 6)
    testfile.write("name: demo-release")
    write_new_line(testfile)
    write_n_space(testfile, 4)
    testfile.write("asserts:")
    write_new_line(testfile)

    return testfile

# Write Assert for each path
def write_assert_path(testfile, levelpathstack):
    path = ''

    for level in list(levelpathstack):
        path = path + levelpathstack[level] + "."
    path = path[:len(path) - 1]

    # TBD: Currently, we will not add path including "command."
    if path.find('command.') < 0:
        write_n_space(testfile, 6)
        testfile.write("- equal: ")
        write_new_line(testfile)
        write_n_space(testfile, 10)
        testfile.write("path: " + path)
        write_new_line(testfile)
        write_n_space(testfile, 10)
        testfile.write("value: [NeedYourInput]")
        write_new_line(testfile)

# Find nth substring in a string
def find_nth(string, substring, n):
   if (n == 1):
       return string.find(substring)
   else:
       return string.find(substring, find_nth(string, substring, n - 1) + 1)


# Ask for a directory
path = input('Enter directory: ')
yamlfiles = get_yaml_files(path)
value_in_next_line = False
testpath = ''

# List all yaml files under template directory
for filename in yamlfiles:
    if testpath != get_test_dir_for(filename):
        testpath = create_test_dir_for(filename)

    testfile = create_test_file_for(filename)
    testfile = create_test_file_header(filename, testfile)

    #read yaml file line by line
    lines = [line.rstrip('\n') for line in open(filename)]
    levelpathstack = {}

    for line in lines:
        # Ignore the comment line with : in it
        if (line.lstrip(' ').startswith('#')):
            continue

        # Replace the starting "-" with " " to count the level
        if line.lstrip(' ').startswith('- '):
            line = line.replace('- ', '  ')
        
        if line.lstrip(' ').startswith('{'):
            if value_in_next_line:
                write_assert_path(testfile, levelpathstack)
                value_in_next_line = False
        elif (line.find(":") > -1):
            spacenumber = len(line) - len(line.lstrip(' '))

            if spacenumber in levelpathstack:
                # Remove all later level
                for levelspace in list(levelpathstack):
                    if levelspace >= spacenumber:
                        del levelpathstack[levelspace]
            
            # Update current level
            pathindicator = line[:line.index(":")].lstrip(' ')
            levelpathstack[spacenumber] = pathindicator

            # if the line ends with :, there's no assert for this path
            if not line.rstrip(' ').endswith(':'):
                write_assert_path(testfile, levelpathstack)
                value_in_next_line = False
            else:
                value_in_next_line = True

    testfile.close()