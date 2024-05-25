```python
// import libs
import cv2
import numpy as np

// load YOLO model
net = cv2.dnn.readNet("yolov3.weights", "yolov3.cfg")
with open("coco.names", "r") as f:
    classes = [line.strip() for line in f.readlines()]

// get YOLO output layer name
layer_names = net.getLayerNames()
output_layers = [layer_names[i - 1] for i in net.getUnconnectedOutLayers()]

// init camera
cap = cv2.VideoCapture(0)

// check camera open or not
if not cap.isOpened():
    print error message
    exit

// Real-time detection cycle
while True:
    // Read frame from the camera
    ret, frame = cap.read()
    if not ret:
        print error message
        break

    // get image size
    height, width, channels = frame.shape

    // process image and prepare it for input into the YOLO network
    // convert images to a blob format suitable for the YOLO network
    blob = cv2.dnn.blobFromImage(frame, 0.00392, (416, 416), (0, 0, 0), True, crop=False)
    net.setInput(blob)
    // propagate forward to get the output of the YOLO network
    outs = net.forward(output_layers)

    // initialize results list
    class_ids = []
    confidences = []
    boxes = []

    // parse the yolo network output
  for each detection in outs:
    for each object in detection:
        scores = object[5:]
        class_id = np.argmax(scores)
        confidence = scores[class_id]

        // filter out low-confidence detections
        if confidence > 0.5:
            // Calculate the center coordinates and size of the object
            center_x = int(object[0] * width)
            center_y = int(object[1] * height)
            w = int(object[2] * width)
            h = int(object[3] * height)

            // calculate the top-left corner coordinates of the bounding box
            x = int(center_x - w / 2)
            y = int(center_y - h / 2)

            // add the detection result to the list
            boxes.append([x, y, w, h])
            confidences.append(float(confidence))
            class_ids.append(class_id)


    // max suppression removes duplicate detection
    indexes = cv2.dnn.NMSBoxes(boxes, confidences, 0.5, 0.4)

    // graph result
    for i in range(len(boxes)):
        if i in indexes:
            x, y, w, h = boxes[i]
            label = classes[class_ids[i]]
            confidence = confidences[i]
            color = (0, 255, 0)
            // add border and label in image
            cv2.rectangle(frame, (x, y), (x + w, y + h), color, 2)
            cv2.putText(frame, f"{label} {confidence:.2f}", (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 2)

    // show
    cv2.imshow("Image", frame)
    // check press "esc" button
    key = cv2.waitKey(1)
    if key == 27:
        break

// release camera and close windows
cap.release()
cv2.destroyAllWindows()
