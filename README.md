# When Crisis Strikes: Sermon Responses to National Emergencies

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE.txt)

> A digital humanities project that explores how Danish sermons respond to moments of national crisis

---

## Table of Contents
- [What This Project Does](#what-this-project-does)
- [Data](#data)
- [Getting Started](#getting-started)
- [Usage](#usage)
- [Outputs](#outputs)
- [Dependencies](#dependencies)
- [Citation & License](#citation--license)
- [About the Project](#about-the-project)

---

## What This Project Does

This repository contains the analysis and visualization code for the project **_When Crisis Strikes_**, which explores how Danish sermons respond to moments of national crisis — specifically the **Schleswig Wars (1848–64)**, the **Occupation period (1940–45)**, and the **COVID-19 pandemic (2020–21)**.

The project investigates how sermons frame crises as **collective experiences**, how they **strengthen social cohesion**, and how they **reactivate national and communal identity**.  
The Python script provided here reproduces all visualizations used in the study.

---

## Data

Located in the `data/` folder:

Due to copyright regulations, the actual sermon texts and metadata are **not stored** in this public repository.  
Contact the author for relevant insight into these files.

In this repository you’ll find:
- A dataset in excel: /data/data.xlsm
- A tidy dataset: /data/data_tidy.CSV. 

---

## Getting Started

1. Clone the repo 
2. Make sure you have Python ≥3.10 installed.
3. Install dependencies:


▶️ Usage
Folder structure
```
- data
    - Kodeark_3.xlms
- documents
- results
    - fig_...
    - ...
- src
    - visualizations.py
- LICENSE.txt
- README.MD
- requirements.txt

Install dependencies:
```bash
pip install -r requirements.txt
```

▶️ Run scripts:
 
```bash
python src/visualizations.py

The script will:

Read Kodeark_3.xlsm

Generate all figures automatically

Save results in /results/

## Outputs
Saved in the `results/` directory:

## Dependencies
See requirements.txt

## AI Assistance
Parts of this code were developed with assistance from ChatGPT (version 5.2), used for standard setup and debugging.

## Citation & License
**License:**  
This project is licensed under the [MIT License](LICENSE.txt).

**Citation:**  
If you use this project in academic work, please cite it as:

> Thunbo, Michael Mørch. *When Crisis Strikes*. GitHub repository, 2026. https://github.com/mmtmf/???

## About the Project

Developed as part of a PhD research project examining sermons in times of national crisis.