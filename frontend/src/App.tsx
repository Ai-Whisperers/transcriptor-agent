import React, { useState } from 'react';

const App: React.FC = () => {
  const [file, setFile] = useState<File | null>(null);
  const [model, setModel] = useState('large-v3');
  const [provider, setProvider] = useState('groq');
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState<string>('');
  const [error, setError] = useState<string>('');

  const handleFileChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    if (e.target.files && e.target.files[0]) {
      setFile(e.target.files[0]);
      setError('');
    }
  };

  const handleTranscribe = async () => {
    if (!file) {
      setError('Please select an audio file first.');
      return;
    }

    setLoading(true);
    setResult('');
    setError('');

    const formData = new FormData();
    formData.append('file', file);

    try {
      const response = await fetch(`/api/transcribe?model=${model}&provider=${provider}`, {
        method: 'POST',
        body: formData,
      });

      if (!response.ok) {
        throw new Error(`Error: ${response.statusText}`);
      }

      const data = await response.json();
      setResult(data.text);
    } catch (err: any) {
      setError(err.message || 'Something went wrong during transcription.');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="container">
      <header>
        <h1>🎙️ Transcriptor</h1>
        <p>AI-Powered Audio-to-Text with Whisper large-v3</p>
      </header>

      <main>
        <div className="card">
          <div className="form-group">
            <label>Select Audio File</label>
            <input type="file" accept="audio/*" onChange={handleFileChange} />
          </div>

          <div className=\"form-group\">
            <label>Transcription Provider</label>
            <select value={provider} onChange={(e) => setProvider(e.target.value)}>
              <option value=\"groq\">Groq (Free & Fast)</option>
              <option value=\"openai\">OpenAI (Premium)</option>
              <option value=\"local\">Local (No API Key)</option>
            </select>
          </div>

          <div className=\"form-group\">
            <label>Whisper Model</label>
            <select value={model} onChange={(e) => setModel(e.target.value)}>
              <option value="tiny">Tiny (Fastest)</option>
              <option value="base">Base</option>
              <option value="small">Small</option>
              <option value="medium">Medium</option>
              <option value="large-v3">Large-v3 (Best Quality)</option>
            </select>
          </div>

          <button 
            onClick={handleTranscribe} 
            disabled={loading || !file}
            className={loading ? 'loading' : ''}
          >
            {loading ? 'Transcribing...' : 'Transcribe Audio'}
          </button>

          {error && <div className="error-message">{error}</div>}
        </div>

        {result && (
          <div className="result-card">
            <h3>Transcription Result</h3>
            <div className="result-text">{result}</div>
            <button className="copy-btn" onClick={() => navigator.clipboard.writeText(result)}>
              Copy to Clipboard
            </button>
          </div>
        )}
      </main>

      <footer>
        <p>Built with React + FastAPI + Whisper</p>
      </footer>
    </div>
  );
};

export default App;
