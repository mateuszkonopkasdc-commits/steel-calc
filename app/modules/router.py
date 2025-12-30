import importlib
import inspect
import streamlit as st

# mapowanie wyboru z menu -> plik w app/modules
MODULE_MAP = {
    # GENERAL DESIGN DATA
    "Angle Workable Gages": "app.modules.materials",     # jeśli masz osobny, zmień na np. app.modules.gages
    "ASTM Material Data": "app.modules.materials",
    "Unit Conversions": "app.modules.conversions",

    # GEOMETRIC LIMITS
    "Bolt Hole Dimensions": "app.modules.bolt_geometry",
    "Bolt Min. Edge Distance": "app.modules.bolt_geometry",
    "Bolt Min. Spacing": "app.modules.bolt_geometry",

    # WELDS
    "Effective Throat of Flare-Groove Welds": "app.modules.welds",
    "Min. Throat of PJP Groove Welds": "app.modules.welds",
    "Min. Size of Fillet Welds": "app.modules.welds",
    "Max. Size of Fillet Welds": "app.modules.welds",

    # COMPONENT LIMIT STATES
    "Shear Strength of Bolts": "app.modules.bolts_strength",
    "Tensile Strength of Bolts": "app.modules.bolts_strength",
}

# jakie nazwy funkcji będziemy próbować wywołać w module
CANDIDATE_FUNCS = ("render", "page", "run", "app", "main")


def dispatch_module(selected: str) -> None:
    mod_path = MODULE_MAP.get(selected)

    st.markdown(
        f'<h1 style="font-size:1.6rem; margin-bottom:0;">📌 {selected}</h1>',
        unsafe_allow_html=True,
    )
    st.divider()

    if not mod_path:
        st.error(f"Brak mapowania modułu dla: **{selected}**")
        st.stop()

    try:
        m = importlib.import_module(mod_path)
    except Exception as e:
        st.error(f"Nie mogę zaimportować: `{mod_path}`")
        st.exception(e)
        st.stop()

    # 1) Najpierw spróbujmy: render(selected) jeśli istnieje i przyjmuje argument
    if hasattr(m, "render") and callable(getattr(m, "render")):
        fn = getattr(m, "render")
        try:
            sig = inspect.signature(fn)
            if len(sig.parameters) == 1:
                return fn(selected)
        except Exception:
            pass

    # 2) Spróbujmy typowych nazw bez argumentów: render/page/run/app/main
    for name in CANDIDATE_FUNCS:
        fn = getattr(m, name, None)
        if callable(fn):
            try:
                return fn()
            except TypeError:
                # np. funkcja wymaga argumentu
                continue
            except Exception as e:
                st.error(f"Błąd w `{mod_path}.{name}()`")
                st.exception(e)
                st.stop()

    # 3) Jeśli nic nie znaleziono -> pokaż debug
    st.warning(
        f"Moduł **{mod_path}** się załadował, ale nie znalazłem funkcji do uruchomienia.\n\n"
        f"Dodaj w tym module funkcję `render()` albo `page()`."
    )
    st.code(
        "\n".join([x for x in dir(m) if not x.startswith("_")])[:4000]
    )
