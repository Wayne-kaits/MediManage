# Contributing to MediManage

Thank you for your interest in contributing to MediManage! This document provides guidelines and instructions for contributing.

## Code of Conduct

- Be respectful and inclusive
- Welcome newcomers and encourage diverse perspectives
- Focus on constructive feedback
- Maintain professionalism in all interactions

## How to Contribute

### Reporting Bugs

1. Check if the bug has already been reported in Issues
2. If not, create a new issue with:
   - Clear, descriptive title
   - Detailed description of the bug
   - Steps to reproduce
   - Expected vs actual behavior
   - Screenshots (if applicable)
   - Environment details (OS, Python version, browser)

### Suggesting Features

1. Check if the feature has already been suggested
2. Create a new issue with:
   - Clear description of the feature
   - Use cases and benefits
   - Possible implementation approach
   - Any relevant examples or mockups

### Pull Requests

1. **Fork the repository**
2. **Create a feature branch**
   ```bash
   git checkout -b feature/your-feature-name
   ```

3. **Make your changes**
   - Write clean, readable code
   - Follow existing code style
   - Add comments for complex logic
   - Update documentation if needed

4. **Test your changes**
   - Ensure the application runs without errors
   - Test all affected functionality
   - Check for any breaking changes

5. **Commit your changes**
   ```bash
   git add .
   git commit -m "Add: Brief description of changes"
   ```

   Commit message format:
   - `Add:` for new features
   - `Fix:` for bug fixes
   - `Update:` for updates to existing features
   - `Refactor:` for code refactoring
   - `Docs:` for documentation changes

6. **Push to your fork**
   ```bash
   git push origin feature/your-feature-name
   ```

7. **Create a Pull Request**
   - Provide a clear title and description
   - Reference any related issues
   - Explain what changes were made and why
   - Include screenshots for UI changes

## Development Setup

1. Clone your fork
   ```bash
   git clone https://github.com/your-username/medimanage.git
   cd medimanage
   ```

2. Create virtual environment
   ```bash
   python -m venv venv
   source venv/bin/activate  # Linux/Mac
   venv\Scripts\activate     # Windows
   ```

3. Install dependencies
   ```bash
   pip install -r requirements.txt
   ```

4. Run the application
   ```bash
   python main.py
   ```

## Code Style Guidelines

### Python Code
- Follow PEP 8 style guide
- Use meaningful variable and function names
- Keep functions focused and concise
- Add docstrings for functions and classes
- Use type hints where appropriate

### HTML/CSS
- Use semantic HTML5 elements
- Maintain consistent indentation (2 spaces)
- Keep CSS organized and commented
- Use Bootstrap classes when possible

### JavaScript
- Use modern ES6+ syntax
- Add comments for complex logic
- Keep functions small and focused
- Handle errors appropriately

## Database Changes

If your changes affect the database:
1. Document the schema changes
2. Provide migration instructions
3. Test with both SQLite and PostgreSQL (if applicable)
4. Ensure backward compatibility when possible

## Testing

- Test all new features thoroughly
- Verify existing functionality still works
- Test on different browsers (Chrome, Firefox, Safari, Edge)
- Test responsive design on mobile devices
- Check for console errors

## Documentation

Update documentation when:
- Adding new features
- Changing existing functionality
- Modifying configuration options
- Updating dependencies

## Questions?

If you have questions:
- Check existing issues and discussions
- Create a new issue with the "question" label
- Be specific about what you need help with

## Recognition

Contributors will be recognized in:
- README.md acknowledgments
- Release notes
- Project documentation

Thank you for contributing to MediManage! 🎉