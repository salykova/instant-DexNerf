import enum
import numpy as np
import argparse
from pathlib import Path
import os
import math
import cv2
import json

#from colmap2nerf import sharpness
from scipy.spatial.transform import Rotation as Rot





def parse_args():
    parser = argparse.ArgumentParser(description="convert a text colmap export to nerf format transforms.json; optionally convert video to images, and optionally run colmap in the first place")
    parser.add_argument("--input_dir", default="./", help="Path to folder with intrinsics.txt, images, c2w")
    parser.add_argument("--img_dir", default="./images", help="Path to images")
    parser.add_argument("--aabb_scale", default=4, choices=["1","2","4","8","16"], help="large scene scale factor. 1=scene fits in unit cube; power of 2 up to 16")
    parser.add_argument("--keep_colmap_coords", action="store_true", help="keep transforms.json in COLMAP's original frame of reference (this will avoid reorienting and repositioning the scene for preview and rendering)")
    parser.add_argument("--out", default="transforms_ours.json", help="output path")
    args = parser.parse_args()
    return args

def variance_of_laplacian(image):
    	return cv2.Laplacian(image, cv2.CV_64F).var()

def sharpness(imagePath):
	image = cv2.imread(imagePath)
	gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
	fm = variance_of_laplacian(gray)
	return fm

def rotmat(a, b):
    a, b = a / np.linalg.norm(a), b / np.linalg.norm(b)
    v = np.cross(a, b)
    c = np.dot(a, b)
    s = np.linalg.norm(v)
    kmat = np.array([[0, -v[2], v[1]], [v[2], 0, -v[0]], [-v[1], v[0], 0]])
    return np.eye(3) + kmat + kmat.dot(kmat) * ((1 - c) / (s ** 2 + 1e-10))

def closest_point_2_lines(oa, da, ob, db): # returns point closest to both rays of form o+t*d, and a weight factor that goes to 0 if the lines are parallel
	da = da / np.linalg.norm(da)
	db = db / np.linalg.norm(db)
	c = np.cross(da, db)
	denom = np.linalg.norm(c)**2
	t = ob - oa
	ta = np.linalg.det([t, db, c]) / (denom + 1e-10)
	tb = np.linalg.det([t, da, c]) / (denom + 1e-10)
	if ta > 0:
		ta = 0
	if tb > 0:
		tb = 0
	return (oa+ta*da+ob+tb*db) * 0.5, denom


if __name__ == "__main__":
    args = parse_args()
    img_dir =  args.img_dir
    img_names = sorted(os.listdir(img_dir))
    with open("associations.txt", "w") as f:
        for img_name in img_names:
            name_base, ext = os.path.splitext(img_name)
            f.write(str(int(name_base)) + " " + img_dir + "/" + img_name + "\n")

    aabb_scale = int(args.aabb_scale)
    input_dir = args.input_dir
    out_path = args.out
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
            angle_x = 2 * math.atan(w / (2 * fx))
            angle_y = 2 * math.atan(h / (2 * fy))
            fov_x = angle_x * 180 / math.pi
            fov_y = angle_y * 180 / math.pi
    print(f"camera:\n\tres={w,h}\n\tcenter={cx,cy}\n\tfocal={fx,fy}\n")

    with open(os.path.join(input_dir, "c2w_quat.txt"), "r") as f:
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
                "offset": [0.5, 2, 0.5],
                "aabb_scale": aabb_scale,
                "frames": [],
            }

            bottom = np.array([0.0, 0.0, 0.0, 1.0]).reshape([1, 4])
            up = np.zeros(3)

            c2w_lines = f.read().splitlines()

            for line in assoc:
                img_num, img_path = (line.split(" "))
                img_num = int(img_num)
                img_path = img_path.rstrip()
                b = sharpness(img_path)
                print(img_path, "sharpness=",b)
                c2w_line = c2w_lines[img_num - 1]
                c2w_line_list = c2w_line.split(" ")
                qvec = np.array(tuple(map(float, c2w_line_list[4:8])))
                tvec = np.array(tuple(map(float, c2w_line_list[1:4])))
                R = Rot.from_quat(qvec).as_matrix()
                t = tvec.reshape([3,1])
                m = np.concatenate([np.concatenate([R, t], 1), bottom], 0)
                c2w = m
                phi = np.pi/2

                c2w =  np.matrix([
    [1,0,0,0],
    [0,np.cos(phi),-np.sin(phi),0],
    [0,np.sin(phi), np.cos(phi),0],
    [0,0,0,1]]) @ c2w

                frame={"file_path":img_path,"sharpness":b,"transform_matrix": c2w}
                out["frames"].append(frame)


    nframes = len(out["frames"])

    for f in out["frames"]:
        f["transform_matrix"] = f["transform_matrix"].tolist()
    print(nframes,"frames")
    print(f"writing {out_path}")
    with open(out_path, "w") as outfile:
        json.dump(out, outfile, indent=2)






