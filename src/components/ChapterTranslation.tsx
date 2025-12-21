import React, { useState } from 'react';
import styles from './ChapterTranslation.module.css';

interface ChapterTranslationProps {
  chapterName: string;
  chapterContent: string;
  onTranslated?: (urduContent: string) => void;
  backendUrl?: string;
}

const ChapterTranslation: React.FC<ChapterTranslationProps> = ({
  chapterName,
  chapterContent,
  onTranslated,
  backendUrl = 'http://localhost:8000'
}) => {
  const [isTranslating, setIsTranslating] = useState(false);
  const [urduContent, setUrduContent] = useState<string | null>(null);

  const handleTranslate = async () => {
    setIsTranslating(true);
    try {
      const response = await fetch(`${backendUrl}/api/translate/urdu`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          content: chapterContent,
          preserve_code_blocks: true
        })
      });

      if (!response.ok) {
        throw new Error('Translation failed');
      }

      const data = await response.json();
      setUrduContent(data.urdu_content);
      onTranslated?.(data.urdu_content);
    } catch (error) {
      console.error('Translation error:', error);
      alert('Failed to translate chapter');
    } finally {
      setIsTranslating(false);
    }
  };

  return (
    <div className={styles.container}>
      <button
        onClick={handleTranslate}
        disabled={isTranslating}
        className={styles.translateButton}
        title="Translate chapter to professional Urdu"
      >
        {isTranslating ? '⏳ Translating...' : '🌐 اردو میں (Translate to Urdu)'}
      </button>

      {urduContent && (
        <div className={styles.urduPanel}>
          <div className={styles.header}>
            <h3>اردو میں (Urdu Translation)</h3>
            <button
              onClick={() => setUrduContent(null)}
              className={styles.closeButton}
              title="Close Urdu translation"
            >
              ✕
            </button>
          </div>
          <div
            className={styles.urduContent}
            dir="rtl"
            lang="ur"
            dangerouslySetInnerHTML={{ __html: urduContent.replace(/\n/g, '<br/>') }}
          />
        </div>
      )}
    </div>
  );
};

export default ChapterTranslation;
