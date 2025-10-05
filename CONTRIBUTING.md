# Contributing to Performia

Thank you for your interest in contributing to Performia! This document provides guidelines and best practices for contributing to the project.

---

## Table of Contents

- [Code of Conduct](#code-of-conduct)
- [Getting Started](#getting-started)
- [Development Workflow](#development-workflow)
- [Code Style Guide](#code-style-guide)
- [Testing Requirements](#testing-requirements)
- [Pull Request Process](#pull-request-process)
- [Commit Message Guidelines](#commit-message-guidelines)
- [Documentation](#documentation)
- [Issue Guidelines](#issue-guidelines)
- [Community](#community)

---

## Code of Conduct

### Our Pledge

We are committed to providing a welcoming and inclusive environment for all contributors. We expect:

- **Respect**: Treat everyone with respect and kindness
- **Openness**: Welcome newcomers and different perspectives
- **Collaboration**: Work together constructively
- **Professionalism**: Focus on the code and ideas, not individuals

### Unacceptable Behavior

- Harassment, discrimination, or offensive comments
- Personal attacks or insults
- Trolling or inflammatory comments
- Publishing others' private information

### Enforcement

Violations can be reported to the project maintainers. All complaints will be reviewed and investigated promptly and fairly.

---

## Getting Started

### Prerequisites

Before contributing, ensure you have:

1. **Required Software**:
   - Python 3.11+
   - Node.js 18+
   - Git

2. **Development Environment**:
   - Code editor (VS Code, PyCharm, etc.)
   - Terminal/command line access

3. **Accounts**:
   - GitHub account
   - OpenAI API key (for testing)
   - Anthropic API key (for testing)

### Initial Setup

1. **Fork the Repository**:
   ```bash
   # Click "Fork" on GitHub
   # Clone your fork
   git clone https://github.com/YOUR_USERNAME/Performia.git
   cd Performia
   ```

2. **Add Upstream Remote**:
   ```bash
   git remote add upstream https://github.com/PerformanceSuite/Performia.git
   git fetch upstream
   ```

3. **Install Dependencies**:
   ```bash
   # Backend
   python -m venv venv
   source venv/bin/activate  # Windows: venv\Scripts\activate
   pip install -r requirements.txt

   # Frontend
   cd frontend
   npm install
   cd ..
   ```

4. **Configure Environment**:
   ```bash
   cp .env.template .env
   # Edit .env with your API keys
   ```

5. **Verify Setup**:
   ```bash
   # Run tests
   pytest backend/tests/
   cd frontend && npm test

   # Start development servers
   python backend/src/services/api/main.py  # Terminal 1
   cd frontend && npm run dev                # Terminal 2
   ```

---

## Development Workflow

### 1. Create Feature Branch

```bash
# Update your fork
git checkout main
git pull upstream main

# Create feature branch
git checkout -b feature/your-feature-name

# Or for bug fixes
git checkout -b fix/issue-description
```

**Branch Naming Conventions**:
- `feature/` - New features
- `fix/` - Bug fixes
- `docs/` - Documentation updates
- `refactor/` - Code refactoring
- `test/` - Test additions/improvements
- `chore/` - Maintenance tasks

### 2. Make Changes

- Write clear, concise code
- Follow code style guidelines
- Add tests for new functionality
- Update documentation as needed
- Keep commits focused and atomic

### 3. Test Thoroughly

```bash
# Backend tests
pytest backend/tests/

# Frontend tests
cd frontend && npm test

# Run specific test
pytest backend/tests/test_pipeline.py::test_asr_service

# Coverage report
pytest --cov=backend/src
```

### 4. Commit Changes

```bash
# Stage changes
git add .

# Commit with conventional commit message
git commit -m "feat: add real-time syllable highlighting"
```

### 5. Push and Create PR

```bash
# Push to your fork
git push origin feature/your-feature-name

# Create Pull Request on GitHub
# Compare: upstream/main <- your-fork/feature/your-feature-name
```

---

## Code Style Guide

### Python Style (PEP 8)

**Key Guidelines**:
- 4 spaces for indentation (no tabs)
- Max line length: 88 characters (Black formatter)
- Use type hints for function signatures
- Docstrings for all public functions/classes

**Example**:
```python
from typing import Optional, List, Dict


def analyze_audio(
    audio_path: str,
    model_size: str = "base",
    language: Optional[str] = None
) -> Dict[str, any]:
    """
    Analyze audio file and extract features.

    Args:
        audio_path: Path to audio file
        model_size: Whisper model size (tiny, base, small, medium, large)
        language: Optional language code (default: auto-detect)

    Returns:
        Dictionary containing analysis results with keys:
        - transcription: Full text transcription
        - segments: List of timed segments
        - language: Detected or specified language

    Raises:
        FileNotFoundError: If audio file doesn't exist
        ValueError: If model_size is invalid
    """
    if not os.path.exists(audio_path):
        raise FileNotFoundError(f"Audio file not found: {audio_path}")

    # Implementation...
    return results
```

**Tools**:
```bash
# Format with Black
pip install black
black backend/src/

# Lint with flake8
pip install flake8
flake8 backend/src/

# Type checking with mypy
pip install mypy
mypy backend/src/
```

### TypeScript/React Style

**Key Guidelines**:
- 2 spaces for indentation
- Use `const` and `let`, never `var`
- Prefer functional components with hooks
- Use TypeScript strict mode
- Props interfaces for all components

**Example**:
```typescript
import React, { useState, useEffect } from 'react';

interface SongCardProps {
  songId: string;
  title: string;
  artist: string;
  onPlay: (songId: string) => void;
}

export const SongCard: React.FC<SongCardProps> = ({
  songId,
  title,
  artist,
  onPlay
}) => {
  const [isHovered, setIsHovered] = useState(false);

  const handleClick = () => {
    onPlay(songId);
  };

  return (
    <div
      className="song-card"
      onMouseEnter={() => setIsHovered(true)}
      onMouseLeave={() => setIsHovered(false)}
      onClick={handleClick}
    >
      <h3>{title}</h3>
      <p>{artist}</p>
    </div>
  );
};
```

**Tools**:
```bash
# Lint with ESLint
npm run lint

# Format with Prettier
npm run format

# Type check
npm run type-check
```

### File Organization

**Backend**:
```
backend/src/services/
├── service_name/
│   ├── __init__.py          # Export public API
│   ├── service.py           # Main service class
│   ├── models.py            # Data models
│   ├── utils.py             # Helper functions
│   └── tests/
│       ├── test_service.py
│       └── test_utils.py
```

**Frontend**:
```
frontend/src/components/
├── ComponentName/
│   ├── ComponentName.tsx     # Component implementation
│   ├── ComponentName.test.tsx # Tests
│   ├── ComponentName.css     # Styles (if not using Tailwind)
│   ├── types.ts              # TypeScript interfaces
│   └── index.ts              # Export
```

---

## Testing Requirements

### Backend Testing

**Requirements**:
- All new functions must have unit tests
- Aim for >80% code coverage
- Use pytest fixtures for common setup
- Mock external API calls

**Example**:
```python
import pytest
from unittest.mock import Mock, patch
from services.asr.service import ASRService


@pytest.fixture
def asr_service():
    """Fixture providing ASRService instance."""
    return ASRService(model_size="tiny")


@pytest.fixture
def sample_audio(tmp_path):
    """Fixture providing sample audio file."""
    audio_file = tmp_path / "test.wav"
    # Create test audio file
    return str(audio_file)


def test_transcribe_success(asr_service, sample_audio):
    """Test successful transcription."""
    result = asr_service.transcribe(sample_audio)

    assert "text" in result
    assert "segments" in result
    assert len(result["segments"]) > 0


@patch('whisper.load_model')
def test_transcribe_with_mock(mock_load_model, asr_service, sample_audio):
    """Test transcription with mocked Whisper model."""
    mock_model = Mock()
    mock_model.transcribe.return_value = {
        "text": "test transcription",
        "segments": []
    }
    mock_load_model.return_value = mock_model

    result = asr_service.transcribe(sample_audio)

    assert result["text"] == "test transcription"
    mock_model.transcribe.assert_called_once()
```

### Frontend Testing

**Requirements**:
- Test user interactions
- Test component rendering
- Test state changes
- Use React Testing Library

**Example**:
```typescript
import { render, screen, fireEvent } from '@testing-library/react';
import { SongCard } from './SongCard';

describe('SongCard', () => {
  const mockOnPlay = jest.fn();

  const defaultProps = {
    songId: '123',
    title: 'Yesterday',
    artist: 'The Beatles',
    onPlay: mockOnPlay
  };

  beforeEach(() => {
    mockOnPlay.mockClear();
  });

  it('renders song title and artist', () => {
    render(<SongCard {...defaultProps} />);

    expect(screen.getByText('Yesterday')).toBeInTheDocument();
    expect(screen.getByText('The Beatles')).toBeInTheDocument();
  });

  it('calls onPlay when clicked', () => {
    render(<SongCard {...defaultProps} />);

    fireEvent.click(screen.getByText('Yesterday'));

    expect(mockOnPlay).toHaveBeenCalledWith('123');
  });
});
```

### Integration Testing

Test complete workflows:

```python
def test_full_pipeline_integration(tmp_path):
    """Test complete audio analysis pipeline."""
    # Upload audio
    response = client.post('/api/analyze', files={'file': audio_file})
    job_id = response.json()['job_id']

    # Poll for completion
    while True:
        status = client.get(f'/api/status/{job_id}')
        if status.json()['status'] == 'COMPLETE':
            break
        time.sleep(1)

    # Get Song Map
    song_map = client.get(f'/api/songmap/{job_id}')

    assert song_map.status_code == 200
    assert 'title' in song_map.json()
    assert 'sections' in song_map.json()
```

---

## Pull Request Process

### Before Submitting

**Checklist**:
- [ ] Code follows style guidelines
- [ ] All tests pass
- [ ] New tests added for new features
- [ ] Documentation updated
- [ ] No merge conflicts with main
- [ ] Commit messages follow convention
- [ ] No sensitive data (API keys, passwords)

### PR Title Format

Use conventional commit format:

```
<type>(<scope>): <description>

Examples:
feat(frontend): add dark mode toggle
fix(backend): resolve ASR timeout issue
docs(readme): update installation instructions
refactor(audio): simplify chord detection logic
```

### PR Description Template

```markdown
## Description
Brief description of changes and motivation.

## Type of Change
- [ ] Bug fix
- [ ] New feature
- [ ] Breaking change
- [ ] Documentation update

## Testing
Describe testing performed:
- Unit tests added/updated
- Manual testing steps
- Edge cases considered

## Screenshots (if applicable)
Add screenshots for UI changes.

## Checklist
- [ ] Code follows style guidelines
- [ ] Tests pass
- [ ] Documentation updated
- [ ] No merge conflicts

## Related Issues
Fixes #123
Relates to #456
```

### Review Process

1. **Automated Checks**: CI runs tests and linters
2. **Code Review**: Maintainer reviews code
3. **Feedback**: Address review comments
4. **Approval**: Once approved, PR can be merged
5. **Merge**: Squash and merge to main branch

---

## Commit Message Guidelines

Follow **Conventional Commits** specification:

### Format

```
<type>(<scope>): <subject>

<body>

<footer>
```

### Types

- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation only
- `style`: Code style (formatting, missing semicolons, etc.)
- `refactor`: Code refactoring
- `perf`: Performance improvement
- `test`: Adding/updating tests
- `chore`: Maintenance tasks
- `ci`: CI/CD changes

### Examples

```bash
# Simple feature
git commit -m "feat: add voice control support"

# Bug fix with scope
git commit -m "fix(audio): resolve Whisper memory leak"

# With body and footer
git commit -m "feat(frontend): add collaborative editing

Implemented real-time collaborative editing using WebSocket.
Users can now edit the same song simultaneously.

Closes #234"

# Breaking change
git commit -m "feat(api)!: change Song Map JSON structure

BREAKING CHANGE: Song Map schema version 2.0
Sections now use 'id' instead of 'name' as primary key."
```

---

## Documentation

### When to Update Documentation

Update docs when you:
- Add new features
- Change APIs or interfaces
- Fix significant bugs
- Change configuration options
- Add new dependencies

### Documentation Files

- **README.md**: Project overview, quick start
- **INSTALLATION.md**: Setup instructions
- **USAGE.md**: User guide
- **ARCHITECTURE.md**: Technical architecture
- **API.md**: API reference
- **CONTRIBUTING.md**: This file

### Code Documentation

**Python Docstrings** (Google style):
```python
def process_audio(audio_path: str, options: Dict) -> Result:
    """
    Process audio file with specified options.

    Args:
        audio_path: Path to audio file
        options: Processing options dict with keys:
            - normalize: Whether to normalize audio (bool)
            - sample_rate: Target sample rate (int)

    Returns:
        Result object containing:
            - success: Whether processing succeeded
            - data: Processed audio data
            - metadata: Audio metadata dict

    Raises:
        FileNotFoundError: If audio file not found
        ProcessingError: If processing fails

    Example:
        >>> result = process_audio('song.wav', {'normalize': True})
        >>> print(result.success)
        True
    """
```

**TypeScript JSDoc**:
```typescript
/**
 * Calculate syllable timing from word timestamps.
 *
 * @param words - Array of words with timestamps
 * @param options - Timing calculation options
 * @returns Array of syllables with precise timing
 *
 * @example
 * ```typescript
 * const syllables = calculateTiming(words, { minDuration: 0.1 });
 * console.log(syllables[0].startTime); // 0.5
 * ```
 */
function calculateTiming(
  words: Word[],
  options: TimingOptions
): Syllable[] {
  // Implementation...
}
```

---

## Issue Guidelines

### Reporting Bugs

Use the bug report template:

```markdown
**Describe the bug**
Clear and concise description of what the bug is.

**To Reproduce**
Steps to reproduce:
1. Go to '...'
2. Click on '...'
3. See error

**Expected behavior**
What you expected to happen.

**Screenshots**
If applicable, add screenshots.

**Environment**
- OS: [e.g., macOS 13.0]
- Python version: [e.g., 3.11.4]
- Node version: [e.g., 18.16.0]
- Browser: [e.g., Chrome 115]

**Additional context**
Any other context about the problem.
```

### Requesting Features

Use the feature request template:

```markdown
**Is your feature request related to a problem?**
Clear description of the problem.

**Describe the solution you'd like**
What you want to happen.

**Describe alternatives you've considered**
Other solutions you've thought about.

**Additional context**
Any other context, screenshots, or examples.
```

### Issue Labels

- `bug`: Something isn't working
- `feature`: New feature request
- `documentation`: Documentation improvements
- `good first issue`: Good for newcomers
- `help wanted`: Extra attention needed
- `priority: high`: High priority
- `priority: low`: Low priority

---

## Community

### Getting Help

- **GitHub Discussions**: Ask questions, share ideas
- **GitHub Issues**: Report bugs, request features
- **Documentation**: Check docs first

### Communication Channels

- **GitHub**: Primary communication platform
- **Pull Requests**: Code review and discussion
- **Issues**: Bug reports and feature requests
- **Discussions**: General questions and ideas

### Recognition

Contributors are recognized in:
- CHANGELOG.md for each release
- Contributors section in README
- GitHub contributors graph

---

## Additional Resources

### Development Tools

- **VS Code Extensions**:
  - Python
  - ESLint
  - Prettier
  - GitLens

- **Browser DevTools**:
  - React Developer Tools
  - Redux DevTools (if using Redux)

### Learning Resources

- [React Documentation](https://react.dev/)
- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [TypeScript Handbook](https://www.typescriptlang.org/docs/)
- [Python Type Hints](https://docs.python.org/3/library/typing.html)

---

## Questions?

If you have questions about contributing:

1. Check existing documentation
2. Search GitHub Issues and Discussions
3. Ask in GitHub Discussions
4. Open a new issue with question label

Thank you for contributing to Performia!

---

*Last updated: October 2025*
