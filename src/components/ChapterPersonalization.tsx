import React, { useState } from 'react';
import styles from './ChapterPersonalization.module.css';

interface UserProfile {
  software_background: 'beginner' | 'intermediate' | 'advanced';
  hardware_experience: 'low' | 'medium' | 'high';
  programming_languages: string[];
  learning_goal: string;
}

interface ChapterPersonalizationProps {
  chapterName: string;
  chapterContent: string;
  onPersonalized?: (personalized Content: string) => void;
  userProfile?: UserProfile;
  backendUrl?: string;
}

const ChapterPersonalization: React.FC<ChapterPersonalizationProps> = ({
  chapterName,
  chapterContent,
  onPersonalized,
  userProfile,
  backendUrl = 'http://localhost:8000'
}) => {
  const [isPersonalizing, setIsPersonalizing] = useState(false);
  const [showForm, setShowForm] = useState(!userProfile);
  const [profile, setProfile] = useState<UserProfile>(
    userProfile || {
      software_background: 'beginner',
      hardware_experience: 'low',
      programming_languages: [],
      learning_goal: ''
    }
  );

  const handlePersonalize = async () => {
    if (!profile) return;

    setIsPersonalizing(true);
    try {
      const response = await fetch(`${backendUrl}/api/personalize/chapter`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          chapter_name: chapterName,
          chapter_content: chapterContent,
          user_profile: profile
        })
      });

      if (!response.ok) {
        throw new Error('Personalization failed');
      }

      const data = await response.json();
      onPersonalized?.(data.personalized_content);
      setShowForm(false);
    } catch (error) {
      console.error('Personalization error:', error);
      alert('Failed to personalize chapter');
    } finally {
      setIsPersonalizing(false);
    }
  };

  const handleProfileChange = (field: keyof UserProfile, value: any) => {
    setProfile(prev => ({ ...prev, [field]: value }));
  };

  return (
    <div className={styles.container}>
      <button
        onClick={() => setShowForm(!showForm)}
        className={styles.toggleButton}
        disabled={isPersonalizing}
        title="Personalize this chapter based on your skill level and goals"
      >
        ⚙️ Personalize Chapter
      </button>

      {showForm && (
        <div className={styles.formPanel}>
          <h3>Personalize This Chapter</h3>
          
          <div className={styles.formGroup}>
            <label htmlFor="sw-level">Software Level:</label>
            <select
              id="sw-level"
              value={profile.software_background}
              onChange={(e) => handleProfileChange('software_background', e.target.value)}
            >
              <option value="beginner">Beginner - New to robotics programming</option>
              <option value="intermediate">Intermediate - Some experience</option>
              <option value="advanced">Advanced - Experienced developer</option>
            </select>
          </div>

          <div className={styles.formGroup}>
            <label htmlFor="hw-exp">Hardware Experience:</label>
            <select
              id="hw-exp"
              value={profile.hardware_experience}
              onChange={(e) => handleProfileChange('hardware_experience', e.target.value)}
            >
              <option value="low">Low - Limited hands-on experience</option>
              <option value="medium">Medium - Some hardware projects</option>
              <option value="high">High - Extensive hardware experience</option>
            </select>
          </div>

          <div className={styles.formGroup}>
            <label htmlFor="langs">Preferred Programming Languages:</label>
            <input
              id="langs"
              type="text"
              placeholder="e.g., Python, C++, ROS"
              value={profile.programming_languages.join(', ')}
              onChange={(e) => handleProfileChange('programming_languages', e.target.value.split(',').map(s => s.trim()))}
            />
          </div>

          <div className={styles.formGroup}>
            <label htmlFor="goal">Learning Goal:</label>
            <input
              id="goal"
              type="text"
              placeholder="e.g., Build autonomous robots, learn ROS 2"
              value={profile.learning_goal}
              onChange={(e) => handleProfileChange('learning_goal', e.target.value)}
            />
          </div>

          <button
            onClick={handlePersonalize}
            disabled={isPersonalizing}
            className={styles.personalizeButton}
          >
            {isPersonalizing ? '⏳ Personalizing...' : '✨ Personalize Now'}
          </button>
        </div>
      )}
    </div>
  );
};

export default ChapterPersonalization;
