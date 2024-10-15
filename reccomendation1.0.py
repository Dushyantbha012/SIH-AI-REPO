from groq import Groq
import PyPDF2


class ProfileAnalyzer:
    def __init__(self, pdf_path, api_key):
        self.pdf_path = pdf_path
        self.api_key = api_key
        self.client = Groq(api_key=self.api_key)

    def extract_text_from_pdf(self):
        text = ""
        with open(self.pdf_path, 'rb') as file:
            reader = PyPDF2.PdfReader(file)
            for page in reader.pages:
                text += page.extract_text() + "\n"
        return text.strip()

    def generate_query(self, job_description):
        return f"""
        Job Description:

        You will critically and in a high level analyze a job seeker's profile based on the following job description and evaluate it across several key parameters. Provide an overall rating out of 100, considering the alignment of the job seeker’s profile which is given to you with the job description. The parameters you should consider are: Skills Match, Experience, Education, Accomplishments, Cultural Fit, Geographical Fit, Career Progression, Availability, Industry Knowledge, and Recommendations/References.

        ---

        Job Description:
        {job_description}

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

    def get_bot_response(self, job_description = ""):
        query = self.generate_query(job_description)
        user_data = self.extract_text_from_pdf()
        chat_completion = self.client.chat.completions.create(
            messages=[
                {
                    "role": "system",
                    "content": "You Are A Profile Analyzer, Analyze The Interview's Profile Professionally"
                },
                {
                    "role": "user",
                    "content": f"Respond to this prompt {query} using this data {user_data}",
                }
            ],
            model="llama3-8b-8192",
            max_tokens=1000
        )
        return chat_completion.choices[0].message.content


analyzer = ProfileAnalyzer(pdf_path='ak.pdf', api_key="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")
response = analyzer.get_bot_response()#Add job decription in this function
print(response)
