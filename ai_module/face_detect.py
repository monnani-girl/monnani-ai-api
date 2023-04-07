import numpy as np
import argparse
import cv2

PROTOTXT = 'ai_module/model/deploy.prototxt.txt'
MODEL = 'ai_module/model/res10_300x300_ssd_iter_140000.caffemodel'

def detect_faces(img_path):
    print("[INFO] loading model...")
    net = cv2.dnn.readNetFromCaffe(PROTOTXT, MODEL)

    image = cv2.imread(img_path)
    (h, w) = image.shape[:2]
    blob = cv2.dnn.blobFromImage(cv2.resize(image, (300, 300)), 1.0,
        (300, 300), (104.0, 177.0, 123.0))

    # pass the blob through the network and obtain the detections and
    # predictions
    print("[INFO] computing object detections...")
    net.setInput(blob)
    detections = net.forward()[0][0]
    faces = []

    for detection in detections:
        if detection[2] < 0.75:
            continue
        box = detection[3:7] * np.array([w, h, w, h])
        (startX, startY, endX, endY) = box.astype("int")
        faces.append({
            'startX' : startX,
            'startY' : startY,
            'endX' : endX,
            'endY' : endY
        })

    return image, faces

def save(image):
    
    image_gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    gray_result = "./img_data/out_img/detect_src_face.jpg"
    cv2.imwrite(gray_result, image_gray)


if __name__=='__main__':
    image, faces = detect_faces('./data/pumpkin.jpg')
    if len(faces) == 0:
        print('아무 얼굴도 탐지되지 않았습니다. 정면 사진을 넣어주세요.')
        exit()
    if len(faces) != 1:
        print('너무 많은 얼굴이 탐지되었습니다. 정확히 한 명만 나온 사진을 넣어주세요.')
        exit()
    face = faces[0]
    image = image[face['startY'] : face['endY'], face['startX'] : face['endX']]
    save(image)