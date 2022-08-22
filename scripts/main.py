

from common import *
from ours2nerf import ours2nerf
from train import train
from depth_est import depth_est


def create_depthmaps(scene_dirs=None, img_dir="rgb", depth_dir="depth", sigma_thrsh=15, train_steps=1000):

	snapshot_file = "base.msgpack"

	# Create example scene_dirs if None
	if scene_dirs is None:
		scene_dirs = [os.path.join(ROOT_DIR, "data/nerf/canister7")]

	# Create transforms.json from intrinsics and extrinsics
	for scene_dir in scene_dirs:
		ours2nerf(scene_dir, img_dir=img_dir)

	# Train NeRF
	for scene_dir in scene_dirs:
		train(scene_dir, n_steps=train_steps, snapshot_file=snapshot_file)
		depth_est(scene_dir, depth_dir=depth_dir, sigma_thrsh=sigma_thrsh, snapshot_file=snapshot_file)

	os.remove(snapshot_file)


if __name__ == '__main__':
	create_depthmaps()