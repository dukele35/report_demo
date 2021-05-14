from report import inference_predictions

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