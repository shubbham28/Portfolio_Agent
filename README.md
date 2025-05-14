# 🎙️ Voice-enabled Portfolio Agent of Shubbham Gupta

An AI-powered, voice-enabled personal portfolio app built with **Streamlit**, **OpenAI GPT-4 + TTS**, and **interactive UI components**. This project turns your CV into an engaging chat-style experience — complete with narrated summaries and interactive buttons for exploring each section.

---

## ✨ Features

- ✅ Clean, dark-themed **Streamlit UI**
- ✅ **Voice playback** (OpenAI TTS-1) for each section and subsection
- ✅ **Third-person summaries** powered by OpenAI GPT
- ✅ **Bullet-point explanations** for clear readability
- ✅ **Subsection drilldown** for Education, Experience, Projects, and Publications
- ✅ **Caching** to avoid redundant API calls
- ✅ **Responsive layout** with smart section toggles

---

## 🧱 Project Structure

```
portfolio-voice-agent/
│
├── app.py                  # Main Streamlit application
├── cv.json	            # All structured CV content
├── config.yaml             # OpenAI credentials (preferred over .env)
├── requirements.txt        # Python dependencies
└── README.md               # You're reading it!
```

---

## 🧠 How It Works

1. **CV is parsed** from `cv.json`
2. User selects a section (like Education or Projects)
3. A **third-person summary** is generated via OpenAI GPT
4. Text-to-speech audio is generated and **auto-plays**
5. The user can click into sub-sections to explore more
6. Bullet summaries are shown for all parts

---

## 📦 Installation

1. **Clone the repo**

```bash
git clone https://github.com/shubbham28/portfolio-voice-agent.git
cd portfolio-voice-agent
```

2. **Install dependencies**

```bash
pip install -r requirements.txt
```

3. **Set your OpenAI API key using `config.yaml`**

```yaml
# config.yaml
openai_api_key: your_openai_key_here
```

4. **Run the app**

```bash
streamlit run app.py
```

---

## 🧾 Example CV Structure (in `cv_data.json`)

```json
{
  "name": "Shubham Gupta",
  "contact": {
    "email": "shubham.gupta28@gmail.com",
    ...
  },
  "education": [...],
  "experience": [...],
  "projects": [...],
  "publications": [...]
}
```

---

## 🚀 Tech Stack

- [Streamlit](https://streamlit.io/)
- [OpenAI GPT](https://platform.openai.com/)
- [OpenAI TTS-1](https://platform.openai.com/docs/guides/text-to-speech)
- Python 3.10+

---

## 💡 Future Enhancements

- 🎨 Improve visual styling and use better graphics/icons for sections
- 📝 Download CV summaries as PDF/audio
- 🗣️ Add voice **input** to navigate via speech
- 🌐 Add support for multilingual narration

---

## 🙌 Acknowledgements

Developed by **Shubbham Gupta** — a Data Scientist passionate about AI agents, Bayesian modeling, and interactive storytelling with tech.

---

## 📄 License

MIT License — see [LICENSE](LICENSE) for details.
