#!/usr/bin/env python3
import os
from pathlib import Path
import rospy
from duckietown_msgs.msg import WheelsCmdStamped
from sensor_msgs.msg import CompressedImage
import cv2
import numpy as np

# termination criteria
criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 30, 0.001)

# prepare object points, like (0,0,0), (1,0,0), (2,0,0) ....,(6,5,0)
objp = np.zeros((5 * 7, 3), np.float32)
objp[:, :2] = np.mgrid[0:7, 0:5].T.reshape(-1, 2)

# Arrays to store object points and image points from all the images.
obj_points = []  # 3d point in real world space
img_points = []  # 2d points in image plane.
BOARDS_NUM = 2
MAX_DIR_CHANGES = 2
NUM_IMAGES_FOR_CALIB = int(os.getenv("IMG_NUM"))
CALIBRATION_BOT_DIR_PATH = "/data/config/calibrations/camera_intrinsic/"
vel = float(os.getenv("VELOCITY"))


def bgr_from_jpg(data):
    """ Returns an OpenCV BGR image from a string """
    s = np.fromstring(data, np.uint8)
    bgr = cv2.imdecode(s, cv2.IMREAD_COLOR)
    if bgr is None:
        msg = 'Could not decode image (cv2.imdecode returned None). '
        msg += 'This is usual a sign of data corruption.'
        raise ValueError(msg)
    return bgr


class MyNode:
    def __init__(self, node_name):
        rospy.init_node(node_name)
        self.img = None
        self.gray = None
        self.im_size = None
        self.pub = rospy.Publisher("~wheels_cmd", WheelsCmdStamped,
                                   queue_size=1)
        self.sub_image = rospy.Subscriber("~image/compressed", CompressedImage,
                                          self.process_image, queue_size=1)

    def process_image(self, image_msg) -> None:
        self.img = bgr_from_jpg(image_msg.data)

    def on_shutdown(self) -> None:
        msg = WheelsCmdStamped()
        msg.vel_left, msg.vel_right = 0.0, 0.0
        self.pub.publish(msg)

    def step(self, cw=True, is_vis=True) -> None:
        msg = WheelsCmdStamped()
        rate = rospy.Rate(10)
        k = 1
        if not is_vis:
            k = 1.5
        msg.vel_left, msg.vel_right = -1 * vel * k, vel * k
        if cw:
            msg.vel_left, msg.vel_right = msg.vel_right, msg.vel_left
        rospy.loginfo(f"Publishing message: left {msg.vel_left}, "
                      f"right {msg.vel_right}")
        self.pub.publish(msg)
        rate.sleep()
        msg.vel_left, msg.vel_right = 0.0, 0.0
        rospy.loginfo("Publishing message: -")
        self.pub.publish(msg)
        rate.sleep()

    def handle_img(self, img):
        self.gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        ret, corners = cv2.findChessboardCorners(self.gray, (7, 5), None)
        if ret:
            print(f"Collect images: {len(obj_points)}/{NUM_IMAGES_FOR_CALIB}")
            obj_points.append(objp)
            corners2 = cv2.cornerSubPix(self.gray, corners, (11, 11), (-1, -1), criteria)
            img_points.append(corners2)
            cv2.drawChessboardCorners(img, (7, 5), corners2, ret)
            return True
        return False

    def fsm(self, state, board):
        if board > BOARDS_NUM - 1:
            return (True, False, True), board - 1
        if board < 0:
            return (False, False, True), board + 1
        rules = {
            # cw,   isVis, restor
            (False, True, False): ((False, True, False), board),  # normal CCW
            (True, True, False): ((True, True, False), board),  # normal CW
            (False, False, False): ((False, False, True), board + 1),
            # insiv when CCW -> go CW back
            (True, False, False): ((True, False, True), board - 1),
            # insiv when CW -> go CCW back
            (True, False, True): ((True, False, True), board),
            # normal CW restoration
            (False, False, True): ((False, False, True), board),
            # normal CCW restoration
            (True, True, True): ((True, True, False), board),
            # restores, now normal CW movement
            (False, True, True): ((False, True, False), board)
            # restores, now normal CCW movement
        }
        return rules[state][0], rules[state][1]

    def run(self) -> None:
        cw = True
        dir_changes = 0
        board = 0
        # cw, isVis, restor
        state = (cw, True, False)
        while not rospy.is_shutdown():
            if self.img is not None:
                if not self.im_size:
                    self.im_size = (self.img.shape[1], self.img.shape[0])
                img = self.img
                is_vis = self.handle_img(img)
                state = (state[0], is_vis, state[2])
                new_state, board = self.fsm(state, board)
                if state[0] != new_state[0]:
                    dir_changes += 1
                state = new_state
                self.step(state[0], is_vis)
                # show res
                cv2.imshow('img', img)
                cv2.waitKey(500)
                if len(obj_points) >= NUM_IMAGES_FOR_CALIB:
                    break
        self.on_shutdown()
        cv2.destroyAllWindows()
        self.sub_image.unregister()
        print(f"Samples num: {len(obj_points)}")
        ret, mtx, dist, rvecs, tvecs = cv2.calibrateCamera(obj_points,
                                                           img_points,
                                                           self.gray.shape[
                                                           ::-1], None, None)
        self.compute_error(rvecs, tvecs, mtx, dist)
        # use monocular camera
        R = np.identity(3)
        t = np.zeros((3, 1))
        Rt = np.concatenate([R, t], axis=-1)  # [R|t]
        projection_mtx = mtx @ Rt  # A[R|t]
        autobot_name = os.getenv("VEHICLE_NAME")
        res = self.get_res(autobot_name, mtx, R, projection_mtx, self.im_size, dist)
        print("\n", res)
        self.write_on_a_bot(res, autobot_name)
        rospy.signal_shutdown('Calibration done!')

    def compute_error(self, rvecs, tvecs, mtx, dist) -> None:
        sum_error = 0
        for i in range(len(obj_points)):
            img_points2, _ = cv2.projectPoints(obj_points[i], rvecs[i],
                                               tvecs[i], mtx, dist)
            error = cv2.norm(img_points[i], img_points2, cv2.NORM_L2) / len(
                img_points2)
            sum_error += error
        print("Total error: ", sum_error / len(obj_points))

    def get_res(self, name, mtx, R, P, size, d) -> str:
        def format_mat(x, precision):
            return ("[%s]" % (
                np.array2string(x, precision=precision, suppress_small=True, separator=", ")
                    .replace("[", "").replace("]", "").replace("\n", "")
            ))

        calmessage = "\n".join([
            "image_width: %d" % size[0],
            "image_height: %d" % size[1],
            "camera_name: " + name,
            "camera_matrix:",
            "  rows: 3",
            "  cols: 3",
            "  data: " + format_mat(mtx, 5),
            "distortion_model: plumb_bob",
            "distortion_coefficients:",
            "  rows: 1",
            "  cols: %d" % len(d),
            "  data: " + format_mat(d, 5),
            "rectification_matrix:",
            "  rows: 3",
            "  cols: 3",
            "  data: " + format_mat(R, 8),
            "projection_matrix:",
            "  rows: 3",
            "  cols: 4",
            "  data: " + format_mat(P, 5),
            ""
        ])
        return calmessage

    def write_on_a_bot(self, data, name: str) -> None:
        file_name = f'{name}.yaml'
        file_dir = str(Path(".").absolute())
        with open(file_name, 'w') as outfile:
            outfile.write(data)
        COPY_COMMAND = f'rsync --rsh=\"sshpass -p quackquack ssh -o StrictHostKeyChecking=no -l duckie\" {file_dir}/{file_name} duckie@{name}.local:{CALIBRATION_BOT_DIR_PATH}'
        os.system(COPY_COMMAND)


if __name__ == '__main__':
    # create the node
    node = MyNode(node_name='intrinsic_autocalibration_node')


    # run node
    node.run()
    # keep spinning
    rospy.spin()
    