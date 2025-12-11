import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler
import logging
import json
from pathlib import Path
from datetime import datetime

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class DataTransformer:
    
    
    CONTINUOUS_FEATURES = [
        'Air temperature [K]',
        'Process temperature [K]',
        'Rotational speed [rpm]',
        'Torque [Nm]',
        'Tool wear [min]'
    ]
    
    def __init__(self, df: pd.DataFrame):
        
        self.df = df.copy()
        self.df_transformed = None
        self.scaler = StandardScaler()
        self.transformation_log = []
        
    def detect_outliers(self, method='iqr', threshold=1.5) -> dict:
        
        logger.info(f"Detecting outliers using {method.upper()} method...")
        
        outlier_info = {}
        
        for feature in self.CONTINUOUS_FEATURES:
            if method == 'iqr':
                Q1 = self.df[feature].quantile(0.25)
                Q3 = self.df[feature].quantile(0.75)
                IQR = Q3 - Q1
                lower_bound = Q1 - threshold * IQR
                upper_bound = Q3 + threshold * IQR
                
                outliers = self.df[(self.df[feature] < lower_bound) | 
                                  (self.df[feature] > upper_bound)]
                
            elif method == 'zscore':
                z_scores = np.abs((self.df[feature] - self.df[feature].mean()) / 
                                 self.df[feature].std())
                outliers = self.df[z_scores > threshold]
            
            outlier_info[feature] = {
                'count': len(outliers),
                'percentage': len(outliers) / len(self.df) * 100,
                'indices': outliers.index.tolist() if len(outliers) < 100 else 'too_many_to_list'
            }
            
            logger.info(f"  • {feature}: {len(outliers)} outliers ({outlier_info[feature]['percentage']:.2f}%)")
        
        self.transformation_log.append({
            'timestamp': datetime.now().isoformat(),
            'operation': 'outlier_detection',
            'method': method,
            'threshold': threshold,
            'results': {k: v['count'] for k, v in outlier_info.items()}
        })
        
        return outlier_info
    
    def normalize_features(self, method='standard') -> pd.DataFrame:
        
        logger.info(f"Normalizing features using {method} scaling...")
        
        self.df_transformed = self.df.copy()
        
        if method == 'standard':
            self.df_transformed[self.CONTINUOUS_FEATURES] = self.scaler.fit_transform(
                self.df[self.CONTINUOUS_FEATURES]
            )
            
            scaling_params = {
                feature: {
                    'mean': float(mean),
                    'std': float(std)
                }
                for feature, mean, std in zip(
                    self.CONTINUOUS_FEATURES,
                    self.scaler.mean_,
                    self.scaler.scale_
                )
            }
            
        elif method == 'minmax':
            from sklearn.preprocessing import MinMaxScaler
            scaler = MinMaxScaler()
            self.df_transformed[self.CONTINUOUS_FEATURES] = scaler.fit_transform(
                self.df[self.CONTINUOUS_FEATURES]
            )
            
            scaling_params = {
                feature: {
                    'min': float(min_val),
                    'max': float(max_val)
                }
                for feature, min_val, max_val in zip(
                    self.CONTINUOUS_FEATURES,
                    scaler.data_min_,
                    scaler.data_max_
                )
            }
        
        elif method == 'robust':
            from sklearn.preprocessing import RobustScaler
            scaler = RobustScaler()
            self.df_transformed[self.CONTINUOUS_FEATURES] = scaler.fit_transform(
                self.df[self.CONTINUOUS_FEATURES]
            )
            
            scaling_params = {
                feature: {
                    'center': float(center),
                    'scale': float(scale)
                }
                for feature, center, scale in zip(
                    self.CONTINUOUS_FEATURES,
                    scaler.center_,
                    scaler.scale_
                )
            }
        
        self.transformation_log.append({
            'timestamp': datetime.now().isoformat(),
            'operation': 'normalization',
            'method': method,
            'features': self.CONTINUOUS_FEATURES,
            'parameters': scaling_params
        })
        
        logger.info(f"✓ Normalization complete for {len(self.CONTINUOUS_FEATURES)} features")
        
        return self.df_transformed
    
    def compute_derived_features(self) -> pd.DataFrame:
        
        logger.info("Computing derived features...")
        
        if self.df_transformed is None:
            self.df_transformed = self.df.copy()
        
        # Temperature difference
        self.df_transformed['Temp_Difference'] = (
            self.df['Process temperature [K]'] - self.df['Air temperature [K]']
        )
        
        # Power (Torque × Rotational Speed)
        # Convert RPM to rad/s: RPM * 2π / 60
        self.df_transformed['Power_Estimate'] = (
            self.df['Torque [Nm]'] * 
            self.df['Rotational speed [rpm]'] * 2 * np.pi / 60
        )
        
        # Tool wear rate (tool wear per unit time - assuming linear)
        # This is a simplified proxy; real rate would need time-series data
        self.df_transformed['Tool_Wear_Category'] = pd.cut(
            self.df['Tool wear [min]'],
            bins=[0, 100, 200, float('inf')],
            labels=['Low', 'Medium', 'High']
        )
        
        derived_features = ['Temp_Difference', 'Power_Estimate', 'Tool_Wear_Category']
        
        self.transformation_log.append({
            'timestamp': datetime.now().isoformat(),
            'operation': 'feature_engineering',
            'derived_features': derived_features,
            'description': 'Added temperature difference, power estimate, and tool wear category'
        })
        
        logger.info(f"✓ Added {len(derived_features)} derived features")
        
        return self.df_transformed
    
    def get_transformation_summary(self) -> str:
        
        summary = ["="*70, "DATA TRANSFORMATION SUMMARY", "="*70, ""]
        
        if not self.transformation_log:
            summary.append("No transformations applied yet.")
        else:
            for idx, log_entry in enumerate(self.transformation_log, 1):
                summary.append(f"{idx}. {log_entry['operation'].upper().replace('_', ' ')}")
                summary.append(f"   Timestamp: {log_entry['timestamp']}")
                for key, value in log_entry.items():
                    if key not in ['timestamp', 'operation']:
                        summary.append(f"   • {key}: {value}")
                summary.append("")
        
        summary.append("="*70)
        return "\n".join(summary)
    
    def save_transformation_log(self, output_path: str):
        
        output_path = Path(output_path)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        
        with open(output_path, 'w') as f:
            json.dump(self.transformation_log, f, indent=2)
        
        logger.info(f"✓ Transformation log saved to {output_path}")


def main():
    """
    Main function for testing transformation module.
    """
    # Example usage
    from load_data import DataLoader
    
    loader = DataLoader('../data/AI4I_2020.csv')
    df = loader.load()
    
    transformer = DataTransformer(df)
    
    # Detect outliers
    outlier_info = transformer.detect_outliers(method='iqr', threshold=1.5)
    
    # Normalize features
    df_normalized = transformer.normalize_features(method='standard')
    
    # Compute derived features
    df_enhanced = transformer.compute_derived_features()
    
    # Print summary
    print(transformer.get_transformation_summary())
    
    # Save log
    transformer.save_transformation_log('../metadata/transformation_log.json')


if __name__ == "__main__":
    main()
