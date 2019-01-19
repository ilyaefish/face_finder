import face_recognition
from shutil import copyfile

# Create an encoding of my facial features that can be compared to other faces
picture_of_me = face_recognition.load_image_file("mavrodis.jpg")
my_face_encoding = face_recognition.face_encodings(picture_of_me)[0]

# Iterate through all the 10,460 pictures
for i in range(1, 10461):
    # Construct the picture name and print it
    file_name = str(i).zfill(5) + ".jpg"
    print(file_name)

    # Load this picture
    new_picture = face_recognition.load_image_file(file_name)

    # Iterate through every face detected in the new picture
    for face_encoding in face_recognition.face_encodings(new_picture):

        # Run the algorithm of face comaprison for the detected face, with 0.5 tolerance
        results = face_recognition.compare_faces([my_face_encoding], face_encoding, 0.5)

        # Save the image to a seperate folder if there is a match
        if results[0] == True:
            copyfile(file_name, "/home/deeplearning/Desktop/my_face/mavrodis/" + file_name)