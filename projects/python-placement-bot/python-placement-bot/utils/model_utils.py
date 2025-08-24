import torch
from transformers import (
    DistilBertTokenizerFast,
    DistilBertForQuestionAnswering,
    DistilBertConfig,
    pipeline
)
from typing import Dict, List, Optional
import logging
from config import *
import os

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class ModelHandler:
    """Handle model loading, inference, and utilities"""
    
    def __init__(self, model_path: str = None, tokenizer_path: str = None):
        """
        Initialize the model handler
        
        Args:
            model_path: Path to the fine-tuned model
            tokenizer_path: Path to the tokenizer
        """
        self.model_path = model_path or MODEL_SAVE_PATH
        self.tokenizer_path = tokenizer_path or TOKENIZER_SAVE_PATH
        self.model = None
        self.tokenizer = None
        self.qa_pipeline = None
        self.device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
        
        logger.info(f"Using device: {self.device}")
    
    def load_model(self) -> bool:
        """
        Load the fine-tuned model and tokenizer
        
        Returns:
            True if successful, False otherwise
        """
        try:
            # Check if fine-tuned model exists
            if os.path.exists(self.model_path) and os.path.exists(self.tokenizer_path):
                # Load fine-tuned model
                logger.info("Loading fine-tuned model...")
                self.tokenizer = DistilBertTokenizerFast.from_pretrained(self.tokenizer_path)
                self.model = DistilBertForQuestionAnswering.from_pretrained(self.model_path)
            else:
                # Load pre-trained model as fallback
                logger.info("Loading pre-trained DistilBERT model...")
                self.tokenizer = DistilBertTokenizerFast.from_pretrained(MODEL_NAME)
                self.model = DistilBertForQuestionAnswering.from_pretrained(MODEL_NAME)
            
            # Move model to device
            self.model.to(self.device)
            self.model.eval()
            
            # Create QA pipeline
            self.qa_pipeline = pipeline(
                "question-answering",
                model=self.model,
                tokenizer=self.tokenizer,
                device=0 if self.device.type == 'cuda' else -1
            )
            
            logger.info("Model loaded successfully")
            return True
            
        except Exception as e:
            logger.error(f"Error loading model: {str(e)}")
            return False
    
    def generate_answer(self, question: str, context: str = None) -> Dict:
        """
        Generate answer for a given question
        
        Args:
            question: User question
            context: Context for the question (optional)
            
        Returns:
            Dictionary with answer and confidence score
        """
        if not self.qa_pipeline:
            logger.error("Model not loaded. Call load_model() first.")
            return {"answer": "Sorry, the model is not available.", "confidence": 0.0}
        
        try:
            # If no context provided, use the question as context
            if not context:
                context = f"This is a Python programming question: {question}"
            
            # Generate answer using pipeline
            result = self.qa_pipeline(
                question=question,
                context=context
            )
            
            return {
                "answer": result['answer'],
                "confidence": result['score'],
                "start": result.get('start', 0),
                "end": result.get('end', 0)
            }
            
        except Exception as e:
            logger.error(f"Error generating answer: {str(e)}")
            return {
                "answer": "I'm sorry, I couldn't generate an answer for that question.",
                "confidence": 0.0
            }
    
    def batch_generate_answers(self, questions: List[str], contexts: List[str] = None) -> List[Dict]:
        """
        Generate answers for multiple questions
        
        Args:
            questions: List of questions
            contexts: List of contexts (optional)
            
        Returns:
            List of answer dictionaries
        """
        if not contexts:
            contexts = [f"This is a Python programming question: {q}" for q in questions]
        
        results = []
        for question, context in zip(questions, contexts):
            result = self.generate_answer(question, context)
            results.append(result)
        
        return results
    
    def tokenize_input(self, question: str, context: str = None) -> Dict:
        """
        Tokenize input for the model
        
        Args:
            question: User question
            context: Context for the question
            
        Returns:
            Tokenized input dictionary
        """
        if not self.tokenizer:
            logger.error("Tokenizer not loaded.")
            return {}
        
        if not context:
            context = f"This is a Python programming question: {question}"
        
        try:
            inputs = self.tokenizer(
                question,
                context,
                add_special_tokens=True,
                max_length=MAX_LENGTH,
                padding='max_length',
                truncation=True,
                return_tensors='pt'
            )
            
            return inputs
            
        except Exception as e:
            logger.error(f"Error tokenizing input: {str(e)}")
            return {}
    
    def get_model_info(self) -> Dict:
        """
        Get information about the loaded model
        
        Returns:
            Dictionary with model information
        """
        if not self.model:
            return {"status": "Model not loaded"}
        
        config = self.model.config
        
        info = {
            "model_type": "DistilBERT for Question Answering",
            "model_name": MODEL_NAME,
            "vocab_size": config.vocab_size,
            "hidden_size": config.hidden_size,
            "num_attention_heads": config.n_heads,
            "num_hidden_layers": config.n_layers,
            "max_position_embeddings": config.max_position_embeddings,
            "device": str(self.device),
            "status": "Model loaded successfully"
        }
        
        return info
    
    def save_model(self, model, tokenizer, save_path: str = None, tokenizer_path: str = None):
        """
        Save model and tokenizer
        
        Args:
            model: Model to save
            tokenizer: Tokenizer to save
            save_path: Path to save model
            tokenizer_path: Path to save tokenizer
        """
        save_path = save_path or self.model_path
        tokenizer_path = tokenizer_path or self.tokenizer_path
        
        try:
            # Create directories if they don't exist
            os.makedirs(save_path, exist_ok=True)
            os.makedirs(tokenizer_path, exist_ok=True)
            
            # Save model and tokenizer
            model.save_pretrained(save_path)
            tokenizer.save_pretrained(tokenizer_path)
            
            logger.info(f"Model saved to {save_path}")
            logger.info(f"Tokenizer saved to {tokenizer_path}")
            
        except Exception as e:
            logger.error(f"Error saving model: {str(e)}")

# Utility functions
def load_pretrained_model(model_name: str = MODEL_NAME):
    """
    Load a pre-trained DistilBERT model
    
    Args:
        model_name: Name of the model to load
        
    Returns:
        Tuple of (model, tokenizer)
    """
    try:
        tokenizer = DistilBertTokenizerFast.from_pretrained(model_name)
        model = DistilBertForQuestionAnswering.from_pretrained(model_name)
        
        logger.info(f"Loaded pre-trained model: {model_name}")
        return model, tokenizer
        
    except Exception as e:
        logger.error(f"Error loading pre-trained model: {str(e)}")
        return None, None

def create_qa_pipeline(model_path: str = None):
    """
    Create a question-answering pipeline
    
    Args:
        model_path: Path to the model (optional)
        
    Returns:
        QA pipeline
    """
    try:
        if model_path and os.path.exists(model_path):
            pipeline_qa = pipeline(
                "question-answering",
                model=model_path,
                tokenizer=model_path
            )
        else:
            pipeline_qa = pipeline(
                "question-answering",
                model=MODEL_NAME,
                tokenizer=MODEL_NAME
            )
        
        logger.info("QA pipeline created successfully")
        return pipeline_qa
        
    except Exception as e:
        logger.error(f"Error creating QA pipeline: {str(e)}")
        return None
