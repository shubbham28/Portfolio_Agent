# portfolio_voice_agent/app.py
import streamlit as st
import time
import json
import os
import yaml
from openai import OpenAI
import base64
import uuid
import tempfile
import streamlit.components.v1 as components


api_key = yaml.safe_load(open("credentials.yaml"))["openai_api_key"]
client = OpenAI(api_key=api_key)

# Load CV data from local file
with open("cv.json") as f:
    cv_data = json.load(f)
    
    
st.set_page_config(page_title="Portfolio Voice Agent", layout="wide")
st.markdown("""
    <style>
    .st-emotion-cache-1avcm0n { padding-top: 1rem; }
    .stMarkdown ul { margin-bottom: 0.25rem; }
    .stButton>button {
        width: 75%;
        height: 3em;
        margin: 0.05em 0;
        font-size: 1.1em;
    }
    .block-container {
        padding-top: 1rem !important;
        padding-bottom: 1rem !important;
    }
    </style>
""", unsafe_allow_html=True)
st.title("🎙️ Voice-enabled Portfolio Agent of Shubbham Gupta")

# ---- Initialize session state ----
for key in ["selected_section", "audio_base64", "audio_suffix", "section_cache", "subsection_cache", "selected_subsection", "clicked_section"]:
    if key not in st.session_state:
        st.session_state[key] = None if "cache" not in key else {}

# ---- Helper functions ----
# Function to safely convert section text into a string
def stringify(text):
    if isinstance(text, dict):
        return "\n".join([f"{k}: {v}" for k, v in text.items()])
    elif isinstance(text, list):
        return "\n".join(map(str, text))
    return str(text)

# Function to generate third-person paragraph summary (use "Shubham" or "he")
def generate_paragraph(text):
    text = stringify(text)
    prompt = (
        "Rewrite the following CV section as a third-person paragraph using 'Shubbham' or 'he' instead of 'the individual' or 'they':\n"
        + text
    )
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.7
    )
    return response.choices[0].message.content.strip()

# Function to generate third-person bullet points (use "Shubham" or "he")
def generate_bullets(text):
    text = stringify(text)
    prompt = (
        "Summarize the following CV section in 3-5 bullet points using 'Shubbham' or 'he' instead of 'the individual' or 'they':\n"
        + text
    )
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.7
    )
    return response.choices[0].message.content.strip()

# Function to use OpenAI's TTS to play text and return base64-encoded audio
def speak_with_openai(text):
    speech_file = tempfile.NamedTemporaryFile(delete=False, suffix=".mp3")
    response = client.audio.speech.create(
        model="tts-1",
        voice="nova",
        input=text
    )
    response.stream_to_file(speech_file.name)
    with open(speech_file.name, "rb") as f:
        audio_bytes = f.read()
    return base64.b64encode(audio_bytes).decode()

def load_section_summary(section, entries):
    if section in st.session_state["section_cache"]:
        return
    # Build text with selected fields depending on section type
    summary_lines = []
    if isinstance(entries, list):
        for entry in entries:
            if section == "education":
                summary_lines.append(
                    f"Degree: {entry.get('degree')}, Institution: {entry.get('institution')}, Details: {entry.get('details')}"
                )
            elif section == "experience":
                summary_lines.append(
                    f"Role: {entry.get('role')} at {entry.get('organization')}, Details: {stringify(entry.get('details'))}"
                )
            elif section == "projects":
                summary_lines.append(
                    f"Project: {entry.get('name')}, Details: {stringify(entry.get('details'))}"
                )
            elif section == "publications":
                summary_lines.append(
                    f"Title: {entry.get('title')}, Abstract: {entry.get('abstract')}"
                )
            else:
                summary_lines.append(stringify(entry))
    else:
        summary_lines.append(stringify(entries))

    full_summary = "\n".join(summary_lines)

    # Generate and cache
    paragraph = generate_paragraph(full_summary)
    bullets = generate_bullets(full_summary)
    audio = speak_with_openai(paragraph)

    st.session_state["section_cache"][section] = {
        "paragraph": paragraph,
        "bullets": bullets,
        "audio": audio,
        "audio_id":section
    }


def load_subsection(section, key, text):
    if key in st.session_state["subsection_cache"]:
        return
    paragraph = generate_paragraph(text)
    audio = speak_with_openai(paragraph)
    bullets = generate_bullets(text)
    st.session_state["subsection_cache"][key] = {
        "paragraph": paragraph,
        "audio": audio,
        "bullets": bullets,
        "audio_id":key
    }


# ---- Layout ----
sidebar, output = st.columns([0.75, 2.25])

with sidebar:
#     st.subheader("👤 Name")
#     st.markdown(cv_data.get("name", "Not provided"))

    st.subheader(" Contact details")
    contact_data = cv_data.get("contact", {})
    if isinstance(contact_data, dict):
        for key, value in contact_data.items():
            st.markdown(f"- **{key.capitalize()}**: {value}")
    else:
        st.markdown(contact_data)

    # Filter out 'name' and 'contact' from options
    sections = [k for k in cv_data.keys() if k not in ["name", "contact"]]

    st.markdown("#### Click on section to know more", unsafe_allow_html=True)
    st.markdown("<hr style='margin-top: -0.5rem;'>", unsafe_allow_html=True)


    for section in sections:
        if st.button(f"🎧 {section.title()}", key=section):
            st.session_state["clicked_section"] = section
            st.session_state["selected_subsection"] = None
            st.session_state["selected_section"] = section
            st.rerun()

# ---- Display section and subsection audio & content ----
if st.session_state.get("selected_section"):
    section = st.session_state["selected_section"]
    load_section_summary(section, cv_data[section])
    summary = st.session_state["section_cache"][section]

    with output:
        # Two persistent placeholders
        section_audio_slot = st.empty()
        subsection_audio_slot = st.empty()

        # If no subsection, show section audio
#         if not st.session_state.get("selected_subsection"):
        subsection_audio_slot.empty()
        html = f"""
        <audio id="{summary['audio_id']}" autoplay controls style="width:100%;">
        <source src="data:audio/mp3;base64,{summary['audio']}" type="audio/mp3">
        </audio>
        """
        section_audio_slot.html(html)

        # Show summary bullets
        st.markdown("### Summary")
        for bullet in summary["bullets"].split("\n"):
            st.markdown(bullet)

        # Subsection buttons
        if isinstance(cv_data[section], list) and section not in ["interests"]:
            st.markdown("### For more details")
            for entry in cv_data[section]:
                if section == "education":
                    key = entry["degree"]
                elif section == "experience":
                    key = f"{entry['role']} – {entry['organization']}"
                elif section == "projects":
                    key = entry["name"]
                elif section == "publications":
                    key = entry["title"]
                else:
                    key = entry.get("name", "Detail")

                if st.button(key, key=key):
                    st.session_state["selected_subsection"] = (section, key)
                    st.rerun()

# ---- Display selected subsection ----
if st.session_state.get("selected_subsection"):
    section, key = st.session_state["selected_subsection"]
    load_subsection(section, key, stringify(next(e for e in cv_data[section] if (
        e.get("degree") == key or e.get("name") == key or e.get("title") == key or f"{e.get('role')} – {e.get('organization')}" == key))))
    sub = st.session_state["subsection_cache"][key]

    with output:
#         section_audio_slot = st.empty()
        subsection_audio_slot = st.empty()

        # Clear section audio, show subsection audio
#         section_audio_slot.empty()
        html = f"""
        <audio id="{sub['audio_id']}" autoplay controls style="width:100%;">
          <source src="data:audio/mp3;base64,{sub['audio']}" type="audio/mp3">
        </audio>
        """
        subsection_audio_slot.html(html)

        st.markdown("##### Bullet Points")
        for bullet in sub["bullets"].split("\n"):
            st.markdown(bullet)



