# Contributing to Context Engineering MCP Platform

First off, thank you for considering contributing to Context Engineering MCP Platform! 🎉

## 🤝 Code of Conduct

This project and everyone participating in it is governed by our Code of Conduct. By participating, you are expected to uphold this code.

## 🚀 How Can I Contribute?

### Reporting Bugs 🐛

Before creating bug reports, please check existing issues as you might find out that you don't need to create one. When you are creating a bug report, please include as many details as possible:

- **Use a clear and descriptive title**
- **Describe the exact steps to reproduce the problem**
- **Provide specific examples to demonstrate the steps**
- **Describe the behavior you observed after following the steps**
- **Explain which behavior you expected to see instead and why**
- **Include screenshots and animated GIFs if possible**

### Suggesting Enhancements 💡

Enhancement suggestions are tracked as GitHub issues. When creating an enhancement suggestion, please include:

- **Use a clear and descriptive title**
- **Provide a step-by-step description of the suggested enhancement**
- **Provide specific examples to demonstrate the steps**
- **Describe the current behavior and explain which behavior you expected**
- **Explain why this enhancement would be useful**

### Pull Requests 🔀

1. Fork the repo and create your branch from `main`
2. If you've added code that should be tested, add tests
3. If you've changed APIs, update the documentation
4. Ensure the test suite passes
5. Make sure your code lints
6. Issue that pull request!

## 📋 Development Process

### Setting Up Your Environment

```bash
# Clone your fork
git clone https://github.com/your-username/context_-engineering_MCP.git
cd context_engineering_mcp_server

# Create a virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
pip install -r requirements-dev.txt  # Development dependencies
```

### Running Tests

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=.

# Run specific test file
pytest tests/test_context_analyzer.py
```

### Code Style

We use:
- **Black** for Python code formatting
- **ESLint** for JavaScript
- **Type hints** for Python code

```bash
# Format Python code
black .

# Lint JavaScript
cd mcp-server && npm run lint
```

### Commit Messages

We follow the [Conventional Commits](https://www.conventionalcommits.org/) specification:

- `feat:` A new feature
- `fix:` A bug fix
- `docs:` Documentation only changes
- `style:` Changes that do not affect the meaning of the code
- `refactor:` A code change that neither fixes a bug nor adds a feature
- `perf:` A code change that improves performance
- `test:` Adding missing tests or correcting existing tests
- `chore:` Changes to the build process or auxiliary tools

Examples:
```
feat: add multi-modal context support
fix: resolve token counting issue in optimizer
docs: update MCP usage examples
```

## 🏗️ Project Structure

```
context_engineering_mcp_server/
├── main.py                 # AI Guides API server
├── context_engineering/    # Core context engineering system
│   ├── context_models.py   # Data models
│   ├── context_analyzer.py # Analysis engine
│   ├── context_optimizer.py # Optimization engine
│   └── template_manager.py # Template management
├── mcp-server/            # MCP server implementation
├── examples/              # Usage examples
└── tests/                 # Test suite
```

## 🧪 Testing Guidelines

- Write tests for all new features
- Maintain test coverage above 80%
- Use meaningful test names
- Include both unit and integration tests

Example test:
```python
def test_context_optimization_reduces_tokens():
    """Test that optimization actually reduces token count"""
    window = create_test_window()
    original_tokens = window.current_tokens
    
    optimizer = ContextOptimizer(api_key)
    result = await optimizer.optimize_context_window(
        window, 
        goals=["reduce_tokens"]
    )
    
    assert window.current_tokens < original_tokens
    assert result.status == "completed"
```

## 📚 Documentation

- Update README.md if you change functionality
- Add docstrings to all functions and classes
- Include type hints
- Update API documentation for endpoint changes

## 🚀 Release Process

1. Update version numbers
2. Update CHANGELOG.md
3. Create a pull request
4. After merge, tag the release
5. Deploy to production

## 💬 Communication

- Use [GitHub Issues](https://github.com/ShunsukeHayashi/context_-engineering_MCP/issues) for bugs and features
- Use [GitHub Discussions](https://github.com/ShunsukeHayashi/context_-engineering_MCP/discussions) for questions
- Be respectful and constructive

## 🎯 Areas Where We Need Help

- **Documentation**: Improving examples and guides
- **Testing**: Adding more test coverage
- **Features**: Multi-language support, cloud deployment
- **Performance**: Optimization algorithms, caching strategies
- **UI/UX**: Dashboard improvements

## 📜 License

By contributing, you agree that your contributions will be licensed under the MIT License.

---

Thank you for contributing! 🙏 Every contribution, no matter how small, makes a difference!