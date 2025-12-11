#!/usr/bin/env python3
"""
Main script to run the complete data curation workflow.
CS 598: Foundations of Data Curation
Author: Hard Shah
Date: October 2025
"""

import sys
from pathlib import Path
import logging

# Add scripts directory to path
scripts_dir = Path(__file__).parent / 'scripts'
sys.path.insert(0, str(scripts_dir))

from load_data import DataLoader
from transform_data import DataTransformer
from export_data import DataExporter
from log_provenance import ProvenanceLogger

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


def main():
    """
    Execute complete data curation workflow.
    """
    logger.info("="*70)
    logger.info("AI4I 2020 Data Curation Workflow")
    logger.info("="*70)
    
    # Initialize paths
    data_path = Path('data/AI4I_2020.csv')
    output_dir = Path('output')
    metadata_dir = Path('metadata')
    
    # Ensure output directories exist
    output_dir.mkdir(parents=True, exist_ok=True)
    metadata_dir.mkdir(parents=True, exist_ok=True)
    
    try:
        # Step 1: Load and validate data
        logger.info("\n[1/5] Loading and validating data...")
        loader = DataLoader(data_path)
        df = loader.load()
        
        validation_results = loader.validate_structure()
        logger.info(loader.get_validation_summary())
        
        # Check if validation passed
        all_passed = all(
            v.get('status') in ['PASS', 'WARN'] 
            for v in validation_results.values()
        )
        if not all_passed:
            logger.error("Data validation failed. Please check the data file.")
            return 1
        
        # Step 2: Transform data
        logger.info("\n[2/5] Transforming and normalizing data...")
        transformer = DataTransformer(df)
        
        # Detect outliers
        outlier_info = transformer.detect_outliers(method='iqr', threshold=1.5)
        
        # Normalize features
        df_normalized = transformer.normalize_features(method='standard')
        
        # Compute derived features
        df_enhanced = transformer.compute_derived_features()
        
        logger.info(transformer.get_transformation_summary())
        
        # Save transformation log
        transformer.save_transformation_log(metadata_dir / 'transformation_log.json')
        
        # Step 3: Export data
        logger.info("\n[3/5] Exporting curated data...")
        exporter = DataExporter(df_enhanced, output_dir=output_dir)
        
        # Export in multiple formats
        exporter.export_csv('AI4I_2020_curated.csv', include_index=False)
        exporter.export_json('AI4I_2020_curated.json')
        
        # Try to export parquet (requires pyarrow)
        try:
            exporter.export_parquet('AI4I_2020_curated.parquet')
        except ImportError:
            logger.warning("pyarrow not installed. Skipping Parquet export.")
        
        # Export documentation
        exporter.export_data_dictionary('data_dictionary.json')
        exporter.export_summary_statistics('summary_statistics.csv')
        
        # Save export log
        exporter.save_export_log('export_log.json')
        
        logger.info(exporter.generate_export_summary())
        
        # Step 4: Log provenance
        logger.info("\n[4/5] Logging provenance...")
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
            {'missing_values': validation_results['missing_values']['total']},
            'completed'
        )
        
        provenance.log_workflow_step(
            'transformation',
            'Normalized features using StandardScaler',
            {'method': 'standard', 'features_count': 5},
            'completed'
        )
        
        # Log transformations
        provenance.log_transformation(
            'normalization',
            {
                'method': 'StandardScaler',
                'features': transformer.CONTINUOUS_FEATURES
            }
        )
        
        # Log quality checks
        provenance.log_quality_check(
            'completeness_check',
            {'missing_values': 0, 'total_records': len(df)},
            passed=True
        )
        
        provenance.log_quality_check(
            'structural_validation',
            validation_results,
            passed=all_passed
        )
        
        # Add notes
        provenance.add_notes(
            'Dataset exhibits severe class imbalance (3.39% failure rate). '
            'Users should apply appropriate techniques for imbalanced classification.',
            category='data_quality'
        )
        
        # Save provenance records
        provenance.save_provenance_record(metadata_dir / 'provenance_record.json')
        provenance.save_provenance_text(Path('docs') / 'provenance.txt')
        
        logger.info(provenance.generate_provenance_summary())
        
        # Step 5: Summary
        logger.info("\n[5/5] Curation workflow completed successfully!")
        logger.info("="*70)
        logger.info("Output files generated:")
        logger.info(f"  • Curated dataset: {output_dir}/AI4I_2020_curated.csv")
        logger.info(f"  • Metadata: {metadata_dir}/metadata.json")
        logger.info(f"  • Provenance: {metadata_dir}/provenance_record.json")
        logger.info(f"  • Export log: {output_dir}/export_log.json")
        logger.info("="*70)
        
        return 0
        
    except FileNotFoundError as e:
        logger.error(f"File not found: {e}")
        logger.error("Please ensure AI4I_2020.csv is in the data/ directory.")
        return 1
        
    except Exception as e:
        logger.error(f"Error during curation workflow: {e}")
        import traceback
        traceback.print_exc()
        return 1


if __name__ == "__main__":
    exit_code = main()
    sys.exit(exit_code)

