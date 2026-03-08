import cv2
import numpy as np
import os

# YOLO files path
yolo_dir = os.path.join("static", "css", "js", "yolo")
yolo_cfg = os.path.join(yolo_dir, "yolov4.cfg")
yolo_weights = os.path.join(yolo_dir, "yolov4.weights")
yolo_classes_file = os.path.join(yolo_dir, "classes.txt")

# Load class names
with open(yolo_classes_file, "r") as f:
    classes = [line.strip() for line in f.readlines()]

# Load YOLO model
net = cv2.dnn.readNet(yolo_weights, yolo_cfg)
layer_names = net.getLayerNames()
output_layers = [layer_names[i - 1] for i in net.getUnconnectedOutLayers().flatten()]

def detect_animals(image_path, conf_threshold=0.5, nms_threshold=0.4):
    """
    Detect animals in an image.
    
    Args:
        image_path (str): Path to image.
        conf_threshold (float): Minimum confidence to consider detection.
        nms_threshold (float): Threshold for non-max suppression.
    
    Returns:
        list: List of dicts with 'animal', 'x', 'y' coordinates.
    """
    img = cv2.imread(image_path)
    height, width = img.shape[:2]

    # Prepare blob
    blob = cv2.dnn.blobFromImage(img, 1/255.0, (608, 608), swapRB=True, crop=False)
    net.setInput(blob)
    outs = net.forward(output_layers)

    boxes = []
    confidences = []
    class_ids = []

    # Loop over each detection
    for out in outs:
        for detection in out:
            scores = detection[5:]
            class_id = np.argmax(scores)
            confidence = scores[class_id]
            if confidence > conf_threshold:
                center_x = int(detection[0] * width)
                center_y = int(detection[1] * height)
                w = int(detection[2] * width)
                h = int(detection[3] * height)
                x = int(center_x - w / 2)
                y = int(center_y - h / 2)

                boxes.append([x, y, w, h])
                confidences.append(float(confidence))
                class_ids.append(class_id)

    # Apply Non-Max Suppression
    indices = cv2.dnn.NMSBoxes(boxes, confidences, conf_threshold, nms_threshold)

    final_detections = []
    if len(indices) > 0:
        for i in indices.flatten():
            class_id = class_ids[i]
            if class_id < len(classes):
                final_detections.append({
                    'animal': classes[class_id],
                    'x': boxes[i][0] + boxes[i][2] // 2,
                    'y': boxes[i][1] + boxes[i][3] // 2
                })
            else:
                print(f"Warning: class_id {class_id} is out of range!")

    return final_detections