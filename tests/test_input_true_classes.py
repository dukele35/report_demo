from report import input_true_classes

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