# Instant DexNerf

Depth/3D Shape estimation of transparent objects using multiview posed RGB images. The project was inspired by [Dex-NeRF: Using a Neural Radiance field to Grasp Transparent Objects](https://sites.google.com/view/dex-nerf) and [Instant Neural Graphics Primitives](https://nvlabs.github.io/instant-ngp/). Combination of two methods provides both fast training/rendering speed and accurate depth map estimation.


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
