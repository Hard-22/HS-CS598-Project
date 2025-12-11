Reproducibility Guide and Environment Setup

This document provides detailed instructions on how to replicate the project environment and execute the data curation workflow. This ensures transparency and reusability of the curation process.

1. System Requirements

-   Operating System: macOS, Linux, or Windows (tested on macOS).
-   Python Version: Python 3.7 or higher.
-   Hardware: Standard commodity hardware (no GPU required).

2. Environment Setup

We use `venv` (standard Python virtual environment) and a `requirements.txt` file to manage dependencies.

Step-by-Step Installation:

1.  Clone or Unzip Project:
    Ensure you are in the root directory of the project (where `main.py` is located).

2.  Create Virtual Environment:
    ```bash
    python3 -m venv venv
    ```

3.  Activate Virtual Environment:
    -   macOS/Linux:
        ```bash
        source venv/bin/activate
        ```
    -   Windows:
        ```cmd
        venv\Scripts\activate
        ```

4.  Install Dependencies:
    ```bash
    pip install -r requirements.txt
    ```

Dependency List (`requirements.txt`)
-   `pandas`: DataFrame manipulation.
-   `numpy`: Numerical operations.
-   `scikit-learn`: Outlier detection and normalization.
-   `matplotlib` & `seaborn`: Visualization.
-   `pyarrow`: Parquet export support.
-   `prov`: Provenance tracking.

3. Workflow Execution

The entire curation process is automated via `main.py`.

To run the full workflow:
```bash
python3 main.py
```

Expected Output
The script will print progress to the console and generate the following artifacts:

-   `output/AI4I_2020_curated.csv`: The final clean dataset.
-   `output/data_dictionary.json`: Machine-readable schema.
-   `metadata/provenance_record.json`: W3C PROV-compliant log of the execution.
-   `metadata/transformation_log.json`: Specific details on outlier removal and normalization parameters.

4. Verification

After running the script, you can verify the integrity of the output by checking `metadata/quality_report.json`. This file contains automated assertions (e.g., specific row counts, null checks) that the script runs at the end of the pipeline.
