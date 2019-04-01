"""
Script to teach classificationbox image classes as described in
https://blog.machinebox.io/how-anyone-can-build-a-machine-learning-image-classifier-from-photos-on-your-hard-drive-very-5c20c6f2764f
https://github.com/machinebox/toys/blob/master/imgclass/main.go
Run from within the root folder containing the folders of images.
"""
import os
import requests

IP = 'localhost'
PORT = '8080'
CLASSIFIER = 'classificationbox'
VALID_FILETYPES = ('.jpg', '.png', '.jpeg')
MODEL_NUM = 'classificationbox_model_num'
TEACH_URL = f"http://{IP}:{PORT}/{CLASSIFIER}/models/{MODEL_NUM}/teach"
HEALTH_URL = f"http://{IP}:{PORT}/readyz"


def check_classifier_health():
    """Check that classifier is reachable"""
    try:
        response = requests.get(HEALTH_URL)
        if response.status_code == 200:
            print("{} health-check passed".format(CLASSIFIER))
            return True
        else:
            print("{} health-check failed".format(CLASSIFIER))
            print(response.status_code)
            return False
    except requests.exceptions.RequestException as exception:
        print("{} is unreachable".format(CLASSIFIER))
        print(exception)


def list_folders(directiory='.'):
    """Returns a list of folders in a dir, defaults to current dir.
    These are not full paths, just the folder."""
    folders = [dir for dir in os.listdir(directiory)
               if os.path.isdir(os.path.join(directiory, dir))
               and not dir.startswith(directiory)
               and not dir.startswith('.')]
    folders.sort(key=str.lower)
    print("Folders found:")
    print(folders)
    return folders


def teach_name_by_file(teach_url, name, file_path):
    """Teach facebox a single name using a single file."""
    file_name = file_path.split("/")[-1]
    file = {'file': open(file_path, 'rb')}
    data = {'name': name, "id": file_name}

    response = requests.post(teach_url, files=file, data=data)

    if response.status_code == 200:
        print("File:{} taught with name:{}".format(file_name, name))
        return True

    elif response.status_code == 400:
        print("Teaching of file:{} failed with message:{}".format(
            file_name, response.text))
        return False

    elif response.status_code == 404:
        print("Teaching of file:{} failed due to :{}".format(
            file_name, response.text))
        return False

def main():
    if check_classifier_health():
        for folder_name in list_folders():
            folder_path = os.path.join(os.getcwd(), folder_name)
            print(f"Entering folder {folder_path}")
            for file in os.listdir(folder_path):
                
                if file.endswith(VALID_FILETYPES):
                    file_path = os.path.join(folder_path, file)
                    print(file_path)
                    teach_name_by_file(teach_url=TEACH_URL,
                                       name=folder_name,
                                       file_path=file_path)


if __name__ == '__main__':
    main()
