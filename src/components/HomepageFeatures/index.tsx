import styles from './styles.module.css';

import React from "react";


export default function HomepageFeatures() {
  const modules = [
    {
      title: "Module 1: Foundations of Embodied AI",
      description:
        "Learn the fundamentals of intelligent systems that connect digital reasoning with the physical world.",
      image: "img/ai1.png",
      bg: "#E8F5E9",
    },
    {
      title: "Module 2: Vision-Language-Action Systems",
      description:
        "Understand how robots see, interpret language, and perform tasks using modern AI models.",
      image: "img/ai2.png",
      bg: "#E8F5E9",
    },
    {
      title: "Module 3: Humanoid Robotics & Deployment",
      description:
        "Build and deploy humanoid robots in simulation and real-world environments.",
      image: "img/ai3.png",
      bg: "#E8F5E9",
    },
  ];

  return (
    <div className={styles.modulesWrapper}>
      {modules.map((mod, index) => (
        <a
          key={index}
          className={styles.moduleCard}
          style={{ backgroundColor: mod.bg }}
        >
          <img src={mod.image} alt={mod.title} className={styles.moduleImage} />
          <h3>{mod.title}</h3>
          <p>{mod.description}</p>
        </a>
      ))}
    </div>
  );
}