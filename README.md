# pyrfuniverse

`pyrfuniverse` is a python package used to interact with `RFUniverse` simulation environment. The description of RFUniverse project can be viewed in the [website](https://sites.google.com/view/rfuniverse).

> Note: We are running towards make full open-source of RFUniverse, if your are interested in use it in your project now, please contact vinjhon2421@gmail.com.

## Installation

### 1. Create a new conda virtual environment and activate it.

```shell
conda create -n rfuniverse python=3.8 -y
conda activate rfuniverse
```

### 2. Clone this repository and move here in command line.

```shell
git clone https://github.com/mvig-robotflow/pyrfuniverse.git
cd pyrfuniverse
```

### 3. Install the python requirements.

```shell
pip install -r requirements.txt
```

For users in China, please remember to change mirror by the following command. This can significantly accelerate 
downloading speed.

```shell
pip install -i https://mirrors.aliyun.com/pypi/simple -r requirements.txt
```

### 4. Install `pyrfuniverse`.

If you want to use `pyrfuniverse` without modifying source code, run the following commands to copy source code to your conda directory.
```shell
python setup.py install
```

Otherwise, you may want to modify source code, then run the following command to construct the link in your conda directory.
```shell
pip install -e .
```

### Citation
If you think our work is useful in your research, please cite:
```
@misc{rfuniverse,
title={RFUniverse},
url={https://github.com/happyCoderJDFJJ/pyrfuniverse},
journal={GitHub}, 
author={Haoyuan Fu, Wenqiang Xu, Han Xue, Huinan Yang, Ruolin Ye, Yongxi Huang, Zhendong Xue, Yanfeng Wang, Cewu Lu}}
```