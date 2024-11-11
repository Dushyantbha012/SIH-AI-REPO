import os
import tempfile
import time
import numpy as np
import scipy.io.wavfile as wavfile
import sounddevice as sd
from gtts import gTTS
import playsound
import sqlite3
import speech_recognition as sr
from transformers import pipeline as hf_pipeline
import torch
import PyPDF2
from groq import Groq

os.environ["TOKENIZERS_PARALLELISM"] = "false"

asr_model = hf_pipeline("automatic-speech-recognition", model="openai/whisper-base", device=0 if torch.cuda.is_available() else -1)

class InterviewAssistant:
    def __init__(self, api_key, pdf_path, db_path="interview_answers.db", n_q=2, duration=30):
        self.api_key = api_key
        self.client = Groq(api_key=api_key)
        self.pdf_path = pdf_path
        self.db_path = db_path
        self.resume = self.extract_text_from_pdf(pdf_path)
        self.n_q = n_q
        self.duration = duration
        self.initialize_database()

    def initialize_database(self):
        self.conn = sqlite3.connect(self.db_path)
        self.cursor = self.conn.cursor()
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS answers (
                question TEXT PRIMARY KEY,
                answer TEXT
            )
        """)
        self.conn.commit()

    def extract_text_from_pdf(self, pdf_path):
        text = ""
        with open(pdf_path, 'rb') as file:
            reader = PyPDF2.PdfReader(file)
            for page in reader.pages:
                text += page.extract_text() + "\n"
        return text.strip()

    def retrieve_all_q_a(self):
        self.cursor.execute("SELECT question, answer FROM answers")
        results = self.cursor.fetchall()
        return {question: answer for question, answer in results}

    def store_answer(self, question, answer):
        self.cursor.execute("INSERT OR REPLACE INTO answers (question, answer) VALUES (?, ?)", (question, answer))
        self.conn.commit()

    def text_to_speech(self, text, lang='en'):
        tts = gTTS(text=text, lang=lang, slow=False)
        with tempfile.NamedTemporaryFile(delete=True, suffix='.mp3') as temp_audio_file:
            tts.save(temp_audio_file.name)
            playsound.playsound(temp_audio_file.name)

    def record_answer(self, threshold=0.1, fs=44100):
        print("Recording your answer...")
        audio = []
        start_time = time.time()
        while (time.time() - start_time) < self.duration:
            data = sd.rec(int(fs * 3), samplerate=fs, channels=1, blocking=True)
            audio.append(data)
            if np.max(np.abs(data)) < threshold:
                print("Silence detected, stopping recording.")
                break
        audio = np.concatenate(audio, axis=0)
        print("Recording finished.")
        return audio

    def convert_audio_to_text(self, audio_data, fs=44100):
        with tempfile.NamedTemporaryFile(suffix=".wav", delete=True) as temp_wav_file:
            wavfile.write(temp_wav_file.name, fs, (audio_data * 32767).astype(np.int16))
            transcription = asr_model(temp_wav_file.name, return_timestamps=True)["text"]
            return transcription

    def generate_question(self, context):
        prompt = f"""
        You are an interviewer. Based on the candidate's resume, which contains the following project details: {self.resume}, 
        and the previous questions that have already been asked: {context}, please generate a follow-up technical or professional question.
        
        Your response should ONLY be the next interview question without any additional explanation.
        """
        
        chat_completion = self.client.chat.completions.create(
            messages=[
                {"role": "system", "content": "You are a formal interviewer thinking through your questions before asking."},
                {"role": "user", "content": prompt}
            ],
            model="llama3-8b-8192",
            max_tokens=1000
        )
        return chat_completion.choices[0].message.content.strip()

    def analyze_responses(self, list_n):
        prompt = f"""
        Based on the following list of question-answer pairs, create an overall analysis of the person's performance.
        Provide specific areas where they can improve. Offer constructive feedback in a professional tone, focusing on actionable improvements in communication, technical understanding, or any other relevant aspects.
        
        Question-Answer pairs: {list_n}
        """
        
        chat_completion = self.client.chat.completions.create(
            messages=[
                {"role": "system", "content": "You are an evaluator providing a performance review."},
                {"role": "user", "content": prompt}
            ],
            model="llama3-8b-8192",
            max_tokens=500
        )
        return chat_completion.choices[0].message.content.strip()

    def conduct_interview(self):
        context_old = self.retrieve_all_q_a()
        
        for _ in range(self.n_q):
            question = self.generate_question(context_old)
            self.text_to_speech(question)

            audio_answer = self.record_answer()
            answer_text = self.convert_audio_to_text(audio_answer)

            if answer_text:
                self.store_answer(question, answer_text)
        
        all_ques_ans = self.retrieve_all_q_a()
        list_n = [{'Question': q, 'Answer': a} for q, a in all_ques_ans.items()]
        print(list_n)
        insight = self.analyze_responses(list_n)
        print(insight)
        self.text_to_speech(insight)

    def close(self):
        self.conn.close()

    def delete_database(self):
        self.close()
        if os.path.exists(self.db_path):
            os.remove(self.db_path)
            print(f"Database '{self.db_path}' has been deleted.")
        else:
            print("Database file not found.")

api_key = "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"
pdf_path = "ak.pdf"

interview_assistant = InterviewAssistant(api_key, pdf_path, n_q=2, duration=1000)
interview_assistant.conduct_interview()
interview_assistant.delete_database()
