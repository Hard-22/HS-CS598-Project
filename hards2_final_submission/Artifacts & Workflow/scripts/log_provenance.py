import json
import logging
from datetime import datetime
from pathlib import Path
import platform
import sys
import subprocess

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class ProvenanceLogger:
    
    
    def __init__(self, project_name: str = "AI4I_2020_Curation"):
        
        self.project_name = project_name
        self.provenance_record = {
            'project_name': project_name,
            'creation_timestamp': datetime.now().isoformat(),
            'dataset_source': {},
            'curation_workflow': [],
            'system_environment': {},
            'data_transformations': [],
            'quality_checks': [],
            'exports': []
        }
        
    def log_dataset_source(self, source_info: dict):
        
        logger.info("Logging dataset source information...")
        
        required_fields = ['title', 'source_url', 'acquisition_date', 'license']
        for field in required_fields:
            if field not in source_info:
                logger.warning(f"Missing recommended field in source_info: {field}")
        
        self.provenance_record['dataset_source'] = {
            **source_info,
            'logged_at': datetime.now().isoformat()
        }
        
        logger.info("✓ Dataset source information logged")
    
    def log_workflow_step(self, step_name: str, description: str, 
                         parameters: dict = None, status: str = 'completed'):
        
        step_record = {
            'step_name': step_name,
            'description': description,
            'timestamp': datetime.now().isoformat(),
            'status': status,
            'parameters': parameters or {}
        }
        
        self.provenance_record['curation_workflow'].append(step_record)
        
        logger.info(f"✓ Logged workflow step: {step_name} ({status})")
    
    def log_transformation(self, transformation_type: str, details: dict):
        
        transformation_record = {
            'type': transformation_type,
            'timestamp': datetime.now().isoformat(),
            'details': details
        }
        
        self.provenance_record['data_transformations'].append(transformation_record)
        
        logger.info(f"✓ Logged transformation: {transformation_type}")
    
    def log_quality_check(self, check_name: str, results: dict, passed: bool):
        
        quality_record = {
            'check_name': check_name,
            'timestamp': datetime.now().isoformat(),
            'passed': passed,
            'results': results
        }
        
        self.provenance_record['quality_checks'].append(quality_record)
        
        status = "PASS" if passed else "FAIL"
        logger.info(f"✓ Logged quality check: {check_name} ({status})")
    
    def log_export(self, export_info: dict):
        
        export_record = {
            **export_info,
            'logged_at': datetime.now().isoformat()
        }
        
        self.provenance_record['exports'].append(export_record)
        
        logger.info(f"✓ Logged export: {export_info.get('format', 'unknown')} format")
    
    def capture_system_environment(self):
        
        logger.info("Capturing system environment...")
        
        try:
            # Python packages
            try:
                import pandas as pd
                import numpy as np
                import sklearn
                
                packages = {
                    'pandas': pd.__version__,
                    'numpy': np.__version__,
                    'scikit-learn': sklearn.__version__
                }
            except ImportError as e:
                packages = {'error': f"Could not import packages: {str(e)}"}
            
            self.provenance_record['system_environment'] = {
                'captured_at': datetime.now().isoformat(),
                'python_version': sys.version,
                'platform': platform.platform(),
                'machine': platform.machine(),
                'processor': platform.processor(),
                'python_implementation': platform.python_implementation(),
                'packages': packages
            }
            
            logger.info("✓ System environment captured")
            
        except Exception as e:
            logger.error(f"Error capturing system environment: {str(e)}")
    
    def add_curator_info(self, curator_name: str, institution: str, 
                        contact: str = None):
        
        self.provenance_record['curator'] = {
            'name': curator_name,
            'institution': institution,
            'contact': contact,
            'added_at': datetime.now().isoformat()
        }
        
        logger.info(f"✓ Curator information added: {curator_name}")
    
    def add_notes(self, note_text: str, category: str = 'general'):
        
        if 'notes' not in self.provenance_record:
            self.provenance_record['notes'] = []
        
        note = {
            'timestamp': datetime.now().isoformat(),
            'category': category,
            'text': note_text
        }
        
        self.provenance_record['notes'].append(note)
        
        logger.info(f"✓ Note added: {category}")
    
    def generate_provenance_summary(self) -> str:
        
        summary = ["="*70, "PROVENANCE SUMMARY", "="*70, ""]
        
        summary.append(f"Project: {self.provenance_record['project_name']}")
        summary.append(f"Created: {self.provenance_record['creation_timestamp']}")
        summary.append("")
        
        if self.provenance_record['dataset_source']:
            summary.append("DATASET SOURCE")
            summary.append("-" * 70)
            for key, value in self.provenance_record['dataset_source'].items():
                if key != 'logged_at':
                    summary.append(f"  • {key}: {value}")
            summary.append("")
        
        if 'curator' in self.provenance_record:
            summary.append("CURATOR INFORMATION")
            summary.append("-" * 70)
            curator = self.provenance_record['curator']
            summary.append(f"  • Name: {curator['name']}")
            summary.append(f"  • Institution: {curator['institution']}")
            if curator.get('contact'):
                summary.append(f"  • Contact: {curator['contact']}")
            summary.append("")
        
        if self.provenance_record['curation_workflow']:
            summary.append(f"CURATION WORKFLOW ({len(self.provenance_record['curation_workflow'])} steps)")
            summary.append("-" * 70)
            for idx, step in enumerate(self.provenance_record['curation_workflow'], 1):
                summary.append(f"  {idx}. {step['step_name']} - {step['status']}")
                summary.append(f"     {step['description']}")
            summary.append("")
        
        if self.provenance_record['data_transformations']:
            summary.append(f"DATA TRANSFORMATIONS ({len(self.provenance_record['data_transformations'])})")
            summary.append("-" * 70)
            for trans in self.provenance_record['data_transformations']:
                summary.append(f"  • {trans['type']} at {trans['timestamp']}")
            summary.append("")
        
        if self.provenance_record['quality_checks']:
            summary.append(f"QUALITY CHECKS ({len(self.provenance_record['quality_checks'])})")
            summary.append("-" * 70)
            passed = sum(1 for check in self.provenance_record['quality_checks'] if check['passed'])
            summary.append(f"  Passed: {passed}/{len(self.provenance_record['quality_checks'])}")
            summary.append("")
        
        if self.provenance_record['exports']:
            summary.append(f"EXPORTS ({len(self.provenance_record['exports'])})")
            summary.append("-" * 70)
            for exp in self.provenance_record['exports']:
                summary.append(f"  • {exp.get('format', 'unknown')} - {exp.get('filename', 'N/A')}")
            summary.append("")
        
        summary.append("="*70)
        return "\n".join(summary)
    
    def save_provenance_record(self, output_path: str = '../metadata/provenance_record.json'):
        
        output_path = Path(output_path)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        
        with open(output_path, 'w') as f:
            json.dump(self.provenance_record, f, indent=2)
        
        logger.info(f"✓ Provenance record saved to {output_path}")
    
    def save_provenance_text(self, output_path: str = '../docs/provenance.txt'):
        
        output_path = Path(output_path)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        
        with open(output_path, 'w') as f:
            f.write(self.generate_provenance_summary())
        
        logger.info(f"✓ Provenance summary saved to {output_path}")


def main():
    
    # Example usage
    provenance = ProvenanceLogger("AI4I_2020_Curation")
    
    # Log dataset source
    provenance.log_dataset_source({
        'title': 'AI4I 2020 Predictive Maintenance Dataset',
        'source_url': 'https://archive.ics.uci.edu/dataset/601',
        'doi': '10.24432/C5HS5C',
        'acquisition_date': '2025-09-28',
        'license': 'CC BY 4.0',
        'original_authors': 'Stephan Matzka'
    })
    
    # Add curator info
    provenance.add_curator_info(
        curator_name='Hard Shah',
        institution='University of Illinois Urbana-Champaign',
        contact='hardshah@example.edu'
    )
    
    # Capture environment
    provenance.capture_system_environment()
    
    # Log workflow steps
    provenance.log_workflow_step(
        'data_acquisition',
        'Downloaded dataset from UCI ML Repository',
        {'source': 'UCI', 'date': '2025-09-28'},
        'completed'
    )
    
    provenance.log_workflow_step(
        'quality_assessment',
        'Performed comprehensive EDA and quality checks',
        {'missing_values': 0, 'duplicates': 0},
        'completed'
    )
    
    # Log transformations
    provenance.log_transformation(
        'normalization',
        {
            'method': 'StandardScaler',
            'features': ['Air temperature [K]', 'Process temperature [K]', 
                        'Rotational speed [rpm]', 'Torque [Nm]', 'Tool wear [min]']
        }
    )
    
    # Log quality checks
    provenance.log_quality_check(
        'completeness_check',
        {'missing_values': 0, 'total_records': 10000},
        passed=True
    )
    
    # Add notes
    provenance.add_notes(
        'Dataset exhibits severe class imbalance (3.39% failure rate). '
        'Users should apply appropriate techniques for imbalanced classification.',
        category='data_quality'
    )
    
    # Print summary
    print(provenance.generate_provenance_summary())
    
    # Save records
    provenance.save_provenance_record('../metadata/provenance_record.json')
    provenance.save_provenance_text('../docs/provenance.txt')


if __name__ == "__main__":
    main()
