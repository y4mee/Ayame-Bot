import { useState, useEffect } from 'react';

export default function Home() {
  const [status, setStatus] = useState('Checking...');
  const [lastPing, setLastPing] = useState(null);
  const [nextPing, setNextPing] = useState(null);

  useEffect(() => {
    // Initial check
    checkStatus();
    pingBot();
    
    // Check status every minute
    const statusInterval = setInterval(checkStatus, 60000);
    
    // Ping bot every 14 minutes to keep it awake
    const pingInterval = setInterval(pingBot, 14 * 60 * 1000);
    
    return () => {
      clearInterval(statusInterval);
      clearInterval(pingInterval);
    };
  }, []);

  const pingBot = async () => {
    try {
      await fetch('/api/ping');
      setLastPing(new Date().toLocaleTimeString());
      console.log('✅ Auto-ping sent');
    } catch (error) {
      console.error('❌ Auto-ping failed:', error);
    }
  };

  const checkStatus = async () => {
    try {
      const response = await fetch('https://ayame-bot.onrender.com/health');
      if (response.ok) {
        setStatus('🟢 Online');
      } else {
        setStatus('🟡 Slow');
      }
    } catch (error) {
      setStatus('🔴 Offline');
    }
  };

  const manualPing = async () => {
    setStatus('Pinging...');
    try {
      await fetch('/api/ping');
      setLastPing(new Date().toLocaleTimeString());
      checkStatus();
    } catch (error) {
      setStatus('❌ Failed');
    }
  };

  return (
    <div style={styles.container}>
      <div style={styles.card}>
        <h1 style={styles.title}>🤖 Ayame Bot</h1>
        <p style={styles.subtitle}>Keep-Alive Service</p>
        
        <div style={styles.statusBox}>
          <div style={styles.statusLabel}>Bot Status</div>
          <div style={styles.statusValue}>{status}</div>
        </div>

        <div style={styles.info}>
          <p>✨ Automatically pings every 14 minutes</p>
          <p>🔄 Keeps bot awake on Render free tier</p>
          {lastPing && <p>⏰ Last ping: {lastPing}</p>}
        </div>

        <button onClick={manualPing} style={styles.button}>
          Ping Now
        </button>

        <div style={styles.footer}>
          <a href="https://ayame-bot.onrender.com/health" target="_blank" rel="noopener noreferrer" style={styles.link}>
            View Bot Health →
          </a>
        </div>
      </div>
    </div>
  );
}

const styles = {
  container: {
    minHeight: '100vh',
    display: 'flex',
    alignItems: 'center',
    justifyContent: 'center',
    background: 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)',
    fontFamily: '-apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif',
    padding: '20px',
  },
  card: {
    background: 'white',
    borderRadius: '20px',
    padding: '40px',
    maxWidth: '500px',
    width: '100%',
    boxShadow: '0 20px 60px rgba(0,0,0,0.3)',
  },
  title: {
    fontSize: '36px',
    fontWeight: 'bold',
    margin: '0 0 10px 0',
    textAlign: 'center',
    background: 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)',
    WebkitBackgroundClip: 'text',
    WebkitTextFillColor: 'transparent',
  },
  subtitle: {
    fontSize: '16px',
    color: '#666',
    textAlign: 'center',
    margin: '0 0 30px 0',
  },
  statusBox: {
    background: '#f7f7f7',
    borderRadius: '12px',
    padding: '20px',
    textAlign: 'center',
    marginBottom: '30px',
  },
  statusLabel: {
    fontSize: '14px',
    color: '#666',
    marginBottom: '8px',
  },
  statusValue: {
    fontSize: '24px',
    fontWeight: 'bold',
  },
  info: {
    background: '#f0f4ff',
    borderRadius: '12px',
    padding: '20px',
    marginBottom: '20px',
  },
  button: {
    width: '100%',
    padding: '15px',
    fontSize: '16px',
    fontWeight: 'bold',
    color: 'white',
    background: 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)',
    border: 'none',
    borderRadius: '12px',
    cursor: 'pointer',
    transition: 'transform 0.2s',
  },
  footer: {
    marginTop: '20px',
    textAlign: 'center',
  },
  link: {
    color: '#667eea',
    textDecoration: 'none',
    fontSize: '14px',
  },
};
