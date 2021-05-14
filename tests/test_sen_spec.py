from report import sen_spec, inference_predictions

def test_sen_spec():
    out = inference_predictions('http://0.0.0.0:5000/predict','test')
    performance = sen_spec(out)
    check_output_type(performance)
    check_output_keys(performance)
    check_output_values_type(performance)

def check_output_type(performance):
    # to test if the output is a dictionary
    assert type(performance) is dict

def check_output_keys(performance):
    # to test if keys of the dictionary output include None, Mild, Moderate, Severe, Proliferative
    keys = set(performance.keys())
    test_keys = {'None','Mild','Moderate','Severe','Proliferative'}
    assert keys == test_keys

def check_output_values_type(performance):
    # to test if values of the dictionary output are dictionaries 
    check = [type(i) is dict for i in performance.values()]
    assert all(check) is True