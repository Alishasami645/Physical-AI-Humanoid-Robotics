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
    """Chat endpoint with SHORT, SIMPLE answers"""
    if not request.query.strip():
        raise HTTPException(status_code=400, detail="Query cannot be empty")
    
    query = request.query.lower()
    
    # Book structure response - SHORT VERSION
    if "chapter" in query or "lesson" in query or "topic" in query or "structure" in query or "kitne" in query or "book" in query or "course" in query:
        return {
            "answer": """# Book Structure

## 6 Chapters Overview

**Ch 1:** Introduction to Physical AI (3 lessons)
**Ch 2:** ROS 2 - Robotic Nervous System (4 lessons)
**Ch 3:** Digital Twin & Simulation with Gazebo & Unity (3 lessons)
**Ch 4:** AI Robot Brain - NVIDIA Isaac (3 lessons)
**Ch 5:** Vision-Language-Action Models (3 lessons)
**Ch 6:** Capstone Project - Build Your Own Robot (3 lessons)

Total: 6 Chapters with 19 Lessons

Each chapter builds on the previous one. Start with Chapter 1! 

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
    
    # Just show the short answer already provided above
    # (This condition is now redundant, can be handled by first condition)
    if False:  # Disabled to avoid duplicate
        pass

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
    
    # Autonomy response - SHORT VERSION
    if "autonomy" in query or "autonomous" in query:
        return {
            "answer": """# What is Autonomy?

**Autonomy = Robot makes decisions and acts independently without human control**

## 5 Levels of Autonomy:
1. **Remote Control** - Human controls everything (no autonomy)
2. **With Assistance** - Robot helps human (partial)
3. **Autonomous Tasks** - Robot does specific jobs (moderate)
4. **Conditional Autonomy** - Robot handles normal situations (high)
5. **Full Autonomy** - Robot handles everything independently (complete)

## How It Works:
**Sense** (cameras/sensors) → **Think** (AI/decision) → **Act** (move/perform) The robot perceives its environment, thinks about what to do, and takes action - all by itself.

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
    
    # ROS 2 response - SHORT VERSION
    if "ros 2" in query or "ros2" in query or "explain ros" in query:
        return {
            "answer": """# ROS 2 - Robot Operating System

**ROS 2 = The nervous system of your robot**

It connects all robot parts and lets them communicate.

## Core Concepts:
- **Nodes** = Independent programs (camera, planner, motor control)
- **Topics** = Data streams (one way: camera → vision processor)
- **Services** = Commands (ask for something, get response)
- **Actions** = Tasks (long jobs with feedback)

## Why Use It?
- Modular design (break complex systems into simple parts)
- Reusable code (thousands of ready-made packages)
- Real-time communication
- Works on any robot type

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
    
    # Physical AI response - SHORT VERSION
    if "physical ai" in query or "what is physical ai" in query:
        return {
            "answer": """# What is Physical AI?

**Physical AI = AI that interacts with the physical world**

## Traditional AI vs Physical AI:
- **Traditional AI**: Text/data processing (ChatGPT, language models)
- **Physical AI**: AI in robots that perceive + understand + act in real world

## Key Components:
1. **Perception** - See/hear the world (cameras, sensors)
2. **Understanding** - AI processes what it sees (computer vision, ML)
3. **Action** - Robot does something physical (move, manipulate)
4. **Learning** - Improves from experience

## Real Examples:
- Humanoid robots
- Self-driving cars
- Robotic arms
- Autonomous drones
- Manufacturing robots

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
    
    # Introduction response - SHORT VERSION
    if "introduction" in query or "start" in query or "hello" in query or "hi" in query:
        return {
            "answer": """# Welcome to Robotics Course!

**Learn to build intelligent robots from scratch.**

## 6 Chapters:
1. **Physical AI** - What is AI in the real world?
2. **ROS 2** - How to program robots
3. **Simulation** - Test robots before building (Gazebo, Unity)
4. **AI Brain** - Computer vision and decision-making (NVIDIA Isaac)
5. **Language** - Make robots understand voice commands
6. **Capstone** - Build your own autonomous humanoid robot

## You'll Learn:
- Robot control & programming
- Simulation & virtual environments
- AI perception & decision-making
- Voice & language processing
- Motion planning
- Real robot deployment

## Ask Me About:
- "What is physical AI?"
- "Explain ROS 2"
- "Tell me about Chapter X"
- "What is autonomy?"

**Let's build robots!**""",
            "sources": [
                {
                    "title": "Chapter 1: Introduction to Physical AI",
                    "section": "Course Overview",
                    "content": "Introduction to Physical AI and Humanoid Robotics"
                }
            ],
            "query": request.query
        }
    
    # Default response - SHORT
    return {
        "answer": f"""Robotics Chatbot Here!

Your Q: {request.query}

Ask me about:
- Physical AI
- ROS 2
- Simulation (Gazebo, Unity)
- AI & Vision
- Voice Commands
- Building Robots
- Any Chapter (1-6)

Try: "Tell me about Chapter 2" or "Explain ROS 2""",
        "sources": [
            {
                "title": "Robotics Book",
                "section": "Help",
                "content": "Ask me anything about robotics!"
            }
        ],
        "query": request.query
    }
