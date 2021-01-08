import zipfile
import os
from os.path import basename

class ScormExtractor:

    def extractScorm(zip_file):
        # btn_select.config(state="disabled")
        with zipfile.ZipFile(zip_file, 'r') as zip_ref:
            extracted_scorm_path = zip_file[:-4]
            zip_ref.extractall(extracted_scorm_path)
            print("extracted_scorm_path: " + extracted_scorm_path + "/imsmanifest.xml")
            return extracted_scorm_path

    def zipScorm(file_path):
        with zipfile.ZipFile("Test-Zip-File", 'w') as zipObj:
            # Iterate over all the files in directory
            for folderName, subfolders, filenames in os.walk(file_path):
                for filename in filenames:
                    # create complete filepath of file in directory
                    file_path = os.path.join(folderName, filename)
                    # Add file to zip
                    zipObj.write(file_path, basename(file_path))

