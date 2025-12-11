#!/usr/bin/env python3
"""
Script to extract all code and content from Project_File.txt
and organize into proper project structure.
"""

import json
import re
from pathlib import Path

# Read the text file
text_file = "/Users/hard/Desktop/598 Data Curation/Project_File.txt"
output_dir = Path("/Users/hard/Desktop/598 Data Curation/AI4I_DataCuration_Project")

with open(text_file, 'r', encoding='utf-8') as f:
    content = f.read()

# Find all script boundaries
markers = {
    'notebook_start': 'Jupyter Notebook: AI4I_Data_Curation.ipynb',
    'load_data_start': 'Python Script: scripts/load_data.py',
    'transform_data_start': 'Python Script: scripts/transform_data.py',
    'export_data_start': 'Python Script: scripts/export_data.py',
    'provenance_start': 'Python Script: scripts/log_provenance.py',
    'metadata_start': '6. Metadata File: metadata/metadata.json',
    'readme_start': 'README File: docs/README.md'
}

# Find line numbers for each marker
lines = content.split('\n')
marker_lines = {}

for marker_name, marker_text in markers.items():
    for i, line in enumerate(lines):
        if line.startswith(marker_text):
            marker_lines[marker_name] = i + 1  # 1-indexed
            break

print("Found markers at lines:")
for marker, line_num in marker_lines.items():
    print(f"  {marker}: line {line_num}")

# Extract notebook JSON (first 713 lines from notebook start)
notebook_start = marker_lines['notebook_start'] - 1  # 0-indexed
notebook_end = marker_lines['load_data_start'] - 1

notebook_lines = lines[notebook_start:notebook_end]

# Join and try to extract JSON
notebook_text = '\n'.join(notebook_lines)
notebook_text = notebook_text.replace('Jupyter Notebook: AI4I_Data_Curation.ipynb', '')

# Extract scripts
load_data_start = marker_lines['load_data_start']
transform_data_start = marker_lines['transform_data_start']
export_data_start = marker_lines['export_data_start']
provenance_start = marker_lines['provenance_start']
metadata_start = marker_lines['metadata_start']
readme_start = marker_lines['readme_start']

def extract_python_script(start_line, end_line):
    """Extract Python code between two line numbers"""
    script_lines = lines[start_line:end_line]
    # Remove the marker line
    if script_lines and script_lines[0].startswith('Python Script:'):
        script_lines = script_lines[1:]
    
    # Also remove any lines that are marker lines
    cleaned_lines = []
    for line in script_lines:
        # Skip marker lines
        if line.strip().startswith('Python Script:'):
            continue
        if line.strip().startswith('Jupyter Notebook:'):
            continue
        if line.strip().startswith('6. Metadata File:'):
            continue
        if line.strip().startswith('README File:'):
            continue
        cleaned_lines.append(line)
    
    script_text = '\n'.join(cleaned_lines)
    
    # Find the first """ and start from there
    idx = script_text.find('"""')
    if idx >= 0:
        return script_text[idx:]
    return script_text

# Extract all sections
load_data_code = extract_python_script(load_data_start, transform_data_start)
transform_data_code = extract_python_script(transform_data_start, export_data_start)
export_data_code = extract_python_script(export_data_start, provenance_start)
provenance_code = extract_python_script(provenance_start, metadata_start)

# Extract metadata JSON
metadata_lines = lines[metadata_start:readme_start]
metadata_text = '\n'.join(metadata_lines)
metadata_text = metadata_text.replace('6. Metadata File: metadata/metadata.json', '')

# Extract README
readme_lines = lines[readme_start:]
readme_text = '\n'.join(readme_lines)
readme_text = readme_text.replace('README File: docs/README.md', '')

# Write files
print("\nCreating files...")

# Save notebook
notebook_path = output_dir / "notebooks" / "AI4I_Data_Curation.ipynb"
print(f"Creating notebook: {notebook_path}")
with open(notebook_path, 'w', encoding='utf-8') as f:
    f.write(notebook_text)

# Save Python scripts
scripts = {
    'scripts/load_data.py': load_data_code,
    'scripts/transform_data.py': transform_data_code,
    'scripts/export_data.py': export_data_code,
    'scripts/log_provenance.py': provenance_code
}

for file_path, code in scripts.items():
    full_path = output_dir / file_path
    print(f"Creating {full_path}")
    with open(full_path, 'w', encoding='utf-8') as f:
        f.write(code)

# Save metadata
metadata_path = output_dir / "metadata" / "metadata.json"
print(f"Creating {metadata_path}")
with open(metadata_path, 'w', encoding='utf-8') as f:
    f.write(metadata_text)

# Save README
readme_path = output_dir / "docs" / "README.md"
print(f"Creating {readme_path}")
with open(readme_path, 'w', encoding='utf-8') as f:
    f.write(readme_text)

print("\nExtraction complete!")

