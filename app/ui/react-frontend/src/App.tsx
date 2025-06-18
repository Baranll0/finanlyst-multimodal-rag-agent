import React, { useState, useRef, useEffect } from 'react';
import './App.css';
import { FaChartLine, FaHistory, FaCog, FaInfoCircle } from 'react-icons/fa';
import { MdAttachFile, MdPlayArrow } from 'react-icons/md';

interface Message {
  sender: 'user' | 'bot';
  text: string;
  details?: string; // Teknik detaylar için
}

const API_ENDPOINT = 'http://localhost:5000/api/chat';

const EXAMPLE_QUESTIONS = [
  'Bu PDF dosyasını özetle',
  'CSV dosyasındaki en yüksek değeri bul',
  'Görseldeki metni çıkar ve ana fikri yaz',
  'Yüklediğim dokümandan anahtar kelimeleri çıkar',
  'Finansal verileri analiz et ve öneri sun',
];

const MENU = [
  { label: 'Chat', icon: <FaChartLine /> },
  { label: 'Geçmiş', icon: <FaHistory /> },
  { label: 'Ayarlar', icon: <FaCog /> },
  { label: 'Hakkında', icon: <FaInfoCircle /> },
];

const SEARCH_TYPES = [
  { label: 'Normal Arama', value: 'normal' },
  { label: 'Akıllı Arama (Reasoning)', value: 'reasoning' },
  { label: 'Vektör Tabanlı Arama', value: 'vector' },
];

const MODELS = [
  { label: 'Llama-3-8B', value: 'llama-3-8b' },
  { label: 'GPT-3.5', value: 'gpt-3.5' },
  { label: 'GPT-4', value: 'gpt-4' },
];

// Tablo olup olmadığını tespit eden fonksiyon
function isTable(text: string): boolean {
  // JSON array veya satır/sütunlu metin (ör: | ile ayrılmış veya CSV)
  try {
    const parsed = JSON.parse(text);
    if (Array.isArray(parsed) && parsed.length > 0 && typeof parsed[0] === 'object') {
      return true;
    }
  } catch {}
  // Basit CSV veya pipe tablosu
  const lines = text.trim().split('\n');
  if (lines.length > 1 && (lines[0].includes(',') || lines[0].includes('|'))) {
    return true;
  }
  return false;
}

// Tabloyu render eden fonksiyon
function RenderTable({ text }: { text: string }) {
  // JSON array ise
  try {
    const parsed = JSON.parse(text);
    if (Array.isArray(parsed) && parsed.length > 0 && typeof parsed[0] === 'object') {
      const headers = Object.keys(parsed[0]);
      return (
        <div className="table-wrapper">
          <table className="ai-table">
            <thead>
              <tr>
                {headers.map(h => <th key={h}>{h}</th>)}
              </tr>
            </thead>
            <tbody>
              {parsed.map((row: any, i: number) => (
                <tr key={i}>
                  {headers.map(h => <td key={h}>{row[h]}</td>)}
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      );
    }
  } catch {}
  // CSV veya pipe tablosu
  const lines = text.trim().split('\n');
  const delimiter = lines[0].includes('|') ? '|' : ',';
  const rows = lines.map(l => l.split(delimiter).map(cell => cell.trim()));
  return (
    <div className="table-wrapper">
      <table className="ai-table">
        <thead>
          <tr>
            {rows[0].map((h, i) => <th key={i}>{h}</th>)}
          </tr>
        </thead>
        <tbody>
          {rows.slice(1).map((row, i) => (
            <tr key={i}>
              {row.map((cell, j) => <td key={j}>{cell}</td>)}
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}

function App() {
  const [messages, setMessages] = useState<Message[]>([
    { sender: 'bot', text: 'Merhaba! PDF, CSV veya görsel yükleyebilir ve mesaj gönderebilirsiniz.', details: '' }
  ]);
  const [input, setInput] = useState('');
  const [file, setFile] = useState<File | null>(null);
  const [fileName, setFileName] = useState<string>('');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string>('');
  const [searchType, setSearchType] = useState('normal');
  const [model, setModel] = useState('llama-3-8b');
  const [temperature, setTemperature] = useState(0.2);
  const messagesEndRef = useRef<HTMLDivElement | null>(null);
  const [showDetails, setShowDetails] = useState<{[key:number]: boolean}>({});
  const [dragActive, setDragActive] = useState(false);

  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [messages]);

  const handleSend = async () => {
    setError('');
    if (!input.trim() && !file) {
      setError('Lütfen önce bir dosya yükleyin veya mesaj yazın.');
      return;
    }
    setLoading(true);
    setMessages(prev => [...prev, { sender: 'user', text: input || (file ? file.name : '') }]);
    try {
      const formData = new FormData();
      formData.append('message', input);
      if (file) {
        formData.append('file', file);
      } else if (fileName) {
        const prevFile = await fetch(fileName).then(r => r.blob());
        formData.append('file', prevFile, fileName.split('/').pop() || 'file');
      }
      formData.append('search_type', searchType);
      formData.append('model', model);
      formData.append('temperature', temperature.toString());
      const res = await fetch(API_ENDPOINT, {
        method: 'POST',
        body: formData
      });
      const data = await res.json();
      setMessages(prev => [...prev, {
        sender: 'bot',
        text: data.reply || 'Cevap alınamadı.',
        details: data.details || 'Oluşturulan Sorgu: MATCH (n) RETURN n LIMIT 1\nİşlem Süresi: 1.2s' // Dummy detay
      }]);
    } catch (err) {
      setMessages(prev => [...prev, { sender: 'bot', text: 'Bir hata oluştu. Lütfen backend ve API endpointini kontrol edin.', details: 'Hata: Backend bağlantısı yok.' }]);
    }
    setInput('');
    setLoading(false);
    setFile(null);
  };

  const handleInputKeyDown = (e: React.KeyboardEvent<HTMLInputElement>) => {
    if (e.key === 'Enter') handleSend();
  };

  const handleFileChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    if (e.target.files && e.target.files[0]) {
      setFile(e.target.files[0]);
      setFileName(URL.createObjectURL(e.target.files[0]));
      setMessages([
        { sender: 'bot', text: 'Dosya yüklendi: ' + e.target.files[0].name + '. Şimdi mesaj gönderebilirsiniz.' }
      ]);
      setInput('');
      setError('');
    }
  };

  const handleDrag = (e: React.DragEvent<HTMLDivElement>) => {
    e.preventDefault();
    e.stopPropagation();
    if (e.type === 'dragenter' || e.type === 'dragover') setDragActive(true);
    else if (e.type === 'dragleave') setDragActive(false);
  };

  const handleDrop = (e: React.DragEvent<HTMLDivElement>) => {
    e.preventDefault();
    e.stopPropagation();
    setDragActive(false);
    if (e.dataTransfer.files && e.dataTransfer.files[0]) {
      setFile(e.dataTransfer.files[0]);
    }
  };

  return (
    <div className="finapp-root dark-theme">
      <aside className="finapp-sidebar">
        <div className="finapp-logo"><FaChartLine size={32} /> Finansal Agent</div>
        <nav className="finapp-menu">
          {MENU.map((item, i) => (
            <div key={i} className="finapp-menu-item">{item.icon}<span>{item.label}</span></div>
          ))}
        </nav>
      </aside>
      <main className="finapp-main">
        <div className="finapp-chat-header">Finansal Agent Sohbet</div>
        <div className="finapp-chat-timeline">
          {messages.map((msg, idx) => (
            <div key={idx} className={`finapp-chat-bubble ${msg.sender}`}>{msg.text}</div>
          ))}
          {loading && <div className="finapp-chat-bubble bot">Yanıt bekleniyor...</div>}
          <div ref={messagesEndRef} />
        </div>
        <div className="finapp-input-row">
          <div
            className={`finapp-upload-zone${dragActive ? ' active' : ''}`}
            onDragEnter={handleDrag}
            onDragOver={handleDrag}
            onDragLeave={handleDrag}
            onDrop={handleDrop}
          >
            <label htmlFor="file-upload" className="finapp-upload-btn">
              <MdAttachFile size={28} />
              <span>+</span>
            </label>
            <input
              id="file-upload"
              type="file"
              accept=".pdf,.csv,image/*"
              style={{ display: 'none' }}
              onChange={handleFileChange}
            />
            {file && <span className="finapp-file-info">{file.name}</span>}
          </div>
          <input
            className="finapp-input"
            type="text"
            placeholder="Mesajınızı yazın..."
            value={input}
            onChange={e => setInput(e.target.value)}
            onKeyDown={handleInputKeyDown}
          />
          <button className="finapp-run-btn" onClick={handleSend}><MdPlayArrow size={28} /></button>
        </div>
        {error && <div className="finapp-file-info" style={{color: 'red'}}>{error}</div>}
      </main>
    </div>
  );
}

export default App; 