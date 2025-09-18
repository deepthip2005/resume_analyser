# matcher.py

from sentence_transformers import SentenceTransformer, util
from sklearn.feature_extraction.text import TfidfVectorizer
from resume_parser import clean_text, extract_skills, get_all_skills

# Load a pre-trained Sentence Transformer model
model = SentenceTransformer('all-MiniLM-L6-v2')

def get_similarity_score(resume_text, job_desc_text, method='sentence_transformer'):
    """
    Calculates the similarity score between resume and job description text.
    
    Args:
        resume_text (str): The cleaned resume text.
        job_desc_text (str): The cleaned job description text.
        method (str): The method to use for similarity ('sentence_transformer' or 'tfidf').
        
    Returns:
        float: A similarity score between 0 and 1.
    """
    if method == 'tfidf':
        # TF-IDF approach
        vectorizer = TfidfVectorizer()
        tfidf_matrix = vectorizer.fit_transform([resume_text, job_desc_text])
        cosine_sim = (tfidf_matrix * tfidf_matrix.T).A
        return cosine_sim[0, 1]
    
    elif method == 'sentence_transformer':
        # Sentence Transformer approach for semantic similarity
        embeddings = model.encode([resume_text, job_desc_text], convert_to_tensor=True)
        cosine_score = util.pytorch_cos_sim(embeddings[0], embeddings[1])
        return cosine_score.item()
        
    return 0.0

def get_match_results(resume_text, job_desc_text):
    """
    Analyzes resume and job description to provide a detailed match report.

    Args:
        resume_text (str): The raw text from the resume.
        job_desc_text (str): The raw text from the job description.

    Returns:
        dict: A dictionary containing match percentage, extracted skills, 
              missing skills, and recommendations.
    """
    # Clean and extract skills from both texts
    cleaned_resume = clean_text(resume_text)
    cleaned_job_desc = clean_text(job_desc_text)
    
    resume_skills = set(extract_skills(cleaned_resume))
    job_desc_skills = set(extract_skills(cleaned_job_desc))

    # Identify matched and missing skills
    matched_skills = list(resume_skills.intersection(job_desc_skills))
    missing_skills = list(job_desc_skills.difference(resume_skills))
    
    # Calculate match percentage
    try:
        match_score = get_similarity_score(cleaned_resume, cleaned_job_desc)
        match_percentage = round(match_score * 100, 2)
    except Exception as e:
        print(f"Error calculating similarity score: {e}")
        match_percentage = 0
        
    # Generate recommendations
    recommendations = []
    if missing_skills:
        recommendations.append(f"Consider adding the following skills to your resume: {', '.join(missing_skills)}.")
    if match_percentage < 50:
        recommendations.append("Your resume could be better tailored to this job. Focus on highlighting skills and experiences directly relevant to the job description.")
    
    # Check for broader skill categories to recommend
    all_skills_dict = get_all_skills()
    for category, skills in all_skills_dict.items():
        if any(s in missing_skills for s in skills):
            recommendations.append(f"Try to add more skills related to the '{category}' domain, as these are prominent in the job description.")

    # If no recommendations, provide a generic positive message
    if not recommendations:
        recommendations.append("Your resume is a great fit for this job! Continue to highlight your strengths.")
        
    return {
        "match_percentage": match_percentage,
        "matched_skills": matched_skills,
        "missing_skills": missing_skills,
        "recommendations": recommendations,
        "resume_skills": list(resume_skills),
        "job_desc_skills": list(job_desc_skills)
    }

if __name__ == '__main__':
    # This block is for demonstration purposes.
    # It shows how to use the matcher directly.
    
    # Dummy resume and job description texts
    resume_text = """
    I have extensive experience in Python and machine learning. 
    I've worked with TensorFlow, Scikit-learn, and have a good understanding of NLP. 
    My work also involves cloud platforms like AWS and databases like SQL.
    """
    job_desc_text = """
    We are looking for a Data Scientist with strong Python skills.
    The ideal candidate has experience with TensorFlow and PyTorch for deep learning.
    Familiarity with NLP techniques and cloud services like AWS is a plus.
    """
    
    print("--- Test Matcher ---")
    results = get_match_results(resume_text, job_desc_text)
    
    print(f"Match Percentage: {results['match_percentage']}%")
    print(f"Matched Skills: {results['matched_skills']}")
    print(f"Missing Skills: {results['missing_skills']}")
    print("Recommendations:")
    for rec in results['recommendations']:
        print(f"- {rec}")