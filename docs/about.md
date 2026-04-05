---
layout: default
title: About
permalink: /about/
---

<div class="hero-section" style="padding: 100px 0; background: var(--background-color); border-bottom: 1px solid var(--border-color); text-align: center;">
    <div class="container">
        <h1 style="font-size: var(--font-size-3xl); letter-spacing: -0.02em; color: var(--text-primary);">Hi, let me introduce myself!</h1>
        <div class="hero-headshots">
            <img src="{{ '/assets/images/personal/profile.svg' | relative_url }}" alt="Headshot 1">
            <img src="{{ '/assets/images/personal/headshot.jpeg' | relative_url }}" alt="Headshot 2">
            <img src="{{ '/assets/images/personal/profile.svg' | relative_url }}" alt="Headshot 3">
        </div>
    </div>
</div>

<div class="about-content">
    <div class="container">
        
        <section class="about-section">
            <h2>About Me</h2>
            <p>
                Hi, my name is Harrison (Harry) Saperstein. I graduated from WPI with my MS/BS in Robotics Engineering back in 2021. Growing up, my Dad brought me to as many FIRST competitions that came to town as we could, and I was always amazed by the teams and their robots. I was too young to grasp the scale of their accomplishments. WPI introduced me to what it means to be robotic, and come Junior year, when I was taking Linear Algebra and Differential Equations alongside courses where I was solving for the kinematics and controls of serial manipulators and turtlebots, I realized I was truly hooked and in trouble. I had grown an itch that was hard to satisfy.
            </p>
            <p>
                When I want to step away from a project, whether I'm stuck, hyperfocused to myown detriment, or need inspiration, I tend to be very active. I love skiing in the winter, I love golfing in the summer, and I especially love Boston sports. Even when I'm at my desk working through the next task to complete, I have some combination of the Sox, B's and Pats playing in the background. When a game isn't on, I turn to YouTube. I enjoy watching makers, like Adam Savage's Tested, Jeremy Fielding or StuffMadeHere, create solutions to real world problems from scratch and bring you along for the ride, to channels like Veritasium or Smarter Every Day where I can always learn something new, to, yes, consumer tech and video games.
            </p>

            <p>
                Please join me on this journey to explore, learn and scratch that itch by solving problems, making robots move, and continuing to grow as an engineer and enthusiast!
            </p>
        </section>

    </div>
</div>

<style>
.about-content {
    padding: var(--spacing-2xl) 0;
}

.hero-headshots {
    margin: var(--spacing-lg) auto 0;
    display: flex;
    justify-content: center;
    gap: var(--spacing-md);
    flex-wrap: wrap;
    max-width: 720px;
}

.hero-headshots img {
    width: 150px;
    height: 150px;
    object-fit: cover;
    border-radius: 50%;
    border: 3px solid var(--surface-color);
    box-shadow: 0 12px 30px rgba(0, 0, 0, 0.12);
}

.about-section {
    margin-bottom: var(--spacing-3xl);
}

.about-section h2 {
    color: var(--text-primary);
    margin-bottom: var(--spacing-lg);
    padding-bottom: var(--spacing-sm);
    border-bottom: 1px solid var(--border-color);
    font-size: var(--font-size-2xl);
    letter-spacing: -0.01em;
}

.features-list {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
    gap: var(--spacing-xl);
    margin-top: var(--spacing-lg);
}

.feature-item {
    padding: var(--spacing-lg);
    background-color: var(--surface-color);
    border-radius: var(--radius-sm);
    border: none;
    box-shadow: 0 4px 20px var(--shadow-color);
    transition: transform var(--transition-normal), box-shadow var(--transition-normal);
}

.feature-item:hover {
    transform: translateY(-4px);
    box-shadow: 0 12px 30px var(--shadow-hover);
}

.feature-item h3 {
    display: flex;
    align-items: center;
    gap: var(--spacing-sm);
    color: var(--text-primary);
    margin-bottom: var(--spacing-md);
}

.feature-item h3 i {
    color: var(--primary-color);
    font-size: var(--font-size-lg);
}

.perfect-for-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
    gap: var(--spacing-lg);
    margin-top: var(--spacing-lg);
}

.perfect-for-item {
    text-align: center;
    padding: var(--spacing-lg);
    background-color: var(--surface-color);
    border-radius: var(--radius-lg);
    border: 1px solid var(--border-color);
}

.perfect-for-item h4 {
    color: var(--primary-color);
    margin-bottom: var(--spacing-sm);
}

.tech-stack {
    display: flex;
    flex-wrap: wrap;
    gap: var(--spacing-lg);
    justify-content: center;
    margin-top: var(--spacing-lg);
}

.tech-item {
    display: flex;
    flex-direction: column;
    align-items: center;
    gap: var(--spacing-sm);
    padding: var(--spacing-lg);
    background-color: var(--surface-color);
    border-radius: var(--radius-lg);
    border: 1px solid var(--border-color);
    min-width: 120px;
}

.tech-item i {
    font-size: var(--font-size-2xl);
    color: var(--accent-color);
}

.tech-item span {
    font-weight: var(--font-weight-medium);
    color: var(--text-primary);
}

.getting-started-steps {
    background-color: var(--surface-color);
    padding: var(--spacing-xl);
    border-radius: var(--radius-lg);
    border: 1px solid var(--border-color);
    margin: var(--spacing-lg) 0;
}

.getting-started-steps li {
    margin-bottom: var(--spacing-md);
    line-height: var(--line-height-relaxed);
}

.cta-buttons {
    display: flex;
    gap: var(--spacing-md);
    justify-content: center;
    flex-wrap: wrap;
    margin-top: var(--spacing-xl);
}

@media (max-width: 640px) {
    .hero-headshots {
        display: grid;
        grid-template-columns: 1fr 1fr;
        grid-template-rows: auto auto;
        gap: var(--spacing-sm);
        justify-items: center;
    }
    .hero-headshots img:nth-child(2) {
        grid-column: 1 / span 2;
        grid-row: 1;
    }
    .hero-headshots img:nth-child(1) {
        grid-column: 1;
        grid-row: 2;
    }
    .hero-headshots img:nth-child(3) {
        grid-column: 2;
        grid-row: 2;
    }
    
    .features-list {
        grid-template-columns: 1fr;
    }
    
    .perfect-for-grid {
        grid-template-columns: 1fr;
    }
    
    .tech-stack {
        justify-content: center;
    }
    
    .cta-buttons {
        flex-direction: column;
        align-items: center;
    }
}
</style>