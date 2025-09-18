# resume_parser.py

import docx
import PyPDF2
from io import BytesIO
from nltk.corpus import stopwords
import re
import nltk

# Download NLTK stopwords and punkt if not already present
try:
    nltk.data.find('corpora/stopwords')
    nltk.data.find('tokenizers/punkt')
except nltk.downloader.DownloadError:
    print("Downloading NLTK data...")
    nltk.download('stopwords')
    nltk.download('punkt')
    print("Download complete.")


def get_all_skills():
    """
    A simple function to get a list of predefined technical skills.
    In a real-world application, this could be a more dynamic list
    or a model-based skill extractor.
    """
    return {
        "programming": ["python", "java", "c++", "javascript", "react", "angular", "node.js"],
        "databases": ["sql", "mysql", "postgresql", "mongodb", "firebase"],
        "cloud": ["aws", "azure", "google cloud", "docker", "kubernetes"],
        "data_science": ["machine learning", "deep learning", "nlp", "pandas", "numpy", "tensorflow", "pytorch", "scikit-learn"],
        "web_dev": ["html", "css", "django", "flask", "spring"],
        "os": ["linux", "windows", "macos"],
        "tools": ["git", "github", "jira", "agile", "scrum", "vscode"]
    }

def extract_text_from_pdf(file_path):
    """
    Extracts text from a PDF file.

    Args:
        file_path (BytesIO): A BytesIO object of the uploaded PDF file.

    Returns:
        str: The extracted text.
    """
    text = ""
    try:
        pdf_reader = PyPDF2.PdfReader(file_path)
        for page in pdf_reader.pages:
            text += page.extract_text()
    except Exception as e:
        print(f"Error extracting PDF text: {e}")
    return text

def extract_text_from_docx(file_path):
    """
    Extracts text from a DOCX file.

    Args:
        file_path (BytesIO): A BytesIO object of the uploaded DOCX file.

    Returns:
        str: The extracted text.
    """
    text = ""
    try:
        doc = docx.Document(file_path)
        for para in doc.paragraphs:
            text += para.text + "\n"
    except Exception as e:
        print(f"Error extracting DOCX text: {e}")
    return text

def clean_text(text):
    """
    Cleans and normalizes text by converting to lowercase, removing
    punctuation, and removing stopwords.

    Args:
        text (str): The raw input text.

    Returns:
        str: The cleaned text.
    """
    # Convert to lowercase
    text = text.lower()
    # Remove punctuation and special characters
    text = re.sub(r'[^\w\s]', '', text)
    # Remove extra spaces
    text = re.sub(r'\s+', ' ', text).strip()
    
    stop_words = set(stopwords.words('english'))
    words = text.split()
    filtered_words = [word for word in words if word not in stop_words]
    
    return " ".join(filtered_words)

def extract_skills(text, predefined_skills_dict=None):
    """
    Extracts a list of skills from the text based on a predefined dictionary.

    Args:
        text (str): The cleaned text.
        predefined_skills_dict (dict): A dictionary of skills categorized by domain.

    Returns:
        list: A list of unique skills found in the text.
    """
    if predefined_skills_dict is None:
        predefined_skills_dict = get_all_skills()
        
    found_skills = set()
    for category in predefined_skills_dict.values():
        for skill in category:
            if re.search(r'\b' + re.escape(skill) + r'\b', text):
                found_skills.add(skill)
                
    return sorted(list(found_skills))

if __name__ == '__main__':
    # This block is for demonstration and testing purposes.
    # It will not run when imported by app.py.
    
    # Create a dummy resume text
    dummy_resume = """
    John Doe
    I am an experienced Python developer with a strong background in web development. 
    My skills include Python, JavaScript, and React. I have worked with SQL and AWS. 
    I am passionate about machine learning and have experience with TensorFlow. 
    I also use Git for version control.
    """
    
    # Clean the text
    cleaned_resume = clean_text(dummy_resume)
    
    # Extract skills
    skills = extract_skills(cleaned_resume)
    
    print("--- Test Resume Parser ---")
    print(f"Original Text:\n{dummy_resume}")
    print(f"Cleaned Text:\n{cleaned_resume}")
    print(f"Extracted Skills:\n{skills}")