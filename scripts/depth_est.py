import pyngp as ngp # noqa
from common import *
import json
import cv2


def depth_est(img_path, depth_folder="depth", sigma_thrsh=15, snapshot_file="base.msgpack"):

	depth_folder_abs = img_path + "/" + depth_folder

	if not os.path.exists(depth_folder_abs):
		os.mkdir(depth_folder_abs)

	transforms_file = img_path + "/" + "transforms.json"
	poses = []

	with open(transforms_file, 'r') as tf:
		meta = json.load(tf)
		for frame in meta['frames']:
			poses.append(frame['transform_matrix'])

	width = int(meta['w'])
	height = int(meta['h'])
	camera_angle_x = meta['camera_angle_x']
	camera_angle_y = meta['camera_angle_y']

	mode = ngp.TestbedMode.Nerf
	configs_dir = os.path.join(ROOT_DIR, "configs", "nerf")
	testbed = ngp.Testbed(mode)
	# testbed.nerf.sharpen = float(0)
	testbed.shall_train = False

	# Load a trained NeRF model
	print("Loading snapshot ", snapshot_file)
	testbed.load_snapshot(snapshot_file)
	testbed.nerf.render_with_camera_distortion = True
	testbed.snap_to_pixel_centers = True
	spp = 1
	testbed.nerf.rendering_min_transmittance = 1e-4
	testbed.fov_axis = 0
	testbed.fov = camera_angle_x * 180 / np.pi
	testbed.fov_axis = 1
	testbed.fov = camera_angle_y * 180 / np.pi

	# Set render mode
	testbed.render_mode = ngp.RenderMode.Depth

	# Adjust DeX threshold value
	testbed.dex_nerf = True
	testbed.sigma_thrsh = sigma_thrsh

	# Set camera matrix
	for i, c2w_matrix in enumerate(poses):
		testbed.set_nerf_camera_matrix(np.matrix(c2w_matrix)[:-1, :])

		# Render image
		depth_raw = testbed.render(width, height, spp, True)  # raw depth values (float, in m)
		depth_raw = depth_raw[..., 0]
		# depth_norm = depth_raw / np.max(depth_raw)
		depth_int = 1000 * depth_raw  # transform depth to mm
		depth_int = depth_int.astype(np.uint16)
		# Save rendered image
		cv2.imwrite(depth_folder_abs + "/" + "{:06}".format(i + 1) + ".png", depth_int)

	ngp.free_temporary_memory()
