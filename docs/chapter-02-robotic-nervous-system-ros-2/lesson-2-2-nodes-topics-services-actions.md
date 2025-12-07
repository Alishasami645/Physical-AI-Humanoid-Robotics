---
id: "lesson-2-2-nodes-topics-services-actions"
title: "Lesson 2.2 — Nodes, Topics, Services, and Actions"
sidebar_label: "Lesson 2.2: Nodes, Topics, Services, Actions"
sidebar: tutorialSidebar
---

# Lesson 2.2: Nodes, Topics, Services, Actions

ROS 2 nodes interact using topics, services, and actions. This enables modular, decoupled robot software that can be scaled.

**Key Concepts:**
- **Node Communication:**
  - Publisher → Topic → Subscriber
- **Service:**
  - Request/response for synchronous operations
- **Action:**
  - Long-running operations
  - Provides feedback and result to clients

**Example Workflow:**
1. Sensor node publishes sensor data on a topic.
2. Processing node subscribes to the topic, analyzes data.
3. Control node receives processed information and commands actuators.


