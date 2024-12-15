import spacy
from sentence_transformers import SentenceTransformer, util
import fitz
from concurrent.futures import ThreadPoolExecutor

def pdf_to_text(pdf_path):
    doc = fitz.open(pdf_path)
    text = ""
    for page_num in range(doc.page_count):
        page = doc[page_num]
        text += page.get_text()
    doc.close()
    return text

model = SentenceTransformer("paraphrase-mpnet-base-v2")
nlp = spacy.load("en_core_web_sm")

def text_to_sentences(text):
    doc = nlp(text)
    sentences = [sent.text.strip() for sent in doc.sents if sent.text.strip()]
    return sentences

def remove_stop_words(text):
    doc = nlp(text)
    return " ".join([token.text for token in doc if not token.is_stop])

def calculate_line_similarity(job_line, resume_lines):
    job_embedding = model.encode(job_line, convert_to_tensor=True)
    resume_embeddings = model.encode(resume_lines, convert_to_tensor=True)
    similarities = util.cos_sim(job_embedding, resume_embeddings)
    return similarities.max().item()

def calculate_max_line_similarity_parallel(job_description_lines, resume_lines):
    max_similarities = []
    with ThreadPoolExecutor() as executor:
        results = list(executor.map(
            lambda job_line: calculate_line_similarity(job_line, resume_lines),
            job_description_lines
        ))
        max_similarities.extend(results)
    return max_similarities

job_description = """Key Responsibilities
Risk Assessment & Analysis:

Conduct regular assessments to identify vulnerabilities in the organization's networks, systems, and applications.
Develop strategies to mitigate identified risks.
Monitoring & Incident Response:

Monitor network traffic for unusual activity and respond to cybersecurity incidents promptly.
Investigate breaches, document incidents, and perform root cause analysis.
Security Implementation:

Deploy and maintain firewalls, intrusion detection systems (IDS), and endpoint protection solutions.
Configure security policies, ensuring compliance with industry standards and regulations.
Training & Awareness:

Educate employees about cybersecurity best practices and the importance of data security.
Develop training materials and conduct workshops to promote a security-conscious culture.
Compliance & Documentation:

Ensure adherence to legal and regulatory requirements such as GDPR, CCPA, HIPAA, or ISO 27001.
Maintain up-to-date documentation on security policies, protocols, and procedures.
Threat Intelligence:

Stay updated with the latest cyber threats, vulnerabilities, and technologies.
Recommend and implement advanced tools and methods to enhance security.
Key Qualifications:
Educational Background: Bachelor’s degree in Computer Science, Information Technology, Cybersecurity, or related field. (Master’s preferred)
Certifications: Industry-recognized certifications like CISSP, CISM, CEH, CompTIA Security+, or similar.
Experience:
Minimum of [X years] of experience in cybersecurity or a related role.
Hands-on experience with penetration testing, vulnerability management tools, and SIEM solutions.
Technical Skills:
Proficiency in tools like Wireshark, Metasploit, or Nessus.
Knowledge of programming/scripting languages like Python, Java, or PowerShell.
Familiarity with cloud security (AWS, Azure, GCP) and endpoint protection systems.
Experience with security frameworks like NIST, MITRE ATT&CK, or COBIT.
Soft Skills:
Strong analytical and problem-solving abilities.
Excellent communication skills to convey technical information to non-technical stakeholders.
Ability to work under pressure and manage multiple priorities."""

resume_text = pdf_to_text("/Users/arunkaul/Desktop/SIH-AI-REPO/SIH-AI-REPO/marketing.pdf")
job_description_sentences = text_to_sentences(job_description)
resume_sentences = text_to_sentences(resume_text)

job_description_sentences_filtered = [remove_stop_words(sentence) for sentence in job_description_sentences]
resume_sentences_filtered = [remove_stop_words(sentence) for sentence in resume_sentences]
resume_sentences_filtered = [line for line in resume_sentences_filtered if len(line) > 20]

print("Filtered Resume Lines: ", resume_sentences_filtered)

line_similarities = calculate_max_line_similarity_parallel(job_description_sentences_filtered, resume_sentences_filtered)

for i, (job_sentence, similarity) in enumerate(zip(job_description_sentences_filtered, line_similarities)):
    print(f"Job Sentence {i+1}: {job_sentence}")
    print(f"Maximum Similarity: {similarity:.4f}\n")

average_similarity = sum(line_similarities) / len(line_similarities)
print(f"Average Similarity: {average_similarity:.4f}")
