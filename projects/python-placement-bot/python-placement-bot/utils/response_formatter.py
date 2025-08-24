import re
import random
from typing import Dict, List
import logging

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class ResponseFormatter:
    """Format and enhance model responses for natural conversation"""
    
    def __init__(self):
        """Initialize the response formatter"""
        self.greeting_phrases = [
            "Great question!",
            "Let me help you with that.",
            "Here's what I can tell you:",
            "That's a fundamental concept in Python.",
            "Excellent question about Python!",
            "I'd be happy to explain that.",
        ]
        
        self.transition_phrases = [
            "Here's how it works:",
            "Let me break it down:",
            "To understand this:",
            "In Python:",
            "The key concept is:",
            "Simply put:",
        ]
        
        self.closing_phrases = [
            "Hope this helps!",
            "Let me know if you need clarification!",
            "Feel free to ask more questions!",
            "This should get you started.",
            "Good luck with your interview preparation!",
            "Keep practicing!",
        ]
        
        self.code_indicators = [
            "Here's an example:",
            "For instance:",
            "Sample code:",
            "Example implementation:",
            "Code example:",
            "Try this:",
        ]
    
    def format_response(self, raw_answer: str, question: str = None, confidence: float = 0.0) -> str:
        """
        Format and enhance the model response
        
        Args:
            raw_answer: Raw answer from the model
            question: Original question (optional)
            confidence: Model confidence score
            
        Returns:
            Formatted response string
        """
        try:
            # Clean the raw answer
            answer = self.clean_answer(raw_answer)
            
            # If confidence is too low, add a disclaimer
            if confidence < 0.3:
                answer = self.add_uncertainty_disclaimer(answer)
            
            # Add conversational elements
            formatted_response = self.add_conversational_elements(answer, question)
            
            # Format code blocks
            formatted_response = self.format_code_blocks(formatted_response)
            
            # Add final touches
            formatted_response = self.add_final_touches(formatted_response)
            
            return formatted_response
            
        except Exception as e:
            logger.error(f"Error formatting response: {str(e)}")
            return "I apologize, but I'm having trouble formatting my response. Please try asking the question again."
    
    def clean_answer(self, answer: str) -> str:
        """
        Clean and normalize the answer text
        
        Args:
            answer: Raw answer text
            
        Returns:
            Cleaned answer
        """
        if not answer:
            return "I don't have a specific answer for that question."
        
        # Remove extra whitespace
        answer = re.sub(r'\s+', ' ', answer.strip())
        
        # Fix common formatting issues
        answer = re.sub(r'\s+([.,:;!?])', r'\1', answer)
        answer = re.sub(r'([.!?])\s*([a-z])', r'\1 \2', answer)
        
        # Ensure proper sentence capitalization
        sentences = answer.split('. ')
        sentences = [s.strip().capitalize() for s in sentences if s.strip()]
        answer = '. '.join(sentences)
        
        return answer
    
    def add_conversational_elements(self, answer: str, question: str = None) -> str:
        """
        Add conversational elements to make the response more natural
        
        Args:
            answer: Cleaned answer
            question: Original question
            
        Returns:
            Response with conversational elements
        """
        response_parts = []
        
        # Add greeting (sometimes)
        if random.random() < 0.3:  # 30% chance
            greeting = random.choice(self.greeting_phrases)
            response_parts.append(greeting)
        
        # Add transition (sometimes)
        if random.random() < 0.4:  # 40% chance
            transition = random.choice(self.transition_phrases)
            response_parts.append(transition)
        
        # Add the main answer
        response_parts.append(answer)
        
        # Add closing (sometimes)
        if random.random() < 0.2:  # 20% chance
            closing = random.choice(self.closing_phrases)
            response_parts.append(closing)
        
        return ' '.join(response_parts)
    
    def format_code_blocks(self, text: str) -> str:
        """
        Format code blocks in the response
        
        Args:
            text: Text containing code
            
        Returns:
            Text with formatted code blocks
        """
        # Look for code patterns
        code_patterns = [
            r'(\w+\([^)]*\))',  # Function calls
            r'(def \w+[^:]*:)',  # Function definitions
            r'(class \w+[^:]*:)',  # Class definitions
            r'(import \w+)',  # Import statements
            r'(from \w+ import \w+)',  # From-import statements
            r'(\w+\.\w+\([^)]*\))',  # Method calls
            r'(\w+\[.*?\])',  # List/dict access
        ]
        
        # Add code indicators before code blocks
        for pattern in code_patterns:
            if re.search(pattern, text):
                # Add code indicator if not already present
                if not any(indicator in text for indicator in self.code_indicators):
                    if random.random() < 0.5:
                        indicator = random.choice(self.code_indicators)
                        # Insert before the first code pattern
                        text = re.sub(pattern, f"{indicator} \\1", text, count=1)
                break
        
        return text
    
    def add_uncertainty_disclaimer(self, answer: str) -> str:
        """
        Add disclaimer for low-confidence answers
        
        Args:
            answer: Original answer
            
        Returns:
            Answer with uncertainty disclaimer
        """
        disclaimers = [
            "I'm not entirely certain, but ",
            "Based on my understanding, ",
            "From what I know, ",
            "I believe ",
            "It seems that ",
        ]
        
        disclaimer = random.choice(disclaimers)
        return disclaimer + answer.lower()
    
    def add_final_touches(self, response: str) -> str:
        """
        Add final formatting touches
        
        Args:
            response: Response text
            
        Returns:
            Final formatted response
        """
        # Ensure proper spacing
        response = re.sub(r'\s+', ' ', response.strip())
        
        # Ensure the response ends with proper punctuation
        if response and response[-1] not in '.!?':
            response += '.'
        
        # Capitalize first letter
        if response:
            response = response[0].upper() + response[1:]
        
        return response
    
    def create_fallback_response(self, question: str = None) -> str:
        """
        Create a fallback response when the model fails
        
        Args:
            question: Original question
            
        Returns:
            Fallback response
        """
        fallback_responses = [
            "I'm sorry, I don't have enough information to answer that specific question.",
            "That's a great question, but I need more context to provide a helpful answer.",
            "I'm not sure about that particular topic. Could you rephrase the question?",
            "That question is beyond my current knowledge. Try asking about basic Python concepts.",
            "I'd love to help, but I need a clearer question to provide a good answer.",
        ]
        
        base_response = random.choice(fallback_responses)
        
        suggestions = [
            "You might want to try asking about Python basics like variables, functions, or data structures.",
            "Consider asking about specific Python concepts like lists, dictionaries, or loops.",
            "Try asking about Python programming fundamentals or interview preparation topics.",
            "Feel free to ask about Python syntax, data types, or common programming patterns.",
        ]
        
        suggestion = random.choice(suggestions)
        return f"{base_response} {suggestion}"
    
    def enhance_code_examples(self, text: str) -> str:
        """
        Enhance code examples in the response
        
        Args:
            text: Text containing code examples
            
        Returns:
            Text with enhanced code examples
        """
        # Add explanatory text around code
        code_explanations = [
            "This code demonstrates:",
            "Here's how you can implement it:",
            "The following example shows:",
            "You can use this approach:",
            "This pattern is useful for:",
        ]
        
        # Look for code patterns and add explanations
        if re.search(r'def \w+|class \w+|import \w+', text):
            if random.random() < 0.6:  # 60% chance
                explanation = random.choice(code_explanations)
                # Insert explanation before code
                text = re.sub(r'(def \w+|class \w+|import \w+)', f"{explanation} \\1", text, count=1)
        
        return text

def format_python_response(answer: str, question: str = None, confidence: float = 0.0) -> str:
    """
    Convenience function to format Python programming responses
    
    Args:
        answer: Raw answer from model
        question: Original question
        confidence: Model confidence score
        
    Returns:
        Formatted response
    """
    formatter = ResponseFormatter()
    return formatter.format_response(answer, question, confidence)