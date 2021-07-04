import firebase_admin
#from google.cloud import storage
from firebase_admin import credentials
from firebase_admin import storage
from firebase_init import get_bucket
import tempfile
import os

def upload_images(request):
    image_res = request.args.get('image_res')
    image_guid = request.args.get('image_guid')
    production = request.args.get('production')
    image_bytes = request.get_data()

    image_file_path = _write_image_to_temp_file(image_bytes, image_guid)
    image_bolb_path = _get_image_blob_path(production, image_guid, image_res)

    _copy_local_file_to_bucket(image_file_path, image_bolb_path)
    _copy_local_file_to_bucket(image_file_path, 'never-fetch/'+ image_bolb_path)


def _copy_local_file_to_bucket(local_file_path, image_bolb_path):
    myblob = get_bucket().blob(image_bolb_path)
    myblob.upload_from_filename(local_file_path)

def _get_image_blob_path(production, image_guid, image_res):
    production_folder = 'debug/'
    if production == 'yes':
        production_folder = 'production/'

    if (image_res == 'regular'):
        production_folder += 'images/'
    else:
        production_folder += 'high-res-images/'
    
    return production_folder + image_guid
    

def _write_image_to_temp_file(image_bytes, image_guid):
    image_file = tempfile.gettempdir() + '/' + image_guid
    f = open(image_file, "wb")
    f.write(image_bytes)
    f.close()
    return image_file


