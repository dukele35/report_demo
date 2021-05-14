from report import *

# ------------------------------- #
##### input_true_classes(dir) #####
# ------------------------------- # 
def test_input_true_classes_type():
    # to test if the output is a dictionary
    assert type(input_true_classes('test')) is dict

def test_input_true_classes_inputformats():
    # to test if the input is in the right formats, i.e. .png, .jpeg or .jpg
    formats = [i.lower().endswith(('.png', '.jpg', '.jpeg')) for i in list(input_true_classes('test').keys())]
    assert all(formats) is True

def test_input_true_classes_inputduplication():
    # to test if any of the images in the input are duplicated with respect to filenames
    assert len(list(input_true_classes('test').keys())) == len(set(input_true_classes('test').keys()))

def test_inpt_true_classes_outputvalues():
    # to test if values of the output dictionary belong to the set of symptons, i.e. None, Mild, Moderate, Severe & Proliferative
    values = set(input_true_classes('test').values())
    test_set = {'None','Mild','Moderate','Severe','Proliferative'}
    assert values.issubset(test_set) is True 


# ------------------------------- #
### SHA256_hashing_images(dir) ####
# ------------------------------- # 
def test_SHA256_hashing_images_type():
    # to test if the output is a dictionary
    assert type(SHA256_hashing_images('test')) is dict

def test_SHA256_hashing_images_inputformats():
    # to test if the input is in the right formats, i.e. .png, .jpeg or .jpg
    formats = [i.lower().endswith(('.png', '.jpg', '.jpeg')) for i in list(SHA256_hashing_images('test').keys())]
    assert all(formats) is True

def test_SHA256_hashing_images_inputduplication():
    # to test if any of the images in the input are duplicated with respect to filenames
    assert len(list(SHA256_hashing_images('test').keys())) == len(set(SHA256_hashing_images('test').keys()))

def test_SHA256_hashing_images_outputduplication():
    # to test if any of the SHA256 in the output are duplicated 
    assert len(list(SHA256_hashing_images('test').values())) == len(set(SHA256_hashing_images('test').values()))


# ------------------------------- #
# inference_predictions(url,dir) ## NB. this function takes significantly more time to run than others 
# ------------------------------- # 
def test_inference_predictions():
    # since inference_predictions(url,dir) takes a lot of time to run
    # this test function contains different tests for inference_predictions(url,dir)
    out = inference_predictions('http://0.0.0.0:5000/predict','test')

    # to test if the output is a dictionary
    assert type(out) is dict

    # to test if the input is in the right formats, i.e. .png, .jpeg or .jpg
    formats = [i.lower().endswith(('.png', '.jpg', '.jpeg')) for i in list(out.keys())]
    assert all(formats) is True

    # to test if values of the dictionary output are also dictionaries
    value_list = [type(i) is dict for i in list(out.values())]
    assert all(value_list) is True 

    # to test if values of the dictionary output are the dictionaries having keys including 'prediction', 'true_class', 'pred_class', 'SHA256'
    check_subdict_keys = [set(i.keys()) == {'pred_class', 'prediction', 'true_class', 'SHA256'} for i in list(out.values())]
    assert all(check_subdict_keys) is True

    
