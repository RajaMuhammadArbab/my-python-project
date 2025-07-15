import os
import glob
import fitz 
import docx
import re
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import tkinter as tk
from tkinter import filedialog, messagebox
from tkinter import *


def extract_text_from_pdf(file_path):
    text = ""
    try:
        doc = fitz.open(file_path)
        for page in doc:
            text += page.get_text()
    except Exception as e:
        print(f"Error reading {file_path}: {e}")
    return text

def extract_text_from_docx(file_path):
    text = ""
    try:
        doc = docx.Document(file_path)
        for para in doc.paragraphs:
            text += para.text + "\n"
    except Exception as e:
        print(f"Error reading {file_path}: {e}")
    return text

def clean_text(text):
    text = re.sub(r'[^a-zA-Z0-9\s]', '', text)
    text = re.sub(r'\s+', ' ', text)
    return text.lower()


def extract_sections(text):
    sections = {"skills": "", "education": "", "experience": ""}
    text = text.lower()

    section_patterns = {
        "skills": re.compile(r"(skills|SKILLS|technical skills|key skills|technical proficiency|expertise)[\\s:\\n]*", re.IGNORECASE),
        "education": re.compile(r"(education|EDUCATION|academic background|educational qualification)[\\s:\\n]*", re.IGNORECASE),
        "experience": re.compile(r"(experience|work experience|WORK EXPEIENCE|EXPERIENCE|professional experience)[\\s:\\n]*", re.IGNORECASE)
    }

    lines = text.splitlines()
    current_section = None
    buffer = {"skills": [], "education": [], "experience": []}

    for line in lines:
        line = line.strip().lower()

        for section, pattern in section_patterns.items():
            if pattern.match(line):
                current_section = section
                break
        else:
            if current_section:
                
                if re.match(r"^[a-z ]{1,20}[:\\-]?$", line) and not section_patterns[current_section].match(line):
                    current_section = None
                else:
                    buffer[current_section].append(line)

    for key in sections:
        sections[key] = " ".join(buffer[key]).strip()

    return sections



def load_resumes(folder_path):
    resume_texts = {}
    for file_path in glob.glob(os.path.join(folder_path, '*')):
        if file_path.endswith(".pdf"):
            text = extract_text_from_pdf(file_path)
        elif file_path.endswith(".docx"):
            text = extract_text_from_docx(file_path)
        else:
            continue
        cleaned = clean_text(text)
        sections = extract_sections(text)
        resume_texts[os.path.basename(file_path)] = {
            "text": cleaned,
            "skills": sections["skills"],
            "education": sections["education"],
            "experience": sections["experience"]
        }
    return resume_texts

def load_job_description(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        jd_text = f.read()
    return clean_text(jd_text)


def rank_resumes(resume_texts, jd_text):
    documents = [r["text"] for r in resume_texts.values()] + [jd_text]
    vectorizer = TfidfVectorizer()
    vectors = vectorizer.fit_transform(documents)
    similarity_scores = cosine_similarity(vectors[-1], vectors[:-1]).flatten()
    ranked_results = sorted(
        zip(resume_texts.keys(), similarity_scores, resume_texts.values()),
        key=lambda x: x[1], reverse=True
    )
    return ranked_results


def save_results(results):
    project_folder = os.path.dirname(os.path.abspath(__file__))
    output_path = os.path.join(project_folder, "results.csv")

    df = pd.DataFrame([
        {
            "Resume File": r[0],
            "Match Score": round(r[1] * 100, 2),
            "Skills": r[2]["skills"],
            "Education": r[2]["education"],
            "Experience": r[2]["experience"]
        } for r in results
    ])

    df.to_csv(output_path, index=False)
    print(f"✅ Results saved to: {output_path}")


def run_gui():
    def browse_resumes():
        folder = filedialog.askdirectory()
        resume_entry.delete(0, END)
        resume_entry.insert(0, folder)

    def browse_jd():
        file_path = filedialog.askopenfilename(filetypes=[("Text files", "*.txt")])
        jd_entry.delete(0, END)
        jd_entry.insert(0, file_path)

    def start_ranking():
        resume_folder = resume_entry.get()
        jd_file = jd_entry.get()
        if not resume_folder or not jd_file:
            messagebox.showerror("Input Error", "Please provide both resume folder and job description file.")
            return
        resumes = load_resumes(resume_folder)
        jd = load_job_description(jd_file)
        results = rank_resumes(resumes, jd)
        save_results(results)
        messagebox.showinfo("Success", "Resume screening completed! Results saved to results.csv")

    root = Tk()
    root.title("AI Resume Screener")
    root.geometry("500x200")

    Label(root, text="Select Resume Folder").pack()
    resume_entry = Entry(root, width=50)
    resume_entry.pack()
    Button(root, text="Browse", command=browse_resumes).pack()

    Label(root, text="Select Job Description (.txt)").pack()
    jd_entry = Entry(root, width=50)
    jd_entry.pack()
    Button(root, text="Browse", command=browse_jd).pack()

    Button(root, text="Start Screening", command=start_ranking).pack(pady=10)

    root.mainloop()


if __name__ == "__main__":
    run_gui()