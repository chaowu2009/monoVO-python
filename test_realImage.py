import numpy as np 
import cv2

from visual_odometry import PinholeCamera, VisualOdometry


cam = PinholeCamera(640.0, 480, 483,45, 483.45, 300.98, 253.10)
vo = VisualOdometry(cam, '/home/hillcrest/project/data/kittk/poses/00.txt')

traj = np.zeros((600,600,3), dtype=np.uint8)

RIGHT = 2;
   
cap = cv2.VideoCapture(RIGHT)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 720)

img_id = 0
while(1):

        ret, img1 = cap.read()

        img = cv2.cvtColor(img1,cv2.COLOR_BGR2GRAY)

	vo.update(img, img_id)

        img_id = img_id + 1

	cur_t = vo.cur_t
	if(img_id > 2):
		x, y, z = cur_t[0], cur_t[1], cur_t[2]
	else:
		x, y, z = 0., 0., 0.
	draw_x, draw_y = int(x)+290, int(z)+90

	cv2.circle(traj, (draw_x,draw_y), 1, (img_id*255/4540,255-img_id*255/4540,0), 1)

	cv2.rectangle(traj, (10, 20), (600, 60), (0,0,0), -1)
	text = "Coordinates: x=%2fm y=%2fm z=%2fm"%(x,y,z)
	cv2.putText(traj, text, (20,40), cv2.FONT_HERSHEY_PLAIN, 1, (255,255,255), 1, 8)

	cv2.imshow('Road facing camera', img)
	cv2.imshow('Trajectory', traj)
	cv2.waitKey(1)

cv2.imwrite('map.png', traj)
