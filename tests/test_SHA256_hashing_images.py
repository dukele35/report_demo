from report import SHA256_hashing_images

def test_SHA256_hashing_images():
    hashed_imgs = SHA256_hashing_images('test')
    check_images_type(hashed_imgs)
    check_input_formats(hashed_imgs)
    check_input_duplication(hashed_imgs)
    check_output_duplication(hashed_imgs)

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

def check_output_duplication(hashed_imgs):
    # to test if any of the SHA256 in the output are duplicated 
    assert len(list(hashed_imgs.values())) == len(set(hashed_imgs.values()))
