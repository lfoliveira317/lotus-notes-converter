# Lotus Notes to React Converter

A comprehensive Python tool for converting Lotus Notes applications to modern React applications.

## Features

- **Cross-platform NSF parsing** - Parse NSF files without requiring Lotus Notes installation
- **React application generation** - Generate complete React applications with Material-UI components
- **Form conversion** - Convert Notes forms to React forms with validation
- **View conversion** - Convert Notes views to React tables with sorting and filtering
- **Data migration** - Extract and convert document data to JSON format
- **Modern UI** - Generated applications use Material-UI for professional appearance
- **Responsive design** - Generated applications work on desktop and mobile devices

## Installation

### From Source

```bash
git clone https://github.com/manus-ai/lotus-notes-converter.git
cd lotus-notes-converter
pip install -e .
```

### Using pip

```bash
pip install lotus-notes-converter
```

## Quick Start

### Convert an NSF file

```bash
lotus-converter convert myapp.nsf ./output-app
```

### Analyze an NSF file

```bash
lotus-converter analyze myapp.nsf
```

### Run the generated React app

```bash
cd output-app
npm install
npm start
```

## Usage

### Command Line Interface

The converter provides a command-line interface with the following commands:

#### Convert Command

Convert a Lotus Notes NSF file to a React application:

```bash
lotus-converter convert [OPTIONS] NSF_FILE OUTPUT_DIR
```

**Options:**
- `--template-dir, -t`: Custom template directory for React generation
- `--force, -f`: Overwrite existing output directory
- `--verbose, -v`: Enable verbose logging

**Example:**
```bash
lotus-converter convert myapp.nsf ./my-react-app --verbose
```

#### Analyze Command

Analyze an NSF file and display its structure:

```bash
lotus-converter analyze NSF_FILE
```

**Example:**
```bash
lotus-converter analyze myapp.nsf
```

#### Version Command

Display version information:

```bash
lotus-converter version
```

### Python API

You can also use the converter programmatically:

```python
from pathlib import Path
from lotus_notes_converter import NotesConverter

# Initialize converter
converter = NotesConverter()

# Convert NSF file
app_model = converter.convert(
    nsf_file=Path("myapp.nsf"),
    output_dir=Path("./my-react-app")
)

print(f"Converted {app_model.name} with {len(app_model.forms)} forms")
```

## Generated React Application

The generated React application includes:

### Features

- **Material-UI components** - Professional, accessible UI components
- **React Router** - Client-side routing for navigation
- **React Hook Form** - Form handling with validation
- **TypeScript support** - Type-safe development
- **Responsive design** - Works on desktop and mobile
- **Search and filtering** - Built-in search functionality
- **CRUD operations** - Create, read, update, delete documents

### Project Structure

```
output-app/
├── public/
│   └── index.html
├── src/
│   ├── components/
│   │   ├── forms/          # Form components
│   │   ├── views/          # View components
│   │   └── Navigation.tsx  # Navigation component
│   ├── data/
│   │   └── appData.json    # Converted data
│   ├── styles/
│   │   └── index.css       # Styles
│   ├── App.tsx             # Main app component
│   └── index.tsx           # Entry point
├── package.json
└── tsconfig.json
```

### Running the Generated App

1. Install dependencies:
   ```bash
   npm install
   ```

2. Start development server:
   ```bash
   npm start
   ```

3. Build for production:
   ```bash
   npm run build
   ```

## Architecture

The converter uses a modular architecture with the following components:

### NSF Parser

- Parses NSF file format directly without external dependencies
- Handles LMBCS character encoding conversion
- Extracts forms, views, documents, and metadata
- Supports various NSF file versions

### Data Models

- Pydantic models for type-safe data representation
- Intermediate format between NSF and React
- Validation and serialization support

### React Generator

- Jinja2 templates for code generation
- Material-UI component generation
- TypeScript support
- Responsive design patterns

### CLI Interface

- Rich console output with progress indicators
- Comprehensive error handling
- Verbose logging support

## Supported NSF Elements

### Forms
- ✅ Text fields
- ✅ Number fields
- ✅ Date/time fields
- ✅ Boolean fields
- ✅ Rich text fields
- ✅ Computed fields
- ✅ Validation rules
- ✅ Field labels and help text

### Views
- ✅ Column definitions
- ✅ Sorting configuration
- ✅ Selection formulas (basic)
- ✅ Categorization
- ✅ Actions

### Documents
- ✅ Field data extraction
- ✅ Metadata preservation
- ✅ Attachment handling (basic)

### Security
- ✅ Access control lists
- ✅ Reader/author fields
- ✅ Role-based permissions

## Limitations

- **Encryption**: Encrypted NSF files require decryption keys
- **Complex formulas**: Advanced @Formula expressions may need manual conversion
- **LotusScript**: Business logic in LotusScript requires manual porting
- **Agents**: Automated agents are not directly converted
- **Rich text**: Complex rich text formatting may be simplified

## Development

### Setup Development Environment

```bash
git clone https://github.com/manus-ai/lotus-notes-converter.git
cd lotus-notes-converter
pip install -e ".[dev]"
```

### Run Tests

```bash
pytest
```

### Code Formatting

```bash
black src/
isort src/
```

### Type Checking

```bash
mypy src/
```

## Contributing

Contributions are welcome! Please read our contributing guidelines and submit pull requests to our GitHub repository.

### Areas for Contribution

- Additional NSF file format support
- Enhanced formula conversion
- Custom React component templates
- Performance optimizations
- Documentation improvements

## License

This project is licensed under the MIT License. See the LICENSE file for details.

## Support

- **Documentation**: [https://lotus-notes-converter.readthedocs.io](https://lotus-notes-converter.readthedocs.io)
- **Issues**: [https://github.com/manus-ai/lotus-notes-converter/issues](https://github.com/manus-ai/lotus-notes-converter/issues)
- **Discussions**: [https://github.com/manus-ai/lotus-notes-converter/discussions](https://github.com/manus-ai/lotus-notes-converter/discussions)

## Acknowledgments

- HCL Software for Lotus Notes/Domino documentation
- The React and Material-UI communities
- Contributors to the libnsfdb project for NSF format research

