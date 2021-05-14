from report import input_true_classes

def test_input_true_classes():
    hashed_imgs = input_true_classes('test')
    check_images_type(hashed_imgs)
    check_input_formats(hashed_imgs)
    check_input_duplication(hashed_imgs)
    check_output_values(hashed_imgs)

def check_images_type(hashed_imgs):
    # to test if the output is a dictionary
    assert type(hashed_imgs) is dict

def check_input_formats(hashed_imgs):
    # to test if the input is in the right formats, i.e. .png, .jpeg or .jpg
    formats = [i.lower().endswith(('.png', '.jpg', '.jpeg')) for i in list(hashed_imgs.keys())]
    assert all(formats) is True

def check_input_duplication(hashed_imgs):
    # to test if any of the images in the input are duplicated with respect to filenames
    assert len(list(hashed_imgs.keys())) == len(set(hashed_imgs.keys()))

def check_output_values(hashed_imgs):
    # to test if values of the output dictionary belong to the set of symptons, i.e. None, Mild, Moderate, Severe & Proliferative
    values = set(hashed_imgs.values())
    test_set = {'None','Mild','Moderate','Severe','Proliferative'}
    assert values.issubset(test_set) is True
