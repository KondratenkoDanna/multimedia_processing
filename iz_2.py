from datetime import datetime
import cv2


def record_webcamera():
    cap = cv2.VideoCapture(1)
    cap.set(3, 640)
    cap.set(4, 480)
    frame_width = int(cap.get(3))
    frame_height = int(cap.get(4))
    frame_size = (frame_width, frame_height)
    out = cv2.VideoWriter('out.avi', cv2.VideoWriter_fourcc('M', 'J', 'P', 'G'), 20, frame_size)
    output = cv2.VideoWriter('output_video.avi', cv2.VideoWriter_fourcc('M', 'J', 'P', 'G'), 20, frame_size)
    ret, frame = cap.read()     # Читаем первый кадр
    dt = str(datetime.now())
    font = cv2.FONT_HERSHEY_SCRIPT_COMPLEX
    frame = cv2.putText(frame, dt, (10, 470), font, 0.8, (210, 155, 155), 4, cv2.LINE_8)
    gray_capture = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    blur_matr = 5
    sigma = 5
    new_frame = cv2.GaussianBlur(gray_capture, (blur_matr, blur_matr), sigma)
    while True:  # Цикл до завершения съемки видео
        old_frame = new_frame  # Скопировать старый кадр
        ret, frame = cap.read()  # Считываем новый кадр
        cv2.imshow('Take a video', frame)
        out.write(frame)
        if not ret:  # Eсли чтение неуспешно, остановить цикл
            break
        gray_capture = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)  # Перевести в черный белый цвет
        new_frame = cv2.GaussianBlur(gray_capture, (blur_matr, blur_matr), sigma)  # Свертка изображения с помощью фильтра Гаусса
        frame_dif = cv2.absdiff(old_frame, new_frame)  # Найти разницу между двумя кадрами в отдельный фрейм
        retval, frame_dif = cv2.threshold(frame_dif, 50, 127, cv2.THRESH_BINARY)  # Провести операцию двоичного разделения для фрейма
        contours, hier = cv2.findContours(frame_dif, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE) # Найти контуры объектов для фрейма
        for i in contours:  # Пройтись по контурам объектов для фрейма, найти контур площадью большей, чем наперед заданный параметр
            if 200 < cv2.contourArea(i):  # Если нашли
                output.write(frame)
                break
        if cv2.waitKey(1) & 0xFF == 27:
            break
    cap.release()
    out.release()
    output.release()
    cv2.destroyAllWindows()


def show_result():
    cap = cv2.VideoCapture(r'output_video.avi', cv2.CAP_ANY)
    cap.set(3, 640)
    cap.set(4, 480)
    try:
        while True:
            ret, frame = cap.read()
            cv2.imshow('Result', frame)
            if cv2.waitKey(1) & 0xFF == 27:
                break
    except:
        print("Video has ended.")
    cap.release()
    cv2.destroyAllWindows()


record_webcamera()
show_result()
