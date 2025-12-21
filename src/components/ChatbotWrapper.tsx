import React from 'react';
import RoboticsRAGChatbot from './RoboticsRAGChatbot';

/**
 * Component that wraps the RoboticsRAGChatbot for use in Docusaurus.
 * This is a client-side component that will be mounted in the layout.
 */
export default function ChatbotWrapper(): JSX.Element {
  // Get backend URL - use 127.0.0.1:8000 for development
  const backendUrl = 'http://127.0.0.1:8000';

  return (
    <RoboticsRAGChatbot backendUrl={backendUrl} />
  );
}
