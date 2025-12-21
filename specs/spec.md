# Physical AI & Humanoid Robotics – Specification

Feature: Physical AI & Humanoid Robotics  
Focus: AI Systems in the Physical World, Embodied Intelligence  
Goal: Bridge the gap between digital brain and physical body. Students apply AI knowledge to control humanoid robots in simulation and real environments.

Modules & Chapters:
1. **Robotic Nervous System (ROS 2)**
   - ROS 2 architecture
   - Nodes, Topics, Services
   - Python agents & URDF
2. **Digital Twin (Gazebo & Unity)**
   - Physics simulation
   - Robot/environment modeling
   - Sensor simulation: LiDAR, IMUs, Depth Cameras
3. **AI-Robot Brain (NVIDIA Isaac)**
   - Isaac Sim, Isaac ROS
   - Path planning & navigation
   - Reinforcement learning
4. **Vision-Language-Action (VLA)**
   - LLM integration
   - Voice-to-Action commands
   - Cognitive planning

Learning Outcomes:
- Understand Physical AI principles
- Master ROS 2 for robot control
- Simulate robots in Gazebo & Unity
- Develop with NVIDIA Isaac
- Integrate GPT/LLMs for conversational robotics
- Design humanoid robots for natural interaction

Hardware Requirements:
- Workstations: NVIDIA RTX GPU, Ubuntu 22.04, 64GB RAM
- Edge AI kits: Jetson Orin Nano, RealSense Camera, ReSpeaker USB Mic
- Optional: Unitree Go2/G1 humanoid robot

Capstone Project:
- Autonomous humanoid robot receives voice commands, navigates obstacles, identifies objects, manipulates them, and reports actions.

## Hackathon Scoring Rubric

### Base Functionality (100 points)
Points will be awarded out of 100 for base functionality as defined in the core learning outcomes and project structure above.

### Bonus Points (Up to 200 additional points)

**1. Claude Code Subagents & Agent Skills (50 bonus points)**
- Participants will receive up to 50 extra bonus points by creating and using reusable intelligence via Claude Code Subagents and Agent Skills in the book project.
- Demonstrates advanced AI integration and code reusability patterns.

**2. Authentication & Personalization Questions (50 bonus points)**
- Participants will receive up to 50 extra bonus points for implementing Signup and Signin using [better-auth.com](https://www.better-auth.com/)
- During signup, the system will ask users questions about their:
  - Software background (e.g., programming experience level, languages known)
  - Hardware background (e.g., familiarity with robotics, embedded systems)
- The collected information enables content personalization based on user background.

**3. Content Personalization by User Background (50 bonus points)**
- Logged users can personalize the content in chapters by pressing a button at the start of each chapter.
- Content difficulty, depth, and examples adapt based on the user's software and hardware background collected during signup.
- Personalization should provide:
  - Beginner, Intermediate, and Advanced difficulty levels
  - Tailored code examples and explanations
  - Relevant prerequisite recommendations

**4. Urdu Language Translation (50 bonus points)**
- Logged users can translate the content to Urdu in the chapters by pressing a button at the start of each chapter.
- Translation should cover:
  - Chapter content (markdown text)
  - Code comments and explanations
  - Technical terminology with proper translations
- Users can toggle between English and Urdu views seamlessly.

### Scoring Breakdown
- **Base Score:** 0-100 points (core functionality)
- **Maximum Bonus:** 200 points (four optional features)
- **Possible Total:** Up to 300 points

Notes:
- Ensure Docusaurus Markdown compatibility.
- Lessons, chapters, diagrams, and UI elements should follow Docusaurus structure.
- Save history prompts for all generated content in: `history/prompts/feature/physical-ai-humanoid-robotics/`.
- All bonus features should integrate seamlessly with the base Docusaurus platform and maintain responsive design.
