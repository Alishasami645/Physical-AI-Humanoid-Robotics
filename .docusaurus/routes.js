import React from 'react';
import ComponentCreator from '@docusaurus/ComponentCreator';

export default [
  {
    path: '/robotics-book/markdown-page',
    component: ComponentCreator('/robotics-book/markdown-page', 'cd0'),
    exact: true
  },
  {
    path: '/robotics-book/docs',
    component: ComponentCreator('/robotics-book/docs', '252'),
    routes: [
      {
        path: '/robotics-book/docs',
        component: ComponentCreator('/robotics-book/docs', '1f2'),
        routes: [
          {
            path: '/robotics-book/docs',
            component: ComponentCreator('/robotics-book/docs', 'e3a'),
            routes: [
              {
                path: '/robotics-book/docs/chapter-01-introduction-to-physical-ai/lesson-1-1-what-is-physical-ai',
                component: ComponentCreator('/robotics-book/docs/chapter-01-introduction-to-physical-ai/lesson-1-1-what-is-physical-ai', '94c'),
                exact: true,
                sidebar: "tutorialSidebar"
              },
              {
                path: '/robotics-book/docs/chapter-01-introduction-to-physical-ai/lesson-1-2-embodied-intelligence',
                component: ComponentCreator('/robotics-book/docs/chapter-01-introduction-to-physical-ai/lesson-1-2-embodied-intelligence', '5b3'),
                exact: true,
                sidebar: "tutorialSidebar"
              },
              {
                path: '/robotics-book/docs/chapter-01-introduction-to-physical-ai/lesson-1-3-course-overview',
                component: ComponentCreator('/robotics-book/docs/chapter-01-introduction-to-physical-ai/lesson-1-3-course-overview', 'eab'),
                exact: true,
                sidebar: "tutorialSidebar"
              },
              {
                path: '/robotics-book/docs/chapter-02-robotic-nervous-system-ros-2/lesson-2-1-ros-2-architecture',
                component: ComponentCreator('/robotics-book/docs/chapter-02-robotic-nervous-system-ros-2/lesson-2-1-ros-2-architecture', '21f'),
                exact: true,
                sidebar: "tutorialSidebar"
              },
              {
                path: '/robotics-book/docs/chapter-02-robotic-nervous-system-ros-2/lesson-2-2-nodes-topics-services-actions',
                component: ComponentCreator('/robotics-book/docs/chapter-02-robotic-nervous-system-ros-2/lesson-2-2-nodes-topics-services-actions', 'fff'),
                exact: true,
                sidebar: "tutorialSidebar"
              },
              {
                path: '/robotics-book/docs/chapter-02-robotic-nervous-system-ros-2/lesson-2-3-python-integration',
                component: ComponentCreator('/robotics-book/docs/chapter-02-robotic-nervous-system-ros-2/lesson-2-3-python-integration', 'f5f'),
                exact: true,
                sidebar: "tutorialSidebar"
              },
              {
                path: '/robotics-book/docs/chapter-02-robotic-nervous-system-ros-2/lesson-2-4-urdf-for-humanoids',
                component: ComponentCreator('/robotics-book/docs/chapter-02-robotic-nervous-system-ros-2/lesson-2-4-urdf-for-humanoids', '107'),
                exact: true,
                sidebar: "tutorialSidebar"
              },
              {
                path: '/robotics-book/docs/chapter-03-digital-twin-gazebo-unity/lesson-3-1-gazebo-simulation-basics',
                component: ComponentCreator('/robotics-book/docs/chapter-03-digital-twin-gazebo-unity/lesson-3-1-gazebo-simulation-basics', '78f'),
                exact: true,
                sidebar: "tutorialSidebar"
              },
              {
                path: '/robotics-book/docs/chapter-03-digital-twin-gazebo-unity/lesson-3-2-sensor-simulation',
                component: ComponentCreator('/robotics-book/docs/chapter-03-digital-twin-gazebo-unity/lesson-3-2-sensor-simulation', '54a'),
                exact: true,
                sidebar: "tutorialSidebar"
              },
              {
                path: '/robotics-book/docs/chapter-03-digital-twin-gazebo-unity/lesson-3-3-high-fidelity-rendering-with-unity',
                component: ComponentCreator('/robotics-book/docs/chapter-03-digital-twin-gazebo-unity/lesson-3-3-high-fidelity-rendering-with-unity', '9b9'),
                exact: true,
                sidebar: "tutorialSidebar"
              },
              {
                path: '/robotics-book/docs/chapter-04-ai-robot-brain-nvidia-isaac/lesson-4-1-isaac-sim-overview',
                component: ComponentCreator('/robotics-book/docs/chapter-04-ai-robot-brain-nvidia-isaac/lesson-4-1-isaac-sim-overview', '380'),
                exact: true,
                sidebar: "tutorialSidebar"
              },
              {
                path: '/robotics-book/docs/chapter-04-ai-robot-brain-nvidia-isaac/lesson-4-2-isaac-ros-for-navigation',
                component: ComponentCreator('/robotics-book/docs/chapter-04-ai-robot-brain-nvidia-isaac/lesson-4-2-isaac-ros-for-navigation', '768'),
                exact: true,
                sidebar: "tutorialSidebar"
              },
              {
                path: '/robotics-book/docs/chapter-04-ai-robot-brain-nvidia-isaac/lesson-4-3-reinforcement-learning',
                component: ComponentCreator('/robotics-book/docs/chapter-04-ai-robot-brain-nvidia-isaac/lesson-4-3-reinforcement-learning', 'd5a'),
                exact: true,
                sidebar: "tutorialSidebar"
              },
              {
                path: '/robotics-book/docs/chapter-05-vision-language-action-vla/lesson-5-1-llm-integration',
                component: ComponentCreator('/robotics-book/docs/chapter-05-vision-language-action-vla/lesson-5-1-llm-integration', '912'),
                exact: true,
                sidebar: "tutorialSidebar"
              },
              {
                path: '/robotics-book/docs/chapter-05-vision-language-action-vla/lesson-5-2-voice-to-action-with-whisper',
                component: ComponentCreator('/robotics-book/docs/chapter-05-vision-language-action-vla/lesson-5-2-voice-to-action-with-whisper', '5fb'),
                exact: true,
                sidebar: "tutorialSidebar"
              },
              {
                path: '/robotics-book/docs/chapter-05-vision-language-action-vla/lesson-5-3-cognitive-planning',
                component: ComponentCreator('/robotics-book/docs/chapter-05-vision-language-action-vla/lesson-5-3-cognitive-planning', '9a0'),
                exact: true,
                sidebar: "tutorialSidebar"
              },
              {
                path: '/robotics-book/docs/chapter-06-capstone-project/lesson-6-1-autonomous-humanoid-overview',
                component: ComponentCreator('/robotics-book/docs/chapter-06-capstone-project/lesson-6-1-autonomous-humanoid-overview', 'b5a'),
                exact: true,
                sidebar: "tutorialSidebar"
              },
              {
                path: '/robotics-book/docs/chapter-06-capstone-project/lesson-6-2-integration-of-modules',
                component: ComponentCreator('/robotics-book/docs/chapter-06-capstone-project/lesson-6-2-integration-of-modules', 'f2a'),
                exact: true,
                sidebar: "tutorialSidebar"
              },
              {
                path: '/robotics-book/docs/chapter-06-capstone-project/lesson-6-3-deployment-assessment',
                component: ComponentCreator('/robotics-book/docs/chapter-06-capstone-project/lesson-6-3-deployment-assessment', '2a1'),
                exact: true,
                sidebar: "tutorialSidebar"
              },
              {
                path: '/robotics-book/docs/intro',
                component: ComponentCreator('/robotics-book/docs/intro', '327'),
                exact: true,
                sidebar: "tutorialSidebar"
              }
            ]
          }
        ]
      }
    ]
  },
  {
    path: '/robotics-book/',
    component: ComponentCreator('/robotics-book/', 'e50'),
    exact: true
  },
  {
    path: '*',
    component: ComponentCreator('*'),
  },
];
