import os
import re

# Folder names
PYQ_FOLDER = "pyqs"
ANSWERKEY_FOLDER = "answerkey"


# -------------------------
# GET AVAILABLE YEARS
# -------------------------

def get_available_years(folder):
    years = set()

    if not os.path.exists(folder): 
        return []

    for file in os.listdir(folder):

        match = re.search(r"(\d{4})", file)

        if match:
            years.add(match.group(1))

    return sorted(years)


# -------------------------
# GET AVAILABLE SHIFTS
# -------------------------

def get_available_shifts(folder, year):

    shifts = []

    if not os.path.exists(folder):
        return []

    print("Folder:", folder)
    print("Files:", os.listdir(folder))

    for file in os.listdir(folder):

        print("Checking:", repr(file))

        if f"{year}_" in file:
            shift = file.split("_")[-1].replace(".pdf", "")
            shifts.append(shift)

    return sorted(shifts)


# -------------------------
# GET PYQ FILE PATH
# -------------------------

def get_pyq_file(year, shift):

    return os.path.join(
        PYQ_FOLDER,
        f"pet{year}_{shift}.pdf"
    )


# -------------------------
# GET ANSWER KEY PATH
# -------------------------

def get_answerkey_file(year, shift):

    return os.path.join(
        ANSWERKEY_FOLDER,
        f"answerkey{year}_{shift}.pdf"
    )