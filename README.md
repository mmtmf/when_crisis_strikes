# When Crisis Strikes  
**Crisis Sermons as Threshold Rhetoric**

[![Python Version](https://img.shields.io/badge/Python-3.12-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![License: CC BY 4.0](https://img.shields.io/badge/Data%20%26%20Docs-CC%20BY%204.0-lightgrey.svg)](LICENSE-DATA)

> A digital humanities project that documents and reproduces figure outputs from a quantitative close reading of Danish sermons across three societal crises, focusing on how explicit crisis framing shifts sermonic content and form. 

---

## Table of Contents
- [What This Project Does](#what-this-project-does)
- [Data](#data)
- [Getting Started](#getting-started)
- [Usage](#usage)
- [Outputs](#outputs)
- [Dependencies](#dependencies)
- [AI Assistance](#ai-assistance)
- [Citation & License](#citation--license)
- [About the Project](#about-the-project)

---

## What This Project Does

This repository provides the documentation and code needed to reproduce the article’s visualization outputs from a coded sermon dataset.

### Visualization Pipeline (`src/visualizations.py`)
- Loads coded data from `data/Kodeark_3.xlsm` (sheet: **"Udregninger 2"**).
- Computes crisis-vs-baseline differences and pooled effects.
- Generates grayscale-friendly, single-column figures.
- Saves figures to the `results/` subfolders.

Figures currently produced in this script include:
- **Figure A:** Δ percentage point small-multiples (crisis-explicit − baseline)
- **Figure B:** Affect vs. exhortation “hinge” comparison
- **Figure C:** Identity repertoire deltas
- **Figure D:** Enemy vs civic-minded solidarity deltas
- **Figure E:** Pooled theology/text-use reweighting profile (Δpp)

---

## Data

Located in the `data/` folder.

Due to copyright regulations, the actual sermon texts are not stored in this public repository. Contact the main author for relevant insight into these files. 

It includes coded/derived materials only, such as:
- `data/Kodeark_3.xlsm` (analysis sheet: *Udregninger 2*)
- `data/codebook/` (codebook describing categories/codes)
- `data/data_dictionary/` (a file descriping the datasheet and relevant calculations)

All the files are in Danish.

---

## Getting Started

Clone the repo and install dependencies in a virtual environment:

```bash
python -m venv .venv
# On Windows
.venv\Scripts\activate
# On macOS/Linux
source .venv/bin/activate
```

Install dependencies: 

```bash
pip install -r requirements.txt 
```
## Usage 

Folder structure: 

- data
    - Kodeark_3.xlsm
    - codebook
    - data-dictionary
- results
    - figure_A...
    - figure_B...
    - figure_C...
    - figure_D...
    - figure_E...
    - figure_hom...
- src
    - visualizations.py
- LICENSE
- LICENSE-DATA
- requirements.txt
- README.md

▶️ Run the visualization script:
```bash
python src/visualizations.py 
```
By default, the script expects:

Input: data/Kodeark_3.xlsm

Output directory: results/ (and subfolders as configured in the script)

If you change paths, update the DEFAULT_DATA_PATH / DEFAULT_RESULTS_DIR variables near the top of the script.

## Outputs

Saved in the results/ directory (organized by figure folders).

## Dependencies

See requirements.txt.

## AI Assistance

Parts of this code were developed with assistance from ChatGPT (versions GPT-5.2), used for standard setup and debugging.

## Citation & License

Code license:
MIT License (see LICENSE)

Data & documentation license (i.e. everything besides the code):
Creative Commons Attribution 4.0 International (CC BY 4.0) (see LICENSE-DATA)

## Citation:
If you use this repository, please cite it as: ... 

## About the Project

Developed as part of a PhD research project examining sermons in times of national crisis.
