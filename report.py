import subprocess
import os
import pandas as pd
import requests
import base64
import json
import hashlib
from sklearn.metrics import confusion_matrix
import numpy as np
import time

def command_operation(command_line):
    '''
    Input: 
        - a string of a command line put in terminal
    Output:
        - run that command line in terminal
    '''
    command = command_line.split()
    return subprocess.run(command, stdout=subprocess.DEVNULL)

def id_running_docker():
    '''
    Input: None
    Output: docker id of the running docker containers
    '''
    docker_id = subprocess.run(["docker", "ps", "-q"], capture_output=True, text=True).stdout
    docker_id = docker_id.replace("\n", "")
    return docker_id

def input_true_classes(dir):
    '''
    Input:
        - directory path contains images in .png, .jpg and .jpeg formats
          e.g. directory
                   ├── image1.png                      
                   └── image2.png   
    Output:
        - a dictionary having keys as file names and values as their true labels/classes including None, Mild, Moderate, Severe & Proliferative
          e.g. {'image1.png': 'Mild', 'image2.png':'Moderate'}
    '''
    true_dict = {}
    for filename in os.listdir(dir):
        if filename.lower().endswith(('.png', '.jpg', '.jpeg')): 
            key = filename.split('_')[0]
            if key == '0':
                true_dict[filename] = 'None'
            if key == '1':
                true_dict[filename] = 'Mild'
            if key == '2':
                true_dict[filename] = 'Moderate'
            if key == '3':
                true_dict[filename] = 'Severe'
            if key == '4':
                true_dict[filename] = 'Proliferative'
    return true_dict

def SHA256_hashing_images(dir):
    '''
    Input:
        - directory path contains images in .png, .jpg and .jpeg formats
          e.g. directory
                   ├── image1.png                      
                   └── image2.png   
    Output:
        - A dictionary has keys as file names and values as SHA 256 hashing
          e.g. {'image1.png': '4539ske2304202...', 'image2.png': '567d4c23567891...'} 
    '''
    hash_dict = {}
    for filename in os.listdir(dir):
        if filename.lower().endswith(('.png', '.jpg', '.jpeg')):
            sha256_hash = hashlib.sha256()
            with open(os.path.join('test', filename), "rb") as f:
                for byte_block in iter(lambda: f.read(4096),b""):
                    sha256_hash.update(byte_block)
                result = sha256_hash.hexdigest()
                hash_dict[filename] = result
    return hash_dict

def inference_predictions(url,dir):
    '''
    Input:
        - url: the endpoint to get an image then to produce a prediction
          e.g. http://SERVICE.URL:8000/prediction 
        - dir: the folder path contains images
          e.g. directory
                   ├── image1.png                      
                   └── image2.png 
    Output: 
        - a dictionary has values as file names and keys as sub-dictionaries as follows:
          e.g. {'image1.png':
                    {'prediction': {'None': 0.1, 'Mild':0.2, 'Moderate':0.3, 'Severe':0.2, 'Proliferative':0.2},
                     'true_class': 'Mild',
                     'pred_class': 'Moderate',
                     'SHA256': '4539ske2304202...'}, 
                'image2.png':
                    {'prediction': {'None': 0.05, 'Mild':0.15, 'Moderate':0.3, 'Severe':0.25, 'Proliferative':0.25},
                     'true_class': 'Moderate',
                     'pred_class': 'Moderate',
                     'SHA256': '567d4c23567891...'}}
    '''
    dic_results = {}
    for filename in os.listdir(dir):
        if filename.lower().endswith(('.png', '.jpg', '.jpeg')): 
            with open(os.path.join(dir,filename), 'rb') as file:
                encod = base64.b64encode(file.read())
                req_file = encod.decode('utf-8')
            files = {'image': req_file}
            data = json.dumps(files)
            res = requests.post(url, data=data)
            dic_results[filename] = res.json()
            dic_results[filename]['true_class'] = input_true_classes(dir)[filename]
            dic_results[filename]['pred_class'] = max(dic_results[filename]['prediction'], key=dic_results[filename]['prediction'].get)
            dic_results[filename]['SHA256'] = SHA256_hashing_images(dir)[filename]
    return dic_results

def sen_spec(dic):
    '''
    Input:
        - a dictionary has values as file names and keys as sub-dictionaries as follows:
          e.g. {'image1.png':
                    {'prediction': {'None': 0.1, 'Mild':0.2, 'Moderate':0.3, 'Severe':0.2, 'Proliferative':0.2},
                     'true_class': 'Mild',
                     'pred_class': 'Moderate',
                     'SHA256': '4539ske2304202...'}, 
                'image2.png':
                    {'prediction': {'None': 0.05, 'Mild':0.15, 'Moderate':0.3, 'Severe':0.25, 'Proliferative':0.25},
                     'true_class': 'Moderate',
                     'pred_class': 'Moderate',
                     'SHA256': '567d4c23567891...'}}
    Output:
        - a dictionary has keys as classes, i.e. None, Mild, Moderate, Severe and Proliferative, 
          and values as sub-dictionaries of the sensitivity and specificity measurements for those classes
          e.g. {'None':{'sensivitity':0.6, 'specificity':0.7}, 
                'Mild':{'sensivitity':0.9, 'specificity':1}, 
                'Moderate':{'sensivitity':0.2, 'specificity':0.4},
                'Severe':{'sensivitity':0.6, 'specificity':0.5},
                'Proliferative':{'sensivitity':0.8, 'specificity':0.5}}
    '''
    df = pd.DataFrame(columns=['id', 'true_class', 'pred_class'])
    for filename in dic:
        row = pd.Series({'id':filename, 'true_class':dic[filename]['true_class'], 'pred_class':dic[filename]['pred_class']})
        df = df.append(row, ignore_index=True)
    cm = confusion_matrix(df['true_class'], df['pred_class'], labels=['None', 'Mild', 'Moderate', 'Severe', 'Proliferative'])
    index = {'None':0, 'Mild':1, 'Moderate':2, 'Severe':3, 'Proliferative':4}
    performance = {}
    for key in index.keys():
        tp = cm[index[key], index[key]]
        fn = sum(np.delete(cm[index[key],:], index[key]))
        fp = sum(np.delete(cm[:,index[key]], index[key]))
        tn = sum(sum(np.delete(np.delete(cm, index[key], 0), index[key], 1)))
        sensitivity = tp / (tp + fn)
        specificity = tn / (tn + fp)
        performance[key] = {'sensitivity':sensitivity, 'specificity':specificity}
    return performance

def json_outputing(dic, filename):
    '''
    Input:
        - dic: a dictionary
        - filename: a desired filemane for exporting
    Output:
        - the filename is saved in .json format in the working directory
    '''
    js = json.dumps(dic)
    with open(filename, 'w') as outfile:
        json.dump(js, outfile)
    print(f'- {filename}       is exported')
    return None

if __name__== "__main__":
    # Step 1. spin up the docker container
    command_operation('docker run -d -p 5000:5000 dukele35/drmvp1:1.0')

    # Step 2. Assigning the url and directory containing images
    url = 'http://0.0.0.0:5000/predict'   # remove this from this 
    dir = 'test/'

    # Step 3. Getting predictions for images in dir
    time.sleep(3)   # NB. There has yet to be a better option to check if container is running. Therefore, this method is still used. 
    dic_results = inference_predictions(url=url, dir=dir)

    # Step 4. Measuring performance for classes including None, Mild, Moderate, Severe & Proliferative
    dic_performance = sen_spec(dic=dic_results)

    # Step 5. Exporting .json reports
    json_outputing(dic=dic_results, filename='report_per_image.json')
    json_outputing(dic=dic_performance, filename='report_performance.json')

    # Step 6. stop docker container
    docker_id = id_running_docker()
    command_operation('docker kill ' + docker_id)
    print('\nExecution is done\n')