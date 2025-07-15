# Installation Guide - Lotus Notes to React Converter

## System Requirements

### Minimum Requirements
- **Operating System**: Windows 10/11, macOS 10.15+, or Linux (Ubuntu 20.04+)
- **Python**: Version 3.11 or higher
- **Node.js**: Version 18 or higher
- **Memory**: 4GB RAM minimum, 8GB recommended
- **Storage**: 2GB free space for installation and generated applications

### Recommended Development Environment
- **IDE**: Visual Studio Code with Python and React extensions
- **Terminal**: PowerShell (Windows), Terminal (macOS), or Bash (Linux)
- **Package Managers**: pip (Python), npm or yarn (Node.js)

## Installation Steps

### Step 1: Install Python Dependencies

#### Option A: Install from Source (Recommended for Development)
```bash
# Clone or extract the project
cd lotus-notes-converter

# Create a virtual environment (recommended)
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate

# Install the package in development mode
pip install -e .
```

#### Option B: Install Dependencies Manually
```bash
# Install required Python packages
pip install click jinja2 pydantic rich typing-extensions
```

### Step 2: Verify Installation

```bash
# Check if the converter is installed correctly
python -m lotus_notes_converter.cli --version

# Or if installed globally:
lotus-notes-converter --version
```

Expected output:
```
Lotus Notes to React Converter v1.0.0
```

### Step 3: Install Node.js Dependencies (for Generated Apps)

The converter generates React applications that require Node.js. Ensure Node.js is installed:

```bash
# Check Node.js version
node --version  # Should be 18.0.0 or higher
npm --version   # Should be 8.0.0 or higher
```

If Node.js is not installed, download it from [nodejs.org](https://nodejs.org/).

## Quick Start

### 1. Create a Sample NSF File
```bash
# Navigate to the examples directory
cd examples

# Create a sample NSF file for testing
python create_sample_nsf.py
```

### 2. Convert NSF to React App
```bash
# Convert the sample NSF file
python -m lotus_notes_converter.cli convert examples/sample.nsf ./my-react-app

# Or with verbose output:
python -m lotus_notes_converter.cli -v convert examples/sample.nsf ./my-react-app
```

### 3. Run the Generated React Application
```bash
# Navigate to the generated app
cd my-react-app

# Install React dependencies
npm install

# Start the development server
npm start
```

The React application will open in your browser at `http://localhost:3000`.

## Command Reference

### Basic Commands

#### Convert NSF to React App
```bash
lotus-notes-converter convert <nsf-file> <output-directory>
```

#### Analyze NSF File Structure
```bash
lotus-notes-converter analyze <nsf-file>
```

#### Get Help
```bash
lotus-notes-converter --help
lotus-notes-converter convert --help
```

### Command Options

#### Global Options
- `-v, --verbose`: Enable verbose logging
- `--help`: Show help message

#### Convert Command Options
- `--force`: Overwrite existing output directory
- `--template`: Specify template (default: "default")

### Example Commands

```bash
# Basic conversion
lotus-notes-converter convert sample.nsf ./output

# Verbose conversion with force overwrite
lotus-notes-converter -v convert sample.nsf ./output --force

# Analyze NSF file structure
lotus-notes-converter analyze sample.nsf
```

## Troubleshooting

### Common Issues and Solutions

#### Issue: "Module not found" error
**Solution**: Ensure you're using the correct Python path:
```bash
# Use full module path
python -m lotus_notes_converter.cli convert sample.nsf ./output

# Or ensure the package is installed
pip install -e .
```

#### Issue: NSF file not found
**Solution**: Check file path and permissions:
```bash
# Use absolute path
lotus-notes-converter convert /full/path/to/sample.nsf ./output

# Check file exists
ls -la sample.nsf
```

#### Issue: React app won't start
**Solution**: Ensure Node.js dependencies are installed:
```bash
cd output-directory
npm install
npm start
```

#### Issue: Port 3000 already in use
**Solution**: React will prompt to use another port, or specify manually:
```bash
PORT=3001 npm start
```

### Debug Mode

Enable debug logging for troubleshooting:
```bash
# Set environment variable for debug logging
export PYTHONPATH=src
python -m lotus_notes_converter.cli -v convert sample.nsf ./output
```

### Log Files

The converter creates log files in the output directory:
- `conversion.log` - Detailed conversion process log
- `errors.log` - Error messages and stack traces

## Development Setup

### For Contributors

#### 1. Clone Repository
```bash
git clone <repository-url>
cd lotus-notes-converter
```

#### 2. Setup Development Environment
```bash
# Create virtual environment
python -m venv venv
source venv/bin/activate  # or venv\Scripts\activate on Windows

# Install development dependencies
pip install -e ".[dev]"
```

#### 3. Run Tests
```bash
# Run unit tests
python -m pytest tests/

# Run with coverage
python -m pytest tests/ --cov=lotus_notes_converter
```

#### 4. Code Quality
```bash
# Format code
black src/

# Lint code
flake8 src/

# Type checking
mypy src/
```

## Production Deployment

### Building Distribution Package
```bash
# Build wheel package
python -m build

# Install from wheel
pip install dist/lotus_notes_converter-1.0.0-py3-none-any.whl
```

### Docker Deployment
```bash
# Build Docker image
docker build -t lotus-notes-converter .

# Run converter in container
docker run -v $(pwd):/workspace lotus-notes-converter convert /workspace/sample.nsf /workspace/output
```

## Support

### Getting Help
1. Check this installation guide
2. Review the README.md file
3. Check the examples directory for sample usage
4. Review the troubleshooting section above

### Reporting Issues
When reporting issues, please include:
- Operating system and version
- Python version (`python --version`)
- Node.js version (`node --version`)
- Complete error message
- Steps to reproduce the issue

### Performance Tips
1. Use SSD storage for better I/O performance
2. Ensure adequate RAM (8GB+ recommended)
3. Close unnecessary applications during conversion
4. Use virtual environments to avoid dependency conflicts

## Next Steps

After successful installation:
1. Try converting a sample NSF file
2. Explore the generated React application
3. Review the project documentation
4. Experiment with your own NSF files
5. Customize the generated applications as needed

For advanced usage and customization options, refer to the main README.md and architecture documentation.

