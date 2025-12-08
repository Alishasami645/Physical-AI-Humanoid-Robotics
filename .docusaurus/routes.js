import React from 'react';
import ComponentCreator from '@docusaurus/ComponentCreator';

export default [
  {
    path: '/__docusaurus/debug',
    component: ComponentCreator('/__docusaurus/debug', '5ff'),
    exact: true
  },
  {
    path: '/__docusaurus/debug/config',
    component: ComponentCreator('/__docusaurus/debug/config', '5ba'),
    exact: true
  },
  {
    path: '/__docusaurus/debug/content',
    component: ComponentCreator('/__docusaurus/debug/content', 'a2b'),
    exact: true
  },
  {
    path: '/__docusaurus/debug/globalData',
    component: ComponentCreator('/__docusaurus/debug/globalData', 'c3c'),
    exact: true
  },
  {
    path: '/__docusaurus/debug/metadata',
    component: ComponentCreator('/__docusaurus/debug/metadata', '156'),
    exact: true
  },
  {
    path: '/__docusaurus/debug/registry',
    component: ComponentCreator('/__docusaurus/debug/registry', '88c'),
    exact: true
  },
  {
    path: '/__docusaurus/debug/routes',
    component: ComponentCreator('/__docusaurus/debug/routes', '000'),
    exact: true
  },
  {
    path: '/markdown-page',
    component: ComponentCreator('/markdown-page', '3d7'),
    exact: true
  },
  {
    path: '/docs',
    component: ComponentCreator('/docs', 'd57'),
    routes: [
      {
        path: '/docs',
        component: ComponentCreator('/docs', '28d'),
        routes: [
          {
            path: '/docs',
            component: ComponentCreator('/docs', '312'),
            routes: [
              {
                path: '/docs/chapter-01-introduction-to-physical-ai/lesson-1-1-what-is-physical-ai',
                component: ComponentCreator('/docs/chapter-01-introduction-to-physical-ai/lesson-1-1-what-is-physical-ai', 'dfb'),
                exact: true,
                sidebar: "tutorialSidebar"
              },
              {
                path: '/docs/chapter-01-introduction-to-physical-ai/lesson-1-2-embodied intelligence',
                component: ComponentCreator('/docs/chapter-01-introduction-to-physical-ai/lesson-1-2-embodied intelligence', '0fc'),
                exact: true,
                sidebar: "tutorialSidebar"
              },
              {
                path: '/docs/chapter-01-introduction-to-physical-ai/lesson-1-3-course overview & learning outcomes',
                component: ComponentCreator('/docs/chapter-01-introduction-to-physical-ai/lesson-1-3-course overview & learning outcomes', 'f39'),
                exact: true,
                sidebar: "tutorialSidebar"
              },
              {
                path: '/docs/chapter-02-robotic-nervous-system-ros-2/lesson-2-1-rOS 2 architecture',
                component: ComponentCreator('/docs/chapter-02-robotic-nervous-system-ros-2/lesson-2-1-rOS 2 architecture', '081'),
                exact: true,
                sidebar: "tutorialSidebar"
              },
              {
                path: '/docs/chapter-02-robotic-nervous-system-ros-2/lesson-2-2-nodes-topics-services-actions',
                component: ComponentCreator('/docs/chapter-02-robotic-nervous-system-ros-2/lesson-2-2-nodes-topics-services-actions', '7b8'),
                exact: true,
                sidebar: "tutorialSidebar"
              },
              {
                path: '/docs/chapter-02-robotic-nervous-system-ros-2/lesson-2-3-python integration',
                component: ComponentCreator('/docs/chapter-02-robotic-nervous-system-ros-2/lesson-2-3-python integration', '3f7'),
                exact: true,
                sidebar: "tutorialSidebar"
              },
              {
                path: '/docs/chapter-02-robotic-nervous-system-ros-2/lesson-2-4-urdf for humanoids',
                component: ComponentCreator('/docs/chapter-02-robotic-nervous-system-ros-2/lesson-2-4-urdf for humanoids', '83d'),
                exact: true,
                sidebar: "tutorialSidebar"
              },
              {
                path: '/docs/chapter-03-digital-twin-gazebo-unity/lesson-3-1-gazebo simulation basics',
                component: ComponentCreator('/docs/chapter-03-digital-twin-gazebo-unity/lesson-3-1-gazebo simulation basics', '6af'),
                exact: true,
                sidebar: "tutorialSidebar"
              },
              {
                path: '/docs/chapter-03-digital-twin-gazebo-unity/lesson-3-2-sensor simulation',
                component: ComponentCreator('/docs/chapter-03-digital-twin-gazebo-unity/lesson-3-2-sensor simulation', '1c1'),
                exact: true,
                sidebar: "tutorialSidebar"
              },
              {
                path: '/docs/chapter-03-digital-twin-gazebo-unity/lesson-3-3-high-fidelity rendering with unity',
                component: ComponentCreator('/docs/chapter-03-digital-twin-gazebo-unity/lesson-3-3-high-fidelity rendering with unity', 'cc0'),
                exact: true,
                sidebar: "tutorialSidebar"
              },
              {
                path: '/docs/chapter-04-ai-robot-brain-nvidia-isaac/lesson-4-1-isaac-sim-overview',
                component: ComponentCreator('/docs/chapter-04-ai-robot-brain-nvidia-isaac/lesson-4-1-isaac-sim-overview', '109'),
                exact: true,
                sidebar: "tutorialSidebar"
              },
              {
                path: '/docs/chapter-04-ai-robot-brain-nvidia-isaac/lesson-4-2-isaac-ros-navigation',
                component: ComponentCreator('/docs/chapter-04-ai-robot-brain-nvidia-isaac/lesson-4-2-isaac-ros-navigation', '919'),
                exact: true,
                sidebar: "tutorialSidebar"
              },
              {
                path: '/docs/chapter-04-ai-robot-brain-nvidia-isaac/lesson-4-3-rl-sim-to-real',
                component: ComponentCreator('/docs/chapter-04-ai-robot-brain-nvidia-isaac/lesson-4-3-rl-sim-to-real', '77b'),
                exact: true,
                sidebar: "tutorialSidebar"
              },
              {
                path: '/docs/chapter-05-vision-language-action-vla/lesson-5-1-llm-integration',
                component: ComponentCreator('/docs/chapter-05-vision-language-action-vla/lesson-5-1-llm-integration', '483'),
                exact: true,
                sidebar: "tutorialSidebar"
              },
              {
                path: '/docs/chapter-05-vision-language-action-vla/lesson-5-2-voice-to-action',
                component: ComponentCreator('/docs/chapter-05-vision-language-action-vla/lesson-5-2-voice-to-action', 'dee'),
                exact: true,
                sidebar: "tutorialSidebar"
              },
              {
                path: '/docs/chapter-05-vision-language-action-vla/lesson-5-3-cognitive-planning',
                component: ComponentCreator('/docs/chapter-05-vision-language-action-vla/lesson-5-3-cognitive-planning', '6c6'),
                exact: true,
                sidebar: "tutorialSidebar"
              },
              {
                path: '/docs/chapter-06-capstone-project/lesson-6-1-autonomous-humanoid-overview',
                component: ComponentCreator('/docs/chapter-06-capstone-project/lesson-6-1-autonomous-humanoid-overview', 'd26'),
                exact: true,
                sidebar: "tutorialSidebar"
              },
              {
                path: '/docs/chapter-06-capstone-project/lesson-6-2-integration-of-modules',
                component: ComponentCreator('/docs/chapter-06-capstone-project/lesson-6-2-integration-of-modules', '688'),
                exact: true,
                sidebar: "tutorialSidebar"
              },
              {
                path: '/docs/chapter-06-capstone-project/lesson-6-3-deployment-assessment',
                component: ComponentCreator('/docs/chapter-06-capstone-project/lesson-6-3-deployment-assessment', 'fab'),
                exact: true,
                sidebar: "tutorialSidebar"
              },
              {
                path: '/docs/intro',
                component: ComponentCreator('/docs/intro', '61d'),
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
    path: '/',
    component: ComponentCreator('/', 'e5f'),
    exact: true
  },
  {
    path: '*',
    component: ComponentCreator('*'),
  },
];
