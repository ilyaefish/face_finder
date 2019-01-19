import face_recognition
from shutil import copyfile
import os
import shutil

import subprocess

PATH = os.getcwd()

ALL_PHOTOS = PATH + "/all_photos/"
MY_PHOTOS = PATH + "/my_photos/"
MY_FOUND_PIC = PATH + "/my_found_pic/"
TEMP_FOLDER = PATH + "/tmp/"
# This is the tolerance (or threshold) of the algorithm. Higher tolerance tells the algorithm to be less strict, while lower means the opposite
TOLARANCE = 0.7
YOUR_FACE_PIC = MY_PHOTOS + "ilya.jpg"

# copy all jpg files to tmp folder
for root, dirs, files in os.walk(ALL_PHOTOS):
    for file in files:
        if file.endswith(".jpg"):
            # print(os.path.join(root, file))
            shutil.copy2(os.path.join(root, file), TEMP_FOLDER)

print("Rename tmp files")
cmd = "./rename_tmp_files.sh"

results = subprocess.run(
    cmd, shell=True, universal_newlines=True, check=True)
print(results.stdout)

my_face_encoding = []


my_faces = glob.glob(MY_PHOTOS + "*.jpg")
# Create an encoding of my facial features that can be compared to other faces
for i in my_faces:
    picture_of_me = face_recognition.load_image_file(YOUR_FACE_PIC)
    my_face_encoding.append(face_recognition.face_encodings(picture_of_me)[0])

file_count = len(os.listdir(TEMP_FOLDER))

# # Iterate through all your pictures
for i in range(1, file_count):
    # Construct the picture name and print it
    file_name = TEMP_FOLDER + str(i).zfill(5) + ".jpg"
    print(file_name)

    # Load this picture
    new_picture = face_recognition.load_image_file(file_name)

    # Iterate through every face detected in the new picture
    for face_encoding in face_recognition.face_encodings(new_picture):

        # Run the algorithm of face comaprison for the detected face, with 0.5 tolerance
        for y in my_face_encoding:
            results = face_recognition.compare_faces([y], face_encoding, TOLARANCE)

            # Save the image to a seperate folder if there is a match
            if results[0] == True:
                print("Found one")
                copyfile(file_name, MY_FOUND_PIC + str(i) + ".jpg")
                break
