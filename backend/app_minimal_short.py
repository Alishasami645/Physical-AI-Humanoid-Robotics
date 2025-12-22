"""
Lightweight Robotics Chatbot API - Short Answer Version
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional, List, Dict, Any
import logging

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
**Ch 3:** Digital Twin & Simulation (Gazebo, Unity) (3 lessons)
**Ch 4:** AI Robot Brain - NVIDIA Isaac (3 lessons)
**Ch 5:** Vision-Language-Action Models (3 lessons)
**Ch 6:** Capstone Project - Build Your Own Robot (3 lessons)

**Total:** 6 Chapters with 19 Lessons

Each chapter builds on the previous one. Start with Chapter 1!""",
            "sources": [
                {
                    "title": "Robotics Course",
                    "section": "Course Structure",
                    "content": "All 6 chapters with 19 lessons"
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
**Sense** (cameras/sensors) → **Think** (AI/decision) → **Act** (move/perform)

Examples: Self-driving cars, warehouse robots, drones""",
            "sources": [
                {
                    "title": "Robotics Autonomy",
                    "section": "What is Autonomy?",
                    "content": "Autonomy levels and examples"
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
- Works on any robot type""",
            "sources": [
                {
                    "title": "Chapter 2: ROS 2",
                    "section": "Introduction",
                    "content": "ROS 2 basics and core concepts"
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
- Manufacturing robots""",
            "sources": [
                {
                    "title": "Chapter 1: Physical AI",
                    "section": "What is Physical AI?",
                    "content": "Definition and importance of Physical AI"
                }
            ],
            "query": request.query
        }
    
    # Gazebo response
    if "gazebo" in query or "simulation" in query:
        return {
            "answer": """# Gazebo & Simulation

**Gazebo = Virtual world where you test robots before building them**

## Why Simulate?
- Cost effective (no expensive hardware failures)
- Faster development (test ideas quickly)
- Safe (no real-world accidents)
- Repeatable (same test every time)

## What Gazebo Does:
- 3D simulation environment
- Physics simulation (gravity, friction, collisions)
- Sensor simulation (cameras, LiDAR, IMU)
- Integration with ROS 2

## Before Real Robot:
Simulation → Test → Debug → Deploy to real robot""",
            "sources": [
                {
                    "title": "Chapter 3: Simulation",
                    "section": "Gazebo",
                    "content": "Gazebo simulator basics"
                }
            ],
            "query": request.query
        }
    
    # Isaac response
    if "isaac" in query or "nvidia" in query or "perception" in query:
        return {
            "answer": """# NVIDIA Isaac - AI for Robots

**Isaac = Platform for AI perception and decision-making in robots**

## What It Does:
- Computer vision (see and understand)
- Object detection (identify things)
- Pose estimation (know where things are)
- Real-time inference (fast processing)

## Isaac Components:
1. **Isaac Sim** - Simulation environment
2. **Isaac ROS** - Integration with ROS 2
3. **AI Models** - Pre-trained vision models

## Real Use Cases:
- Autonomous navigation
- Picking objects (warehouse robots)
- Manufacturing quality control
- Healthcare assistance""",
            "sources": [
                {
                    "title": "Chapter 4: AI Robot Brain",
                    "section": "NVIDIA Isaac",
                    "content": "Isaac platform for robot perception"
                }
            ],
            "query": request.query
        }
    
    # VLA response
    if "vla" in query or "language" in query or "voice" in query or "whisper" in query:
        return {
            "answer": """# Vision-Language-Action (VLA) Models

**VLA = Robots that understand language and act accordingly**

## How It Works:
1. **Listen** - Robot hears voice command ("Pick up the cup")
2. **Understand** - AI processes the command
3. **Plan** - Decides what action to take
4. **Act** - Performs the action

## Technologies Used:
- **Whisper** - Speech-to-text (OpenAI)
- **Language Models** - Understanding commands
- **Vision Models** - See what to do
- **Control Systems** - Execute actions

## Example Flow:
Voice Command → Text → Understanding → Vision → Action""",
            "sources": [
                {
                    "title": "Chapter 5: Vision-Language-Action",
                    "section": "VLA Basics",
                    "content": "Language-conditioned robot actions"
                }
            ],
            "query": request.query
        }
    
    # Capstone response
    if "capstone" in query or "project" in query or "build" in query:
        return {
            "answer": """# Capstone Project - Build Your Robot

**Your goal: Create a complete autonomous humanoid robot system**

## What You'll Build:
- Robot structure (using URDF)
- Simulation environment
- AI perception system
- Voice control interface
- Autonomous navigation
- Real robot deployment

## Project Phases:
1. **Design** - Plan your robot
2. **Simulate** - Build and test in Gazebo
3. **Code** - Write ROS 2 nodes
4. **Integrate** - Connect all components
5. **Deploy** - Test on real hardware
6. **Present** - Show your work!

## Technologies Combined:
ROS 2 + Gazebo + Isaac + Vision + Language + Control Systems""",
            "sources": [
                {
                    "title": "Chapter 6: Capstone",
                    "section": "Project Overview",
                    "content": "Build your autonomous robot"
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
                    "title": "Course",
                    "section": "Welcome",
                    "content": "Introduction to robotics course"
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

Try: "Tell me about Chapter 2" or "Explain ROS 2\"""",
        "sources": [
            {
                "title": "Robotics Course",
                "section": "Help",
                "content": "Ask anything about robotics!"
            }
        ],
        "query": request.query
    }
