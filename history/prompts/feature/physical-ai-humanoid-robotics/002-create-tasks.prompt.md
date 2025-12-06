# Tasks Prompt for Physical AI Humanoid Robotics Docusaurus Textbook

## Objective
Generate high-quality, actionable tasks for building the Docusaurus textbook based on the implementation plan in `plan.md` and specifications in `spec.md`. Each task should be clear, measurable, and aligned with the course outline.

## Requirements
1. **Target Directory**: `my-books/docs/`
2. **Task Structure**:
   - Task ID (e.g., Task 1.1, Task 2.2)
   - Description
   - Expected output (Markdown file, diagram, image, etc.)
   - Dependencies (if any)
   - Status: `not_started`, `in_progress`, `complete`
3. **Content Coverage**:
   - Include all chapters and lessons
   - Include ROS 2, Gazebo, NVIDIA Isaac, VLA, Capstone
   - Include diagrams, images, and UI elements
4. **Consistency**: Ensure task formatting and naming conventions are consistent.

## Example Tasks
- **Task 1.1**: Create `chapter-01-intro.md` with lessons on Foundations of Physical AI and Embodied Intelligence.  
  **Output**: Markdown files with headings, bullet points, and learning outcomes.  
  **Dependencies**: None.  
  **Status**: `not_started`

- **Task 2.1**: Generate `chapter-02-ros2-fundamentals.md` with ROS 2 architecture, nodes, topics, services, and Python examples.  
  **Output**: Markdown file with code blocks and diagrams.  
  **Dependencies**: Task 1.1  
  **Status**: `not_started`

- **Task 5.1**: Generate `chapter-05-vla.md` with Vision-Language-Action content, Whisper integration, and cognitive planning examples.  
  **Output**: Markdown file with Mermaid diagrams and UI elements.  
  **Dependencies**: Previous chapters  
  **Status**: `not_started`

## Instructions for Task Generation
1. Assign each lesson a separate task if content is substantial.
2. Include all UI elements and illustrative images.
3. Track progress in `tasks.md` with status updates.
4. Ensure tasks follow the structure above and align with the implementation plan.

## History/Contributions
- Save history prompt in: `history/prompts/feature/physical-ai-humanoid-robotics/002-create-tasks.prompt.md`.
- Track creation and updates of each Markdown file as part of task execution.

## Notes
- Never modify files outside `my-books/docs/` and `history/`.
- Tasks must reflect the plan defined in `plan.md`.
