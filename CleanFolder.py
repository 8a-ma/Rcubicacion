import os
import glob

def CleanFolder(path):
    files = glob.glob(os.path.join(path, "*"))
    [os.remove(f) for f in files]
    print("Clean Folder's Success")