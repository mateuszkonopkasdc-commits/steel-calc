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


def render_image(name: str, width: str = "100%", height: str | None = None) -> None:
    """
    Renderuje obraz z folderu /assets po nazwie pliku bez rozszerzenia.
    Obsługuje: png/jpg/jpeg/webp.
    Przykład: render_image("table_2_4")
    """
    exts = [".png", ".jpg", ".jpeg", ".webp", ".PNG", ".JPG", ".JPEG", ".WEBP"]

    # assets jest w root projektu (steel-calc/assets)
    # Ten plik jest w app/utils/images.py => trzeba wyjść 2 poziomy do root.
    base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
    assets_dir = os.path.join(base_dir, "assets")

    img_data = None
    for ext in exts:
        p = os.path.join(assets_dir, f"{name}{ext}")
        img_data = _get_image_base64(p)
        if img_data:
            break

    if not img_data:
        # cicho – nie spamujemy, ale w razie czego możesz odkomentować:
        # st.warning(f"Brak pliku obrazu w assets dla: {name}")
        return

    style = f"width:{width}; border-radius:6px;"
    if height:
        style += f" height:{height}; object-fit: contain;"

    st.markdown(
        f'<img src="data:image/png;base64,{img_data}" style="{style}">',
        unsafe_allow_html=True
    )


# kompatybilność z wcześniejszą nazwą, jeśli gdzieś jej używasz:
render_svg_image = render_image
