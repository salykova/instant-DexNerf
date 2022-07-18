# Instant DexNerf

Depth estimation of transparent objects using only posed multiview RGB images. The project was inspired by [Dex-NeRF: Using a Neural Radiance field to Grasp Transparent Objects](https://sites.google.com/view/dex-nerf) and [Instant Neural Graphics Primitives](https://nvlabs.github.io/instant-ngp/). Combination of two methods provides both fast training/rendering speed and accurate depth map estimation.

**Code will be released soon** 🤩🤩🤩

## Results
### Example 1

<img width="736" height="414" src="https://user-images.githubusercontent.com/63703454/179602630-30016a08-e02c-4971-b796-676f96979c04.png">
<img width="736" height="414" src="https://user-images.githubusercontent.com/63703454/179602966-24cdd54a-6509-49d0-95ad-6f1041116d73.png">

### Example 2

<img width="736" height="414" src="https://user-images.githubusercontent.com/63703454/179603164-1598cb07-4a96-47cb-b77a-0c9075b8dba9.png">
<img width="736" height="414" src="https://user-images.githubusercontent.com/63703454/179603204-75c15303-b14e-42f2-9926-d58a5887cfcf.png">

### Depth error
#### Example 1
<img width="736" height="414" src="https://user-images.githubusercontent.com/63703454/179604356-9462dc21-bd98-441d-a51e-eb2793ebf071.png">

#### Example 2
<img width="736" height="414" src="https://user-images.githubusercontent.com/63703454/179604376-b7b6ebec-bb04-4385-aad7-88133f52847d.png">
<img width="810" height="110" src="https://user-images.githubusercontent.com/63703454/179604566-97ade0e4-765c-4434-b100-6166805a024c.png">

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
