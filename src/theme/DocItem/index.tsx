'use client';

import React from 'react';
import OriginalDocItem from '@theme-original/DocItem';
import ChapterActions from '../../components/ChapterActions/ChapterActions';

export default function DocItem(props) {
  // Try to extract a readable chapter name from metadata
  const metadata = props?.content?.metadata || {};
  const chapterName = metadata.title || metadata.id || metadata.source || 'Chapter';

  return (
    <>
      <div style={{ padding: '12px 0' }}>
        <ChapterActions chapterName={chapterName} />
      </div>
      <OriginalDocItem {...props} />
    </>
  );
}
