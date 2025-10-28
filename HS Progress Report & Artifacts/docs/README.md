# AI4I 2020 Predictive Maintenance Dataset (Curated)

**Curator:** Hard Shah  
**Institution:** University of Illinois Urbana-Champaign  
**Course:** CS 598: Foundations of Data Curation  
**Date:** October 21, 2025

## Overview

This curated version of the AI4I 2020 Predictive Maintenance Dataset, originally published by Stephan Matzka in 2020, contains 10,000 synthetic records of industrial machine sensor readings for predictive maintenance research and machine learning applications.

Enhancements include comprehensive metadata following DataCite Schema 4.4, quality assessment documentation and summaries, reproducible transformation workflows with full provenance tracking, detailed bias and limitation documentation, multi-format exports (CSV, JSON, Parquet), and guidance for handling class imbalance.

### Curation Information:

- **Acquisition Date:** September 15, 2025
- **Curation Completion:** October 21, 2025
- **Curator:** Hard Shah
- **Curation Framework:** DCC Curation Lifecycle Model

## Dataset Description

The AI4I 2020 Predictive Maintenance Dataset is a synthetic dataset generated using physics-based failure models to simulate industrial machine operations. It is designed for educational purposes, algorithm benchmarking, and predictive maintenance research.

### Key Characteristics:

- **Total Records:** 10,000
- **Total Features:** 14 (5 numerical, 1 categorical, 6 binary, 2 identifiers)
- **Target Variable:** Machine failure (binary: 0=normal, 1=failure)
- **Failure Modes:** 5 distinct types (TWF, HDF, PWF, OSF, RNF)
- **Class Distribution:** 96.61% normal operations, 3.39% failures
- **Data Generation:** Synthetic, based on established industrial failure physics
- **Missing Values:** None
- **Duplicate Records:** None

### Generation Methodology:

The dataset was synthetically generated using random sampling within realistic industrial ranges, temperature and tool wear models, and physics-based failure models (TWF, HDF, PWF, OSF, RNF).

The source code for data generation is not publicly available, limiting full reproducibility.

## Feature Descriptions

### Identifier Features:

- **UDI** – Integer – Unique identifier (1-10000)
- **Product ID** – String – Product identifier with quality variant and serial number

### Input Features:

- **Type** – Categorical – L/M/H – Product quality variant (Low 60%, Medium 30%, High 10%)
- **Air temperature [K]** – Float – 295.3–304.5 – Mean 300.0 – Ambient air temperature
- **Process temperature [K]** – Float – 305.7–313.8 – Mean 310.0 – Process temperature correlated with air temperature
- **Rotational speed [rpm]** – Integer – 1168–2886 – Mean 1538 – Tool rotational speed
- **Torque [Nm]** – Float – 3.8–76.6 – Mean 40.0 – Tool torque
- **Tool wear [min]** – Integer – 0–253 – Mean 108 – Accumulated tool wear

### Target Variable:

- **Machine failure** – Binary – 0=normal, 1=failure – 0: 9661, 1: 339

### Failure Mode Flags:

- **TWF** – Tool Wear Failure – 45
- **HDF** – Heat Dissipation Failure – 115
- **PWF** – Power Failure – 95
- **OSF** – Overstrain Failure – 98
- **RNF** – Random Failure – 18

Some failure events involve multiple simultaneous modes.

## Data Quality Assessment

- **Completeness:** Excellent (no missing values, 100% complete).
- **Consistency:** Excellent (no duplicates, all types consistent).
- **Balance:** Poor (96.61% vs 3.39%, severe imbalance).
- **Documentation:** Strong (enhanced with metadata).
- **Outlier Analysis:**
  Outliers were found in most continuous features but retained as potential failure indicators.
- **Feature Correlation:** Air temperature and process temperature have a correlation of 0.88.

## Working with Imbalanced Data

The class imbalance (96.61% vs 3.39%) poses challenges.
Problems with naive approaches: accuracy is misleading and minority class detection is poor.

### Recommended strategies:

- Use metrics like Precision, Recall, F1-Score, ROC-AUC, PR-AUC, and Confusion Matrix.
- Apply resampling techniques (SMOTE, undersampling, combination methods).
- Use class weights, ensemble methods, or cost-sensitive learning.
- Optimize thresholds rather than using the default 0.5 cutoff.

## Known Limitations and Biases

- **Synthetic Data:** Lacks real-world complexity, noise, and environmental factors.
- **Generation Code Unavailable:** Original process cannot be fully replicated.
- **Severe Class Imbalance:** Only 3.39% failure cases.
- **Feature Multicollinearity:** High correlation (r=0.88) between temperature variables.

### Potential Biases:

- Sampling bias due to unbalanced quality variants, feature selection bias, and temporal bias due to snapshot data without true time-series structure.

## Intended Use Cases

### Appropriate Uses:

- Educational purposes for teaching predictive maintenance concepts
- Benchmarking machine learning algorithms for imbalanced classification
- Prototyping predictive maintenance workflows
- Research on explainable AI for industrial applications

### Inappropriate Uses:

- Direct implementation in critical industrial systems without validation
- Regulatory compliance or safety-critical applications
- Replacement for domain expertise in maintenance planning
- Commercial deployment without additional real-world validation

The dataset is primarily intended for educational and research purposes, not for direct industrial implementation without additional validation and customization.

## Curation Workflow

The curation followed the DCC Curation Lifecycle Model:

1. **Conceptualize & Create/Receive**
2. **Appraise & Select**
3. **Ingest**
4. **Preservation Action**
5. **Transform**
6. **Description & Metadata**
7. **Access & Reuse**

The curation process enhanced the dataset with comprehensive documentation, quality assessment, and usage guidelines to improve its educational and research value.

## File Structure

The project includes folders for data, notebooks, scripts, metadata, docs, output, and a requirements file. Each contains related datasets, scripts, logs, and documentation.

## Usage Instructions

### Environment Setup:

- Python 3.7 or higher is required.
- Install dependencies using `pip install -r requirements.txt`.

### Data Processing:

- Steps include loading the dataset, running quality assessments, transforming data, applying SMOTE, and training predictive models with appropriate evaluation metrics.

### Reproducing the Workflow:

- Install dependencies, download the dataset, run the Jupyter notebook, execute transformation and export scripts, and generate provenance logs.

Original Dataset Citation:
Matzka, S. (2020). AI4I 2020 Predictive Maintenance Dataset. UCI Machine Learning Repository. https://doi.org/10.24432/C5HS5C
