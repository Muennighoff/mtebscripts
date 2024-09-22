# MTEB Paper resources

This repository contains scripts & resources for the [MTEB paper]([https://github.com/embeddings-benchmark/mteb](https://arxiv.org/abs/2210.07316)). Some scripts rely on a results folder, which can be obtained via `git clone https://huggingface.co/datasets/mteb/results`. **These scripts are unlikely to work with the latest version of MTEB but rather the [1.0.0 release](https://github.com/embeddings-benchmark/mteb/releases/tag/1.0.0) when the paper was released;** they are solely to ease reproduction of the original paper. Please refer to the [MTEB repository](https://github.com/embeddings-benchmark/mteb/tree/main/scripts) for scripts and resources to work with the latest version and please open any issues with MTEB there; if you have issues with the original MTEB paper you can open them here.

<!-- TOC -->

- [Talks](#talks)
- [Benchmark](#benchmark)
- [Env Setup](#env-setup)
- [Model setup](#model-setup)
    - [Download](#download)
    - [Load](#load)

<!-- /TOC -->

## Talks

- [Link to 12min presentation on MTEB](https://www.youtube.com/watch?v=Tilgr1hjziw&t=81s&pp=ygUFTVRFQiA%3D) by Niklas Muennighoff
- [Link to 5min presentation on MTEB](https://www.youtube.com/watch?v=S6XY9mFRHGs&t=17s&pp=ygUFTVRFQiA%3D) by Nils Reimers

## Benchmark

Basic with Internet
```python
from mteb import MTEB
from sentence_transformers import SentenceTransformer
model_path = "/gpfswork/rech/six/commun/models/Muennighoff_SGPT-125M-weightedmean-nli-bitfit"
model_name = model_path.split("/")[-1].split("_")[-1]
model = SentenceTransformer(model_path)
evaluation = MTEB(tasks=["Banking77Classification"])
evaluation.run(model, output_folder=f"results/{model_name}")
```

No Internet Access (Download data first)
```python
import os
os.environ["HF_DATASETS_OFFLINE"]="1" # 1 for offline
os.environ["TRANSFORMERS_OFFLINE"]="1" # 1 for offline
os.environ["TRANSFORMERS_CACHE"]="/gpfswork/rech/six/commun/models"
os.environ["HF_DATASETS_CACHE"]="/gpfswork/rech/six/commun/datasets"
os.environ["HF_MODULES_CACHE"]="/gpfswork/rech/six/commun/modules"
os.environ["HF_METRICS_CACHE"]="/gpfswork/rech/six/commun/metrics"
from mteb import MTEB
from sentence_transformers import SentenceTransformer
model_path = "/gpfswork/rech/six/commun/models/Muennighoff_SGPT-125M-weightedmean-nli-bitfit"
model_name = model_path.split("/")[-1].split("_")[-1]
model = SentenceTransformer(model_path)
evaluation = MTEB(tasks=["Banking77Classification"])
evaluation.run(model, output_folder=f"results/{model_name}")
```


## Env Setup

```bash
export CONDA_ENVS_PATH=$six_ALL_CCFRWORK/conda

conda create -y -n hf-prod python=3.8
conda activate hf-prod

# pt-1.10.1 / cuda 11.3
conda install pytorch torchvision torchaudio cudatoolkit=11.3 -c pytorch

# Custom fork that uses offline datasets
!pip install --upgrade git+https://github.com/Muennighoff/mteb.git@offlineaccess
!pip install --upgrade git+https://github.com/Muennighoff/sentence-transformers.git@sgpt_poolings
# If you want to run BEIR tasks
!pip install --upgrade git+https://github.com/beir-cellar/beir.git
```

## Model setup

### Download

```python
import os
import sentence_transformers
os.environ["SENTENCE_TRANSFORMERS_HOME"] = "/gpfswork/rech/six/commun/models"
sentence_transformers_cache_dir = os.getenv("SENTENCE_TRANSFORMERS_HOME")
model_repo="sentence-transformers/allenai-specter"
revision="29f9f45ff2a85fe9dfe8ce2cef3d8ec4e65c5f37"
model_path = os.path.join(sentence_transformers_cache_dir, model_repo.replace("/", "_"))
model_path_tmp = sentence_transformers.util.snapshot_download(
    repo_id=model_repo,
    revision=revision,
    cache_dir=sentence_transformers_cache_dir,
    library_name="sentence-transformers",
    library_version=sentence_transformers.__version__,
    ignore_files=["flax_model.msgpack", "rust_model.ot", "tf_model.h5",],
)
os.rename(model_path_tmp, model_path)
```

### Load

```python
model = SentenceTransformer("/gpfswork/rech/six/commun/models/Muennighoff_SGPT-125M-weightedmean-nli-bitfit")
```
