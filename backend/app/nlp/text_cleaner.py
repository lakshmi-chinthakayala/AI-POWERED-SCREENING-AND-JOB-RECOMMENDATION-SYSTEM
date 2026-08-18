"""
Text Preprocessing and Cleaning Module.
Provides NLP text normalization, stopword filtering, punctuation removal, and tokenization.
"""

import re
import string

# Stopwords set (fallback if NLTK is loading)
BASIC_STOPWORDS = {
    "a", "about", "above", "after", "again", "against", "all", "am", "an", "and", "any",
    "are", "aren't", "as", "at", "be", "because", "been", "before", "being", "below",
    "between", "both", "but", "by", "can't", "cannot", "could", "couldn't", "did",
    "didn't", "do", "does", "doesn't", "doing", "don't", "down", "during", "each",
    "few", "for", "from", "further", "had", "hadn't", "has", "hasn't", "have", "haven't",
    "having", "he", "he'd", "he'll", "he's", "her", "here", "here's", "hers", "herself",
    "him", "himself", "his", "how", "how's", "i", "i'd", "i'll", "i'm", "i've", "if",
    "in", "into", "is", "isn't", "it", "it's", "its", "itself", "let's", "me", "more",
    "most", "mustn't", "my", "myself", "no", "nor", "not", "of", "off", "on", "once",
    "only", "or", "other", "ought", "our", "ours", "ourselves", "out", "over", "own",
    "same", "shan't", "she", "she'd", "she'll", "she's", "should", "shouldn't", "so",
    "some", "such", "than", "that", "that's", "the", "their", "theirs", "them",
    "themselves", "then", "there", "there's", "these", "they", "they'd", "they'll",
    "they're", "they've", "this", "those", "through", "to", "too", "under", "until",
    "up", "very", "was", "wasn't", "we", "we'd", "we'll", "we're", "we've", "were",
    "weren't", "what", "what's", "when", "when's", "where", "where's", "which", "while",
    "who", "who's", "whom", "why", "why's", "with", "won't", "would", "wouldn't", "you",
    "you'd", "you'll", "you're", "you've", "your", "yours", "yourself", "yourselves"
}

def clean_text(text: str) -> str:
    """
    Cleans raw text: converts to lowercase, removes non-printable characters, 
    replaces multiple spaces, standardizes newlines.
    """
    if not text:
        return ""
    
    # Convert to lowercase
    text = text.lower()
    
    # Replace tabs and newlines with spaces
    text = re.sub(r'[\r\n\t]+', ' ', text)
    
    # Replace non-ascii chars safely
    text = re.sub(r'[^\x00-\x7F]+', ' ', text)
    
    # Remove multiple spaces
    text = re.sub(r'\s+', ' ', text).strip()
    
    return text

def preprocess_for_tfidf(text: str) -> str:
    """
    Normalizes text specifically for TF-IDF Vectorization:
    removes punctuation, numbers, and stopwords.
    """
    text = clean_text(text)
    
    # Remove special punctuation but keep spaces
    text = re.sub(r'[^\w\s]', ' ', text)
    
    # Tokenize words
    tokens = text.split()
    
    # Filter stopwords and short tokens
    cleaned_tokens = [t for t in tokens if t not in BASIC_STOPWORDS and len(t) > 1 and not t.isdigit()]
    
    return " ".join(cleaned_tokens)

def extract_email(text: str) -> str:
    """Extracts email address using regex."""
    email_pattern = r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}'
    match = re.search(email_pattern, text)
    return match.group(0) if match else ""

def extract_phone(text: str) -> str:
    """Extracts phone number using regex."""
    phone_pattern = r'(?:(?:\+?\d{1,3}[-.\s]?)?\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}|\+\d{10,12})'
    match = re.search(phone_pattern, text)
    return match.group(0) if match else ""

def extract_linkedin(text: str) -> str:
    """Extracts LinkedIn profile URL."""
    pattern = r'(?:https?://)?(?:www\.)?linkedin\.com/in/[a-zA-Z0-9_-]+'
    match = re.search(pattern, text, re.IGNORECASE)
    return match.group(0) if match else ""

def extract_github(text: str) -> str:
    """Extracts GitHub profile URL."""
    pattern = r'(?:https?://)?(?:www\.)?github\.com/[a-zA-Z0-9_-]+'
    match = re.search(pattern, text, re.IGNORECASE)
    return match.group(0) if match else ""
