#MODELO PRE ENTRENADO

import cv2 
import numpy as np 
import time

#importamos el modelo de yolo pre-entrenado
modelConfiguration = "C:\TFG deteccion de personas\darknet-master\cfg\yolov3-tiny.cfg" 
modelWeights = "C:\TFG deteccion de personas\darknet-master\cfg\yolov3-tiny.weights"
model = cv2.dnn.readNet("C:\TFG deteccion de personas\darknet-master\cfg\yolov3.weights", "C:\TFG deteccion de personas\darknet-master\cfg\yolov3.cfg" )

#ahora vamos a asignar los nombres de las clases pre-entrenadas 
classes = []
with open("C:\TFG deteccion de personas\darknet-master\data\coco.names", "r") as f:
    classes = [line.strip() for line in f.readlines()]

#sacamos os nombres de las capas 
layer_names = model.getLayerNames()
output_layers = [layer_names[i - 1] for i in model.getUnconnectedOutLayers()]
colors = np.random.uniform(0, 255, size = (len(classes), 3))

#ahora vamos a cargar la camara y aplicamos la deteccion de objetos
#para las pruebas he cargado videos 

#lee el video o la camara llamada
#camera = cv2.VideoCapture(0)
video = cv2.VideoCapture('aeropuerto.mp4')

font = cv2.FONT_HERSHEY_PLAIN
starting_time = time.time()
frame_id = 0

while True:
    #a, frame = camera.read()
    ret, frame = video.read()
    if ret == False: break #linea de error 
    frame_id += 1
    height, width, channels = frame.shape
    while True:
         #a, frame = camera.read()
        ret, frame = video.read()    
        frame_id += 1
        height, width, channels = frame.shape
        #deteccion de objetos 
        blob = cv2.dnn.blobFromImage(frame, 0.00392, (416, 416), (0, 0, 0), True, crop=False)
        model.setInput(blob)
        outs = model.forward(output_layers)
        #informacion de la pantalla
        class_ids = []
        confidences = []
        boxes = []
        for out in outs:    
            for detection in out:
                scores = detection[5:]
                class_id = np.argmax(scores)
                confidence = scores[class_id]
                if confidence > 0.2:
                    #deteccion de objeto
                    centerX = int(detection[0] * width)
                    centerY = int(detection[1] * height)
                    w = int(detection[2] * width)
                    h = int(detection[3] * height)
                    #defino las coordenadas del rectangulo que marca la deteccion
                    x = int(centerX - w/2)
                    y = int(centerY - h/2)
                    boxes.append([x, y, w, h])
                    confidences.append(float(confidence))
                    class_ids.append(class_id)
        #print("Cantidad de detecciones:", len(boxes))
        #print("Confianzas:", confidences)
        #print("Clases:", class_ids)
        
        indexs = cv2.dnn.NMSBoxes(boxes, confidences, 0.4, 0.3)
        #print("indices despues de NMS:", indexs)
        for i in range(len(boxes)):
            if i in indexs:
                #print("hola for")
                x, y, w, h = boxes[i]
                label = str(classes[class_ids[i]])
                confidence = confidences[i]
                color = colors[class_ids[i]]
                cv2.rectangle(frame, (x,y), (x+w, y+h), color, 2)
                cv2.rectangle(frame, (x, y), (x+w, y+30), color, -1)
                cv2.putText(frame, label + " " + str(round(confidence, 2)), (x, y+30), font, 2, (255, 255, 255), 1)

        #print("hola")
        elapsed_time = time.time() - starting_time
        fps = frame_id / elapsed_time
        cv2.putText(frame, "FPS: " + str(round(fps, 2)), (10, 50), font, 3, (0, 0, 0), 3)
        cv2.imshow('Laura', frame)


        if cv2.waitKey(30) & 0xFF == 27: break 

    video.release()
    cv2.destroyAllWindows()
        