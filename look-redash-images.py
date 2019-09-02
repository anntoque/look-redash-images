import requests
from google.cloud import storage
from google.api_core.exceptions import from_http_response
import re

def get_docket_image_tags():
    result = requests.get(
        'https://registry.hub.docker.com/v2/repositories/redash/redash/tags/?page_size=10000',
        params={'pase_size':'100000'})
    
    result_json = result.json()
    tags = []

    for x in result_json['results']:
        tag_name = x['name']
        tags.append(tag_name)
    
    return tags

def find_disk_image(tags):
    client = storage.Client.from_service_account_json(
        './gcp-key.json')
    bucket = client.bucket('redash-images')

    gce_images = []

    for name in tags:
        # blob = storage.blob.Blob('redash.5.0.2-b5486-build2.tar.gz', bucket)
        if name.count('.') == 3:
            name = name[:5]+'-'+name[6:]
        else:
            pass

        blob = storage.blob.Blob('redash.'+name+'-build2.tar.gz', bucket)
        
        try:
            is_blob_check = blob.exists()
        except:
            is_blob_check = False
        
        print('redash.'+name+'-build2.tar.gz: '+str(is_blob_check))
        
        if is_blob_check is True:
            gce_images.append('redash.'+name+'-build2.tar.gz')
        else:
            pass
    
    return gce_images

if __name__ =='__main__':
    redas_tags = get_docket_image_tags()
    gce_redash_images = find_disk_image(redas_tags)
    
    for images in gce_redash_images:
        print(images)
