import pytest
import pandas as pd
from src.preprocess import Preprocessor

def test_load_data():
    """
    Simple test to verify data loading
    """
    # Create test data
    test_data = pd.DataFrame({
        'variance': [1.0, 2.0],
        'skewness': [3.0, 4.0],
        'curtosis': [5.0, 6.0],
        'entropy': [7.0, 8.0],
        'class': [0, 1]
    })
    
    # Save test data to temporary file
    test_file = "test_banknotes.csv"
    test_data.to_csv(test_file, index=False)
    
    try:
        # Create Preprocessor instance
        preprocessor = Preprocessor(test_file)
        
        # Load the data
        loaded_data = preprocessor.load_data()
        
        # Verify data was loaded correctly
        pd.testing.assert_frame_equal(loaded_data, test_data)
        
    finally:
        # Delete temporary file
        import os
        if os.path.exists(test_file):
            os.remove(test_file)