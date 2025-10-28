import pandas as pd
import numpy as np
import json
import logging
from pathlib import Path
from datetime import datetime
import hashlib

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class DataExporter:
    
    
    def __init__(self, df: pd.DataFrame, output_dir: str = '../output'):
        
        self.df = df
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)
        self.export_log = []
        
    def calculate_checksum(self, file_path: Path, algorithm='sha256') -> str:
        
        hash_func = hashlib.sha256() if algorithm == 'sha256' else hashlib.md5()
        
        with open(file_path, 'rb') as f:
            for chunk in iter(lambda: f.read(4096), b''):
                hash_func.update(chunk)
        
        return hash_func.hexdigest()
    
    def export_csv(self, filename: str = 'AI4I_2020_curated.csv', 
                   include_index: bool = False) -> Path:
        
        output_path = self.output_dir / filename
        
        logger.info(f"Exporting dataset to CSV: {output_path}")
        
        self.df.to_csv(output_path, index=include_index)
        
        checksum = self.calculate_checksum(output_path)
        file_size_mb = output_path.stat().st_size / (1024 ** 2)
        
        self.export_log.append({
            'timestamp': datetime.now().isoformat(),
            'format': 'CSV',
            'filename': filename,
            'path': str(output_path),
            'rows': len(self.df),
            'columns': len(self.df.columns),
            'size_mb': round(file_size_mb, 2),
            'checksum_sha256': checksum
        })
        
        logger.info(f"✓ CSV export complete: {len(self.df)} rows, {file_size_mb:.2f} MB")
        logger.info(f"  SHA256: {checksum}")
        
        return output_path
    
    def export_json(self, filename: str = 'AI4I_2020_curated.json',
                    orient: str = 'records') -> Path:
        
        output_path = self.output_dir / filename
        
        logger.info(f"Exporting dataset to JSON: {output_path}")
        
        self.df.to_json(output_path, orient=orient, indent=2)
        
        checksum = self.calculate_checksum(output_path)
        file_size_mb = output_path.stat().st_size / (1024 ** 2)
        
        self.export_log.append({
            'timestamp': datetime.now().isoformat(),
            'format': 'JSON',
            'filename': filename,
            'path': str(output_path),
            'orient': orient,
            'rows': len(self.df),
            'size_mb': round(file_size_mb, 2),
            'checksum_sha256': checksum
        })
        
        logger.info(f"✓ JSON export complete: {file_size_mb:.2f} MB")
        logger.info(f"  SHA256: {checksum}")
        
        return output_path
    
    def export_parquet(self, filename: str = 'AI4I_2020_curated.parquet',
                       compression: str = 'snappy') -> Path:
        
        output_path = self.output_dir / filename
        
        logger.info(f"Exporting dataset to Parquet: {output_path}")
        
        try:
            self.df.to_parquet(output_path, compression=compression, index=False)
            
            checksum = self.calculate_checksum(output_path)
            file_size_mb = output_path.stat().st_size / (1024 ** 2)
            
            self.export_log.append({
                'timestamp': datetime.now().isoformat(),
                'format': 'Parquet',
                'filename': filename,
                'path': str(output_path),
                'compression': compression,
                'rows': len(self.df),
                'size_mb': round(file_size_mb, 2),
                'checksum_sha256': checksum
            })
            
            logger.info(f"✓ Parquet export complete: {file_size_mb:.2f} MB")
            logger.info(f"  SHA256: {checksum}")
            
            return output_path
            
        except ImportError:
            logger.warning("Parquet export requires 'pyarrow' or 'fastparquet'. Skipping.")
            return None
    
    def export_data_dictionary(self, filename: str = 'data_dictionary.json') -> Path:
        
        output_path = self.output_dir / filename
        
        logger.info(f"Generating data dictionary: {output_path}")
        
        data_dict = {}
        
        for column in self.df.columns:
            col_data = {
                'dtype': str(self.df[column].dtype),
                'non_null_count': int(self.df[column].count()),
                'null_count': int(self.df[column].isnull().sum()),
                'unique_values': int(self.df[column].nunique())
            }
            
            if pd.api.types.is_numeric_dtype(self.df[column]):
                col_data.update({
                    'mean': float(self.df[column].mean()),
                    'std': float(self.df[column].std()),
                    'min': float(self.df[column].min()),
                    'max': float(self.df[column].max()),
                    'median': float(self.df[column].median())
                })
            elif pd.api.types.is_categorical_dtype(self.df[column]) or self.df[column].dtype == 'object':
                value_counts = self.df[column].value_counts().head(10).to_dict()
                col_data['top_values'] = {str(k): int(v) for k, v in value_counts.items()}
            
            data_dict[column] = col_data
        
        with open(output_path, 'w') as f:
            json.dump(data_dict, f, indent=2)
        
        logger.info(f"✓ Data dictionary exported: {len(data_dict)} features documented")
        
        return output_path
    
    def export_summary_statistics(self, filename: str = 'summary_statistics.csv') -> Path:
        
        output_path = self.output_dir / filename
        
        logger.info(f"Exporting summary statistics: {output_path}")
        
        numeric_cols = self.df.select_dtypes(include=[np.number]).columns
        summary_stats = self.df[numeric_cols].describe()
        
        summary_stats.to_csv(output_path)
        
        logger.info(f"✓ Summary statistics exported for {len(numeric_cols)} numerical features")
        
        return output_path
    
    def save_export_log(self, filename: str = 'export_log.json'):
        
        output_path = self.output_dir / filename
        
        with open(output_path, 'w') as f:
            json.dump(self.export_log, f, indent=2)
        
        logger.info(f"✓ Export log saved: {output_path}")
    
    def generate_export_summary(self) -> str:
        
        summary = ["="*70, "DATA EXPORT SUMMARY", "="*70, ""]
        
        if not self.export_log:
            summary.append("No exports completed yet.")
        else:
            summary.append(f"Total exports: {len(self.export_log)}")
            summary.append(f"Output directory: {self.output_dir}")
            summary.append("")
            
            for idx, log_entry in enumerate(self.export_log, 1):
                summary.append(f"{idx}. {log_entry['format']} Export")
                summary.append(f"   Filename: {log_entry['filename']}")
                summary.append(f"   Size: {log_entry.get('size_mb', 'N/A')} MB")
                if 'checksum_sha256' in log_entry:
                    summary.append(f"   SHA256: {log_entry['checksum_sha256'][:16]}...")
                summary.append(f"   Timestamp: {log_entry['timestamp']}")
                summary.append("")
        
        summary.append("="*70)
        return "\n".join(summary)


def main():
    
    # Example usage
    from load_data import DataLoader
    from transform_data import DataTransformer
    
    # Load and transform data
    loader = DataLoader('../data/AI4I_2020.csv')
    df = loader.load()
    
    transformer = DataTransformer(df)
    df_transformed = transformer.normalize_features(method='standard')
    
    # Export data
    exporter = DataExporter(df_transformed, output_dir='../output')
    
    # Export in multiple formats
    exporter.export_csv('AI4I_2020_curated.csv')
    exporter.export_json('AI4I_2020_curated.json')
    exporter.export_parquet('AI4I_2020_curated.parquet')
    
    # Export documentation
    exporter.export_data_dictionary('data_dictionary.json')
    exporter.export_summary_statistics('summary_statistics.csv')
    
    # Save log
    exporter.save_export_log('export_log.json')
    
    # Print summary
    print(exporter.generate_export_summary())


if __name__ == "__main__":
    main()

