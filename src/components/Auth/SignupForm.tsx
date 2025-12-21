import React, { useState } from 'react';

interface SignupProps {
  onSignedUp?: (user: any) => void;
}

export default function SignupForm({ onSignedUp }: SignupProps) {
  const [email, setEmail] = useState('');
  const [softwareBackground, setSoftwareBackground] = useState('Beginner');
  const [hardwareExperience, setHardwareExperience] = useState('Low');
  const [programmingLanguages, setProgrammingLanguages] = useState('');
  const [learningGoal, setLearningGoal] = useState('');
  const [status, setStatus] = useState<string | null>(null);

  const submit = async (e: React.FormEvent) => {
    e.preventDefault();
    setStatus('Saving...');

    const payload = {
      external_id: localStorage.getItem('external_id') || undefined,
      email,
      software_background: softwareBackground,
      hardware_experience: hardwareExperience,
      programming_languages: programmingLanguages.split(',').map(s => s.trim()).filter(Boolean),
      learning_goal: learningGoal,
    };

    try {
      const res = await fetch(`${window.location.origin}/api/auth/signup`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(payload),
      });
      const data = await res.json();
      if (res.ok) {
        setStatus('Saved');
        if (data.user && data.user.external_id) {
          localStorage.setItem('external_id', data.user.external_id);
        }
        onSignedUp?.(data.user);
      } else {
        setStatus(data.detail || 'Error');
      }
    } catch (err) {
      setStatus('Network error');
    }
  };

  return (
    <form onSubmit={submit} style={{ padding: 12, border: '1px solid #eee', borderRadius: 6 }}>
      <h4>Personalize your learning</h4>
      <label>Email<br />
        <input value={email} onChange={e => setEmail(e.target.value)} />
      </label>
      <br />
      <label>Software background<br />
        <select value={softwareBackground} onChange={e => setSoftwareBackground(e.target.value)}>
          <option>Beginner</option>
          <option>Intermediate</option>
          <option>Advanced</option>
        </select>
      </label>
      <br />
      <label>Hardware experience<br />
        <select value={hardwareExperience} onChange={e => setHardwareExperience(e.target.value)}>
          <option>Low</option>
          <option>Medium</option>
          <option>High</option>
        </select>
      </label>
      <br />
      <label>Programming languages (comma separated)<br />
        <input value={programmingLanguages} onChange={e => setProgrammingLanguages(e.target.value)} />
      </label>
      <br />
      <label>Learning goal<br />
        <input value={learningGoal} onChange={e => setLearningGoal(e.target.value)} />
      </label>
      <br />
      <button type="submit">Save personalization</button>
      {status && <div style={{ marginTop: 8 }}>{status}</div>}
    </form>
  );
}
