"""
Categorized Skill Dictionary for AI Resume Screening & Job Recommendation System.
Contains 100+ technical skills across major domains.
"""

SKILL_CATEGORIES = {
    "Programming": [
        "python", "java", "c++", "c", "c#", "javascript", "typescript", "go",
        "rust", "r", "scala", "kotlin", "swift", "php", "ruby", "bash", "shell",
        "powershell", "perl", "dart"
    ],
    "AI / ML": [
        "machine learning", "deep learning", "scikit-learn", "tensorflow", "pytorch",
        "keras", "xgboost", "lightgbm", "random forest", "svm", "support vector machine",
        "decision trees", "gradient boosting", "neural networks", "artificial neural networks",
        "reinforcement learning", "supervised learning", "unsupervised learning",
        "feature engineering", "model deployment", "mlops", "mlflow", "optuna", "hyperparameter tuning"
    ],
    "NLP": [
        "nlp", "natural language processing", "nltk", "spacy", "transformers", "bert",
        "roberta", "t5", "hugging face", "word2vec", "glove", "fasttext", "tokenization",
        "lemmatization", "stemming", "named entity recognition", "ner", "sentiment analysis",
        "text classification", "topic modeling", "lda", "llm", "large language models",
        "langchain", "llama", "gpt", "prompt engineering", "vector databases", "chromadb", "pinecone"
    ],
    "Computer Vision": [
        "computer vision", "opencv", "cnn", "convolutional neural networks", "yolo",
        "image processing", "object detection", "image segmentation", "resnet",
        "vgg", "transfer learning", "pil", "pillow", "mediapipe", "tesseract", "ocr",
        "optical character recognition", "face recognition", "pose estimation"
    ],
    "Data Science": [
        "sql", "pandas", "numpy", "scipy", "power bi", "tableau", "matplotlib",
        "seaborn", "plotly", "data analysis", "data visualization", "exploratory data analysis",
        "eda", "statistics", "data mining", "data cleaning", "big data", "pyspark",
        "apache spark", "excel", "statmodels"
    ],
    "Cloud & DevOps": [
        "docker", "kubernetes", "aws", "amazon web services", "gcp", "google cloud",
        "azure", "microsoft azure", "git", "github", "gitlab", "ci/cd", "jenkins",
        "terraform", "linux", "unix", "bash scripting", "cloud architecture", "serverless",
        "lambda", "s3", "ec2"
    ],
    "Web Development": [
        "html", "html5", "css", "css3", "react", "react.js", "vue", "vue.js",
        "angular", "fastapi", "flask", "django", "node.js", "express", "rest api",
        "graphql", "tailwind css", "bootstrap", "webhooks", "json", "xml", "websockets"
    ],
    "Databases": [
        "postgresql", "sqlite", "mysql", "mongodb", "redis", "elasticsearch",
        "firebase", "neo4j", "cassandra", "dynamodb", "oracle", "sql server",
        "orm", "sqlalchemy"
    ]
}

# Flattened list for fast matching
ALL_SKILLS = set()
SKILL_TO_CATEGORY = {}

for category, skills in SKILL_CATEGORIES.items():
    for skill in skills:
        ALL_SKILLS.add(skill.lower())
        SKILL_TO_CATEGORY[skill.lower()] = category

# Standardized canonical names display mapping
CANONICAL_SKILL_NAMES = {
    "python": "Python", "java": "Java", "c++": "C++", "c": "C", "c#": "C#",
    "javascript": "JavaScript", "typescript": "TypeScript", "go": "Go", "rust": "Rust",
    "r": "R", "scala": "Scala", "kotlin": "Kotlin", "swift": "Swift", "php": "PHP",
    "ruby": "Ruby", "bash": "Bash", "shell": "Shell", "powershell": "PowerShell",
    "machine learning": "Machine Learning", "deep learning": "Deep Learning",
    "scikit-learn": "Scikit-Learn", "tensorflow": "TensorFlow", "pytorch": "PyTorch",
    "keras": "Keras", "xgboost": "XGBoost", "lightgbm": "LightGBM", "random forest": "Random Forest",
    "svm": "SVM", "support vector machine": "Support Vector Machine",
    "decision trees": "Decision Trees", "gradient boosting": "Gradient Boosting",
    "neural networks": "Neural Networks", "reinforcement learning": "Reinforcement Learning",
    "nlp": "NLP", "natural language processing": "Natural Language Processing",
    "nltk": "NLTK", "spacy": "spaCy", "transformers": "Transformers", "bert": "BERT",
    "hugging face": "Hugging Face", "word2vec": "Word2Vec", "tokenization": "Tokenization",
    "named entity recognition": "Named Entity Recognition", "ner": "NER",
    "sentiment analysis": "Sentiment Analysis", "llm": "LLM", "large language models": "Large Language Models",
    "langchain": "LangChain", "gpt": "GPT", "computer vision": "Computer Vision",
    "opencv": "OpenCV", "cnn": "CNN", "yolo": "YOLO", "image processing": "Image Processing",
    "object detection": "Object Detection", "tesseract": "Tesseract", "ocr": "OCR",
    "sql": "SQL", "pandas": "Pandas", "numpy": "NumPy", "scipy": "SciPy",
    "power bi": "Power BI", "tableau": "Tableau", "matplotlib": "Matplotlib",
    "seaborn": "Seaborn", "plotly": "Plotly", "data analysis": "Data Analysis",
    "statistics": "Statistics", "excel": "Excel", "docker": "Docker",
    "kubernetes": "Kubernetes", "aws": "AWS", "gcp": "GCP", "azure": "Azure",
    "git": "Git", "github": "GitHub", "ci/cd": "CI/CD", "linux": "Linux",
    "html": "HTML", "css": "CSS", "react": "React", "react.js": "React",
    "vue": "Vue.js", "angular": "Angular", "fastapi": "FastAPI",
    "flask": "Flask", "django": "Django", "node.js": "Node.js", "rest api": "REST API",
    "postgresql": "PostgreSQL", "sqlite": "SQLite", "mysql": "MySQL",
    "mongodb": "MongoDB", "redis": "Redis", "elasticsearch": "Elasticsearch"
}

def get_canonical_skill_name(skill_lower: str) -> str:
    return CANONICAL_SKILL_NAMES.get(skill_lower.strip(), skill_lower.strip().title())
