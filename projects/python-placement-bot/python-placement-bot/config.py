MODEL_NAME = "distilbert-base-uncased"
MODEL_SAVE_PATH = "./models/fine_tuned_distilbert/"
TOKENIZER_SAVE_PATH = "./models/tokenizer/"

# Data Configuration
RAW_DATA_PATH = "./data/raw/"
PROCESSED_DATA_PATH = "./data/processed/"
SAMPLE_DATA_PATH = "./data/sample_data.json"

# Training Configuration
MAX_LENGTH = 512
BATCH_SIZE = 16
LEARNING_RATE = 2e-5
NUM_EPOCHS = 3
WARMUP_STEPS = 500
WEIGHT_DECAY = 0.01
EVAL_STRATEGY = "epoch"
SAVE_STRATEGY = "epoch"
LOGGING_STEPS = 100

# Response Generation Configuration
MAX_RESPONSE_LENGTH = 300
TEMPERATURE = 0.7
TOP_K = 50
TOP_P = 0.9
DO_SAMPLE = True

# Web Interface Configuration
STREAMLIT_PORT = 8501
PAGE_TITLE = "Python Placement Prep Assistant"
PAGE_ICON = "🐍"
LAYOUT = "wide"

# Dataset Configuration
DATASET_SPLIT_RATIO = {
    "train": 0.8,
    "validation": 0.1,
    "test": 0.1
}

# Preprocessing Configuration
MIN_QUESTION_LENGTH = 10
MAX_QUESTION_LENGTH = 1000
MIN_ANSWER_LENGTH = 20
MAX_ANSWER_LENGTH = 2000

# Model Performance Configuration
EARLY_STOPPING_PATIENCE = 3
SAVE_TOTAL_LIMIT = 2
EVALUATION_BATCH_SIZE = 32