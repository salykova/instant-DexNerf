from common import *
import math
import cv2
from scipy.spatial.transform import Rotation as Rot
import json


def variance_of_laplacian(image):
	return cv2.Laplacian(image, cv2.CV_64F).var()


def sharpness(imagePath):
	image = cv2.imread(imagePath)
	gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
	fm = variance_of_laplacian(gray)
	return fm


def ours2nerf(scene_dir, img_dir="rgb", aabb_scale=4, output_file="transforms.json"):

	img_dir_full = os.path.join(scene_dir, img_dir)
	img_names = sorted(os.listdir(img_dir_full))

	img_paths_list = []

	for img_name in img_names:
		img_paths_list.append(os.path.join(img_dir_full, img_name))

	aabb_scale = int(aabb_scale)
	out_path = os.path.join(scene_dir, output_file)
	print(f'Outputting to {out_path}...')
	with open(os.path.join(scene_dir, "intrinsics.txt"), "r") as f:
		for line in f:
			elems = line.split(" ")
			w = float(elems[0])
			h = float(elems[1])
			fx = float(elems[2])
			fy = float(elems[6])
			cx = float(elems[4])
			cy = float(elems[7])
			scene_geometry = int(elems[11])
			if scene_geometry == 360:
				offset = [0.5, 2, 0.5]
			elif scene_geometry == 180:
				offset = [1, 1.8, 0.7]
			else:
				raise ValueError("Unknown scene geometry, must be 360 or 180 (forward facing)")

			angle_x = 2 * math.atan(w / (2 * fx))
			angle_y = 2 * math.atan(h / (2 * fy))
			#fov_x = angle_x * 180 / math.pi
			#fov_y = angle_y * 180 / math.pi

	with open(os.path.join(scene_dir, "groundtruth_handeye.txt"), "r") as f:
		out = {
			"camera_angle_x": angle_x,
			"camera_angle_y": angle_y,
			"fl_x": fx,
			"fl_y": fy,
			"cx": cx,
			"cy": cy,
			"w": w,
			"h": h,
			"scale": 1.7,
			"offset": offset,
			"aabb_scale": aabb_scale,
			"frames": [],
		}

		bottom = np.array([0.0, 0.0, 0.0, 1.0]).reshape([1, 4])

		c2w_lines = f.read().splitlines()

		for img_num, img_path in enumerate(img_paths_list, start=1):
			b = sharpness(img_path)
			c2w_line = c2w_lines[img_num - 1]
			c2w_line_list = c2w_line.split(" ")
			qvec = np.array(tuple(map(float, c2w_line_list[4:8])))
			tvec = np.array(tuple(map(float, c2w_line_list[1:4])))
			R = Rot.from_quat(qvec).as_matrix()
			t = tvec.reshape([3, 1])
			m = np.concatenate([np.concatenate([R, t], 1), bottom], 0)
			c2w = m
			phi = np.pi / 2
			transform_matrix = np.matrix([
				[1, 0, 0, 0],
				[0, np.cos(phi), -np.sin(phi), 0],
				[0, np.sin(phi), np.cos(phi), 0],
				[0, 0, 0, 1]])
			c2w = transform_matrix @ c2w
			frame = {"file_path": os.path.join(img_dir, os.path.basename(img_path)), "sharpness": b, "transform_matrix": c2w}
			out["frames"].append(frame)

	for f in out["frames"]:
		f["transform_matrix"] = f["transform_matrix"].tolist()

	with open(out_path, "w") as outfile:
		json.dump(out, outfile, indent=2)