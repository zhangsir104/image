from hashlib import md5


# image page to md5
def image_to_md5(image):
    m = md5()
    m.update(image)
    img_md5 = m.hexdigest()
    return img_md5