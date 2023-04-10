# creating mupltiple directories using list
import os
folder_name = ['P', 'Q', 'K', 'B', 'N', 'R']
try:
    for i in folder_name:
        path = os.path.join(os.getcwd(), i)
        os.mkdir(path)
except OSError:
    print("Creation of the directory %s failed" % path)
