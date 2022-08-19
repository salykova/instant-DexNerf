import argparse
import os
import commentjson as json

import numpy as np

import sys
import time

from common import *
from scenes import scenes_nerf, scenes_image, scenes_sdf, scenes_volume, setup_colored_sdf

from tqdm import tqdm

import pyngp as ngp # noqa


def train(scene, n_steps=5000, sigma_thrsh=15, save_weights="base.msgpack"):

	mode = ngp.TestbedMode.Nerf
	configs_dir = os.path.join(ROOT_DIR, "configs", "nerf")
	base_network = os.path.join(configs_dir, "base.json")
	network = base_network
	testbed = ngp.Testbed(mode)
	testbed.nerf.sharpen = float(0)
	testbed.load_training_data(scene)
	testbed.reload_network_from_file(network)
	testbed.dex_nerf = True
	testbed.sigma_thrsh = sigma_thrsh
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

	if save_weights:
		print("Saving snapshot ", save_weights)
		testbed.save_snapshot(save_weights, False)

	testbed.clear_training_data()
	ngp.free_temporary_memory()
