import zipfile

class ScormExtractor:

    def extractScorm(zip_file):
        # btn_select.config(state="disabled")
        with zipfile.ZipFile(zip_file, 'r') as zip_ref:
            global extracted_scorm_path
            extracted_scorm_path = zip_file[:-4]
            zip_ref.extractall(extracted_scorm_path)
            ims_manifest = extracted_scorm_path + "/imsmanifest.xml"
            print("extracted_scorm_path: " + ims_manifest)
            return ims_manifest
