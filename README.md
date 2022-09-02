# Instant DexNerf

Depth/3D Shape estimation of transparent objects using multiview posed RGB images. The project was inspired by [Dex-NeRF: Using a Neural Radiance field to Grasp Transparent Objects](https://sites.google.com/view/dex-nerf) and [Instant Neural Graphics Primitives](https://nvlabs.github.io/instant-ngp/). Combination of two methods provides both fast training/rendering speed and accurate depth map estimation.

## How to install
For installation steps please refer to [Instant NGP](https://github.com/NVlabs/instant-ngp). 

## How to run
There is an example of a scene with transparent object. Run from the command line
```
./build/testbed --scene data/nerf/canister/transforms.json
```
In the GUI you can adjust sigma parameter and switch between normal and Dex depth rendering. By default, sigma = 15.

## How to create depth maps of captured scenes
In ``` /scripts ``` folder there is a [main.py](https://github.com/salykovaa/instant-DexNerf/blob/main/scripts/main.py) script
for depth map generation.

1. First, fill the [scene_dirs](https://github.com/salykovaa/instant-DexNerf/blob/main/scripts/main.py#L9) list with paths to your folders with rgb images. These folders must have the following structure. In ```/data/nerf/canister``` you can find examples of ```groundtruth_handeye.txt``` and ``` intrinsics.txt ```
```
├── scene_folder
│   ├── img_dir (folder with rgb images. default "rgb", but you can change the name in main.py) 
│   ├── groundtruth_handeye.txt (contains c2w extrinsics as quaternions for each image. x,y,z,w format)
|   ├── intrinsics.txt (w h fx 0 cx 0 fy cy 0 0 1 [360 or 180]). 180 for forward-facing scene, 360 for 360° scene.
```
2. Set parameters for training and rendering: ```depth_dir```, ```sigma_thrsh```, ```aabb_scale```, ``` train_steps ```
3. Run ```main.py``` Rendered depth maps are found in ```scene_folder/depth_dir``` folder.

**Note**: if you use world coordinate system different from ours, please adapt ```transform_matrix``` in [ours2nerf.py](https://github.com/salykovaa/instant-DexNerf/blob/main/scripts/ours2nerf.py#L85). c2w matrices are multiplied by ```transform_matrix```
before they written to the transforms.json file. Otherwise, poses are expected to be in **OPENCV** format.

**Depending on your scene geometry, you may need to tune [scale](https://github.com/salykovaa/instant-DexNerf/blob/main/scripts/ours2nerf.py#L64), [offset](https://github.com/salykovaa/instant-DexNerf/blob/main/scripts/ours2nerf.py#L43) parameters !!!**

## Results
### Example 1

![000039](https://user-images.githubusercontent.com/63703454/179689907-855bbce7-355e-4ec3-8d32-d9458c950dd7.png)
![rendered_depth1](https://user-images.githubusercontent.com/63703454/179689927-d61fad50-18e1-4010-8e1b-826a2d465e4a.png)

### Example 2

![000050](https://user-images.githubusercontent.com/63703454/179689986-17ca4f76-409d-430d-b2c6-51ad8461abab.png)
![rendered_depth2](https://user-images.githubusercontent.com/63703454/179690005-c097abb0-3cf1-443c-ba83-53c2077c3e0d.png)

### Depth error
#### Example 1
![error_depth1](https://user-images.githubusercontent.com/63703454/179690100-710bb937-8958-4d31-88fa-fb7f7e2499cb.png)
![cbar](https://user-images.githubusercontent.com/63703454/179690127-83629d6b-aedb-4eae-9e2b-2028e7b870d2.png)

#### Example 2
![error_depth2](https://user-images.githubusercontent.com/63703454/179690059-f3fec438-3bfd-4a0b-b4cf-2ac9dffa01ba.png)
![cbar](https://user-images.githubusercontent.com/63703454/179690127-83629d6b-aedb-4eae-9e2b-2028e7b870d2.png)

## Citation
Kudos to the authors for their great work
```
@inproceedings{IchnowskiAvigal2021DexNeRF,
  title={{Dex-NeRF}: Using a Neural Radiance field to Grasp Transparent Objects},
  author={Ichnowski*, Jeffrey and Avigal*, Yahav and Kerr, Justin and Goldberg, Ken},
  booktitle={Conference on Robot Learning (CoRL)},
  year={2020}
}
```
```
@article{mueller2022instant,
    author = {Thomas M\"uller and Alex Evans and Christoph Schied and Alexander Keller},
    title = {Instant Neural Graphics Primitives with a Multiresolution Hash Encoding},
    journal = {ACM Trans. Graph.},
    issue_date = {July 2022},
    volume = {41},
    number = {4},
    month = jul,
    year = {2022},
    pages = {102:1--102:15},
    articleno = {102},
    numpages = {15},
    url = {https://doi.org/10.1145/3528223.3530127},
    doi = {10.1145/3528223.3530127},
    publisher = {ACM},
    address = {New York, NY, USA},
}
```
