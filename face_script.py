import face_recognition
from shutil import copyfile
import os
import shutil
import glob
from PIL import Image
from tqdm import tqdm
from pathlib import Path

PATH = os.getcwd()

ALL_PHOTOS = PATH + "/all_photos/"
MY_PHOTOS = PATH + "/my_photos/"
MY_FOUND_PIC = PATH + "/my_found_pic/"
TEMP_FOLDER = PATH + "/tmp/"

"""This is the tolerance (or threshold) of the algorithm.
Higher tolerance tells the algorithm to be less strict, while lower means the opposite
"""
TOLARANCE = 0.5

print("Deleting old tmp images")

os.system('rm -rf %s/*,jpg' % TEMP_FOLDER)

print("Copying your images to tmp file\n")

for root, dirs, files in tqdm(os.walk(ALL_PHOTOS)):
    for file in files:
        if file.endswith(".jpg"):
            # print(os.path.join(root, file))
            shutil.copy2(os.path.join(root, file), TEMP_FOLDER)

file_count = len(os.listdir(TEMP_FOLDER))
print("You have " + str(file_count) + " pictures")

print("Resizing your pictures in tmp folder if bigger then 0.5 Mb")
# # Iterate through all your pictures
my_tmp_files = glob.glob(TEMP_FOLDER + "*.jpg")

for pic in tqdm(my_tmp_files):
    image = Image.open(pic)
    image_size = int(len(image.fp.read()))
    if image_size > 1000000:
        width, height = image.size
        quartersizedIm = image.resize((int(width / 2), int(height / 2)))
    quartersizedIm.save(pic.replace(".jpg", "-small.jpg"))
    os.remove(pic)

print("Deleting old my_found_pics")
#
os.system('rm -rf %s/*,jpg' % MY_FOUND_PIC)

print("Searching for your pics")
my_face_encoding = []

my_faces = glob.glob(MY_PHOTOS + "*.jpg")
# Create an encoding of my facial features that can be compared to other faces
for i in my_faces:
    picture_of_me = face_recognition.load_image_file(i)
    my_face_encoding.append(face_recognition.face_encodings(picture_of_me)[0])

my_tmp_files = glob.glob(TEMP_FOLDER + "*.jpg")

match_count = 0
for i in tqdm(my_tmp_files):
    # Construct the pictures name

    file_name = i
    # Load this picture
    new_picture = face_recognition.load_image_file(file_name)

    # Iterate through every face detected in the new picture
    for new_face_encoding in face_recognition.face_encodings(new_picture):

        # Run the algorithm of face comaprison for the detected face, with 0.5 tolerance
        for j, y in enumerate(my_face_encoding):
            results = face_recognition.compare_faces([y], new_face_encoding, TOLARANCE)
            print("comparing " + os.path.basename(file_name) + "    with:" + os.path.basename(my_faces[j]))
            # Save the image to a dedicated folder if there is a match
            if results[0]:
                print("Found one")
                match_count += 1
                copyfile(file_name, MY_FOUND_PIC + Path(file_name).name)
                break

print("We found " + str(match_count) + " of your pictures, find them in: " + MY_FOUND_PIC)
