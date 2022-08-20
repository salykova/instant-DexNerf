#!/usr/bin/env python3

# Copyright (c) 2020-2022, NVIDIA CORPORATION.  All rights reserved.
#
# NVIDIA CORPORATION and its licensors retain all intellectual property
# and proprietary rights in and to this software, related documentation
# and any modifications thereto.  Any use, reproduction, disclosure or
# distribution of this software and related documentation without an express
# license agreement from NVIDIA CORPORATION is strictly prohibited.

import json
import math
import cv2
from common import *
from scipy.spatial.transform import Rotation as Rot
from train import train
from depth_est import depth_est
import pyngp as ngp # noqa\


def variance_of_laplacian(image):
	return cv2.Laplacian(image, cv2.CV_64F).var()


def sharpness(imagePath):
	image = cv2.imread(imagePath)
	gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
	fm = variance_of_laplacian(gray)
	return fm


def ours2nerf(input_dir, img_dir="rgb", aabb_scale=4, output_file="transforms.json"):

	img_dir_abs = input_dir + "/" + img_dir
	img_names = sorted(os.listdir(img_dir_abs))
	with open(input_dir + "/" + "associations.txt", "w") as f:
		for img_name in img_names:
			name_base, ext = os.path.splitext(img_name)
			f.write(str(int(name_base)) + " " + img_dir_abs + "/" + img_name + "\n")

	aabb_scale = int(aabb_scale)
	input_dir = input_dir
	out_path = input_dir + "/" + output_file
	print(f'Outputting to {out_path}...')
	with open(os.path.join(input_dir, "intrinsics.txt"), "r") as f:
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

	with open(os.path.join(input_dir, "groundtruth_handeye.txt"), "r") as f:
		with open(os.path.join(input_dir, "associations.txt"), "r") as assoc:
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

			for line in assoc:
				img_num_str, img_dir_abs = line.split(" ")
				img_dir_abs = img_dir_abs.rstrip()
				img_num_int = int(img_num_str)
				b = sharpness(img_dir_abs)
				c2w_line = c2w_lines[img_num_int - 1]
				c2w_line_list = c2w_line.split(" ")
				qvec = np.array(tuple(map(float, c2w_line_list[4:8])))
				tvec = np.array(tuple(map(float, c2w_line_list[1:4])))
				R = Rot.from_quat(qvec).as_matrix()
				t = tvec.reshape([3, 1])
				m = np.concatenate([np.concatenate([R, t], 1), bottom], 0)
				c2w = m
				phi = np.pi / 2

				c2w = np.matrix([
					[1, 0, 0, 0],
					[0, np.cos(phi), -np.sin(phi), 0],
					[0, np.sin(phi), np.cos(phi), 0],
					[0, 0, 0, 1]]) @ c2w

				frame = {"file_path": img_dir + "/" + os.path.basename(img_dir_abs), "sharpness": b, "transform_matrix": c2w}
				out["frames"].append(frame)

	for f in out["frames"]:
		f["transform_matrix"] = f["transform_matrix"].tolist()

	with open(out_path, "w") as outfile:
		json.dump(out, outfile, indent=2)


def create_depthmaps(img_paths=None, depth_folder="depth", sigma_thrsh=15, train_steps=100):

	snapshot_file = "base.msgpack"

	if img_paths is None:
		img_paths = ["abs. path#1", "abs. path#2, ..."]

	for img_path in img_paths:
		ours2nerf(img_path)

	for img_path in img_paths:
		# Train NeRF
		train(img_path, sigma_thrsh=sigma_thrsh, n_steps=train_steps, save_weights=snapshot_file)
		depth_est(img_path, depth_folder=depth_folder, sigma_thrsh=sigma_thrsh, snapshot_file=snapshot_file)

	os.remove(snapshot_file)


if __name__ == '__main__':
	create_depthmaps()
