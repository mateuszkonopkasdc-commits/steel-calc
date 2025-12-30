SHAPE_SERIES_LIST = ["W", "M", "S", "HP", "C", "MC", "L", "HSS Rect.", "HSS Round", "Pipe"]

ASTM_DETAILED_DATA = {
    "ASTM Designation": {
        "A36": {"Fy": "36", "Fu": "58-80", "Shapes": ["W", "M", "S", "HP", "C", "MC", "L"]},
        "A53 Gr. B": {"Fy": "35", "Fu": "60", "Shapes": ["Pipe"]},
        "A500 Gr. B": {"Shapes": ["HSS Rect.", "HSS Round"], "Fu": "58"},
        "A500 Gr. C": {"Shapes": ["HSS Rect.", "HSS Round"], "Fu": "62"},
        "A501 Gr. A": {"Fy": "36", "Fu": "58", "Shapes": ["HSS Rect.", "HSS Round", "Pipe"]},
        "A501 Gr. B": {"Fy": "50", "Fu": "70", "Shapes": ["HSS Rect.", "HSS Round"]},
        "A529 Gr. 50": {"Fy": "50", "Fu": "70-100", "Shapes": ["W", "M", "S", "C", "MC", "L"]},
        "A529 Gr. 55": {"Fy": "55", "Fu": "70-100", "Shapes": ["W", "M", "S", "C", "MC", "L"]},
        "A572 Gr. 42": {"Fy": "42", "Fu": "60", "Shapes": ["W", "M", "S", "HP", "C", "MC", "L"]},
        "A572 Gr. 50": {"Fy": "50", "Fu": "65", "Shapes": ["W", "M", "S", "HP", "C", "MC", "L"]},
        "A572 Gr. 55": {"Fy": "55", "Fu": "70", "Shapes": ["W", "M", "S", "C", "MC", "L"]},
        "A572 Gr. 60": {"Fy": "60", "Fu": "75", "Shapes": ["W", "M", "S", "C", "MC", "L"]},
        "A572 Gr. 65": {"Fy": "65", "Fu": "80", "Shapes": ["W", "M", "S", "C", "MC", "L"]},
        "A588 Gr. 50": {"Fy": "50", "Fu": "70", "Shapes": ["W", "M", "S", "HP", "C", "MC", "L"]},
        "A618 Gr. I & II": {"Fy": "50", "Fu": "70", "Shapes": ["HSS Round"]},
        "A618 Gr. III": {"Fy": "50", "Fu": "65", "Shapes": ["HSS Round"]},
        "A709 Gr. 36": {"Fy": "36", "Fu": "58", "Shapes": ["W", "M", "S", "HP", "C", "MC", "L"]},
        "A709 Gr. 50": {"Fy": "50", "Fu": "65", "Shapes": ["W", "M", "S", "HP", "C", "MC", "L"]},
        "A709 Gr. 50W": {"Fy": "50", "Fu": "70", "Shapes": ["W", "M", "S", "HP", "C", "MC", "L"]},
        "A847": {"Fy": "50", "Fu": "70", "Shapes": ["HSS Rect.", "HSS Round"]},
        "A913 Gr. 50": {"Fy": "50", "Fu": "65", "Shapes": ["W", "M", "S", "HP"]},
        "A913 Gr. 60": {"Fy": "60", "Fu": "75", "Shapes": ["W", "M", "S", "HP"]},
        "A913 Gr. 65": {"Fy": "65", "Fu": "80", "Shapes": ["W", "M", "S", "HP"]},
        "A913 Gr. 70": {"Fy": "70", "Fu": "90", "Shapes": ["W", "M", "S", "HP"]},
        "A992": {"Fy": "50", "Fu": "65", "Shapes": ["W", "M", "S", "HP", "C", "MC", "L"]},
        "A1065": {"Fy": "50", "Fu": "60", "Shapes": ["HSS Rect."]},
        "A1085": {"Fy": "50", "Fu": "65", "Shapes": ["HSS Rect.", "HSS Round"]}
    }
}

GAGE_DATA = {
    "1": {"g": "5/8"}, "1 1/4": {"g": "3/4"}, "1 1/2": {"g": "7/8"}, "1 3/4": {"g": "1"},
    "2": {"g": "1 1/8"}, "2 1/2": {"g": "1 3/8"}, "3": {"g": "1 3/4"}, "3 1/2": {"g": "2"},
    "4": {"g": "2 1/2"}, "5": {"g": "3", "g1": "2"}, "6": {"g": "3 1/2", "g1": "2 1/4", "g2": "2 1/2"},
    "7": {"g": "4", "g1": "2 1/2", "g2": "3"}, "8": {"g": "4 1/2", "g1": "3", "g2": "3"},
    "9": {"g": "5", "g1": "3", "g2": "3", "g3": "3"},
    "10": {"g": "5 1/2", "g1": "3 1/2", "g2": "3 1/2", "g3": "3 1/2"},
    "12": {"g": "6 1/2", "g1": "4 1/2", "g2": "4 1/2", "g3": "4 1/2", "g4": "4 1/2"}
}

BOLT_GEOM_DATA = {
    "1/2":  {"d": 0.500, "base_edge": 0.750, "hole": {"Standard": 0.5625, "Oversize": 0.625, "Short-Slot": 0.5625, "Long-Slot": 1.25}},
    "5/8":  {"d": 0.625, "base_edge": 0.875, "hole": {"Standard": 0.6875, "Oversize": 0.8125, "Short-Slot": 0.6875, "Long-Slot": 1.5625}},
    "3/4":  {"d": 0.750, "base_edge": 1.000, "hole": {"Standard": 0.8125, "Oversize": 0.9375, "Short-Slot": 1.000, "Long-Slot": 1.875}},
    "7/8":  {"d": 0.875, "base_edge": 1.125, "hole": {"Standard": 0.9375, "Oversize": 1.0625, "Short-Slot": 1.125, "Long-Slot": 2.1875}},
    "1":    {"d": 1.000, "base_edge": 1.250, "hole": {"Standard": 1.125, "Oversize": 1.25, "Short-Slot": 1.3125, "Long-Slot": 2.5}},
    "1 1/8": {"d": 1.125, "base_edge": 1.500, "hole": {"Standard": 1.25, "Oversize": 1.4375, "Short-Slot": 1.25, "Long-Slot": 2.8125}},
    "1 1/4": {"d": 1.250, "base_edge": 1.625, "hole": {"Standard": 1.375, "Oversize": 1.5625, "Short-Slot": 1.375, "Long-Slot": 3.125}}
}

NOMINAL_BOLT_STRESS = {
    "Group A (e.g., A325)": {"Shear_N": 54.0, "Shear_X": 68.0, "Tension": 90.0},
    "Group B (e.g., A490)": {"Shear_N": 68.0, "Shear_X": 84.0, "Tension": 113.0},
    "Group C (e.g., F3043)": {"Shear_N": 90.0, "Shear_X": 113.0, "Tension": 150.0},
    "A307 bolts":           {"Shear_N": 27.0, "Shear_X": 27.0, "Tension": 45.0}
}

BOLT_AREAS = {
    "1/2": 0.196, "5/8": 0.307, "3/4": 0.442, "7/8": 0.601,
    "1": 0.785, "1 1/8": 0.994, "1 1/4": 1.23, "1 3/8": 1.48, "1 1/2": 1.77
}

HOLE_DATA_STR = {
    "1/2":  {"Standard": "9/16", "Oversize": "5/8", "Short-Slot": "9/16 x 11/16", "Long-Slot": "9/16 x 1 1/4"},
    "5/8":  {"Standard": "11/16", "Oversize": "13/16", "Short-Slot": "11/16 x 7/8", "Long-Slot": "11/16 x 1 9/16"},
    "3/4":  {"Standard": "13/16", "Oversize": "15/16", "Short-Slot": "13/16 x 1", "Long-Slot": "13/16 x 1 7/8"},
    "7/8":  {"Standard": "15/16", "Oversize": "1 1/16", "Short-Slot": "15/16 x 1 1/8", "Long-Slot": "15/16 x 2 3/16"},
    "1":    {"Standard": "1 1/8", "Oversize": "1 1/4", "Short-Slot": "1 1/8 x 1 5/16", "Long-Slot": "1 1/8 x 2 1/2"},
    "1 1/8": {"Standard": "1 1/4", "Oversize": "1 7/16", "Short-Slot": "1 1/4 x 1 9/16", "Long-Slot": "1 1/4 x 2 13/16"},
    "1 1/4": {"Standard": "1 3/8", "Oversize": "1 9/16", "Short-Slot": "1 3/8 x 1 11/16", "Long-Slot": "1 3/8 x 3 1/8"}
}
