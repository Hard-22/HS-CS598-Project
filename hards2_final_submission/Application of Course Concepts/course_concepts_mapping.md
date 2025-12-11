Application of Course Concepts

This document explicitly maps the practical components of this project to the theoretical frameworks and concepts covered in CS 598 Foundations of Data Curation.

1. Data Lifecycle (Module 1)

Concept: The DCC Curation Lifecycle Model describes the stages of data curation from conceptualization to access and reuse.

Application:
-   Conceptualize: Defined in `docs/README.md` (Objective: create a dataset for imbalanced learning).
-   Appraise & Select: Implemented in `scripts/transform_data.py`. We identified outliers but selected to keep them based on domain value.
-   Ingest: `scripts/load_data.py` handles the validations upon loading.
-   Preservation: Migration to CSV/JSON (`scripts/export_data.py`) ensures format longevity.
-   Description: Generation of `metadata/metadata.json`.
-   Access: Creation of the `final_submission` package.

2. Ethical & Legal Constraints (Module 2)

Concept: Assessing privacy regarding human subjects, intellectual property, and potential for harm/bias.

Application:
-   Privacy: The dataset is synthetic (see `docs/README.md`), effectively eliminating privacy risks related to human subjects.
-   Algorithmic Bias: We documented "Known Limitations" in `docs/README.md` regarding how the class imbalance can lead to biased model outcomes if not handled.
-   Licensing: We applied a CC BY 4.0 license (see `metadata/metadata.json`), facilitating open reuse compared to proprietary industrial data.

3. Data Quality (Module 6)

Concept: Quality dimensions including Completeness, Uniqueness, Consistency, and Validity.

Application:
-   Automated Validation: `scripts/load_data.py` runs assertions:
    -   Completeness: Checks for `null` values.
    -   Uniqueness: Checks for duplicate rows.
    -   Validity: Verifies column data types against the schema.
-   Evidence of these checks is found in `metadata/quality_report.json`.

4. Metadata & Documentation (Module 8)

Concept: Using standard schemas to make data understandable and discoverable.

Application:
-   DataCite Schema: We mapped our metadata fields (Creator, Title, Publisher, Year, Description) to the DataCite 4.4 standard in `metadata/metadata.json`.
-   Data Dictionary: We created `output/data_dictionary.json` as a "Codebook," defining every variable, its unit (e.g., Kelvin, rpm), and its range. This is critical Representation Information (OAIS).

5. Provenance (Module 12)

Concept: Tracking the lineage of data—Entities, Activities, and Agents (W3C PROV).

Application:
-   Implementation: `scripts/log_provenance.py` contains a `ProvenanceLogger` class.
-   Execution:
    -   Entity: The raw CSV.
    -   Activity: `StandardScaler` (normalization).
    -   Agent: The `transform_data` script.
-   Result: `metadata/provenance_record.json` captures this graph, allowing a future user to audit exactly how the "Curated" dataset was derived from the "Raw" one.

6. Workflow Automation (Module 12/13)

Concept: Reproducibility through scripting vs. manual "point-and-click" Excel cleaning.

Application:
-   The entire project is wrapped in a single entry point `main.py`.
-   Dependency management is handled via `requirements.txt`.
-   This approach ensures that the curation process is transparent (code is visible) and repeatable (deterministic output).
