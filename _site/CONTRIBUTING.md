# Contributing to MESGRO

Thank you for your interest in contributing to MESGRO! This document provides guidelines and instructions for contributing to this robotics and mechatronics portfolio template.

## 🤝 Ways to Contribute

### 🐛 Bug Reports
- Use the GitHub issue tracker
- Include detailed reproduction steps
- Provide browser/system information
- Include screenshots if relevant

### ✨ Feature Requests
- Check existing issues first
- Clearly describe the feature
- Explain the use case and benefits
- Consider implementation complexity

### 💻 Code Contributions
- Fork the repository
- Create a feature branch
- Follow coding standards
- Add tests if applicable
- Update documentation

### 📚 Documentation
- Fix typos and grammar
- Improve clarity and examples
- Add missing documentation
- Update outdated information

## 🚀 Getting Started

### Development Setup
1. **Fork and Clone**
   ```bash
   git clone https://github.com/yourusername/MESGRO.git
   cd MESGRO
   ```

2. **Install Dependencies**
   ```bash
   bundle install
   ```

3. **Start Development Server**
   ```bash
   bundle exec jekyll serve --livereload
   ```

4. **Create Feature Branch**
   ```bash
   git checkout -b feature/your-feature-name
   ```

### Project Structure
```
MESGRO/
├── _config.yml          # Site configuration
├── _layouts/            # Page templates
├── _includes/           # Reusable components
├── _sass/              # Stylesheet source
├── _projects/          # Project markdown files
├── assets/             # Static assets
└── README.md           # Project documentation
```

## 📝 Coding Standards

### HTML/Liquid
- Use semantic HTML5 elements
- Follow accessibility best practices
- Use consistent indentation (2 spaces)
- Include alt text for images
- Test with screen readers

### CSS/SCSS
- Use BEM methodology for class naming
- Follow the existing SCSS structure
- Use CSS custom properties for theming
- Ensure responsive design
- Test on multiple browsers

### JavaScript
- Use modern ES6+ syntax
- Follow ESLint configuration
- Add JSDoc comments for functions
- Handle errors gracefully
- Test across browsers

### Markdown
- Use consistent heading hierarchy
- Include alt text for images
- Follow project front matter structure
- Use code blocks with language specification

## 🧪 Testing

### Manual Testing
- Test on desktop and mobile
- Verify in multiple browsers
- Check dark/light theme switching
- Test 3D model loading
- Validate responsive design

### Automated Testing
- Jekyll build must pass
- CSS validation
- HTML validation
- Link checking
- Performance testing

## 📋 Pull Request Process

### Before Submitting
1. Test your changes thoroughly
2. Update documentation if needed
3. Follow commit message conventions
4. Rebase on latest main branch
5. Ensure CI passes

### Commit Messages
Use conventional commit format:
```
type(scope): description

feat(viewer): add support for GLB models
fix(css): resolve mobile navigation issue
docs(readme): update installation instructions
```

### Pull Request Template
- Clear title and description
- Link to related issues
- List changes made
- Include screenshots for UI changes
- Add testing instructions

## 🎨 Design Guidelines

### Visual Design
- Follow existing color scheme
- Maintain consistent spacing
- Use system fonts when possible
- Ensure sufficient color contrast
- Support both light and dark themes

### User Experience
- Prioritize mobile-first design
- Keep loading times minimal
- Provide clear navigation
- Include helpful error messages
- Make content scannable

### Accessibility
- Use semantic HTML
- Include ARIA labels
- Test with keyboard navigation
- Ensure screen reader compatibility
- Maintain color contrast ratios

## 🏷️ Issue Labels

### Type Labels
- `bug`: Something isn't working
- `enhancement`: New feature or request
- `documentation`: Improvements to docs
- `question`: Further information needed

### Priority Labels
- `priority: high`: Critical issues
- `priority: medium`: Normal priority
- `priority: low`: Nice to have

### Status Labels
- `good first issue`: Good for newcomers
- `help wanted`: Extra attention needed
- `wontfix`: Won't be worked on

## 🚀 Release Process

### Version Management
- Follow semantic versioning (SemVer)
- Update version in `_config.yml`
- Create release notes
- Tag releases in Git

### Release Types
- **Major**: Breaking changes
- **Minor**: New features, backward compatible
- **Patch**: Bug fixes, backward compatible

## 📞 Getting Help

### Communication Channels
- **GitHub Issues**: Bug reports and feature requests
- **GitHub Discussions**: General questions and ideas
- **Email**: For private matters

### Response Times
- Issues: Within 48 hours
- Pull requests: Within 1 week
- Questions: Within 24 hours

## 📋 Code of Conduct

### Our Standards
- Be respectful and inclusive
- Welcome newcomers
- Provide constructive feedback
- Focus on what's best for the community
- Show empathy towards others

### Unacceptable Behavior
- Harassment or discrimination
- Trolling or insulting comments
- Personal or political attacks
- Publishing private information
- Other unprofessional conduct

### Enforcement
- Report issues to project maintainers
- Violations may result in temporary or permanent bans
- Decisions will be made fairly and transparently

## 🏆 Recognition

### Contributors
- All contributors listed in README
- Regular contributors may become maintainers
- Special recognition for significant contributions

### Types of Recognition
- Mention in release notes
- Contributor badge
- Social media shoutouts
- Speaking opportunities

## 📚 Resources

### Jekyll Development
- [Jekyll Documentation](https://jekyllrb.com/docs/)
- [Liquid Template Language](https://shopify.github.io/liquid/)
- [GitHub Pages](https://pages.github.com/)

### Web Development
- [MDN Web Docs](https://developer.mozilla.org/)
- [Can I Use](https://caniuse.com/)
- [Accessibility Guidelines](https://www.w3.org/WAI/WCAG21/quickref/)

### Robotics Resources
- [Robot Operating System](https://www.ros.org/)
- [IEEE Robotics](https://www.ieee-ras.org/)
- [Robotics Stack Exchange](https://robotics.stackexchange.com/)

Thank you for contributing to MESGRO! 🤖✨