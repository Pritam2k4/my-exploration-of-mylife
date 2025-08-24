import json
import pandas as pd
import numpy as np
from typing import List, Dict, Tuple
import re
from sklearn.model_selection import train_test_split
from config import *
import os
import logging

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class DataProcessor:
    """Handle data loading, cleaning, and preprocessing"""
    
    def __init__(self):
        """Initialize the data processor"""
        self.raw_data = None
        self.processed_data = None
        
    def load_raw_data(self, file_path: str = None) -> List[Dict]:
        """
        Load raw data from various sources
        
        Args:
            file_path: Path to the data file
            
        Returns:
            List of question-answer dictionaries
        """
        if file_path is None:
            file_path = SAMPLE_DATA_PATH
            
        try:
            if file_path.endswith('.json'):
                with open(file_path, 'r', encoding='utf-8') as f:
                    data = json.load(f)
            elif file_path.endswith('.csv'):
                df = pd.read_csv(file_path)
                data = df.to_dict('records')
            else:
                raise ValueError("Unsupported file format. Use JSON or CSV.")
                
            self.raw_data = data
            logger.info(f"Loaded {len(data)} records from {file_path}")
            return data
            
        except Exception as e:
            logger.error(f"Error loading data: {str(e)}")
            return []
    
    def clean_text(self, text: str) -> str:
        """
        Clean and normalize text data
        
        Args:
            text: Raw text to clean
            
        Returns:
            Cleaned text
        """
        if not text:
            return ""
            
        # Remove extra whitespace
        text = re.sub(r'\s+', ' ', text.strip())
        
    