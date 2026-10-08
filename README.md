# fastMRI Brain Reconstruction

A research project on accelerated multi-coil brain MRI reconstruction using the fastMRI dataset.

## Project stages

1. Mathematical multi-coil RSS reconstruction.
2. 4× k-space undersampling and zero-filled reconstruction.
3. U-Net and ResUNet reconstruction.
4. GAN-based reconstruction experiments.
5. Streamlit app deployment.

## Dataset

This project uses the fastMRI multi-coil brain dataset.

The raw HDF5 files are not included in this repository. Users must obtain the dataset separately and update the data path in the notebooks.

## Current results

| Model | PSNR | SSIM |
|---|---:|---:|
| Zero-filled 4× | 22.953 | 0.6004 |
| U-Net 4× | 27.110 | 0.6903 |
| ResUNet 4× | 26.960 | 0.6835 |

These values correspond to the fixed experimental configuration documented in the notebooks.

## Run the Streamlit App

Keep these files in the same folder:

- `app.py` — Streamlit interface and inference.
- `model.py` — U-Net generator architecture.
- `requirements.txt` — required Python packages.
- `best_gan_4x.pth` — trained GAN checkpoint.

From that folder, install dependencies and start the app:

```bash
pip install -r requirements.txt
streamlit run app.py
```

Open the local URL shown in the terminal and upload the grayscale MRI image named streamlit_input.png from assets folder to view the model output.

This is an image-domain research demo, not a raw k-space reconstruction
interface or a clinical diagnostic tool. Its reported validation metrics
apply to the notebook’s fastMRI preprocessing pipeline.

## Disclaimer

This is a research and educational project. It is not intended for clinical diagnosis or medical decision-making.
