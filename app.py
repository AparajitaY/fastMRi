
import os

import numpy as np
import streamlit as st
import torch

from PIL import Image
from model import UNetBetter


st.set_page_config(
    page_title="fastMRI Reconstruction",
    page_icon="🧠",
    layout="wide"
)


BASE_DIR = os.path.dirname(
    os.path.abspath(__file__)
)

CHECKPOINT_PATH = os.path.join(
    BASE_DIR,
    "best_gan_4x.pth"
)

DEVICE = torch.device("cpu")


@st.cache_resource
def load_model():
    model = UNetBetter().to(DEVICE)

    checkpoint = torch.load(
        CHECKPOINT_PATH,
        map_location=DEVICE
    )

    model.load_state_dict(
        checkpoint["model_state_dict"]
    )

    model.eval()

    return model


def prepare_image(uploaded_file):
    image = Image.open(uploaded_file).convert("L")
    image = image.resize((256, 256))

    image_array = np.asarray(
        image,
        dtype=np.float32
    )

    image_array = image_array / 255.0

    tensor = torch.from_numpy(
        image_array
    ).unsqueeze(0).unsqueeze(0)

    return image, tensor


st.title("fastMRI Reconstruction")
st.write(
    "Upload a grayscale MRI image to generate a reconstructed image "
    "using the trained GAN model."
)

uploaded_file = st.file_uploader(
    "Upload an MRI image",
    type=["png", "jpg", "jpeg"]
)

if uploaded_file is not None:
    original_image, input_tensor = prepare_image(
        uploaded_file
    )

    model = load_model()

    with torch.no_grad():
        reconstructed = model(
            input_tensor.to(DEVICE)
        )

    reconstructed = reconstructed.squeeze().numpy()
    reconstructed = np.clip(
        reconstructed,
        0.0,
        1.0
    )

    output_image = Image.fromarray(
        (reconstructed * 255).astype(np.uint8)
    )

    column1, column2 = st.columns(2)

    with column1:
        st.subheader("Input image")
        st.image(
            original_image,
            use_container_width=True
        )

    with column2:
        st.subheader("Reconstruction")
        st.image(
            output_image,
            use_container_width=True
        )

    st.download_button(
        label="Download reconstruction",
        data=output_image.tobytes(),
        file_name="reconstructed_mri.png",
        mime="image/png"
    )
