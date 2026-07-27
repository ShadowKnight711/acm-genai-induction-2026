# Project Sentinel: Eyes of the Highway Reserve

Satellite land-cover classification for the reserve-highway corridor, built as a comparison of four training strategies on the EuroSAT dataset (Sentinel-2 RGB imagery, 10 land-use classes).

## The Brief

A forest department satellite feeds down top-down imagery of the reserve every few hours. This project builds and compares image classifiers that could realistically run on that pipeline — tagging each patch of land as forest, river, highway, farmland, residential, or one of the other EuroSAT classes.

## Dataset

- **EuroSAT RGB** (JPEG version) — [Kaggle link](https://www.kaggle.com/datasets/apollo2506/eurosat-dataset)
- 27,000 images total, 10 classes, 64×64 px
- Split: 70% train (18,900) / 15% val (4,050) / 15% test (4,050), fixed random seed for reproducibility

## Model Architectures

**1. TinyVGG (trained from scratch)**
A small VGG-style CNN: 3 convolutional blocks (each with two 3×3 conv layers + ReLU + max-pool), channel depth doubling per block (32 → 64 → 128), followed by a fully-connected classifier head with dropout (0.3) for regularization. No pretrained weights — every layer learns directly from EuroSAT.

**2. ResNet18 (transfer learning)**
ResNet18 pretrained on ImageNet, with all convolutional layers **frozen** and only the final fully-connected layer replaced and trained for our 10 classes. This is the "feature extraction" style of transfer learning — reusing ImageNet's learned visual features as a fixed backbone.

Both architectures were trained twice each: once on the dataset without augmentation, once with augmentation (random horizontal flip, random vertical flip, random rotation ±15°) — chosen because top-down satellite imagery has no fixed "up" direction, making flips/rotations realistic, label-preserving transformations for this domain.

- Optimizer: Adam, lr=0.001
- Loss: CrossEntropyLoss
- Epochs: 10
- Batch size: 64

## Results

| Model | Augmentation | Best Val Acc | Final Train Acc | Test Acc |
|---|---|---|---|---|
| TinyVGG (scratch) | No | 0.9136 | 0.9387 | **0.9141** |
| TinyVGG (scratch) | Yes | 0.9170 | 0.9152 | 0.9081 |
| ResNet18 (transfer) | No | 0.8657 | 0.8638 | 0.8654 |
| ResNet18 (transfer) | Yes | 0.8240 | 0.8073 | 0.8180 |

### Confusion Matrices
![alt text](image-4.png)![alt text](image-5.png)![alt text](image-6.png)![alt text](image-7.png)

### Loss & Accuracy Curves

![alt text](image.png)![alt text](image-1.png)![alt text](image-2.png)![alt text](image-3.png)

## Analysis

The from-scratch TinyVGG **outperformed** the frozen ResNet18 transfer model on every metric — a result that looks counterintuitive at first, but makes sense given the setup:

- ImageNet's pretrained features are tuned for natural, ground-level photography (everyday objects, animals, people) — a poor visual match for top-down 64×64 satellite patches. Because the ResNet18 backbone was **fully frozen**, it had no way to adapt those mismatched features to the new domain; only the final classification layer could learn anything EuroSAT-specific.
- TinyVGG, trained end-to-end from random initialization, had no such mismatch — every layer learned directly from satellite imagery patterns.

Augmentation had a **mixed effect**: it gave TinyVGG a small boost in best validation accuracy (0.9136 → 0.9170) but noticeably hurt the transfer model (0.8657 → 0.8240 best val acc). This is consistent with the frozen-backbone limitation above — augmented inputs are harder to classify, and a backbone that can't adapt its features has less capacity to compensate.

**Takeaway for the actual pipeline:** for a domain this different from ImageNet, a well-designed model trained from scratch on in-domain data outperformed a frozen pretrained backbone. A stronger transfer-learning setup — unfreezing and fine-tuning some of ResNet's later layers, rather than freezing all of them — would likely close or reverse this gap, and is a natural next step.

## How to Run

1. Download EuroSAT RGB from the Kaggle link above, extract so `EuroSAT_RGB/` sits next to the notebook (containing one subfolder per class)
2. `pip install torch torchvision numpy matplotlib scikit-learn pandas jupyter`
3. Open `Task2.ipynb` and run all cells top to bottom

Trained and run locally on an RTX 5070 Laptop GPU (CUDA 12.8, PyTorch nightly build for Blackwell architecture support).

