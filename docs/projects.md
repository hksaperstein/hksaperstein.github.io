---
layout: default
title: Projects
permalink: /projects/
---

<div class="projects-hero" style="padding: 100px 0; background: var(--background-color); border-bottom: 1px solid var(--border-color);">
    <div class="container">
        <h1 style="color: var(--text-primary); font-size: var(--font-size-3xl); letter-spacing: -0.02em;">Archive</h1>
        <p style="color: var(--text-secondary); opacity: 0.7; max-width: 600px; margin: 0 auto; font-weight: 300;">An index of robotics research, engineering prototypes, and design systems developed over the years.</p>
    </div>
</div>

<div class="projects-page">
    <div class="container">
        
        <!-- Filter Buttons -->
        <div class="projects-filters" style="margin: 60px 0;">
            <button class="filter-btn active" data-filter="all">All Works</button>
            {% for category in site.project_categories %}
                <button class="filter-btn" data-filter="{{ category.slug }}">{{ category.name }}</button>
            {% endfor %}
        </div>
        
        <!-- Projects Grid -->
        <div class="projects-grid" id="projects-grid">
            {% for project in site.projects %}
            <article class="project-card" 
                     data-categories="{% for cat in project.categories %}{{ cat | slugify }} {% endfor %}">
                
                <!-- Project Image/Preview -->
                <div class="project-preview">
                    {% if project.featured_image %}
                        <img src="{{ project.featured_image | relative_url }}" 
                             alt="{{ project.title }}" 
                             class="project-image">
                    {% elsif project.models.first %}
                        <div class="model-preview">
                            <model-viewer 
                                src="{{ project.models.first.file | relative_url }}"
                                alt="{{ project.title }}"
                                camera-controls
                                auto-rotate
                                class="preview-model">
                            </model-viewer>
                        </div>
                    {% else %}
                        <div class="project-placeholder">
                            <i class="fas fa-robot"></i>
                        </div>
                    {% endif %}
                    
                    <div class="project-overlay">
                        <a href="{{ project.url | relative_url }}" class="project-link">
                            <i class="fas fa-eye"></i>
                            View Project
                        </a>
                    </div>
                </div>
                
                <!-- Project Info -->
                <div class="project-info">
                    <div class="project-categories">
                        {% for category in project.categories %}
                            <span class="category-tag">{{ category }}</span>
                        {% endfor %}
                    </div>
                    
                    <h3 class="project-title">
                        <a href="{{ project.url | relative_url }}">{{ project.title }}</a>
                    </h3>
                    
                    <p class="project-excerpt">{{ project.description | truncate: 120 }}</p>
                    
                    <div class="project-features">
                        {% if project.models %}
                            <span class="feature-badge" title="3D Models">
                                <i class="fas fa-cube"></i>
                                {{ project.models.size }}
                            </span>
                        {% endif %}
                        
                        {% if project.schematics %}
                            <span class="feature-badge" title="Schematics">
                                <i class="fas fa-microchip"></i>
                                {{ project.schematics.size }}
                            </span>
                        {% endif %}
                        
                        {% if project.code_files %}
                            <span class="feature-badge" title="Code Files">
                                <i class="fas fa-code"></i>
                                {{ project.code_files.size }}
                            </span>
                        {% endif %}
                        
                        {% if project.gallery %}
                            <span class="feature-badge" title="Media">
                                <i class="fas fa-images"></i>
                                {{ project.gallery.size }}
                            </span>
                        {% endif %}
                    </div>
                    
                    <div class="project-meta">
                        {% if project.date %}
                            <span class="project-date">
                                <i class="fas fa-calendar"></i>
                                {{ project.date | date: "%B %Y" }}
                            </span>
                        {% endif %}
                        
                        {% if project.github_url %}
                            <a href="{{ project.github_url }}" class="github-link" target="_blank">
                                <i class="fab fa-github"></i>
                            </a>
                        {% endif %}
                    </div>
                </div>
            </article>
            {% endfor %}
        </div>
        
        {% if site.projects.size == 0 %}
        <div class="no-projects">
            <div class="no-projects-content">
                <i class="fas fa-robot"></i>
                <h3>No Projects Yet</h3>
                <p>Check back soon for exciting robotics and mechatronics projects!</p>
                <a href="https://github.com/aojedao/MESGRO" class="btn-primary" target="_blank">
                    Contribute to MESGRO
                </a>
            </div>
        </div>
        {% endif %}
        
    </div>
</div>

<script>
// Project filtering functionality
document.addEventListener('DOMContentLoaded', function() {
    const filterButtons = document.querySelectorAll('.filter-btn');
    const projectCards = document.querySelectorAll('.project-card');
    
    filterButtons.forEach(button => {
        button.addEventListener('click', function() {
            const filter = this.getAttribute('data-filter');
            
            // Update active button
            filterButtons.forEach(btn => btn.classList.remove('active'));
            this.classList.add('active');
            
            // Filter projects
            projectCards.forEach(card => {
                if (filter === 'all') {
                    card.style.display = 'block';
                } else {
                    const categories = card.getAttribute('data-categories');
                    if (categories.includes(filter)) {
                        card.style.display = 'block';
                    } else {
                        card.style.display = 'none';
                    }
                }
            });
        });
    });
});
</script>