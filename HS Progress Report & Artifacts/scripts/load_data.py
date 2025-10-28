import pandas as pd
import numpy as np
from pathlib import Path
import logging
from datetime import datetime

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class DataLoader:
    
    EXPECTED_COLUMNS = [
        'UDI', 'Product ID', 'Type', 'Air temperature [K]', 
        'Process temperature [K]', 'Rotational speed [rpm]', 
        'Torque [Nm]', 'Tool wear [min]', 'Machine failure',
        'TWF', 'HDF', 'PWF', 'OSF', 'RNF'
    ]
    
    EXPECTED_DTYPES = {
        'UDI': 'int64',
        'Product ID': 'object',
        'Type': 'object',
        'Air temperature [K]': 'float64',
        'Process temperature [K]': 'float64',
        'Rotational speed [rpm]': 'int64',
        'Torque [Nm]': 'float64',
        'Tool wear [min]': 'int64',
        'Machine failure': 'int64',
        'TWF': 'int64',
        'HDF': 'int64',
        'PWF': 'int64',
        'OSF': 'int64',
        'RNF': 'int64'
    }
    
    EXPECTED_ROWS = 10000
    
    def __init__(self, data_path: str):
        
        self.data_path = Path(data_path)
        self.df = None
        self.validation_results = {}
        
    def load(self) -> pd.DataFrame:
        
        logger.info(f"Loading dataset from {self.data_path}")
        
        if not self.data_path.exists():
            error_msg = f"Dataset file not found: {self.data_path}"
            logger.error(error_msg)
            raise FileNotFoundError(error_msg)
        
        try:
            self.df = pd.read_csv(self.data_path)
            logger.info(f"✓ Dataset loaded successfully: {self.df.shape[0]} rows × {self.df.shape[1]} columns")
            return self.df
        except Exception as e:
            logger.error(f"Error loading dataset: {str(e)}")
            raise
    
    def validate_structure(self) -> dict:
        
        if self.df is None:
            raise ValueError("Dataset not loaded. Call load() first.")
        
        logger.info("Validating dataset structure...")
        results = {}
        
        # Check number of rows
        results['row_count'] = {
            'expected': self.EXPECTED_ROWS,
            'actual': len(self.df),
            'status': 'PASS' if len(self.df) == self.EXPECTED_ROWS else 'WARN'
        }
        
        # Check columns
        missing_cols = set(self.EXPECTED_COLUMNS) - set(self.df.columns)
        extra_cols = set(self.df.columns) - set(self.EXPECTED_COLUMNS)
        
        results['columns'] = {
            'expected': len(self.EXPECTED_COLUMNS),
            'actual': len(self.df.columns),
            'missing': list(missing_cols),
            'extra': list(extra_cols),
            'status': 'PASS' if not missing_cols else 'FAIL'
        }
        
        # Check data types
        dtype_mismatches = []
        for col, expected_dtype in self.EXPECTED_DTYPES.items():
            if col in self.df.columns:
                actual_dtype = str(self.df[col].dtype)
                if actual_dtype != expected_dtype:
                    dtype_mismatches.append({
                        'column': col,
                        'expected': expected_dtype,
                        'actual': actual_dtype
                    })
        
        results['data_types'] = {
            'mismatches': dtype_mismatches,
            'status': 'PASS' if not dtype_mismatches else 'WARN'
        }
        
        # Check for missing values
        missing_values = self.df.isnull().sum().sum()
        results['missing_values'] = {
            'total': int(missing_values),
            'status': 'PASS' if missing_values == 0 else 'WARN'
        }
        
        # Check for duplicates
        duplicates = self.df.duplicated().sum()
        results['duplicates'] = {
            'total': int(duplicates),
            'status': 'PASS' if duplicates == 0 else 'WARN'
        }
        
        self.validation_results = results
        
        # Log results
        overall_status = all(v['status'] in ['PASS', 'WARN'] for v in results.values())
        if overall_status:
            logger.info("✓ Validation completed successfully")
        else:
            logger.warning("⚠ Validation completed with warnings or failures")
        
        return results
    
    def get_validation_summary(self) -> str:
        
        if not self.validation_results:
            return "No validation results available. Run validate_structure() first."
        
        summary = ["="*70, "DATASET VALIDATION SUMMARY", "="*70, ""]
        
        for check_name, check_results in self.validation_results.items():
            status_symbol = "✓" if check_results['status'] == 'PASS' else "⚠" if check_results['status'] == 'WARN' else "✗"
            summary.append(f"{status_symbol} {check_name.upper().replace('_', ' ')}: {check_results['status']}")
            
            for key, value in check_results.items():
                if key != 'status' and value:
                    if isinstance(value, (list, dict)) and value:
                        summary.append(f"  • {key}: {value}")
                    elif not isinstance(value, (list, dict)):
                        summary.append(f"  • {key}: {value}")
            summary.append("")
        
        summary.append("="*70)
        return "\n".join(summary)
    
    def get_basic_info(self) -> dict:
        
        if self.df is None:
            raise ValueError("Dataset not loaded. Call load() first.")
        
        return {
            'rows': len(self.df),
            'columns': len(self.df.columns),
            'column_names': list(self.df.columns),
            'memory_usage_mb': self.df.memory_usage(deep=True).sum() / 1024**2,
            'load_timestamp': datetime.now().isoformat()
        }


def main():
    
    # Example usage
    data_path = '../data/AI4I_2020.csv'
    
    loader = DataLoader(data_path)
    
    try:
        # Load data
        df = loader.load()
        
        # Validate structure
        validation_results = loader.validate_structure()
        
        # Print summary
        print(loader.get_validation_summary())
        
        # Get basic info
        info = loader.get_basic_info()
        print(f"\nDataset loaded at: {info['load_timestamp']}")
        print(f"Memory usage: {info['memory_usage_mb']:.2f} MB")
        
    except Exception as e:
        logger.error(f"Error in main execution: {str(e)}")
        raise


if __name__ == "__main__":
    main()
