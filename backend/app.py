from flask import Flask, request, jsonify
from flask_cors import CORS
import speech_recognition as sr
import language_tool_python
import io
import tempfile
import os

app = Flask(__name__)
CORS(app)  # Allow React to talk to Flask

# Initialize speech recognizer and grammar checker
recognizer = sr.Recognizer()
spanish_tool = language_tool_python.LanguageTool("es")

@app.route("/analyze-spanish", methods=["POST"])
def analyze_spanish():
    try:
        # Get audio file from request
        audio_file = request.files["audio"]
        
        # Save temporarily to process
        with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as tmp_file:
            audio_file.save(tmp_file.name)
            
            # Convert audio to text
            with sr.AudioFile(tmp_file.name) as source:
                audio_data = recognizer.record(source)
                try:
                    # Use Google's Spanish recognition
                    transcript = recognizer.recognize_google(audio_data, language="es-ES")
                except sr.UnknownValueError:
                    return jsonify({"error": "Could not understand audio"}), 400
                except sr.RequestError:
                    return jsonify({"error": "Speech recognition service error"}), 500
        
        # Clean up temp file
        os.unlink(tmp_file.name)
        
        # Check for grammar errors
        matches = spanish_tool.check(transcript)
        
        corrections = []
        for match in matches:
            corrections.append({
                "original": match.context,
                "corrected": match.replacements[0] if match.replacements else "No suggestion",
                "explanation": f"Error: {match.message}"
            })
        
        return jsonify({
            "transcript": transcript,
            "corrections": corrections
        })
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True, port=5000)
