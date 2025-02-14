# Language Guardian

Language Guardian is a real-time application designed to detect offensive language in both text and audio inputs. Utilizing a transformer-based model for hate speech detection and a custom CSV file of offensive words, the app highlights problematic language and provides immediate feedback.


## Features

- **Text Input:** Analyze any text by highlighting detected offensive words.
- **Real-time Audio:** Transcribe and analyze speech captured from your microphone in real time.
- **Upload Audio:** Upload audio files (WAV, MP3, OGG, FLAC, etc.) for transcription and offensive language detection.

## Installation

1. **Clone the Repository**

   ```bash
   git clone https://github.com/Saurabh1221SK/LanguageGuardian.git
   cd LanguageGuardian
   ```

2. **Install Dependencies**

   ```bash
   pip install -r requirements.txt
   ```

   > **Note:** Ensure that `ffmpeg` is installed on your system (required by pydub for audio conversion).  
   On Ubuntu, install with:
   ```bash
   sudo apt-get install ffmpeg
   ```
   On Windows, download and add ffmpeg to your system PATH.

## Usage

To start the application, run:

```bash
streamlit run app.py
```

Open the provided URL in your browser. You can choose between "Text Input", "Real-time Audio", or "Upload Audio" to analyze content for offensive language.

## File Structure

- **app.py**: The main Streamlit application file that handles user interaction.
- **detector.py**: Contains the `AudioProcessor` class that processes audio input and converts files to a compatible format.
- **offense_detector.py**: Implements the `OffensiveDetector` class for detecting offensive words using a transformer model and a custom CSV file.
- **list.csv**: CSV file containing offensive words. It should include a column named `Offensive_Word`.
- **requirements.txt**: Lists all the Python packages required by the project.

## Customization

- **Offensive Words List:**  
  Update `list.csv` with your own list of offensive words. Ensure the CSV file includes a column titled `Offensive_Word`.

- **Transformer Model:**  
  Change the model used by `OffensiveDetector` by modifying the `model_name` parameter in its constructor.

## Live Demo

Experience the application live at: [languageguardian.streamlit.app](https://languageguardian.streamlit.app)

## Contributing

Contributions are welcome! Feel free to open an issue or submit a pull request if you have ideas or improvements.
