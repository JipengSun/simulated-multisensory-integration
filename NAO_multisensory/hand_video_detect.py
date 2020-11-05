import cv2
import numpy as np

net = cv2.dnn.readNetFromDarknet(
    "/Users/Jipeng/PycharmProjects/simulated_multisensory_integration/NAO_multisensory/yolov3-tiny.cfg",
    "/Users/Jipeng/PycharmProjects/simulated_multisensory_integration/NAO_multisensory/yolo/weights/yolov3-tiny_150000.weights")
layer_names = net.getLayerNames()
output_layers = [layer_names[i[0] - 1] for i in net.getUnconnectedOutLayers()]
classes = [line.strip() for line in
           open("/Users/Jipeng/PycharmProjects/simulated_multisensory_integration/NAO_multisensory/yolo/obj.names")]
colors = [(0, 0, 255), (255, 0, 0), (0, 255, 0)]


def yolo_detect(frame):
    # forward propogation
    img = cv2.resize(frame, None, fx=0.4, fy=0.4)
    height, width, channels = img.shape
    blob = cv2.dnn.blobFromImage(img, 1 / 255.0, (416, 416), (0, 0, 0), True, crop=False)
    net.setInput(blob)
    outs = net.forward(output_layers)

    # get detection boxes
    class_ids = []
    confidences = []
    boxes = []

    for out in outs:
        for detection in out:
            tx, ty, tw, th, confidence = detection[0:5]
            scores = detection[5:]
            class_id = np.argmax(scores)
            if confidence > 0.3:
                center_x = int(tx * width)
                center_y = int(ty * height)
                w = int(tw * width)
                h = int(th * height)

                # 取得箱子方框座標
                x = int(center_x - w / 2)
                y = int(center_y - h / 2)
                boxes.append([x, y, w, h])
                confidences.append(float(confidence))
                class_ids.append(class_id)

    # draw boxes
    indexes = cv2.dnn.NMSBoxes(boxes, confidences, 0.3, 0.4)
    font = cv2.FONT_HERSHEY_SIMPLEX
    for i in range(len(boxes)):
        if i in indexes:
            x, y, w, h = boxes[i]
            label = str(classes[class_ids[i]])
            color = colors[class_ids[i]]
            cv2.rectangle(img, (x, y), (x + w, y + h), color, 2)
            cv2.putText(img, label, (x, y + 15), font, 0.5, color, 2)
    return img



import cv2
import imutils

video_path = '/Users/Jipeng/PycharmProjects/simulated_multisensory_integration/NAO_multisensory/sample_video.avi'
VIDEO_IN = cv2.VideoCapture(video_path)

while True:
    hasFrame, frame = VIDEO_IN.read()

    img = yolo_detect(frame)
    cv2.imshow("Frame", imutils.resize(img, width=850))

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

VIDEO_IN.release()
cv2.destroyAllWindows()