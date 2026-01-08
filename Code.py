import React, { useState, useEffect } from 'react';

const BellSecuritySystem = () => {
  const [token, setToken] = useState(null);
  const [idea, setIdea] = useState("");
  const [vault, setVault] = useState([]);
  const [status, setStatus] = useState("SYSTEM_READY");

  // Mathematical Identity: a^2 + b^2 = 1
  const checkUnity = (a, b) => Math.abs((Math.pow(a, 2) + Math.pow(b, 2)) - 1.0) < 1e-9;

  const generateToken = () => {
    const array = new Uint32Array(1);
    window.crypto.getRandomValues(array);
    const theta = (array[0] % 360) * (Math.PI / 180);

    const a = Math.cos(theta);
    const b = Math.sin(theta);

    setToken({ a, b, id: btoa(Math.random()).substring(0, 8) });
    setStatus("TOKEN_ARMED");
  };

  const secureAndBurn = () => {
    if (!token || !idea) return;

    if (checkUnity(token.a, token.b)) {
      const newEntry = {
        id: token.id,
        content: idea,
        signature: `${token.a.toFixed(4)}|${token.b.toFixed(4)}`,
        timestamp: new Date().toLocaleTimeString(),
      };

      setVault([newEntry, ...vault]);
      setToken(null); // THE BURN
      setIdea("");
      setStatus("ENTRY_SECURED_TOKEN_VOID");
    } else {
      setStatus("CRITICAL_FAILURE_MATH_MISMATCH");
    }
  };

  return (
    <div style={styles.container}>
      <header style={styles.header}>
        <h1 style={styles.glitch}>COVERAGE.SERVICES</h1>
        <p style={styles.subtitle}>Bell-State One-Time-Pad Security Engine</p>
      </header>

      <main style={styles.main}>
        <div style={styles.terminal}>
          <p style={styles.status}>STATUS: <span style={token ? styles.armed : styles.ready}>{status}</span></p>
          
          <input 
            style={styles.input}
            placeholder="INPUT SECRET IDEA..."
            value={idea}
            onChange={(e) => setIdea(e.target.value)}
          />

          <div style={styles.buttonRow}>
            <button style={styles.button} onClick={generateToken} disabled={!!token}>GENERATE KEY</button>
            <button style={styles.burnButton} onClick={secureAndBurn} disabled={!token || !idea}>SECURE & BURN</button>
          </div>

          {token && (
            <div style={styles.tokenDisplay}>
              <small>ACTIVE BELL STATE:</small>
              <code>|ψ⟩ = {token.a.toFixed(6)}|00⟩ + {token.b.toFixed(6)}|11⟩</code>
            </div>
          )}
        </div>

        <section style={styles.vault}>
          <h3>IDEA VAULT (SECURED HASHES)</h3>
          {vault.map((item) => (
            <div key={item.id} style={styles.vaultItem}>
              <strong>[{item.timestamp}] ID: {item.id}</strong>
              <p>{item.content}</p>
              <small style={styles.sig}>SIG: {item.signature} (UNITY_VERIFIED)</small>
            </div>
          ))}
        </section>
      </main>
    </div>
  );
};

const styles = {
  container: { backgroundColor: '#050505', color: '#00ff41', minHeight: '100vh', padding: '40px', fontFamily: '"Courier New", Courier, monospace' },
  header: { textAlign: 'center', marginBottom: '40px', borderBottom: '1px solid #00ff41' },
  subtitle: { color: '#008f11', letterSpacing: '2px' },
  terminal: { background: '#0a0a0a', padding: '20px', borderRadius: '5px', border: '1px solid #333', marginBottom: '30px' },
  input: { background: 'transparent', border: 'none', borderBottom: '1px solid #00ff41', color: '#fff', width: '100%', padding: '10px', marginBottom: '20px', outline: 'none', fontSize: '1.1rem' },
  buttonRow: { display: 'flex', gap: '10px' },
  button: { background: '#00ff41', color: '#000', border: 'none', padding: '10px 20px', cursor: 'pointer', fontWeight: 'bold' },
  burnButton: { background: '#ff003c', color: '#fff', border: 'none', padding: '10px 20px', cursor: 'pointer', fontWeight: 'bold' },
  tokenDisplay: { marginTop: '20px', color: '#008f11' },
  vault: { marginTop: '20px' },
  vaultItem: { borderLeft: '2px solid #00ff41', paddingLeft: '15px', marginBottom: '15px', background: '#111', padding: '10px' },
  sig: { color: '#008f11', fontSize: '0.7rem' },
  ready: { color: '#00ff41' },
  armed: { color: '#ff003c', animation: 'blink 1s infinite' }
};

export default BellSecuritySystem;
