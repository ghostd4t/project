import cv2

top, right, bottom, left = 10, 450+10, 360+10, 10  # Sample values.


input_video = cv2.VideoCapture('Sample_Vid.mp4')

fourcc = cv2.VideoWriter_fourcc(*'XVID')
output_movie = cv2.VideoWriter('videoPrueba.avi', fourcc, 30, (450, 360))

while True:
    ret, frame = input_video.read()

    if not ret:
        break

    # Following crop assumes the video is colored,
    # in case it's Grayscale, you may use: crop_img = frame[top:bottom, left:right]
    crop_img = frame[top:bottom, left:right, :]

    output_movie.write(crop_img)


# Closes the video writer.
output_movie.release()