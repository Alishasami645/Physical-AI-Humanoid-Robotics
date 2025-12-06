# Implementation Plan Prompt for Physical AI Humanoid Robotics Docusaurus Textbook

## Objective
Generate a complete, high-quality Docusaurus textbook for the "Physical AI & Humanoid Robotics" course. The textbook should include all chapters, lessons, learning outcomes, illustrative diagrams, and UI elements. Content must reflect the specifications in `specs/feature/physical-ai-humanoid-robotics/spec.md`.

## Requirements
1. **Target Directory**: `my-books/docs/`
2. **Chapters and Lessons**: Include all chapters as per the course outline. Each chapter must have multiple lessons with clear learning outcomes.
3. **UI/UX Elements**: Include Docusaurus-compatible images, diagrams (Mermaid), and callouts where appropriate.
4. **Consistency**: Ensure consistent Markdown formatting, headings, and links.
5. **Edge Cases**: Include edge computing, ROS 2 nodes, Gazebo simulations, NVIDIA Isaac, VLA integration, and capstone project workflow.
6. **File Naming**: Use lowercase, hyphen-separated filenames for each chapter/lesson (e.g., `chapter-01-intro.md`).

## Chapters Overview
- **Chapter 1: Introduction to Physical AI**
  - Lessons: Foundations, Embodied Intelligence, Humanoid Robotics Overview
- **Chapter 2: ROS 2 Fundamentals**
  - Lessons: Nodes, Topics, Services, Launch Files, Python Packages
- **Chapter 3: Robot Simulation with Gazebo**
  - Lessons: URDF, SDF, Physics, Sensors, Unity Visualization
- **Chapter 4: NVIDIA Isaac AI**
  - Lessons: Isaac SDK, Perception, Manipulation, Sim-to-Real Transfer
- **Chapter 5: Vision-Language-Action**
  - Lessons: Voice-to-Action, Cognitive Planning, Multi-modal Interaction
- **Chapter 6: Capstone Project**
  - Lessons: Autonomous Humanoid, Obstacle Navigation, Object Manipulation

## Instructions for Text Generation
1. Create each chapter folder and lesson Markdown file inside `my-books/docs/`.
2. Include all learning outcomes at the start of each lesson.
3. Include illustrative images from `my-books/static/img/` such as `undraw_docusaurus_react.svg`.
4. Add Mermaid diagrams for ROS 2 architecture, sensor systems, and VLA workflows.
5. Preserve Docusaurus configuration (`docusaurus.config.ts`), sidebar (`sidebars.ts`), and TS config files.
6. Follow proper Markdown conventions: headings, bullet points, code blocks, callouts, links.
7. Generate content in English, but highlight key terms for emphasis.

## History/Contributions
- Save history prompt in: `history/prompts/feature/physical-ai-humanoid-robotics/001-create-implementation-plan.prompt.md`.
- Track all generated files for chapters, lessons, and UI assets.

## Notes
- Never modify files outside `my-books/docs/` and `history/`.
- Ensure all content is aligned with course outline and spec file.
