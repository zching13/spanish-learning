import React, { useState } from 'react';
import { AudioRecorder } from 'react-audio-voice-recorder';
import axios from 'axios';

function App() {
  const [transcript, setTranscript] = useState('');
  const [corrections, setCorrections] = useState([]);

  const addAudioElement = (blob) => {
    const formData = new FormData();
    formData.append('audio', blob, 'recording.webm');
    
    // Send to Flask backend
    axios.post('http://localhost:5000/analyze-spanish', formData)
      .then(response => {
        setTranscript(response.data.transcript);
        setCorrections(response.data.corrections);
      })
      .catch(error => console.error('Error:', error));
  };

  return (
    <div style={{ padding: '20px' }}>
      <h1>Spanish Learning Assistant</h1>
      <AudioRecorder 
        onRecordingComplete={addAudioElement}
        audioTrackConstraints={{
          noiseSuppression: true,
          echoCancellation: true,
        }}
      />
      
      {transcript && (
        <div>
          <h3>What you said:</h3>
          <p>{transcript}</p>
        </div>
      )}
      
      {corrections.length > 0 && (
        <div>
          <h3>Corrections:</h3>
          {corrections.map((correction, index) => (
            <div key={index} style={{ marginBottom: '10px', padding: '10px', backgroundColor: '#f0f0f0' }}>
              <p><strong>You said:</strong> {correction.original}</p>
              <p><strong>Correct version:</strong> {correction.corrected}</p>
              <p><strong>Explanation:</strong> {correction.explanation}</p>
            </div>
          ))}
        </div>
      )}
    </div>
  );
}

export default App;
