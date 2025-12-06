# Lesson 2.4: URDF for Humanoids

URDF (Unified Robot Description Format) is an XML-based format used to describe the structure and properties of robots in ROS 2. It allows simulation, visualization, and integration of humanoid robots in Gazebo or RViz.

**Key Concepts:**
- **Links:** Represent rigid parts of the robot (head, torso, arms, legs)
- **Joints:** Define how links move relative to each other (revolute, continuous, fixed)
- **Sensors & Actuators:** Cameras, IMUs, motors, servos
- **Kinematics & Dynamics:** Joint limits, mass, center of gravity, inertia
- **Simulation & Visualization:** Used in Gazebo, RViz for testing motion, balance, and manipulation

**Example Workflow:**
1. Define all links (torso, limbs, head) in URDF XML.
2. Define joints connecting the links.
3. Attach sensors (camera, IMU) and actuators (motors, servos).
4. Load the URDF in Gazebo to simulate walking, grasping, or navigation.
5. Visualize robot structure and sensor data in RViz.


**Notes:**
- Always check joint limits and collision properties.
- Use `xacro` files for reusable and parametric URDFs.
- URDF is critical for building a humanoid’s digital twin in ROS 2.

