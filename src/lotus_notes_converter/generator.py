"""
React Generator Module

This module generates React applications from parsed Lotus Notes data.
"""

import json
import logging
from pathlib import Path
from typing import Dict, List, Any, Optional
from jinja2 import Environment, FileSystemLoader, Template

from .models import (
    ApplicationModel, FormModel, ViewModel, FieldModel, FieldType,
    ColumnModel, DocumentModel
)
from .exceptions import ReactGenerationError, TemplateError


logger = logging.getLogger(__name__)


class ReactGenerator:
    """Generates React applications from Lotus Notes data."""
    
    def __init__(self, template_dir: Optional[Path] = None):
        """Initialize the React generator."""
        self.template_dir = template_dir or Path(__file__).parent / "templates"
        self.jinja_env = self._setup_jinja_environment()
    
    def _setup_jinja_environment(self) -> Environment:
        """Setup Jinja2 environment with custom filters."""
        env = Environment(
            loader=FileSystemLoader(str(self.template_dir)),
            trim_blocks=True,
            lstrip_blocks=True
        )
        
        # Add custom filters
        env.filters['camel_case'] = self._camel_case
        env.filters['pascal_case'] = self._pascal_case
        env.filters['kebab_case'] = self._kebab_case
        env.filters['field_type_to_input'] = self._field_type_to_input_type
        env.filters['field_type_to_validation'] = self._field_type_to_validation
        
        return env
    
    def generate_react_app(self, app: ApplicationModel, output_dir: Path) -> None:
        """Generate a complete React application."""
        logger.info(f"Generating React app for {app.name}")
        
        try:
            # Create output directory structure
            self._create_directory_structure(output_dir)
            
            # Generate package.json
            self._generate_package_json(app, output_dir)
            
            # Generate main App component
            self._generate_app_component(app, output_dir)
            
            # Generate form components
            for form in app.forms:
                self._generate_form_component(form, output_dir)
            
            # Generate view components
            for view in app.views:
                self._generate_view_component(view, output_dir)
            
            # Generate data files
            self._generate_data_files(app, output_dir)
            
            # Generate routing
            self._generate_routing(app, output_dir)
            
            # Generate styles
            self._generate_styles(output_dir)
            
            # Generate configuration files
            self._generate_config_files(output_dir)
            
            logger.info(f"React app generated successfully in {output_dir}")
            
        except Exception as e:
            raise ReactGenerationError(f"Failed to generate React app: {e}")
    
    def _create_directory_structure(self, output_dir: Path) -> None:
        """Create the React app directory structure."""
        directories = [
            "src",
            "src/components",
            "src/components/forms",
            "src/components/views",
            "src/data",
            "src/styles",
            "src/utils",
            "public"
        ]
        
        for dir_path in directories:
            (output_dir / dir_path).mkdir(parents=True, exist_ok=True)
    
    def _generate_package_json(self, app: ApplicationModel, output_dir: Path) -> None:
        """Generate package.json file."""
        package_data = {
            "name": self._kebab_case(app.name),
            "version": "1.0.0",
            "description": app.description or f"React app converted from {app.name}",
            "private": True,
            "dependencies": {
                "react": "^18.2.0",
                "react-dom": "^18.2.0",
                "react-router-dom": "^6.8.0",
                "react-hook-form": "^7.43.0",
                "@mui/material": "^5.11.0",
                "@mui/icons-material": "^5.11.0",
                "@emotion/react": "^11.10.0",
                "@emotion/styled": "^11.10.0",
                "axios": "^1.3.0",
                "date-fns": "^2.29.0"
            },
            "devDependencies": {
                "@types/react": "^18.0.0",
                "@types/react-dom": "^18.0.0",
                "react-scripts": "5.0.1",
                "typescript": "^4.9.0"
            },
            "scripts": {
                "start": "react-scripts start",
                "build": "react-scripts build",
                "test": "react-scripts test",
                "eject": "react-scripts eject"
            },
            "eslintConfig": {
                "extends": ["react-app", "react-app/jest"]
            },
            "browserslist": {
                "production": [">0.2%", "not dead", "not op_mini all"],
                "development": ["last 1 chrome version", "last 1 firefox version", "last 1 safari version"]
            }
        }
        
        with open(output_dir / "package.json", "w") as f:
            json.dump(package_data, f, indent=2)
    
    def _generate_app_component(self, app: ApplicationModel, output_dir: Path) -> None:
        """Generate the main App component."""
        # Generate imports for views and forms
        view_imports = []
        form_imports = []
        
        for view in app.views:
            view_name = self._pascal_case(view.name)
            view_imports.append(f"import {view_name}View from './components/views/{view_name}View';")
        
        for form in app.forms:
            form_name = self._pascal_case(form.name)
            form_imports.append(f"import {form_name}Form from './components/forms/{form_name}Form';")
        
        # Generate routes for views and forms
        view_routes = []
        form_routes = []
        
        for view in app.views:
            view_name = self._pascal_case(view.name)
            view_kebab = self._kebab_case(view.name)
            view_routes.append(f'            <Route path="/{view_kebab}" element={{<{view_name}View />}} />')
        
        for form in app.forms:
            form_name = self._pascal_case(form.name)
            form_kebab = self._kebab_case(form.name)
            form_routes.append(f'            <Route path="/{form_kebab}" element={{<{form_name}Form />}} />')
            form_routes.append(f'            <Route path="/{form_kebab}/:id" element={{<{form_name}Form />}} />')
        
        default_view = self._pascal_case(app.views[0].name) if app.views else "AllDocuments"
        
        content = f'''import React from 'react';
import {{ BrowserRouter as Router, Routes, Route }} from 'react-router-dom';
import {{ ThemeProvider, createTheme }} from '@mui/material/styles';
import CssBaseline from '@mui/material/CssBaseline';
import AppBar from '@mui/material/AppBar';
import Toolbar from '@mui/material/Toolbar';
import Typography from '@mui/material/Typography';
import Container from '@mui/material/Container';
import Navigation from './components/Navigation';
{chr(10).join(view_imports)}
{chr(10).join(form_imports)}

const theme = createTheme({{
  palette: {{
    primary: {{
      main: '#1976d2',
    }},
    secondary: {{
      main: '#dc004e',
    }},
  }},
}});

function App() {{
  return (
    <ThemeProvider theme={{theme}}>
      <CssBaseline />
      <Router>
        <AppBar position="static">
          <Toolbar>
            <Typography variant="h6" component="div" sx={{{{ flexGrow: 1 }}}}>
              {app.name}
            </Typography>
          </Toolbar>
        </AppBar>
        <Navigation />
        <Container maxWidth="lg" sx={{{{ mt: 4, mb: 4 }}}}>
          <Routes>
            <Route path="/" element={{<{default_view}View />}} />
{chr(10).join(view_routes)}
{chr(10).join(form_routes)}
          </Routes>
        </Container>
      </Router>
    </ThemeProvider>
  );
}}

export default App;'''
        
        with open(output_dir / "src" / "App.tsx", "w") as f:
            f.write(content)
    
    def _generate_form_component(self, form: FormModel, output_dir: Path) -> None:
        """Generate a React form component."""
        form_name = self._pascal_case(form.name)
        
        # Generate field components
        field_components = []
        for field in form.fields:
            field_name = self._camel_case(field.name)
            rules_str = f"{{ required: '{field.label} is required' }}" if field.required else "{}"
            
            if field.type == FieldType.TEXT:
                field_components.append(f'''            <Grid item xs={{12}} md={{6}}>
              <Controller
                name="{field_name}"
                control={{control}}
                defaultValue=""
                rules={rules_str}
                render={{({{ field: fieldProps }}) => (
                  <TextField
                    {{...fieldProps}}
                    label="{field.label}"
                    fullWidth
                    error={{!!errors.{field_name}}}
                    helperText={{errors.{field_name}?.message}}
                  />
                )}}
              />
            </Grid>''')
            elif field.type == FieldType.RICH_TEXT:
                field_components.append(f'''            <Grid item xs={{12}}>
              <Controller
                name="{field_name}"
                control={{control}}
                defaultValue=""
                rules={rules_str}
                render={{({{ field: fieldProps }}) => (
                  <TextField
                    {{...fieldProps}}
                    label="{field.label}"
                    multiline
                    rows={{4}}
                    fullWidth
                    error={{!!errors.{field_name}}}
                    helperText={{errors.{field_name}?.message}}
                  />
                )}}
              />
            </Grid>''')
            else:
                field_components.append(f'''            <Grid item xs={{12}} md={{6}}>
              <Controller
                name="{field_name}"
                control={{control}}
                defaultValue=""
                rules={rules_str}
                render={{({{ field: fieldProps }}) => (
                  <TextField
                    {{...fieldProps}}
                    label="{field.label}"
                    fullWidth
                    error={{!!errors.{field_name}}}
                    helperText={{errors.{field_name}?.message}}
                  />
                )}}
              />
            </Grid>''')
        
        # Generate TypeScript interface
        interface_fields = []
        for field in form.fields:
            field_name = self._camel_case(field.name)
            ts_type = self._field_type_to_validation(field.type)
            interface_fields.append(f"  {field_name}: {ts_type};")
        
        content = f'''import React, {{ useState, useEffect }} from 'react';
import {{ useParams, useNavigate }} from 'react-router-dom';
import {{ useForm, Controller }} from 'react-hook-form';
import {{
  Paper,
  TextField,
  Button,
  Typography,
  Box,
  Grid
}} from '@mui/material';

interface {form_name}Data {{
{chr(10).join(interface_fields)}
}}

const {form_name}Form: React.FC = () => {{
  const {{ id }} = useParams<{{ id: string }}>();
  const navigate = useNavigate();
  const {{ control, handleSubmit, reset, formState: {{ errors }} }} = useForm<{form_name}Data>();
  const [loading, setLoading] = useState(false);

  useEffect(() => {{
    if (id) {{
      loadDocument(id);
    }}
  }}, [id]);

  const loadDocument = async (documentId: string) => {{
    try {{
      setLoading(true);
      console.log('Loading document:', documentId);
    }} catch (error) {{
      console.error('Error loading document:', error);
    }} finally {{
      setLoading(false);
    }}
  }};

  const onSubmit = async (data: {form_name}Data) => {{
    try {{
      setLoading(true);
      console.log('Saving form data:', data);
      navigate('/all-documents');
    }} catch (error) {{
      console.error('Error saving form:', error);
    }} finally {{
      setLoading(false);
    }}
  }};

  return (
    <Paper elevation={{3}} sx={{{{ p: 3 }}}}>
      <Typography variant="h4" gutterBottom>
        {form.name} {{id ? '(Edit)' : '(New)'}}
      </Typography>
      
      <Box component="form" onSubmit={{handleSubmit(onSubmit)}} sx={{{{ mt: 2 }}}}>
        <Grid container spacing={{3}}>
{chr(10).join(field_components)}
        </Grid>
        
        <Box sx={{{{ mt: 3, display: 'flex', gap: 2 }}}}>
          <Button
            type="submit"
            variant="contained"
            disabled={{loading}}
          >
            {{loading ? 'Saving...' : 'Save'}}
          </Button>
          <Button
            variant="outlined"
            onClick={{() => navigate('/all-documents')}}
          >
            Cancel
          </Button>
        </Box>
      </Box>
    </Paper>
  );
}};

export default {form_name}Form;'''
        
        form_file = output_dir / "src" / "components" / "forms" / f"{form_name}Form.tsx"
        with open(form_file, "w") as f:
            f.write(content)
    
    def _generate_view_component(self, view: ViewModel, output_dir: Path) -> None:
        """Generate a React view component."""
        view_name = self._pascal_case(view.name)
        
        # Generate table headers
        headers = []
        for column in view.columns:
            headers.append(f'              <TableCell>{column.title}</TableCell>')
        
        # Generate table cells for data display
        cells = []
        for column in view.columns:
            column_name = self._camel_case(column.name)
            if column.data_type in [FieldType.DATE, FieldType.DATETIME]:
                cells.append(f'                  <TableCell>{{new Date(item.{column_name}).toLocaleDateString()}}</TableCell>')
            else:
                cells.append(f'                  <TableCell>{{item.{column_name}}}</TableCell>')
        
        # Generate interface fields
        interface_fields = []
        for column in view.columns:
            column_name = self._camel_case(column.name)
            ts_type = self._field_type_to_validation(column.data_type)
            interface_fields.append(f"  {column_name}: {ts_type};")
        
        content = f'''import React, {{ useState, useEffect }} from 'react';
import {{ useNavigate }} from 'react-router-dom';
import {{
  Paper,
  Table,
  TableBody,
  TableCell,
  TableContainer,
  TableHead,
  TableRow,
  TablePagination,
  Button,
  Typography,
  Box,
  TextField,
  InputAdornment,
  IconButton
}} from '@mui/material';
import {{
  Add as AddIcon,
  Search as SearchIcon,
  Edit as EditIcon,
  Delete as DeleteIcon
}} from '@mui/icons-material';

interface {view_name}Item {{
  id: string;
{chr(10).join(interface_fields)}
}}

const {view_name}View: React.FC = () => {{
  const navigate = useNavigate();
  const [data, setData] = useState<{view_name}Item[]>([]);
  const [loading, setLoading] = useState(true);
  const [page, setPage] = useState(0);
  const [rowsPerPage, setRowsPerPage] = useState(10);
  const [searchTerm, setSearchTerm] = useState('');

  useEffect(() => {{
    loadData();
  }}, []);

  const loadData = async () => {{
    try {{
      setLoading(true);
      // Sample data for demonstration
      const sampleData: {view_name}Item[] = [
        {{
          id: '1',
{chr(10).join([f"          {self._camel_case(col.name)}: 'Sample {col.title} 1'," for col in view.columns])}
        }},
        {{
          id: '2',
{chr(10).join([f"          {self._camel_case(col.name)}: 'Sample {col.title} 2'," for col in view.columns])}
        }}
      ];
      setData(sampleData);
    }} catch (error) {{
      console.error('Error loading data:', error);
    }} finally {{
      setLoading(false);
    }}
  }};

  const handleEdit = (id: string) => {{
    navigate(`/default-form/${{id}}`);
  }};

  const handleDelete = async (id: string) => {{
    if (window.confirm('Are you sure you want to delete this item?')) {{
      try {{
        setData(data.filter(item => item.id !== id));
      }} catch (error) {{
        console.error('Error deleting item:', error);
      }}
    }}
  }};

  const filteredData = data.filter(item =>
    Object.values(item).some(value =>
      value.toString().toLowerCase().includes(searchTerm.toLowerCase())
    )
  );

  const paginatedData = filteredData.slice(
    page * rowsPerPage,
    page * rowsPerPage + rowsPerPage
  );

  return (
    <Paper elevation={{3}} sx={{{{ p: 3 }}}}>
      <Box sx={{{{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', mb: 3 }}}}>
        <Typography variant="h4">
          {view.name}
        </Typography>
        <Button
          variant="contained"
          startIcon={{<AddIcon />}}
          onClick={{() => navigate('/default-form')}}
        >
          Add New
        </Button>
      </Box>

      <Box sx={{{{ mb: 3 }}}}>
        <TextField
          placeholder="Search..."
          value={{searchTerm}}
          onChange={{(e) => setSearchTerm(e.target.value)}}
          InputProps={{{{
            startAdornment: (
              <InputAdornment position="start">
                <SearchIcon />
              </InputAdornment>
            ),
          }}}}
          sx={{{{ minWidth: 300 }}}}
        />
      </Box>

      <TableContainer>
        <Table>
          <TableHead>
            <TableRow>
{chr(10).join(headers)}
              <TableCell>Actions</TableCell>
            </TableRow>
          </TableHead>
          <TableBody>
            {{loading ? (
              <TableRow>
                <TableCell colSpan={{{len(view.columns) + 1}}} align="center">
                  Loading...
                </TableCell>
              </TableRow>
            ) : paginatedData.length === 0 ? (
              <TableRow>
                <TableCell colSpan={{{len(view.columns) + 1}}} align="center">
                  No data found
                </TableCell>
              </TableRow>
            ) : (
              paginatedData.map((item) => (
                <TableRow key={{item.id}}>
{chr(10).join(cells)}
                  <TableCell>
                    <IconButton onClick={{() => handleEdit(item.id)}} size="small">
                      <EditIcon />
                    </IconButton>
                    <IconButton onClick={{() => handleDelete(item.id)}} size="small">
                      <DeleteIcon />
                    </IconButton>
                  </TableCell>
                </TableRow>
              ))
            )}}
          </TableBody>
        </Table>
      </TableContainer>

      <TablePagination
        rowsPerPageOptions={{[5, 10, 25]}}
        component="div"
        count={{filteredData.length}}
        rowsPerPage={{rowsPerPage}}
        page={{page}}
        onPageChange={{(_, newPage) => setPage(newPage)}}
        onRowsPerPageChange={{(event) => {{
          setRowsPerPage(parseInt(event.target.value, 10));
          setPage(0);
        }}}}
      />
    </Paper>
  );
}};

export default {view_name}View;'''
        
        view_file = output_dir / "src" / "components" / "views" / f"{view_name}View.tsx"
        with open(view_file, "w") as f:
            f.write(content)
    
    def _generate_data_files(self, app: ApplicationModel, output_dir: Path) -> None:
        """Generate data files for the application."""
        # Generate sample data
        data = {
            "documents": [doc.dict() for doc in app.documents],
            "forms": [form.dict() for form in app.forms],
            "views": [view.dict() for view in app.views]
        }
        
        with open(output_dir / "src" / "data" / "appData.json", "w") as f:
            json.dump(data, f, indent=2, default=str)
    
    def _generate_routing(self, app: ApplicationModel, output_dir: Path) -> None:
        """Generate navigation component."""
        # Generate navigation items for views and forms
        view_items = []
        form_items = []
        
        for view in app.views:
            view_kebab = self._kebab_case(view.name)
            view_items.append(f'''        <ListItem disablePadding>
          <ListItemButton
            component={{Link}}
            to="/{view_kebab}"
            selected={{location.pathname === '/{view_kebab}'}}
          >
            <ListItemIcon>
              <ViewListIcon />
            </ListItemIcon>
            <ListItemText primary="{view.name}" />
          </ListItemButton>
        </ListItem>''')
        
        for form in app.forms:
            form_kebab = self._kebab_case(form.name)
            form_items.append(f'''        <ListItem disablePadding>
          <ListItemButton
            component={{Link}}
            to="/{form_kebab}"
            selected={{location.pathname === '/{form_kebab}'}}
          >
            <ListItemIcon>
              <FormIcon />
            </ListItemIcon>
            <ListItemText primary="New {form.name}" />
          </ListItemButton>
        </ListItem>''')
        
        content = f'''import React from 'react';
import {{ Link, useLocation }} from 'react-router-dom';
import {{
  Drawer,
  List,
  ListItem,
  ListItemButton,
  ListItemIcon,
  ListItemText,
  Divider
}} from '@mui/material';
import {{
  ViewList as ViewListIcon,
  Description as FormIcon
}} from '@mui/icons-material';

const Navigation: React.FC = () => {{
  const location = useLocation();

  return (
    <Drawer
      variant="permanent"
      sx={{{{
        width: 240,
        flexShrink: 0,
        '& .MuiDrawer-paper': {{
          width: 240,
          boxSizing: 'border-box',
          top: 64, // Height of AppBar
          height: 'calc(100% - 64px)',
        }},
      }}}}
    >
      <List>
        <ListItem disablePadding>
          <ListItemButton
            component={{Link}}
            to="/"
            selected={{location.pathname === '/'}}
          >
            <ListItemIcon>
              <ViewListIcon />
            </ListItemIcon>
            <ListItemText primary="Home" />
          </ListItemButton>
        </ListItem>
        
        <Divider />
        
{chr(10).join(view_items)}
        
        <Divider />
        
{chr(10).join(form_items)}
      </List>
    </Drawer>
  );
}};

export default Navigation;'''
        
        with open(output_dir / "src" / "components" / "Navigation.tsx", "w") as f:
            f.write(content)
    
    def _generate_styles(self, output_dir: Path) -> None:
        """Generate CSS styles."""
        css_content = '''body {
  margin: 0;
  font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', 'Roboto', 'Oxygen',
    'Ubuntu', 'Cantarell', 'Fira Sans', 'Droid Sans', 'Helvetica Neue',
    sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
}

code {
  font-family: source-code-pro, Menlo, Monaco, Consolas, 'Courier New',
    monospace;
}

.App {
  text-align: center;
}

.App-header {
  background-color: #282c34;
  padding: 20px;
  color: white;
}'''
        
        with open(output_dir / "src" / "index.css", "w") as f:
            f.write(css_content)
    
    def _generate_config_files(self, output_dir: Path) -> None:
        """Generate configuration files."""
        # Generate index.tsx
        index_content = '''import React from 'react';
import ReactDOM from 'react-dom/client';
import './index.css';
import App from './App';

const root = ReactDOM.createRoot(
  document.getElementById('root') as HTMLElement
);
root.render(
  <React.StrictMode>
    <App />
  </React.StrictMode>
);'''
        
        with open(output_dir / "src" / "index.tsx", "w") as f:
            f.write(index_content)
        
        # Generate public/index.html
        html_content = '''<!DOCTYPE html>
<html lang="en">
  <head>
    <meta charset="utf-8" />
    <link rel="icon" href="%PUBLIC_URL%/favicon.ico" />
    <meta name="viewport" content="width=device-width, initial-scale=1" />
    <meta name="theme-color" content="#000000" />
    <meta
      name="description"
      content="React app converted from Lotus Notes"
    />
    <title>Lotus Notes React App</title>
  </head>
  <body>
    <noscript>You need to enable JavaScript to run this app.</noscript>
    <div id="root"></div>
  </body>
</html>'''
        
        with open(output_dir / "public" / "index.html", "w") as f:
            f.write(html_content)
        
        # Generate tsconfig.json
        tsconfig = {
            "compilerOptions": {
                "target": "es5",
                "lib": ["dom", "dom.iterable", "es6"],
                "allowJs": True,
                "skipLibCheck": True,
                "esModuleInterop": True,
                "allowSyntheticDefaultImports": True,
                "strict": True,
                "forceConsistentCasingInFileNames": True,
                "noFallthroughCasesInSwitch": True,
                "module": "esnext",
                "moduleResolution": "node",
                "resolveJsonModule": True,
                "isolatedModules": True,
                "noEmit": True,
                "jsx": "react-jsx"
            },
            "include": ["src"]
        }
        
        with open(output_dir / "tsconfig.json", "w") as f:
            json.dump(tsconfig, f, indent=2)
    
    # Helper methods for string transformations
    def _camel_case(self, text: str) -> str:
        """Convert text to camelCase."""
        words = text.replace('-', '_').split('_')
        return words[0].lower() + ''.join(word.capitalize() for word in words[1:])
    
    def _pascal_case(self, text: str) -> str:
        """Convert text to PascalCase."""
        words = text.replace('-', '_').split('_')
        return ''.join(word.capitalize() for word in words)
    
    def _kebab_case(self, text: str) -> str:
        """Convert text to kebab-case."""
        return text.lower().replace('_', '-').replace(' ', '-')
    
    def _field_type_to_input_type(self, field_type: FieldType) -> str:
        """Convert field type to HTML input type."""
        mapping = {
            FieldType.TEXT: "text",
            FieldType.NUMBER: "number",
            FieldType.DATE: "date",
            FieldType.TIME: "time",
            FieldType.DATETIME: "datetime-local",
            FieldType.BOOLEAN: "checkbox",
            FieldType.RICH_TEXT: "textarea"
        }
        return mapping.get(field_type, "text")
    
    def _field_type_to_validation(self, field_type: FieldType) -> str:
        """Convert field type to TypeScript type."""
        mapping = {
            FieldType.TEXT: "string",
            FieldType.NUMBER: "number",
            FieldType.DATE: "string",
            FieldType.TIME: "string", 
            FieldType.DATETIME: "string",
            FieldType.BOOLEAN: "boolean",
            FieldType.RICH_TEXT: "string",
            FieldType.NAMES: "string",
            FieldType.KEYWORDS: "string[]",
            FieldType.DOCLINK: "string",
            FieldType.ATTACHMENT: "string[]"
        }
        return mapping.get(field_type, "string")

