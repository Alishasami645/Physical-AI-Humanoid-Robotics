"""
Lightweight Robotics Chatbot API - Minimal version to test connectivity
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional, List, Dict, Any
import logging
import json

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Create app
app = FastAPI(
    title="Robotics Book RAG Chatbot",
    version="1.0.0"
)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Models
class ChatRequest(BaseModel):
    query: str
    selected_text: Optional[str] = None

class ChatResponse(BaseModel):
    answer: str
    sources: List[Dict[str, Any]]
    query: str

# ============ ENDPOINTS ============

@app.get("/health")
async def health():
    """Health check"""
    return {
        "status": "healthy",
        "service": "Robotics Book RAG Chatbot",
        "version": "1.0.0"
    }

@app.post("/api/chat")
async def chat(request: ChatRequest):
    """Chat endpoint with comprehensive book responses"""
    if not request.query.strip():
        raise HTTPException(status_code=400, detail="Query cannot be empty")
    
    query = request.query.lower()
    
    # Book structure response
    if "chapter" in query or "lesson" in query or "topic" in query or "structure" in query or "kitne" in query or "book" in query or "course" in query:
        return {
            "answer": """# Physical AI & Humanoid Robotics - Complete Book Structure

## Overview
This comprehensive course has **6 Chapters** with **19 Lessons** covering everything needed to build intelligent humanoid robots.

---

## CHAPTER 1: Introduction to Physical AI (3 Lessons)

**Chapter Overview:** Understand what Physical AI is and why it matters.

### Lesson 1.1 - What is Physical AI?
- Definition: AI that interacts with the physical world
- Difference from traditional AI
- Real-world impact and applications
- Why robots need physical understanding

### Lesson 1.2 - Embodied Intelligence
- Intelligence comes from having a body
- Sensors and actuators as intelligence
- How physical constraints shape learning
- Examples: Humanoid vs wheeled robots

### Lesson 1.3 - Course Overview
- What you'll build in this course
- Prerequisites and setup
- Tools and technologies used
- Learning path and progression

---

## CHAPTER 2: Robotic Nervous System - ROS 2 (4 Lessons)

**Chapter Overview:** Master ROS 2 - the framework that connects all robot parts.

### Lesson 2.1 - ROS 2 Architecture
- ROS 2 fundamentals and design
- Nodes, topics, services explained
- How ROS 2 manages communication
- Comparing ROS 1 vs ROS 2

### Lesson 2.2 - Nodes, Topics, Services & Actions
- Creating publisher/subscriber nodes
- Topic-based communication
- Service request-response pattern
- Actions for long-running tasks
- Building a complete ROS 2 system

### Lesson 2.3 - Python Integration
- Writing ROS 2 nodes in Python
- Using rclpy library
- Creating custom messages
- Debugging ROS 2 applications
- Common patterns and best practices

### Lesson 2.4 - URDF for Humanoids
- URDF file format (description language)
- Robot kinematics description
- Links and joints definition
- Building a humanoid robot description
- Visualization in RViz

---

## CHAPTER 3: Digital Twin & Simulation (3 Lessons)

**Chapter Overview:** Create virtual robots before building physical ones.

### Lesson 3.1 - Gazebo Simulation Basics
- Gazebo simulator setup
- Creating 3D robot models
- Physics simulation
- Sensor simulation in Gazebo
- Running simulations with ROS 2

### Lesson 3.2 - Sensor Simulation
- Camera simulation
- LiDAR/Depth sensor simulation
- IMU (motion sensor) simulation
- Touch and force sensors
- Realistic sensor noise modeling

### Lesson 3.3 - High-Fidelity Rendering with Unity
- Unity for photorealistic simulation
- Bridging Unity and ROS 2
- Building realistic training environments
- Graphics vs physics simulation
- Using Unity for learning and testing

---

## CHAPTER 4: AI Robot Brain - NVIDIA Isaac (3 Lessons)

**Chapter Overview:** Add AI perception and decision-making to your robot.

### Lesson 4.1 - Isaac Sim Overview
- NVIDIA Isaac platform introduction
- Isaac Sim for realistic simulation
- GPU-accelerated physics
- Synthetic data generation
- Training robots in simulation

### Lesson 4.2 - Isaac ROS for Navigation
- Navigation stack with Isaac
- Path planning algorithms
- Obstacle detection and avoidance
- Autonomous navigation
- Integrating with ROS 2

### Lesson 4.3 - Reinforcement Learning
- Training robots with RL
- Policy learning
- Reward functions
- Transfer learning (sim-to-real)
- DRL frameworks and tools

---

## CHAPTER 5: Vision-Language-Action (VLA) Models (3 Lessons)

**Chapter Overview:** Enable robots to understand language and act accordingly.

### Lesson 5.1 - LLM Integration
- Large Language Models for robotics
- Prompt engineering for robots
- Natural language understanding
- Semantic parsing
- Building a language interface

### Lesson 5.2 - Voice to Action with Whisper
- Speech recognition with OpenAI Whisper
- Converting voice to text
- Processing voice commands
- Real-time audio streaming
- Multi-language support

### Lesson 5.3 - Cognitive Planning
- From language to action
- Task planning with language
- Hierarchical task decomposition
- Reasoning and decision making
- Building intelligent robot behaviors

---

## CHAPTER 6: Capstone Project (3 Lessons)

**Chapter Overview:** Build a complete autonomous humanoid system.

### Lesson 6.1 - Autonomous Humanoid Overview
- Complete system architecture
- Integrating all previous components
- Sensor fusion
- Real-time decision making
- System optimization

### Lesson 6.2 - Integration of Modules
- Connecting ROS 2 nodes
- Integrating simulation and real robot
- Sensor-to-decision pipeline
- Performance tuning
- Debugging complex systems

### Lesson 6.3 - Deployment & Assessment
- Deploying on physical robot
- Sim-to-real transfer
- Testing and validation
- Safety considerations
- Production-ready robotics

---

## Learning Path Summary

### Beginner (Chapters 1-2)
- Understand robotics fundamentals
- Learn ROS 2 basics
- Build your first robot system

### Intermediate (Chapters 3-4)
- Simulate robots
- Add AI perception
- Autonomous navigation

### Advanced (Chapters 5-6)
- Language understanding
- Complex behaviors
- Production systems

---

## Total Content
- **6 Major Chapters**
- **19 Detailed Lessons**
- **Hundreds of code examples**
- **Project-based learning**
- **From theory to deployment**

---

## What You'll Build
1. ROS 2 robot control system
2. Simulated humanoid robot
3. Autonomous navigation system
4. AI-powered perception
5. Voice-controlled robot
6. Complete autonomous humanoid

---

**Ready to start?** Ask about any specific chapter or lesson!
""",
            "sources": [
                {
                    "title": "Physical AI & Humanoid Robotics",
                    "section": "Complete Course Structure",
                    "content": "All 6 chapters, 19 lessons, and complete learning path"
                }
            ],
            "query": request.query
        }
    
    # Book structure response
    if "chapter" in query or "lesson" in query or "topic" in query or "structure" in query or "kitne" in query:
        return {
            "answer": """# Book Structure: Physical AI & Humanoid Robotics

## Complete Book Overview

This course has **6 Main Chapters** with **Multiple Lessons** in each chapter. Here's the complete structure:

---

## CHAPTER 1: Introduction to Physical AI

### Topics Covered:
1. What is Physical AI?
   - Definition and concepts
   - Embodied intelligence
   - AI vs Physical AI differences

2. Real-World Applications
   - Manufacturing robots
   - Healthcare robotics
   - Autonomous vehicles
   - Service robots

3. Course Roadmap
   - What you'll build
   - Prerequisites
   - Learning outcomes

**Duration:** 2-3 weeks
**Difficulty:** Beginner

---

## CHAPTER 2: Robotic Nervous System (ROS 2)

### Lessons in this Chapter:

**Lesson 2.1: ROS 2 Architecture**
- What is ROS 2?
- Comparison with ROS 1
- Publish-Subscribe model
- DDS (Data Distribution Service)

**Lesson 2.2: Nodes, Topics, Services, Actions**
- Understanding Nodes
- Topic-based communication
- Service request-response
- Action long-running tasks
- Practical examples

**Lesson 2.3: Python Integration**
- Setting up ROS 2 with Python
- Writing your first node
- Publishing and subscribing
- Service implementation
- Code examples

**Lesson 2.4: URDF for Humanoids**
- URDF (Unified Robot Description Format)
- Creating robot models
- Joint definitions
- Kinematic chains
- Building a humanoid structure

**Duration:** 3-4 weeks
**Difficulty:** Intermediate

---

## CHAPTER 3: Digital Twin & Simulation (Gazebo + Unity)

### Topics in this Chapter:

**Lesson 3.1: Gazebo Simulation Basics**
- Introduction to Gazebo
- Physics engine
- Creating virtual environments
- Adding robots to simulation
- Running simulations

**Lesson 3.2: Advanced Gazebo**
- Sensor simulation
- Camera simulation
- IMU and LiDAR
- Plugin development
- Debugging in simulation

**Lesson 3.3: Unity for Robotics**
- Unity robotics toolkit
- 3D visualization
- Real-time simulation
- Human-robot interaction visualization

**Lesson 3.4: Sim-to-Real Transfer**
- Testing in simulation first
- Transferring to real robots
- Safety considerations
- Validation techniques

**Duration:** 3-4 weeks
**Difficulty:** Intermediate to Advanced

---

## CHAPTER 4: AI Robot Brain (NVIDIA Isaac)

### Topics in this Chapter:

**Lesson 4.1: NVIDIA Isaac Overview**
- Introduction to Isaac
- Hardware requirements
- Software setup
- Isaac Sim

**Lesson 4.2: Computer Vision for Robots**
- Image processing basics
- Object detection
- Pose estimation
- Semantic segmentation
- Real-time processing

**Lesson 4.3: Perception Pipeline**
- Sensor fusion
- Multi-camera systems
- Real-world challenges
- Performance optimization

**Lesson 4.4: AI Decision Making**
- Neural networks for robotics
- Deep learning models
- Training and inference
- Edge computing

**Duration:** 4-5 weeks
**Difficulty:** Advanced

---

## CHAPTER 5: Vision-Language-Action (VLA) Models

### Topics in this Chapter:

**Lesson 5.1: Multimodal AI**
- Understanding VLA models
- Vision transformers
- Language models
- Integration

**Lesson 5.2: Language-Conditioned Actions**
- Natural language understanding
- Converting language to actions
- Real-world examples
- Building VLA systems

**Lesson 5.3: Robot Adaptation**
- Learning from human demonstrations
- Reinforcement learning basics
- Fine-tuning models
- Transfer learning

**Lesson 5.4: Advanced Applications**
- Multi-robot coordination
- Complex task planning
- Reasoning in robotics
- Future directions

**Duration:** 4-5 weeks
**Difficulty:** Advanced

---

## CHAPTER 6: Capstone Project

### Project Components:

**Part 1: System Integration**
- Combine all previous learnings
- Build complete autonomous system
- Integrate perception, planning, and control

**Part 2: Humanoid Robot Development**
- Design humanoid structure (using URDF)
- Implement kinematics
- Control algorithms

**Part 3: Real-World Deployment**
- Testing on physical hardware
- Debugging real-world issues
- Performance evaluation
- Documentation

**Part 4: Presentation & Evaluation**
- Demonstrate your robot
- Explain your design choices
- Discuss challenges and solutions

**Duration:** 6-8 weeks
**Difficulty:** Advanced

---

## Total Course Structure

| Chapter | Duration | Total Lessons | Difficulty |
|---------|----------|---------------|-----------|
| Ch 1: Physical AI Intro | 2-3 weeks | 3 | Beginner |
| Ch 2: ROS 2 | 3-4 weeks | 4 | Intermediate |
| Ch 3: Gazebo + Unity | 3-4 weeks | 4 | Intermediate |
| Ch 4: NVIDIA Isaac | 4-5 weeks | 4 | Advanced |
| Ch 5: VLA Models | 4-5 weeks | 4 | Advanced |
| Ch 6: Capstone Project | 6-8 weeks | 4 parts | Advanced |
| **TOTAL** | **22-29 weeks** | **23 lessons** | **Mixed** |

---

## Key Topics You'll Learn

### Robotics Fundamentals
- Robot kinematics and dynamics
- Motion planning
- Control systems
- Sensor integration

### Software Development
- ROS 2 programming
- Python for robotics
- Real-time systems
- Distributed computing

### AI/ML Concepts
- Computer vision
- Deep learning
- Reinforcement learning
- Natural language processing

### Hardware Integration
- Actuator control
- Sensor reading
- Real-world debugging
- Performance optimization

---

## Learning Path

1. **Start with Chapter 1** - Understand what Physical AI is
2. **Move to Chapter 2** - Learn the software foundation (ROS 2)
3. **Chapter 3** - Practice in simulation before real hardware
4. **Chapter 4** - Add AI perception to your robot
5. **Chapter 5** - Make your robot understand language
6. **Chapter 6** - Build your complete autonomous system

---

## Prerequisites

- Basic Python programming
- Basic understanding of linear algebra
- Familiarity with command line/terminal
- Ubuntu/Linux knowledge helpful

---

**Total Learning Time:** 5-7 months (intensive study)

Each chapter builds on the previous one. Complete Chapter 1 before moving to Chapter 2!

Ready to start? Ask about any specific chapter or lesson!
""",
            "sources": [
                {
                    "title": "Course Structure",
                    "section": "Complete Book Overview",
                    "content": "All chapters, lessons, and topics in the Physical AI and Humanoid Robotics course"
                }
            ],
            "query": request.query
        }
    
    # Autonomy response
    if "autonomy" in query or "autonomous" in query:
        return {
            "answer": """# Autonomy in Robotics Explained

## What is Autonomy?

**Autonomy** means a robot can **make decisions and act independently** without human control. The robot perceives its environment, thinks about what to do, and takes action - all by itself.

### Simple Definition
**Autonomy = Perception + Decision Making + Action (without human control)**

---

## Levels of Autonomy

### Level 1: Remote Control (No Autonomy)
- Human controls every movement
- Robot is just a tool
- Example: Video game controller for robot arm
- No intelligence needed

### Level 2: Teleoperation with Assistance
- Human gives commands
- Robot helps with some tasks
- Sensors assist but human decides
- Example: Self-parking cars (human presses button)

### Level 3: Autonomous Tasks
- Robot does specific jobs independently
- Human sets the goal
- Robot figures out how to achieve it
- Example: Vacuum cleaner finding optimal path

### Level 4: Conditional Autonomy
- Robot makes decisions in normal situations
- Can handle unexpected events
- Asks human for help if confused
- Example: Self-driving car (mostly autonomous)

### Level 5: Full Autonomy
- Complete independent operation
- Handles all situations
- No human intervention needed
- Example: Deep space explorer robot

---

## How Does Autonomy Work?

### Step 1: Perception
Robot uses sensors to understand the world:
- Cameras (vision)
- LiDAR (distance measurement)
- Microphones (sound)
- Touch sensors
- Motion sensors (IMU)

### Step 2: Processing
Robot analyzes the sensor data:
- What objects are around?
- Where am I?
- What's changed since last moment?
- What should I do?

### Step 3: Decision Making
Robot chooses what to do:
- Path planning (where to go)
- Action selection (what to do)
- Safety checking (is this safe?)
- Goal prioritization

### Step 4: Action
Robot executes the decision:
- Move motors
- Change direction
- Grasp objects
- Speak or communicate

---

## Key Components for Autonomy

### 1. Sensors (Eyes & Ears)
Without sensors = No autonomy. Robot can't see or hear = Can't make good decisions.

### 2. Processing Power (Brain)
Without computation = No thinking. Robot needs to process data quickly. Fast decisions = Better autonomy.

### 3. Decision Algorithms (Intelligence)
Without AI/ML = No smart decisions. Pure reaction = Not true autonomy. Learning improves autonomy over time.

### 4. Actuators (Muscles)
Without motors/joints = Can't act. Robot must actually do something. Action = Proof of autonomy.

---

## Real-World Examples

### Fully Autonomous (Level 5)
- Space rovers exploring Mars
- Delivery drones (in specific routes)
- Warehouse robots sorting packages
- Autonomous lawnmowers

### Highly Autonomous (Level 4)
- Self-driving cars
- Drones with obstacle avoidance
- Humanoid robots in factories
- Medical robots

### Assisted Autonomy (Level 3)
- Smart vacuum cleaners
- Robotic arms in surgery
- Semi-autonomous vehicles
- GPS-guided robots

---

## Autonomy vs Control

| Aspect | Manual Control | Autonomous |
|--------|----------------|-----------|
| Decision Making | Human decides | Robot decides |
| Perception | Limited feedback | Full sensor suite |
| Speed | Slow (human lag) | Fast (real-time) |
| Consistency | Variable | Repeatable |
| Complexity | Simple paths | Complex tasks |
| Intelligence | None | AI/ML algorithms |
| Human Effort | High | Low |

---

## Challenges to Autonomy

### 1. Perception Challenges
- Noisy sensor data
- Incomplete information
- Unpredictable environments
- Dynamic obstacles

### 2. Decision Challenges
- Ambiguous situations
- Unforeseen scenarios
- Resource constraints
- Real-time requirements

### 3. Action Challenges
- Mechanical failures
- Unexpected physics
- Interaction effects
- Unpredictable outcomes

### 4. Safety Challenges
- Ensuring safe actions
- Avoiding harm
- Ethical decision making
- Liability and responsibility

---

## Building Autonomous Robots

### In This Course, You'll Learn:

**Chapter 1** - Why autonomy matters in Physical AI
**Chapter 2** - ROS 2 (framework for autonomous systems)
**Chapter 3** - Simulation (test autonomy safely)
**Chapter 4** - AI perception (Isaac)
**Chapter 5** - Understanding language (VLA)
**Chapter 6** - Building fully autonomous humanoid

### Tools You'll Use:
- ROS 2 (robot framework)
- Gazebo (simulation)
- NVIDIA Isaac (AI)
- Python (programming)
- Machine Learning (intelligence)

---

## The Future of Autonomy

- More sensors = Better perception
- Faster AI = Better decisions
- Better simulation = Safer testing
- Real-time processing = Instant actions
- Learning systems = Improving robots

---

## Key Takeaway

**True autonomy means:**
- Robot understands its world (Perception)
- Robot knows what to do (Intelligence)
- Robot acts without human control (Action)
- Robot learns from experience (Improvement)

---

**Ready to build autonomous robots?** This course teaches you everything needed!
""",
            "sources": [
                {
                    "title": "Robotics Autonomy",
                    "section": "What is Autonomy?",
                    "content": "Complete explanation of autonomy levels, components, and implementation"
                }
            ],
            "query": request.query
        }
    
    # ROS 2 response
    if "ros 2" in query or "ros2" in query or "explain ros" in query:
        return {
            "answer": """# ROS 2: The Robotic Nervous System

## What is ROS 2?

**ROS 2** (Robot Operating System 2) is a flexible framework for writing robot software. It's the "nervous system" of your robot - managing communication, coordination, and data flow between different components.

Think of it like:
- **Nervous System** - Connects sensors to the brain to muscles
- **Bus System** - Carries messages between different robot parts
- **Middleware** - Software layer that handles all the hard parts of robotics

## Core Concepts

### 1. Nodes
- Independent programs/processes in your robot
- Example nodes: camera_driver, motion_planner, sensor_reader
- Nodes communicate with each other
- Can run on the same computer or across a network

### 2. Topics
- Communication channels where nodes publish/subscribe data
- One-way streaming of data
- Publishers: Nodes that send data (e.g., camera publishing images)
- Subscribers: Nodes that receive data (e.g., vision processor reading images)

Example:
```
Camera Node ----publishes to----> /camera/image (topic) ----subscribes---- Vision Node
```

### 3. Services
- Request-response communication (like function calls)
- A node asks another node to do something and waits for reply
- Synchronous communication
- Example: "Please move to position X" -> Robot responds "Done!"

### 4. Actions
- Long-running tasks with feedback
- Combine features of topics and services
- Example: "Move to location 10 meters away"
  - Goal: Go to location
  - Feedback: Current position updates
  - Result: Success/Failure

## ROS 2 Architecture

```
Your Robot
|
+-- Camera Node (publishes images)
|
+-- IMU Sensor Node (publishes orientation)
|
+-- Motion Planner (subscribes to sensors, publishes commands)
|
+-- Motor Controller Node (subscribes to commands, controls motors)
|
+-- Vision Processor (subscribes to images)
```

## Why ROS 2 is Important

1. **Modularity** - Break down complex tasks into simple nodes
2. **Reusability** - Use existing nodes and packages
3. **Real-time** - Better timing and determinism than ROS 1
4. **Scalability** - Works on tiny robots to massive systems
5. **Community** - Thousands of ready-made packages
6. **Multi-robot** - Supports swarms and collaborative robots

## Key ROS 2 Features

| Feature | Purpose |
|---------|---------|
| **Publish/Subscribe** | Real-time data streaming |
| **Services** | Request-response calls |
| **Actions** | Long tasks with feedback |
| **Parameters** | Configuration management |
| **Launch Files** | Start multiple nodes easily |
| **Middleware** | Works with DDS for communication |

## ROS 2 in Robotics

- **Autonomous Vehicles** - Coordinating sensors, planning, control
- **Humanoid Robots** - Managing multiple limbs, sensors
- **Drones** - Flight control, obstacle avoidance, navigation
- **Manipulator Arms** - Joint control, gripper operation
- **Mobile Robots** - Navigation, obstacle detection, mapping

## Python Integration

ROS 2 works great with Python:

```python
import rclpy
from std_msgs.msg import String

class MyNode:
    def __init__(self):
        self.node = rclpy.create_node('my_node')
        self.publisher = self.node.create_publisher(String, 'topic_name')
        self.subscription = self.node.create_subscription(
            String, 'input_topic', self.callback
        )
    
    def callback(self, msg):
        # Process incoming message
        response = String()
        response.data = f"Received: {msg.data}"
        self.publisher.publish(response)
```

## Common ROS 2 Commands

- `ros2 run package_name node_name` - Run a single node
- `ros2 launch package_name launch_file.py` - Run multiple nodes
- `ros2 topic list` - See all active topics
- `ros2 topic echo /topic_name` - Listen to a topic
- `ros2 node list` - See all running nodes
- `ros2 service call /service_name args` - Call a service

## The Future with ROS 2

ROS 2 is the modern standard for robotics, offering:
- Better security
- Easier distributed computing
- Real-time capabilities
- Production-ready reliability

---

**Next Steps:** Learn to build your first ROS 2 node, create topics, and make nodes communicate! This is the foundation of all robot programming.
""",
            "sources": [
                {
                    "title": "Chapter 2: Robotic Nervous System (ROS 2)",
                    "section": "Introduction to ROS 2",
                    "content": "Understanding ROS 2 architecture, nodes, topics, and services"
                }
            ],
            "query": request.query
        }
    
    # Physical AI response
    if "physical ai" in query or "what is physical ai" in query:
        return {
            "answer": """# Physical AI Explained

## What is Physical AI?

**Physical AI** is the intersection of **Artificial Intelligence** and the **Physical World**. It's about creating intelligent systems that can:

- Perceive their environment (using cameras, sensors, LiDAR)
- Understand what they see (computer vision, AI models)
- Reason about the world (decision-making algorithms)
- Act physically (move, manipulate, interact)
- Learn from experience (machine learning)

## Key Differences

### Traditional AI
- Runs on computers/cloud
- Processes data and text
- No physical interaction
- Example: ChatGPT, language models

### Physical AI (Embodied AI)
- Lives in robots and physical devices
- Perceives + understands + acts in the real world
- Must handle real-world complexity
- Example: Humanoid robots, autonomous vehicles, robotic arms

## Why Physical AI Matters

1. **Real-World Impact** - Directly affects the physical world
2. **Embodied Learning** - Understanding through physical interaction
3. **Robotics Revolution** - Enabling autonomous systems
4. **Real-time Processing** - Must respond to dynamic environments

## Embodied Intelligence

**Embodied Intelligence** means intelligence comes from having a BODY:
- The robot's physical form shapes how it thinks
- Sensors provide direct environment feedback
- Physical constraints drive learning

Example: A humanoid robot learns to walk by actually walking, feeling the physics, and adjusting balance in real-time.

## Real-World Applications

- Manufacturing: Robotic arms assembling products
- Healthcare: Surgical robots, rehabilitation robots
- Autonomous Vehicles: Self-driving cars
- Home Robotics: Service robots, humanoids
- Research: Exploration, space robotics
- Service Industry: Delivery and service robots

## The Future

Physical AI is the next frontier of AI - moving beyond software to create intelligent machines that can truly interact with and understand the physical world. This course teaches you how to build these systems from scratch!

---

**Ready to learn?** Continue to Chapter 1 or ask more questions!""",
            "sources": [
                {
                    "title": "Chapter 1: Introduction to Physical AI",
                    "section": "What is Physical AI?",
                    "content": "Definition and importance of Physical AI and embodied intelligence"
                }
            ],
            "query": request.query
        }
    
    # Introduction response
    if "introduction" in query or "start" in query or "hello" in query:
        return {
            "answer": """# Welcome to Physical AI & Humanoid Robotics

## Introduction to the Course

This comprehensive course introduces you to the fascinating world of **Physical AI** and **Humanoid Robotics**. You'll learn the fundamentals of building intelligent robots that can perceive, learn, and act in the physical world.

### What You'll Learn:

**Chapter 1: Introduction to Physical AI**
- What is Physical AI and embodied intelligence
- How robotics bridges AI and the physical world
- Real-world applications and impact

**Chapter 2: Robotic Nervous System (ROS 2)**
- Architecture of modern robotics operating systems
- Nodes, topics, services, and actions
- Python integration for robot control

**Chapter 3: Digital Twin & Simulation (Gazebo + Unity)**
- Creating virtual robot replicas
- Simulation-based testing and development
- Real-to-sim and sim-to-real transfer

**Chapter 4: AI Robot Brain (NVIDIA Isaac)**
- AI-powered perception and decision making
- Computer vision for robotics
- Real-time inference on edge devices

**Chapter 5: Vision-Language-Action (VLA) Models**
- Multimodal AI for robot understanding
- Language-conditioned robotic actions
- Building adaptive robot controllers

**Chapter 6: Capstone Project**
- Build a complete autonomous humanoid system
- Integrate all concepts into a working robot

### Key Topics:
- ROS 2 Architecture and Programming
- Gazebo Simulation Environment
- 3D Models and URDF Files
- NVIDIA Isaac Sim and Perceptor
- Vision and Language Models
- Motion Planning and Control

**Let's begin your robotics journey!** Ask any question about the chapters above, and I'll provide detailed explanations.""",
            "sources": [
                {
                    "title": "Chapter 1: Introduction to Physical AI",
                    "section": "Course Overview",
                    "content": "Introduction to Physical AI and Humanoid Robotics"
                }
            ],
            "query": request.query
        }
    
    # Default response
    return {
        "answer": f"""I'm the Robotics Chatbot! I'm here to help you learn about **Physical AI & Humanoid Robotics**.

Your question: "{request.query}"

I can help with:
- **Chapter 1**: Introduction to Physical AI and embodied intelligence
- **Chapter 2**: ROS 2 and the robotic nervous system
- **Chapter 3**: Digital twins with Gazebo and Unity
- **Chapter 4**: AI robot brain with NVIDIA Isaac
- **Chapter 5**: Vision-Language-Action models
- **Chapter 6**: Capstone projects

Try asking:
- "What is physical AI?"
- "Explain ROS 2"
- "How do robots perceive the world?"
- "Tell me about the capstone project"

Or type **"introduction"** to get started!""",
        "sources": [
            {
                "title": "Robotics Book",
                "section": "Help",
                "content": "Ask me anything about robotics!"
            }
        ],
        "query": request.query
    }

if __name__ == "__main__":
    import uvicorn
    print("[*] Starting Robotics Chatbot Backend...")
    print("[*] http://localhost:8000")
    print("[*] API Docs: http://localhost:8000/docs")
    print("[*] Health: http://localhost:8000/health")
    uvicorn.run(app, host="0.0.0.0", port=8000, log_level="info")
