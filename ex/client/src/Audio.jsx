import React, { useState, useRef } from 'react';
import { Upload, Volume2, Pause, Play, VolumeX } from 'lucide-react';
import './Audio.css';

const Audio = () => {
  const [selectedFile, setSelectedFile] = useState(null);
  const [isConverting, setIsConverting] = useState(false);
  const [textContent, setTextContent] = useState('');
  const [isPlaying, setIsPlaying] = useState(false);
  const [isMuted, setIsMuted] = useState(false);
  
  // Reference to store the speech synthesis utterance
  const speechUtteranceRef = useRef(null);

  const handleFileChange = async (event) => {
    const file = event.target.files[0];
    if (file && file.type === 'application/pdf') {
      setSelectedFile(file);
      setTextContent('');
      // Here you would implement PDF text extraction
      // For demo, we'll use a placeholder text
      setTextContent("This is the amazon financial report. In this report we can see Executive Summary, Income Statement Analysis, Balance Sheet Analysis, Cash Flow Statement Analysis, Key Financial Ratios, Revenue & Cost Breakdown, Market & Competitive Analysis, Debt & Capital Structure, Financial Forecasts, Risks & Challenges, Management Strategy & Outlook*`");
    } else {
      alert('Please upload a PDF file');
    }
  };

  const handleConversion = () => {
    if (!textContent) return;
    
    // Stop any ongoing speech
    if (speechUtteranceRef.current) {
      window.speechSynthesis.cancel();
    }

    // Create a new speech utterance
    const utterance = new SpeechSynthesisUtterance(textContent);
    speechUtteranceRef.current = utterance;

    // Configure speech settings
    utterance.rate = 1.0;  // Speed of speech (0.1 to 10)
    utterance.pitch = 1.0; // Pitch of voice (0 to 2)
    utterance.volume = isMuted ? 0 : 1;

    // Handle speech events
    utterance.onstart = () => setIsPlaying(true);
    utterance.onend = () => {
      setIsPlaying(false);
      speechUtteranceRef.current = null;
    };
    utterance.onerror = (event) => {
      console.error('Speech synthesis error:', event);
      setIsPlaying(false);
      speechUtteranceRef.current = null;
    };

    // Start speaking
    window.speechSynthesis.speak(utterance);
  };

  const togglePlayPause = () => {
    if (isPlaying) {
      window.speechSynthesis.pause();
      setIsPlaying(false);
    } else {
      if (speechUtteranceRef.current) {
        window.speechSynthesis.resume();
      } else {
        handleConversion();
      }
      setIsPlaying(true);
    }
  };

  const toggleMute = () => {
    setIsMuted(!isMuted);
    if (speechUtteranceRef.current) {
      speechUtteranceRef.current.volume = isMuted ? 1 : 0;
    }
  };

  const stopSpeaking = () => {
    window.speechSynthesis.cancel();
    speechUtteranceRef.current = null;
    setIsPlaying(false);
  };

  // Clean up on component unmount
  React.useEffect(() => {
    return () => {
      if (speechUtteranceRef.current) {
        window.speechSynthesis.cancel();
      }
    };
  }, []);

  return (
    <div className="converter-container1">
    <div className="converter-container">
      <h1 className="converter-title">PDF to Audiobook Converter</h1>
      
      <div className="upload-section">
        <label className="file-input-label">
          <input
            type="file"
            accept=".pdf"
            onChange={handleFileChange}
            className="file-input"
          />
          <Upload className="upload-icon" />
          <span>{selectedFile ? selectedFile.name : 'Choose PDF file'}</span>
        </label>
      </div>

      {textContent && (
        <div className="text-preview">
          <h3>Extracted Text Preview:</h3>
          <p>{textContent.slice(0, 200)}...</p>
        </div>
      )}

      <div className="audio-controls">
        <button
          className={`play-button ${!textContent ? 'disabled' : ''}`}
          onClick={togglePlayPause}
          disabled={!textContent}
        >
          {isPlaying ? <Pause className="control-icon" /> : <Play className="control-icon" />}
          {isPlaying ? 'Pause' : 'Play'}
        </button>

        <button className="mute-button" onClick={toggleMute}>
          {isMuted ? <VolumeX className="control-icon" /> : <Volume2 className="control-icon" />}
        </button>

        {isPlaying && (
          <button className="stop-button" onClick={stopSpeaking}>
            Stop
          </button>
        )}
      </div>
    </div>
    </div>
  );
};

export default Audio;