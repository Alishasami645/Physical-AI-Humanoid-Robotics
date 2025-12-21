import React, { useState, useRef, useEffect } from 'react';
import styles from './ChatBot.module.css';

interface Message {
  id: string;
  role: 'user' | 'assistant';
  content: string;
  selectedText?: string;
  sources?: Array<{
    title: string;
    chapter: string;
    content: string;
    score: number;
  }>;
  timestamp: Date;
}

interface ChatBotProps {
  backendUrl?: string;
}

const RoboticsRAGChatbot: React.FC<ChatBotProps> = ({ 
  backendUrl = 'http://127.0.0.1:8000'
}) => {
  const [messages, setMessages] = useState<Message[]>([]);
  const [inputValue, setInputValue] = useState('');
  const [selectedText, setSelectedText] = useState<string>('');
  const [isLoading, setIsLoading] = useState(false);
  const [isOpen, setIsOpen] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const messagesEndRef = useRef<HTMLDivElement>(null);
  const inputRef = useRef<HTMLInputElement>(null);

  // Auto-scroll to bottom when new messages arrive
  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [messages]);

  // Initialize with welcome message
  useEffect(() => {
    if (messages.length === 0) {
      setMessages([
        {
          id: '0',
          role: 'assistant',
          content: 'Welcome to the Robotics Book Assistant! 👋 I can help you understand concepts from the Physical AI & Humanoid Robotics book. You can ask me questions about any topic, or highlight text to get explanations about specific passages.',
          timestamp: new Date(),
        },
      ]);
    }
  }, []);

  // Handle text selection
  useEffect(() => {
    const handleTextSelection = () => {
      const selected = window.getSelection()?.toString().trim();
      if (selected && selected.length > 10) {
        setSelectedText(selected);
      } else {
        setSelectedText('');
      }
    };

    document.addEventListener('mouseup', handleTextSelection);
    document.addEventListener('touchend', handleTextSelection);

    return () => {
      document.removeEventListener('mouseup', handleTextSelection);
      document.removeEventListener('touchend', handleTextSelection);
    };
  }, []);

  const sendMessage = async () => {
    if (!inputValue.trim()) {
      setError('Please enter a message');
      return;
    }

    const userMessage: Message = {
      id: Date.now().toString(),
      role: 'user',
      content: inputValue,
      selectedText: selectedText || undefined,
      timestamp: new Date(),
    };

    setMessages(prev => [...prev, userMessage]);
    setInputValue('');
    setSelectedText('');
    setIsLoading(true);
    setError(null);

    try {
      const conversationHistory = messages
        .filter(m => m.role === 'user' || m.role === 'assistant')
        .map(m => ({
          role: m.role,
          content: m.content,
        }));

      const externalId = typeof window !== 'undefined' ? localStorage.getItem('external_id') : null;

      const response = await fetch(`${backendUrl}/api/chat`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          query: userMessage.content,
          selected_text: userMessage.selectedText || null,
          conversation_history: conversationHistory,
          external_id: externalId,
        }),
      });

      if (!response.ok) {
        throw new Error(`API Error: ${response.statusText}`);
      }

      const data = await response.json();

      const assistantMessage: Message = {
        id: (Date.now() + 1).toString(),
        role: 'assistant',
        content: data.answer,
        sources: data.sources,
        timestamp: new Date(),
      };

      setMessages(prev => [...prev, assistantMessage]);
    } catch (err) {
      const errorMessage = err instanceof Error ? err.message : 'Unknown error occurred';
      setError(errorMessage);
      console.error('Chat error:', err);

      // Add error message to chat
      const errorMsg: Message = {
        id: (Date.now() + 1).toString(),
        role: 'assistant',
        content: `Sorry, I encountered an error: ${errorMessage}. Please make sure the backend is running and properly configured.`,
        timestamp: new Date(),
      };
      setMessages(prev => [...prev, errorMsg]);
    } finally {
      setIsLoading(false);
    }
  };

  const handleKeyDown = (e: React.KeyboardEvent) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      sendMessage();
    }
  };

  const toggleChat = () => {
    setIsOpen(!isOpen);
    if (!isOpen) {
      setTimeout(() => inputRef.current?.focus(), 100);
    }
  };

  return (
    <>
      {/* Chat Widget Button */}
      {!isOpen && (
        <button
          className={styles.chatButton}
          onClick={toggleChat}
          title="Open Robotics Book Assistant"
          aria-label="Open chat"
        >
          <span className={styles.chatIcon}>💬</span>
        </button>
      )}

      {/* Chat Window */}
      {isOpen && (
        <div className={styles.chatContainer}>
          {/* Header */}
          <div className={styles.header}>
            <div className={styles.headerContent}>
              <h3>Robotics Book Assistant</h3>
              <p>Ask me anything about the book</p>
            </div>
            <button
              className={styles.closeButton}
              onClick={toggleChat}
              aria-label="Close chat"
            >
              ✕
            </button>
          </div>

          {/* Messages */}
          <div className={styles.messagesContainer}>
            {messages.map(message => (
              <div key={message.id} className={`${styles.message} ${styles[message.role]}`}>
                <div className={styles.messageContent}>
                  <div className={styles.messageText}>{message.content}</div>

                  {/* Sources */}
                  {message.sources && message.sources.length > 0 && (
                    <div className={styles.sources}>
                      <details>
                        <summary>📚 {message.sources.length} Source(s)</summary>
                        <div className={styles.sourcesList}>
                          {message.sources.map((source, idx) => (
                            <div key={idx} className={styles.sourceItem}>
                              <strong>{source.title}</strong>
                              <small>{source.chapter}</small>
                              <p>{source.content.substring(0, 150)}...</p>
                            </div>
                          ))}
                        </div>
                      </details>
                    </div>
                  )}

                  {/* Selected Text Indicator */}
                  {message.selectedText && (
                    <div className={styles.selectedTextBadge}>
                      📍 Based on selected text
                    </div>
                  )}
                </div>
              </div>
            ))}

            {isLoading && (
              <div className={`${styles.message} ${styles.assistant}`}>
                <div className={styles.loadingIndicator}>
                  <span></span>
                  <span></span>
                  <span></span>
                </div>
              </div>
            )}

            <div ref={messagesEndRef} />
          </div>

          {/* Error Message */}
          {error && (
            <div className={styles.errorBanner}>
              ⚠️ {error}
            </div>
          )}

          {/* Selected Text Display */}
          {selectedText && (
            <div className={styles.selectedTextDisplay}>
              <small>📌 Selected: "{selectedText.substring(0, 60)}..."</small>
            </div>
          )}

          {/* Input */}
          <div className={styles.inputContainer}>
            <input
              ref={inputRef}
              type="text"
              value={inputValue}
              onChange={e => setInputValue(e.target.value)}
              onKeyDown={handleKeyDown}
              placeholder={selectedText ? 'Ask about the selected text...' : 'Ask a question...'}
              disabled={isLoading}
              className={styles.input}
            />
            <button
              onClick={sendMessage}
              disabled={isLoading || !inputValue.trim()}
              className={styles.sendButton}
              aria-label="Send message"
            >
              {isLoading ? '⏳' : '→'}
            </button>
          </div>
        </div>
      )}
    </>
  );
};

export default RoboticsRAGChatbot;
