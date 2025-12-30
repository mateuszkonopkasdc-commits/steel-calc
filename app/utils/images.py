import os
import base64
import streamlit as st
from pathlib import Path

def get_image_base64(path: str):
    try:
        if os.path.exists(path):
            with open(path, "rb") as f:
                return base64.b64encode(f.read()).decode()
    except:
        return None
    return None

def assets_dir() -> Path:
    # app/utils/images.py -> app/utils -> app -> (project root) -> assets
    return Path(__file__).resolve().parents[2] / "assets"

def render_svg_image(name: str, width: str = "100%", height: str | None = None):
    img_data = None
    exts = [".png", ".jpg", ".jpeg", ".PNG", ".JPG", ".webp"]
    base = assets_dir()

    for ext in exts:
        path = base / f"{name}{ext}"
        if path.exists():
            img_data = get_image_base64(str(path))
            break

    if img_data:
        style = f"width:{width}; border-radius:4px;"
        if height:
            style += f" height:{height}; object-fit: contain;"
        st.markdown(f'<img src="data:image/png;base64,{img_data}" style="{style}">', unsafe_allow_html=True)
