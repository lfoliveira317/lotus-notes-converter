"""
Tests for the data models.
"""

import pytest
from datetime import datetime
from lotus_notes_converter.models import (
    ApplicationModel, FormModel, ViewModel, FieldModel, FieldType,
    ValidationRuleModel, ValidationRuleType, ColumnModel, DocumentModel
)


class TestFieldModel:
    """Tests for FieldModel."""
    
    def test_create_basic_field(self):
        """Test creating a basic field."""
        field = FieldModel(
            id="test_field",
            name="TestField",
            type=FieldType.TEXT,
            label="Test Field"
        )
        
        assert field.id == "test_field"
        assert field.name == "TestField"
        assert field.type == FieldType.TEXT
        assert field.label == "Test Field"
        assert field.required is False
        assert field.validation_rules == []
    
    def test_create_field_with_validation(self):
        """Test creating a field with validation rules."""
        validation_rule = ValidationRuleModel(
            type=ValidationRuleType.REQUIRED,
            message="This field is required"
        )
        
        field = FieldModel(
            id="required_field",
            name="RequiredField",
            type=FieldType.TEXT,
            label="Required Field",
            required=True,
            validation_rules=[validation_rule]
        )
        
        assert field.required is True
        assert len(field.validation_rules) == 1
        assert field.validation_rules[0].type == ValidationRuleType.REQUIRED


class TestFormModel:
    """Tests for FormModel."""
    
    def test_create_basic_form(self):
        """Test creating a basic form."""
        form = FormModel(
            id="test_form",
            name="TestForm",
            description="A test form"
        )
        
        assert form.id == "test_form"
        assert form.name == "TestForm"
        assert form.description == "A test form"
        assert form.fields == []
    
    def test_create_form_with_fields(self):
        """Test creating a form with fields."""
        field1 = FieldModel(
            id="field1",
            name="Field1",
            type=FieldType.TEXT,
            label="Field 1"
        )
        
        field2 = FieldModel(
            id="field2",
            name="Field2",
            type=FieldType.NUMBER,
            label="Field 2"
        )
        
        form = FormModel(
            id="test_form",
            name="TestForm",
            fields=[field1, field2]
        )
        
        assert len(form.fields) == 2
        assert form.fields[0].name == "Field1"
        assert form.fields[1].type == FieldType.NUMBER


class TestViewModel:
    """Tests for ViewModel."""
    
    def test_create_basic_view(self):
        """Test creating a basic view."""
        view = ViewModel(
            id="test_view",
            name="TestView",
            description="A test view"
        )
        
        assert view.id == "test_view"
        assert view.name == "TestView"
        assert view.description == "A test view"
        assert view.columns == []
        assert view.default_view is False
    
    def test_create_view_with_columns(self):
        """Test creating a view with columns."""
        column1 = ColumnModel(
            id="col1",
            name="column1",
            title="Column 1",
            data_type=FieldType.TEXT
        )
        
        column2 = ColumnModel(
            id="col2",
            name="column2",
            title="Column 2",
            data_type=FieldType.DATE
        )
        
        view = ViewModel(
            id="test_view",
            name="TestView",
            columns=[column1, column2]
        )
        
        assert len(view.columns) == 2
        assert view.columns[0].title == "Column 1"
        assert view.columns[1].data_type == FieldType.DATE


class TestApplicationModel:
    """Tests for ApplicationModel."""
    
    def test_create_basic_application(self):
        """Test creating a basic application."""
        app = ApplicationModel(
            id="test_app",
            name="TestApp",
            description="A test application"
        )
        
        assert app.id == "test_app"
        assert app.name == "TestApp"
        assert app.description == "A test application"
        assert app.forms == []
        assert app.views == []
        assert app.documents == []
    
    def test_get_form_by_name(self):
        """Test getting a form by name."""
        form1 = FormModel(id="form1", name="Form1")
        form2 = FormModel(id="form2", name="Form2", alias="FormAlias")
        
        app = ApplicationModel(
            id="test_app",
            name="TestApp",
            forms=[form1, form2]
        )
        
        # Test finding by name
        found_form = app.get_form_by_name("Form1")
        assert found_form is not None
        assert found_form.id == "form1"
        
        # Test finding by alias
        found_form = app.get_form_by_name("FormAlias")
        assert found_form is not None
        assert found_form.id == "form2"
        
        # Test not found
        found_form = app.get_form_by_name("NonExistent")
        assert found_form is None
    
    def test_get_view_by_name(self):
        """Test getting a view by name."""
        view1 = ViewModel(id="view1", name="View1")
        view2 = ViewModel(id="view2", name="View2", alias="ViewAlias")
        
        app = ApplicationModel(
            id="test_app",
            name="TestApp",
            views=[view1, view2]
        )
        
        # Test finding by name
        found_view = app.get_view_by_name("View1")
        assert found_view is not None
        assert found_view.id == "view1"
        
        # Test finding by alias
        found_view = app.get_view_by_name("ViewAlias")
        assert found_view is not None
        assert found_view.id == "view2"
        
        # Test not found
        found_view = app.get_view_by_name("NonExistent")
        assert found_view is None
    
    def test_get_documents_by_form(self):
        """Test getting documents by form name."""
        doc1 = DocumentModel(id="doc1", form_name="Form1", fields={"title": "Doc 1"})
        doc2 = DocumentModel(id="doc2", form_name="Form2", fields={"title": "Doc 2"})
        doc3 = DocumentModel(id="doc3", form_name="Form1", fields={"title": "Doc 3"})
        
        app = ApplicationModel(
            id="test_app",
            name="TestApp",
            documents=[doc1, doc2, doc3]
        )
        
        # Test getting documents for Form1
        form1_docs = app.get_documents_by_form("Form1")
        assert len(form1_docs) == 2
        assert form1_docs[0].id == "doc1"
        assert form1_docs[1].id == "doc3"
        
        # Test getting documents for Form2
        form2_docs = app.get_documents_by_form("Form2")
        assert len(form2_docs) == 1
        assert form2_docs[0].id == "doc2"
        
        # Test getting documents for non-existent form
        no_docs = app.get_documents_by_form("NonExistent")
        assert len(no_docs) == 0


class TestDocumentModel:
    """Tests for DocumentModel."""
    
    def test_create_basic_document(self):
        """Test creating a basic document."""
        doc = DocumentModel(
            id="test_doc",
            form_name="TestForm",
            fields={"title": "Test Document", "content": "Test content"}
        )
        
        assert doc.id == "test_doc"
        assert doc.form_name == "TestForm"
        assert doc.fields["title"] == "Test Document"
        assert doc.fields["content"] == "Test content"
        assert doc.attachments == []

