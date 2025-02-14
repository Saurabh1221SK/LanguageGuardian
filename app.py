import streamlit as st
import threading
from offense_detector import OffensiveDetector
from detector import AudioProcessor

st.set_page_config(
    page_title="Language Guardian",
    page_icon="🛡️",
    layout="wide"
)

@st.cache_resource
def load_components():
    return {
        'detector': OffensiveDetector(),
        'audio_processor': AudioProcessor()
    }

def analyze_text(text):
    offensive_words, highlighted = components['detector'].detect(text)
    return {
        'offensive': offensive_words,
        'highlighted': highlighted,
        'word_count': len(text.split())
    }

def realtime_audio_ui():
    st.write("## Real-time Speech Analysis")
    if 'listening' not in st.session_state:
        st.session_state.listening = False
    col1, col2 = st.columns(2)
    with col1:
        if st.button("Start Listening", disabled=st.session_state.listening):
            st.session_state.listening = True
            threading.Thread(target=components['audio_processor'].start_listening, daemon=True).start()
    with col2:
        if st.button("Stop Listening", disabled=not st.session_state.listening):
            components['audio_processor'].stop_listening()
            st.session_state.listening = False
    while not components['audio_processor'].audio_queue.empty():
        text = components['audio_processor'].audio_queue.get()
        results = analyze_text(text)
        st.write(f"**Detected Text:** {results['highlighted']}")
        if results['offensive']:
            st.error(f"Offensive words detected: {', '.join(results['offensive'])}")
        else:
            st.success("No offensive content detected")

def main():
    st.title("🛡️ Real-time Language Guardian")
    input_method = st.radio(
        "Choose Input Method:",
        ["Text Input", "Real-time Audio", "Upload Audio"],
        horizontal=True
    )
    if input_method == "Text Input":
        text = st.text_area("Enter text to analyze:", height=150)
        if st.button("Analyze Text"):
            results = analyze_text(text)
            st.markdown(f"**Results:** {results['highlighted']}")
            st.write(f"Detected offensive words: {results['offensive'] or 'None'}")
    elif input_method == "Real-time Audio":
        realtime_audio_ui()
    elif input_method == "Upload Audio":
        uploaded_file = st.file_uploader("Upload an audio file (WAV, MP3, etc.)", type=["wav", "mp3", "ogg", "flac"])
        if uploaded_file is not None:
            st.audio(uploaded_file, format='audio/wav')
            text = components['audio_processor'].process_audio_file(uploaded_file)
            st.write(f"**Extracted Text:** {text}")
            if text and text != "Could not understand the audio.":
                results = analyze_text(text)
                st.markdown(f"**Results:** {results['highlighted']}")
                st.write(f"Detected offensive words: {results['offensive'] or 'None'}")

if __name__ == "__main__":
    components = load_components()
    main()
