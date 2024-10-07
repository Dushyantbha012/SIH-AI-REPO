from groq import Groq
import PyPDF2


def extract_text_from_pdf(pdf_path):
    text = ""
    with open(pdf_path, 'rb') as file:
        reader = PyPDF2.PdfReader(file)
        for page in reader.pages:
            text += page.extract_text() + "\n"
    return text.strip()


def get_bot_response(user_input):
    client = Groq(api_key="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")
    chat_completion = client.chat.completions.create(
    messages=[
        {
            "role": "system",
            "content": "You Are An Profile Analyser Analyse The Interviews Profile Professionaly"
        },
        {
            "role": "user",
            "content": f"Respond to this prompt {user_input} using this data {extract_text_from_pdf('ak.pdf')}",
        }
    ],
    model="llama3-8b-8192",
    max_tokens=1000)
    return chat_completion.choices[0].message.content

job = """
    Objectives of this role
Collaborate with product design and engineering teams to develop an understanding of needs
Research and devise innovative statistical models for data analysis
Communicate findings to all stakeholders
Enable smarter business processes by using analytics for meaningful insights
Keep current with technical and industry developments
Responsibilities
Serve as lead data strategist to identify and integrate new datasets that can be leveraged through our product capabilities, and work closely with the engineering team in the development of data products
Execute analytical experiments to help solve problems across various domains and industries
Identify relevant data sources and sets to mine for client business needs, and collect large structured and unstructured datasets and variables
Devise and utilize algorithms and models to mine big-data stores; perform data and error analysis to improve models; clean and validate data for uniformity and accuracy
Analyze data for trends and patterns, and interpret data with clear objectives in mind
Implement analytical models in production by collaborating with software developers and machine-learning engineers
Required skills and qualifications
Seven or more years of experience in data science
Proficiency with data mining, mathematics, and statistical analysis
Advanced experience in pattern recognition and predictive modeling
Experience with Excel, PowerPoint, Tableau, SQL, and programming languages (ex: Java/Python, SAS)
Ability to work effectively in a dynamic, research-oriented group that has several concurrent projects
Preferred skills and qualifications
Bachelor’s degree (or equivalent) in statistics, applied mathematics, or related discipline
Two or more years of project management experience
Professional certification
"""
qu = f"""

Job Description:

    You will critically and in a high level analyze a job seeker's profile based on the following job description and evaluate it across several key parameters. Provide an overall rating out of 100, considering the alignment of the job seeker’s profile which is given to you with the job description. The parameters you should consider are: Skills Match, Experience, Education, Accomplishments, Cultural Fit, Geographical Fit, Career Progression, Availability, Industry Knowledge, and Recommendations/References.

---

Job Description:
{job}

---

Instructions:

1. Skills Match (0-20 points):
   - Evaluate how well the job seeker's technical and soft skills align with the job requirements.

2. Experience (0-20 points):
   - Consider the relevance of the job seeker's years of experience, prior roles, and industry experience to the job description.

3. Education (0-10 points):
   - Assess the relevance of the job seeker’s educational background, including degrees and certifications, to the job requirements.

4. Accomplishments (0-10 points):
   - Evaluate the significance of the job seeker's professional achievements and project experience in relation to the job description.

5. Cultural Fit (0-10 points):
   - Determine how well the job seeker’s values and adaptability align with the company’s culture and work environment.

6. Geographical Fit (0-5 points):
   - Consider the job seeker’s location in relation to the job location and their willingness to relocate, if necessary.

7. Career Progression (0-10 points):
   - Evaluate the job seeker’s career growth trajectory and their ability to take on increasing responsibilities.

8. Availability (0-5 points):
   - Assess the job seeker’s availability to start work and their willingness to commit to the company.

9. Industry Knowledge (0-5 points):
   - Evaluate the job seeker’s understanding of industry trends and market conditions, and their ability to contribute valuable insights.

10. Recommendations/References (0-5 points):
    - Assess the quality and relevance of the job seeker’s recommendations or references.

---
Output format:

Overall Rating: [Sum of all points out of 100]

Strengths:
- [Strength 1]
- [Strength 2]
- ...

Weaknesses:
- [Weakness 1]
- [Weakness 2]
- ...

Overall Assessment:
[Provide a brief summary of the job seeker’s strengths and weaknesses in relation to the job description, highlighting the key factors that influenced the overall rating.]

"""

print(get_bot_response(qu))
