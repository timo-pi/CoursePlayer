import zipfile
import os
from os.path import basename

class ScormExtractor:

    """    def createFolder(directory):
            try:
                if not os.path.exists(directory):
                    os.makedirs(directory)
            except OSError:
                print('Warning: Directory already exists: ' + directory)"""

"""    def extractScorm(zip_file):
        # btn_select.config(state="disabled")
        with zipfile.ZipFile(zip_file, 'r') as zip_ref:

            # create /temp folder
            filename = os.path.basename(zip_file)
            dirname = os.path.dirname(zip_file)
            extract_path = os.path.join(dirname, 'temp', filename)
            extracted_scorm_path = extract_path[:-4]

            zip_ref.extractall(extracted_scorm_path)
            print("extracted_scorm_path: " + extracted_scorm_path + "/imsmanifest.xml")
            return extracted_scorm_path"""
