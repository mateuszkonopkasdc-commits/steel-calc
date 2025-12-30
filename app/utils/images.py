import os
import base64
import streamlit as st


def _get_image_base64(path: str) -> str | None:
    try:
        if os.path.exists(path):
            with open(path, "rb") as f:
                return base64.b64encode(f.read()).decode("utf-8")
    except Exception:
        return None
    return None


def _find_asset_path(name: str, folder: str = "assets") -> str | None:
    """
    Find file in assets by base name (without extension).
    Supports: png/jpg/jpeg/webp (case-insensitive).
    """
    exts = [".png", ".jpg", ".jpeg", ".webp", ".PNG", ".JPG", ".JPEG", ".WEBP"]
    for ext in exts:
        path = os.path.join(folder, f"{name}{ext}")
        if os.path.exists(path):
            return path
    return None


def render_image(name: str, width: str = "100%", height: str | None = None, folder: str = "assets") -> None:
    """
    Renders an image from assets folder by base name (without extension).
    """
    path = _find_asset_path(name, folder=folder)
    if not path:
        return

    img_data = _get_image_base64(path)
    if not img_data:
        return

    style = f"width:{width}; border-radius:10px;"
    if height:
        style += f" height:{height}; object-fit:contain;"

    st.markdown(
        f'<img src="data:image/png;base64,{img_data}" style="{style}"/>',
        unsafe_allow_html=True,
    )


# ===== KOMPATYBILNOŚĆ ZE STARYM KODEM =====
# Twoje moduły wołają render_svg_image(...).
# U Ciebie to tak naprawdę renderowanie obrazków z assets (png/jpg/webp),
# więc robimy alias na render_image.

def render_svg_image(name: str, width: str = "100%", height: str | None = None) -> None:
    """
    Backward-compatible alias used in older modules.
    """
    render_image(name=name, width=width, height=height, folder="assets")
