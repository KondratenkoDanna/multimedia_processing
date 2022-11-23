import cv2
import numpy as np


def print_video():
    cap = cv2.VideoCapture('/Users/danna_fely/Documents/фоточки/2022-09-17 11.50.31.mp4', cv2.CAP_ANY)
    w = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    h = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    fourcc = cv2.VideoWriter_fourcc(*'XVID')
    video_writer = cv2.VideoWriter("output.mov", fourcc, 30, (w, h))

    ret, frame = cap.read()
    cur_gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    cur_blur = cv2.GaussianBlur(cur_gray, (11, 11), 11)

    while True:
        ret, frame = cap.read()
        if not(ret):
            break
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        blur = cv2.GaussianBlur(gray, (11, 11), 11)
        absdiff = cv2.absdiff(cur_blur, blur)

        thresh = cv2.threshold(absdiff, 0, 255, cv2.THRESH_BINARY)

        cv2.imshow('frame', thresh)
        # video_writer.write(blur)
        if cv2.waitKey(16) & 0xFF == 27:
            break
    cap.release()
    cv2.destroyAllWindows()


print_video()