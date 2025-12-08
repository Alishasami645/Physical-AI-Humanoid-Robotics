import React from 'react';
import ComponentCreator from '@docusaurus/ComponentCreator';

export default [
  {
    path: '/robotics-book/__docusaurus/debug',
    component: ComponentCreator('/robotics-book/__docusaurus/debug', '341'),
    exact: true
  },
  {
    path: '/robotics-book/__docusaurus/debug/config',
    component: ComponentCreator('/robotics-book/__docusaurus/debug/config', '145'),
    exact: true
  },
  {
    path: '/robotics-book/__docusaurus/debug/content',
    component: ComponentCreator('/robotics-book/__docusaurus/debug/content', 'bcc'),
    exact: true
  },
  {
    path: '/robotics-book/__docusaurus/debug/globalData',
    component: ComponentCreator('/robotics-book/__docusaurus/debug/globalData', '00d'),
    exact: true
  },
  {
    path: '/robotics-book/__docusaurus/debug/metadata',
    component: ComponentCreator('/robotics-book/__docusaurus/debug/metadata', 'c19'),
    exact: true
  },
  {
    path: '/robotics-book/__docusaurus/debug/registry',
    component: ComponentCreator('/robotics-book/__docusaurus/debug/registry', '8ea'),
    exact: true
  },
  {
    path: '/robotics-book/__docusaurus/debug/routes',
    component: ComponentCreator('/robotics-book/__docusaurus/debug/routes', '168'),
    exact: true
  },
  {
    path: '/robotics-book/markdown-page',
    component: ComponentCreator('/robotics-book/markdown-page', 'cd0'),
    exact: true
  },
  {
    path: '/robotics-book/docs',
    component: ComponentCreator('/robotics-book/docs', '753'),
    routes: [
      {
        path: '/robotics-book/docs',
        component: ComponentCreator('/robotics-book/docs', '1fe'),
        routes: [
          {
            path: '/robotics-book/docs',
            component: ComponentCreator('/robotics-book/docs', '329'),
            routes: [
              {
                path: '/robotics-book/docs/chapter-01-introduction-to-physical-ai/lesson-1-1-what-is-physical-ai',
                component: ComponentCreator('/robotics-book/docs/chapter-01-introduction-to-physical-ai/lesson-1-1-what-is-physical-ai', '94c'),
                exact: true,
                sidebar: "tutorialSidebar"
              },
              {
                path: '/robotics-book/docs/chapter-01-introduction-to-physical-ai/lesson-1-2-embodied intelligence',
                component: ComponentCreator('/robotics-book/docs/chapter-01-introduction-to-physical-ai/lesson-1-2-embodied intelligence', '9c6'),
                exact: true,
                sidebar: "tutorialSidebar"
              },
              {
                path: '/robotics-book/docs/chapter-01-introduction-to-physical-ai/lesson-1-3-course overview & learning outcomes',
                component: ComponentCreator('/robotics-book/docs/chapter-01-introduction-to-physical-ai/lesson-1-3-course overview & learning outcomes', 'dd6'),
                exact: true,
                sidebar: "tutorialSidebar"
              },
              {
                path: '/robotics-book/docs/chapter-02-robotic-nervous-system-ros-2/lesson-2-1-rOS 2 architecture',
                component: ComponentCreator('/robotics-book/docs/chapter-02-robotic-nervous-system-ros-2/lesson-2-1-rOS 2 architecture', '42a'),
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
                path: '/robotics-book/docs/chapter-02-robotic-nervous-system-ros-2/lesson-2-3-python integration',
                component: ComponentCreator('/robotics-book/docs/chapter-02-robotic-nervous-system-ros-2/lesson-2-3-python integration', 'a6d'),
                exact: true,
                sidebar: "tutorialSidebar"
              },
              {
                path: '/robotics-book/docs/chapter-02-robotic-nervous-system-ros-2/lesson-2-4-urdf for humanoids',
                component: ComponentCreator('/robotics-book/docs/chapter-02-robotic-nervous-system-ros-2/lesson-2-4-urdf for humanoids', '852'),
                exact: true,
                sidebar: "tutorialSidebar"
              },
              {
                path: '/robotics-book/docs/chapter-03-digital-twin-gazebo-unity/lesson-3-1-gazebo simulation basics',
                component: ComponentCreator('/robotics-book/docs/chapter-03-digital-twin-gazebo-unity/lesson-3-1-gazebo simulation basics', '4ec'),
                exact: true,
                sidebar: "tutorialSidebar"
              },
              {
                path: '/robotics-book/docs/chapter-03-digital-twin-gazebo-unity/lesson-3-2-sensor simulation',
                component: ComponentCreator('/robotics-book/docs/chapter-03-digital-twin-gazebo-unity/lesson-3-2-sensor simulation', 'c53'),
                exact: true,
                sidebar: "tutorialSidebar"
              },
              {
                path: '/robotics-book/docs/chapter-03-digital-twin-gazebo-unity/lesson-3-3-high-fidelity rendering with unity',
                component: ComponentCreator('/robotics-book/docs/chapter-03-digital-twin-gazebo-unity/lesson-3-3-high-fidelity rendering with unity', '535'),
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
                path: '/robotics-book/docs/chapter-04-ai-robot-brain-nvidia-isaac/lesson-4-2-isaac-ros-navigation',
                component: ComponentCreator('/robotics-book/docs/chapter-04-ai-robot-brain-nvidia-isaac/lesson-4-2-isaac-ros-navigation', 'd8d'),
                exact: true,
                sidebar: "tutorialSidebar"
              },
              {
                path: '/robotics-book/docs/chapter-04-ai-robot-brain-nvidia-isaac/lesson-4-3-rl-sim-to-real',
                component: ComponentCreator('/robotics-book/docs/chapter-04-ai-robot-brain-nvidia-isaac/lesson-4-3-rl-sim-to-real', '2b5'),
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
                path: '/robotics-book/docs/chapter-05-vision-language-action-vla/lesson-5-2-voice-to-action',
                component: ComponentCreator('/robotics-book/docs/chapter-05-vision-language-action-vla/lesson-5-2-voice-to-action', '56c'),
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
