import cv2
import support
import numpy as np
import math

img_original = cv2.imread("/home/havo/autograding/wep-app-autograding/phieu.png")

width_origin, height_origin = img_original.shape[1], img_original.shape[0]
cap = cv2.VideoCapture(0)
while True:
    success,frame = cap.read()
    if success:
        width_frame, height_frame = frame.shape[1], frame.shape[0]
        width_img = (width_origin * height_frame) // height_origin
        width_frame2 = width_frame // 2
        width_img2 = width_img // 2
        x1 = width_frame2 - width_img2
        x2 = width_frame2 + width_img2
        y1 = 0
        y2 = height_frame
        frame2 = frame.copy()
        cv2.rectangle(frame2,(x1,y1),(x1+100,y1+100),(0,255,0),2)
        cv2.rectangle(frame2,(x2-100,y1),(x2,y1+100),(0,255,0),2)
        cv2.rectangle(frame2,(x1,y2-100),(x1+100,y2),(0,255,0),2)
        cv2.rectangle(frame2,(x2-100,y2-100),(x2,y2),(0,255,0),2)

        img_gray = cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)
        img_blur = cv2.GaussianBlur(img_gray,(5,5),2)
        img_canny = cv2.Canny(img_blur,100,200)

        cnt,_ = cv2.findContours(img_canny,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_NONE)
        ListCon = []
        for c in cnt:
            area = cv2.contourArea(c)
            if area > 100:
                peri = cv2.arcLength(c,True)
                approx = cv2.approxPolyDP(c,peri*0.02,True)
                if len(approx) == 4 or len(approx) == 5:
                    ListCon.append(c)
        cv2.drawContours(frame2,ListCon,-1,(0,255,0),2)

        if len(ListCon) == 6:
            for i in range(len(ListCon)):
                corn = support.get_corn(ListCon[i])
                corn = np.array(corn)
                x = support.rearrage_point(corn)
                new_points = [[],[],[],[]]
                new_points[0] = corn[x[0][0]]
                new_points[1] = corn[x[1][0]]
                new_points[2] = corn[x[2][0]]
                new_points[3] = corn[x[3][0]]
                ListCon[i] = new_points

            ListCon = sorted(ListCon,key = support.total_point)
            ListCon = np.array(ListCon)
            x_index = support.rearrage_point(ListCon.sum(1))
            x1 = ListCon[x_index[0][0]][3]
            x2 = ListCon[x_index[1][0]][2]
            x3 = ListCon[x_index[2][0]][1]
            x4 = ListCon[x_index[3][0]][0]
            print(x1,x2,x3,x4)

            width = x2[0] - x1[0]
            height = x3[1] - x1[1]
            width2 = x4[0] - x3[0]

            if abs(width-width2) < 30 and height > 100:

                pts1 = np.float32([x1,x2,x3,x4])
                pts2 = np.float32([[0,0],[width,0],[0,height],[width,height]])
                matrix = cv2.getPerspectiveTransform(pts1,pts2)
                imgwrap = cv2.warpPerspective(img_gray,matrix,(width,height))
                img_BD = imgwrap.copy()
                cv2.imwrite('/home/havo/autograding/wep-app-autograding/img.jpg',img_BD)
                cv2.imshow("ttttt",img_BD)

        cv2.imshow("frame 2", frame2)
        
        if cv2.waitKey(1) & 0xFF == 'q':
            cv2.destroyAllWindows()
            break

    else:
        print("loi mo camera")   
        break