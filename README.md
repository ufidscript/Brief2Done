# Brief2Done 📋

**Turn confusing assignment briefs into clear, actionable steps using local AI.**

Brief2Done is a student-focused application that helps users understand assignment instructions, identify submission requirements, and plan their work.

It combines Python-based information extraction with a locally running AI model powered by Ollama.

## The Problem

Students often receive assignment briefs containing multiple instructions, deadlines, formatting requirements, and word limits.

Understanding these requirements and organizing them into actionable steps can be challenging.

Brief2Done aims to simplify this process.

## Features

- **Assignment analysis:** Summarizes the main task.
- **Word-count detection:** Identifies common word-count ranges.
- **Submission format detection:** Recognizes PDF, DOCX, and DOC references.
- **Deadline detection:** Recognizes common weekday deadlines.
- **Requirements checklist:** Organizes the main task and detected submission constraints.
- **Optional suggestions:** Provides AI-generated ideas to help students plan their work.
- **Local AI processing:** Uses Ollama to run Gemma locally.

## Tech Stack

- Python
- Gradio
- Ollama
- Gemma 3 (1B)
- Regular expressions (Regex)

## Getting Started

### Prerequisites

Install:

- Python 3.13
- Ollama
- Git (optional)

Download the `gemma3:1b` model:

```bash
ollama pull gemma3:1b
```

### Installation

Clone the repository:

```bash
git clone https://github.com/YOUR_USERNAME/Brief2Done.git
cd Brief2Done
```

Create a virtual environment:

```bash
python -m venv .venv
```

Install dependencies:

```bash
.venv\Scripts\python.exe -m pip install -r requirements.txt
```

### Run the Application

Ensure Ollama is running locally, then execute:

```bash
.venv\Scripts\python.exe app.py
```

Open the local Gradio URL shown in your terminal.

## How It Works

1. The student pastes an assignment brief.
2. Python extracts recognizable word-count ranges, submission formats, and weekday deadlines.
3. The application sends the brief to a locally running Gemma model through Ollama.
4. Gemma generates a main-task summary and optional suggestions.
5. Brief2Done displays the extracted information and a requirements checklist.

## Example

**Input:**

> Write a report explaining process management, memory management, and file management in operating systems. Submit the report as a PDF of 1500–2000 words by Friday.

**Detected details:**

- Word count: 1500–2000 words
- File format: PDF
- Deadline: Friday

**Main task:** Explain process management, memory management, and file management in operating systems.

## Current Limitations

Brief2Done is an early-stage prototype.

- Word-count, file-format, and deadline detection use simple patterns and may miss unusual wording.
- Weekday deadlines are not converted into calendar dates.
- AI-generated summaries and suggestions may be incomplete or inaccurate.
- The requirements checklist does not yet separate every instruction into an independently verified task.
- The application currently supports pasted text rather than uploaded documents.
- Users must install and run Ollama locally.

Students should always verify results against their original assignment instructions.

## Future Improvements

- Support PDF and DOCX assignment uploads.
- Improve requirement extraction and verification.
- Add interactive checklists.
- Support more deadline formats.
- Improve accessibility and mobile responsiveness.

## Hackathon

Built as a prototype for the Hacktoberfest 2026 Week 3 “Slow and Steady” DEV Challenge.

## License

License to be added.
