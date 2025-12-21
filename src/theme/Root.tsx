import React, { Suspense, lazy } from 'react';
import ClientOnly from '../components/ClientOnlyWrapper';
import { AuthProvider } from '../components/Auth/AuthProvider';

const ChatbotWrapper = lazy(() => import('../components/ChatbotWrapper'));

export default function Root({ children }) {
  return (
    <AuthProvider>
      <>
        {children}
        <ClientOnly fallback={null}>
          <Suspense fallback={null}>
            <ChatbotWrapper />
          </Suspense>
        </ClientOnly>
      </>
    </AuthProvider>
  );
}
