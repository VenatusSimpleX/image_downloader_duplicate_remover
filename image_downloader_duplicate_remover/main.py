import requests
import shutil
from PIL import Image
import imagehash
import os

# Put your list of image links here
TARGETS = []


def main():
    downloaded = []
    # Download all images
    for i in range(len(TARGETS)):
        print('Downloading images: {}'.format(
            displayProgress(i + 1, len(TARGETS))), end='\r')
        url = TARGETS[i]
        response = requests.get(url, stream=True)

        # Rename to standardized format
        new_filename = 'thumb-{:02d}.jpg'.format(i + 1)

        with open('downloaded/{}'.format(new_filename), 'wb') as out_file:
            shutil.copyfileobj(response.raw, out_file)

        downloaded.append(new_filename)

        del response
    print()

    # Compare each image with each other based on downloaded list
    cutoff = 5
    for i in range(len(downloaded) - 1):
        print('Checking images: {}'.format(
            displayProgress(i + 1, len(downloaded) - 1)), end='\r')

        # Bypass the checking if is duplicate
        if "_" in downloaded[i]:
            continue

        hash_i = imagehash.average_hash(Image.open(
            'downloaded/{}'.format(downloaded[i])))
        for j in range(i + 1, len(downloaded)):
            hash_j = imagehash.average_hash(Image.open(
                'downloaded/{}'.format(downloaded[j])))

            if hash_i - hash_j < cutoff:
                path = 'downloaded/'
                original_file = downloaded[j]
                new_file = '{}_SAME AS {}'.format(downloaded[j], downloaded[i])
                os.rename(path + original_file, path + new_file)

                downloaded[j] = new_file
    print()


def displayProgress(current, limit):
    return '{}/{} ({:.2f}%)'.format(current, limit, current / limit * 100)


main()
print('Done')
