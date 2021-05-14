from report import inference_predictions

def test_input_true_classes():
    out = inference_predictions('http://0.0.0.0:5000/predict','test')
    check_input_formats(out)
    check_input_duplication(out)
    check_output_type(out)
    check_output_values(out)
    check_output_values_keys(out)
    
def check_input_formats(out):
    # to test if the input is in the right formats, i.e. .png, .jpeg or .jpg
    formats = [i.lower().endswith(('.png', '.jpg', '.jpeg')) for i in list(out.keys())]
    assert all(formats) is True

def check_input_duplication(out):
    # to test if any of the images in the input are duplicated with respect to filenames
    assert len(list(out.keys())) == len(set(out.keys()))

def check_output_type(out):
    # to test if the output is a dictionary
    assert type(out) is dict

def check_output_values(out):
    # to test if values of the dictionary output are also dictionaries
    value_list = [type(i) is dict for i in list(out.values())]
    assert all(value_list) is True

def check_output_values_keys(out):
    # to test if values of the dictionary output are the dictionaries having keys including 'prediction', 'true_class', 'pred_class', 'SHA256'
    check_subdict_keys = [set(i.keys()) == {'pred_class', 'prediction', 'true_class', 'SHA256'} for i in list(out.values())]
    assert all(check_subdict_keys) is True