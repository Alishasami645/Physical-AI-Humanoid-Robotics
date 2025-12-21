'use client';

import React, { useEffect, useState } from 'react';

interface Props {
  chapterName: string;
}

export default function ChapterActions({ chapterName }: Props) {
  const [message, setMessage] = useState<string | null>(null);
  const [isTranslated, setIsTranslated] = useState(false);
  const [originalHtml, setOriginalHtml] = useState<string | null>(null);
  const [disabled, setDisabled] = useState(false);

  const isLoggedIn = typeof window !== 'undefined' && Boolean(localStorage.getItem('external_id'));

  useEffect(() => {
    const checkStatus = async () => {
      if (!isLoggedIn) return;
      try {
        const externalId = localStorage.getItem('external_id');
        if (!externalId) return;
        const backendUrl = 'http://localhost:8000';
        const res = await fetch(`${backendUrl}/api/users/${encodeURIComponent(externalId)}/award-status/${encodeURIComponent(chapterName)}`);
        if (!res.ok) return;
        const data = await res.json();
        if (data.awarded || data.remaining === 0) {
          setDisabled(true);
          setIsTranslated(Boolean(data.awarded));
          setMessage(data.awarded ? 'Already translated — bonus awarded' : 'Max bonus reached');
        }
      } catch (err) {
        console.error('Failed to fetch award status', err);
      }
    };
    checkStatus();
  }, [isLoggedIn, chapterName]);

  const handleTranslate = async () => {
    setMessage('Translating...');
    setDisabled(true);
    try {
      const contentEl =
        document.querySelector('article') ||
        document.querySelector('.markdown-body') ||
        document.querySelector('main') ||
        document.body;

      const content = contentEl ? (contentEl.textContent || '') : '';
      if (!content.trim()) {
        setMessage('No content found to translate');
        setDisabled(false);
        return;
      }

      const backendUrl = 'http://localhost:8000';
      console.log('Translating with backend URL:', backendUrl);
      const res = await fetch(`${backendUrl}/api/translate/urdu`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ content, preserve_code_blocks: true }),
      });

      console.log('Translation response status:', res.status);
      const data = await res.json();
      console.log('Translation response data:', data);
      if (res.ok && data.urdu_content) {
        if (contentEl) {
          if (!originalHtml) setOriginalHtml((contentEl as HTMLElement).innerHTML);
          (contentEl as HTMLElement).innerText = data.urdu_content;
          setIsTranslated(true);
          setMessage('Translation complete');

          if (isLoggedIn) {
            try {
              const externalId = localStorage.getItem('external_id');
              if (externalId) {
                const awardRes = await fetch(`${backendUrl}/api/users/award-bonus`, {
                  method: 'POST',
                  headers: { 'Content-Type': 'application/json' },
                  body: JSON.stringify({ external_id: externalId, chapter: chapterName, points: 50 }),
                });
                const awardData = await awardRes.json();
                if (awardRes.ok && awardData.awarded) {
                  setMessage(`Translation complete — you earned ${awardData.awarded_points} bonus points (total ${awardData.total_points})`);
                } else if (awardRes.ok && !awardData.awarded) {
                  setMessage(`Translation complete — bonus already claimed (total ${awardData.total_points})`);
                }
              }
            } catch (err) {
              console.error('Award bonus failed', err);
            }
          }
        } else {
          setMessage('Translation complete but could not find content element to replace');
        }
      } else {
        const errorMsg = (data && data.detail) || 'Translation failed';
        setMessage(errorMsg);
        console.error('Translation API error:', errorMsg, data);
      }
    } catch (err) {
      const errorMsg = err instanceof Error ? err.message : 'Network error while translating';
      setMessage(errorMsg);
      console.error('Translation error:', err);
    } finally {
      setDisabled(false);
    }
  };

  const handleToggle = () => {
    const contentEl =
      document.querySelector('article') ||
      document.querySelector('.markdown-body') ||
      document.querySelector('main') ||
      document.body;
    if (!contentEl) return;

    if (isTranslated) {
      if (originalHtml !== null) {
        (contentEl as HTMLElement).innerHTML = originalHtml;
      }
      setIsTranslated(false);
      setMessage('Restored original English content');
    } else {
      void handleTranslate();
    }
  };

  return (
    <div style={{ margin: '16px 0', display: 'flex', gap: 12, alignItems: 'center', flexWrap: 'wrap' }}>
      <button
        onClick={() => {
          if (isLoggedIn) void handleTranslate();
        }}
        disabled={disabled || !isLoggedIn}
        title={isLoggedIn ? '' : 'Sign in to translate and earn bonus points'}
        style={{
          padding: '8px 16px',
          backgroundColor: isLoggedIn ? '#10a37f' : '#ccc',
          color: isLoggedIn ? 'white' : '#666',
          border: 'none',
          borderRadius: '4px',
          cursor: isLoggedIn && !disabled ? 'pointer' : 'not-allowed',
          fontSize: '14px',
          fontWeight: 500,
        }}
      >
        🌍 Translate to Urdu
      </button>

      {isLoggedIn && (
        <button
          onClick={handleToggle}
          disabled={disabled}
          style={{
            padding: '8px 12px',
            backgroundColor: isTranslated ? '#f39c12' : '#e0e0e0',
            color: isTranslated ? 'white' : '#333',
            border: 'none',
            borderRadius: '4px',
            cursor: disabled ? 'not-allowed' : 'pointer',
            fontSize: '13px',
          }}
        >
          {isTranslated ? '🔁 Restore English' : '🔁 Translate / Restore'}
        </button>
      )}

      {message && (
        <span style={{ marginLeft: 8, fontSize: '14px', color: '#666' }}>{message}</span>
      )}
    </div>
  );
}
