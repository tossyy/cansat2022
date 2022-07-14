import picamera
import cv2
import numpy as np

class Camera:
    
    def __init__(self):
        self.camera = picamera.PiCamera()
        print('キャメラ初期化完了')
    
    def take_pic(self, file_path):
        self.camera.capture(file_path)

    def detect_center(self, file_path):
        img = cv2.imread(file_path) # 画像を読み込む
        
        height, width = img.shape[:2] # 画像のサイズを取得する

        hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV) # 色基準で2値化する

        # 色の範囲を指定する
        lower_color1 = np.array([0,127,0])
        upper_color1= np.array([30,255,255])

        lower_color2 = np.array([150,127,0])
        upper_color2 = np.array([179,255,255])

        # 指定した色に基づいたマスク画像の生成
        mask1 = cv2.inRange(hsv, lower_color1, upper_color1)
        mask2 = cv2.inRange(hsv, lower_color2, upper_color2)
        mask = mask1 + mask2

        # 非ゼロのピクセルが連続してできた領域を検出する
        nlabels, labels, stats, centroids = cv2.connectedComponentsWithStats(mask)

        #　画像の背景の番号は 0 とラベリングされているので、実際のオブジェクトの数は nlabels - 1 となる
        nlabels = nlabels - 1
        labels = np.delete(labels, obj=0, axis=0)
        stats = np.delete(stats, obj=0, axis=0)
        centroids = np.delete(centroids, obj=0, axis=0)
        percent = stats[:,4] / (height*width)

        max_index = np.argmax(percent)

        res = {}
        res['height'] = height
        res['width'] = width
        res['percent'] = percent[max_index]
        res['center'] = centroids[max_index]
        
        return percent[max_index], centroids[max_index]


