#deteccion de movimiento en ciertos puntos de la imagen
#de momento solo detecta en caso de que haya algun movimiento


import cv2 #importo openCV
import numpy as np

#primero visualizo el video
video = cv2.VideoCapture('dron3.mp4')

#sacamos el fondo 
#usando esto hacemos que el objeto que se mueve se vea en blanco el fondo en negro
#esto hara mas facil la diferenciacion de los que se mueve y lo que no
fondo = cv2.bgsegm.createBackgroundSubtractorMOG()

#el kernel lo usamos para mejorar la imagen cuando la tenemos en forma binaria
kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE,(3,3))

#leo el video frame por frame usando imshow
while True: 
    
    ret, frame = video.read()
    
    if ret == False: break #linea de error 
    
    #para facilitar el background la imagen la pasamos a escala de grises
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    
    #vamos a poner una marca para saber si ya se ha detectado movimiento o no 
    #en caso de que no se haya detectado aparecera un rectangulo de color negro
    #y el mensaje de que todavia no se ha detectado movimiento
    
    #cv2.rectangle(frame,(0,0),(frame.shape[1],40),(0,0,0),-1)
    color = (0, 255, 0)
    #detector = "Todavia no se ha detectado movimiento"
  
    #--------------------------------------------------------------------------
    #especificacion del cuadrado donde se detecta el movimiento
    # 1. Especifico los puntos del frame donde voy a detectar el movimiento
    zona = np.array([[0,0], [640,0], [640,frame.shape[0]], [0,frame.shape[0]]])
    
    # 2. Vamos a marcar el contorno de la zona que vamos a analizar con un drawContours
    cv2.drawContours(frame, [zona], -1, color, 2)
    

    # 3. Ahora vamos a crear una imagen auxiliar que nos va a ayudar despues
    #    a poder determianr el area en el que va a estar el detector  
    ima_aux = np.zeros(shape=(frame.shape[:2]), dtype=np.uint8) #matriz de ceros
    ima_aux = cv2.drawContours(ima_aux, [zona], -1, (255), -1) #imagen binaria que se muestra en blanco
    ima_area = cv2.bitwise_and(gray, gray, mask=ima_aux) #vemos el trozo de imagen que corresponde a esa parte en escala de grises
 
    # 4. Por ultimo, sacamos el fondo donde esta la imagen binaria que hemos marcado de color blanco     
    fondo_mask = fondo.apply(ima_area)
	#para limpiar la imagen del posible ruido que haya hacemos lo siguiente
    fondo_mask = cv2.morphologyEx(fondo_mask, cv2.MORPH_OPEN, kernel)
    fondo_mask = cv2.dilate(fondo_mask, None, iterations=2)
    
    # 5. Filtramos los contornos de acuerdo con sus areas 
    #    luego analizamos cada uno de los contornos detectados:
    contornos = cv2.findContours(fondo_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)[0]
    for contornos in contornos:
        if cv2.contourArea(contornos) > 150 and cv2.contourArea(contornos) < 400: #lo entiende como que hay un movimiento
            x, y, w, h = cv2.boundingRect(contornos) #sacamos los valores de ancho altura..
            cv2.rectangle(frame, (x,y), (x+w, y+h),(0,255,0), 2)
            #detector = "Se ha Detectado Movimiento!"
            #color = (0, 0, 255)
      
      
    #para poder ver el texto usamos la siguiente funcion de OpenCV
    #cv2.putText(frame, detector, (10,30), cv2.FONT_HERSHEY_TRIPLEX, 1, color, 1)
    
    cv2.imshow('frame', frame)
   #cv2.imshow('ima_aux', ima_aux)
    
    i = cv2.waitKey(30) & 0xFF
    if i == 27: break 

video.release()
cv2.destroyAllWindows()