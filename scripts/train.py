

import time
from common import *
from tqdm import tqdm
import pyngp as ngp


def train(scene_dir, n_steps=1000, snapshot_file="base.msgpack"):

	mode = ngp.TestbedMode.Nerf
	configs_dir = os.path.join(ROOT_DIR, "configs", "nerf")
	base_network = os.path.join(configs_dir, "base.json")
	network = base_network
	testbed = ngp.Testbed(mode)
	testbed.nerf.sharpen = float(0)
	testbed.load_training_data(scene_dir)
	testbed.reload_network_from_file(network)
	testbed.shall_train = True
	testbed.nerf.render_with_camera_distortion = True

	old_training_step = 0
	n_steps = n_steps
	if n_steps < 0:
		n_steps = 100000

	tqdm_last_update = 0
	if n_steps > 0:
		with tqdm(desc="Training", total=n_steps, unit="step") as t:
			while testbed.frame():
				if testbed.want_repl():
					repl(testbed)
				# What will happen when training is done?
				if testbed.training_step >= n_steps:
					break

				# Update progress bar
				if testbed.training_step < old_training_step or old_training_step == 0:
					old_training_step = 0
					t.reset()

				now = time.monotonic()
				if now - tqdm_last_update > 0.1:
					t.update(testbed.training_step - old_training_step)
					t.set_postfix(loss=testbed.loss)
					old_training_step = testbed.training_step
					tqdm_last_update = now

	if snapshot_file:
		print("Saving snapshot ", snapshot_file)
		testbed.save_snapshot(snapshot_file, False)

	testbed.clear_training_data()
	ngp.free_temporary_memory()
