# app.py

import streamlit as st
from io import BytesIO
import os

# Import functions from the other files
from resume_parser import extract_text_from_pdf, extract_text_from_docx, extract_skills
from matcher import get_match_results

def main():
    """
    The main function for the Streamlit application.
    """
    st.set_page_config(page_title="Resume Analyzer & Job Matcher", layout="wide")
    
    st.title("Resume Analyzer & Job Match Recommendation System")
    st.markdown("Easily analyze your resume against a job description to see how well you match and get personalized recommendations.")

    # Main content area with columns for input
    col1, col2 = st.columns([1, 1])

    # Resume Upload
    with col1:
        st.subheader("Upload Your Resume")
        resume_file = st.file_uploader("Choose a file", type=["pdf", "docx"])
        
        resume_text = ""
        if resume_file:
            file_extension = os.path.splitext(resume_file.name)[1]
            try:
                if file_extension.lower() == ".pdf":
                    st.info("Extracting text from PDF...")
                    resume_text = extract_text_from_pdf(BytesIO(resume_file.getvalue()))
                elif file_extension.lower() == ".docx":
                    st.info("Extracting text from DOCX...")
                    resume_text = extract_text_from_docx(BytesIO(resume_file.getvalue()))
                st.success("Resume uploaded and text extracted!")
            except Exception as e:
                st.error(f"Error processing the resume file: {e}")

    # Job Description Input
    with col2:
        st.subheader("Enter or Upload Job Description")
        job_desc_text = st.text_area("Paste the job description here:", height=300)
        
    st.markdown("---")

    # Analyze Button
    if st.button("Analyze Match", use_container_width=True, type="primary"):
        if not resume_text or not job_desc_text:
            st.warning("Please upload a resume and paste the job description to continue.")
        else:
            with st.spinner("Analyzing... This may take a moment."):
                # Get the analysis results from the matcher
                results = get_match_results(resume_text, job_desc_text)
            
            # Display results in a clean layout
            st.success("Analysis Complete!")
            st.markdown("### Match Report")
            
            # Display match percentage
            match_percentage = results['match_percentage']
            st.metric("Overall Fit Score", f"{match_percentage}%")
            
            st.markdown("---")
            
            # Display skills sections
            skills_col1, skills_col2 = st.columns(2)
            
            with skills_col1:
                st.markdown("#### Skills on Your Resume")
                if results['resume_skills']:
                    st.markdown(
                        f"**Found {len(results['resume_skills'])} skills:**"
                    )
                    st.markdown(f"```python\n{', '.join(results['resume_skills'])}\n```")
                else:
                    st.info("No skills found on your resume using our current list.")
                    
            with skills_col2:
                st.markdown("#### Job Description Skills")
                if results['job_desc_skills']:
                    st.markdown(
                        f"**Found {len(results['job_desc_skills'])} skills:**"
                    )
                    st.markdown(f"```python\n{', '.join(results['job_desc_skills'])}\n```")
                else:
                    st.info("No skills found in the job description using our current list.")
            
            st.markdown("---")

            # Display match and missing skills
            st.markdown("#### Matched Skills")
            if results['matched_skills']:
                st.success("✅ **Matched Skills:** " + ", ".join(results['matched_skills']))
            else:
                st.warning("No direct skill matches found.")

            st.markdown("#### Missing Skills")
            if results['missing_skills']:
                st.error("⚠️ **Missing Skills:** " + ", ".join(results['missing_skills']))
            else:
                st.success("Your resume contains all the identified skills from the job description!")

            st.markdown("---")
            
            # Display recommendations
            st.markdown("### Recommendations to Improve Your Resume")
            for rec in results['recommendations']:
                st.markdown(f"**•** {rec}")
    
    st.markdown("---")
    st.markdown("#### How to Run This Project")
    st.code("""
# 1. Install dependencies
pip install -r requirements.txt

# 2. Run the Streamlit app
streamlit run app.py
    """)

if __name__ == "__main__":
    main()