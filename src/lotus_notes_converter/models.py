"""
Data models for the Lotus Notes to React conversion system.

These models serve as the intermediate representation between NSF parsing
and React application generation.
"""

from datetime import datetime
from enum import Enum
from typing import Any, Dict, List, Optional, Union
from pydantic import BaseModel, Field


class FieldType(str, Enum):
    """Enumeration of supported field types."""
    TEXT = "text"
    NUMBER = "number"
    DATE = "date"
    TIME = "time"
    DATETIME = "datetime"
    BOOLEAN = "boolean"
    RICH_TEXT = "rich_text"
    NAMES = "names"
    KEYWORDS = "keywords"
    DOCLINK = "doclink"
    ATTACHMENT = "attachment"
    COMPUTED = "computed"


class ValidationRuleType(str, Enum):
    """Types of validation rules."""
    REQUIRED = "required"
    MIN_LENGTH = "min_length"
    MAX_LENGTH = "max_length"
    MIN_VALUE = "min_value"
    MAX_VALUE = "max_value"
    PATTERN = "pattern"
    CUSTOM = "custom"


class AccessLevel(str, Enum):
    """Access levels for security models."""
    NO_ACCESS = "no_access"
    DEPOSITOR = "depositor"
    READER = "reader"
    AUTHOR = "author"
    EDITOR = "editor"
    DESIGNER = "designer"
    MANAGER = "manager"


class ValidationRuleModel(BaseModel):
    """Model for field validation rules."""
    type: ValidationRuleType
    value: Optional[Union[str, int, float]] = None
    message: Optional[str] = None
    formula: Optional[str] = None


class ChoiceModel(BaseModel):
    """Model for field choice options."""
    value: str
    label: str
    selected: bool = False


class DisplayPropertiesModel(BaseModel):
    """Model for field display properties."""
    width: Optional[int] = None
    height: Optional[int] = None
    font_name: Optional[str] = None
    font_size: Optional[int] = None
    font_bold: bool = False
    font_italic: bool = False
    color: Optional[str] = None
    background_color: Optional[str] = None
    alignment: Optional[str] = None
    visible: bool = True
    read_only: bool = False


class FieldModel(BaseModel):
    """Model representing a form field."""
    id: str
    name: str
    type: FieldType
    label: str
    description: Optional[str] = None
    required: bool = False
    default_value: Optional[Any] = None
    validation_rules: List[ValidationRuleModel] = Field(default_factory=list)
    display_properties: Optional[DisplayPropertiesModel] = None
    computed_formula: Optional[str] = None
    choices: List[ChoiceModel] = Field(default_factory=list)
    help_text: Optional[str] = None


class LayoutModel(BaseModel):
    """Model for form layout information."""
    width: Optional[int] = None
    height: Optional[int] = None
    sections: List[Dict[str, Any]] = Field(default_factory=list)
    tab_order: List[str] = Field(default_factory=list)
    responsive: bool = True


class ActionModel(BaseModel):
    """Model for form/view actions."""
    id: str
    name: str
    label: str
    description: Optional[str] = None
    formula: Optional[str] = None
    script: Optional[str] = None
    script_language: Optional[str] = None
    button_style: Optional[str] = None
    icon: Optional[str] = None
    hotkey: Optional[str] = None
    visible: bool = True
    enabled: bool = True


class SecurityModel(BaseModel):
    """Model for security settings."""
    read_access: List[str] = Field(default_factory=list)
    write_access: List[str] = Field(default_factory=list)
    delete_access: List[str] = Field(default_factory=list)
    default_access: AccessLevel = AccessLevel.READER
    inherit_from_parent: bool = True


class SubformModel(BaseModel):
    """Model for embedded subforms."""
    id: str
    name: str
    fields: List[FieldModel] = Field(default_factory=list)
    layout: Optional[LayoutModel] = None


class FormModel(BaseModel):
    """Model representing a Lotus Notes form."""
    id: str
    name: str
    alias: Optional[str] = None
    description: Optional[str] = None
    fields: List[FieldModel] = Field(default_factory=list)
    layout: Optional[LayoutModel] = None
    actions: List[ActionModel] = Field(default_factory=list)
    validation_rules: List[ValidationRuleModel] = Field(default_factory=list)
    security: Optional[SecurityModel] = None
    computed_fields: List[FieldModel] = Field(default_factory=list)
    subforms: List[SubformModel] = Field(default_factory=list)
    created_date: Optional[datetime] = None
    modified_date: Optional[datetime] = None
    version: Optional[str] = None


class ColumnModel(BaseModel):
    """Model for view columns."""
    id: str
    name: str
    title: str
    field_name: Optional[str] = None
    formula: Optional[str] = None
    width: Optional[int] = None
    alignment: Optional[str] = None
    sortable: bool = True
    resizable: bool = True
    visible: bool = True
    data_type: FieldType = FieldType.TEXT
    format: Optional[str] = None


class SortingModel(BaseModel):
    """Model for view sorting configuration."""
    column_id: str
    direction: str = "asc"  # "asc" or "desc"
    priority: int = 0


class CategorizationModel(BaseModel):
    """Model for view categorization."""
    column_id: str
    show_totals: bool = False
    expand_by_default: bool = True


class ViewModel(BaseModel):
    """Model representing a Lotus Notes view."""
    id: str
    name: str
    alias: Optional[str] = None
    description: Optional[str] = None
    selection_formula: Optional[str] = None
    columns: List[ColumnModel] = Field(default_factory=list)
    sorting: List[SortingModel] = Field(default_factory=list)
    categorization: Optional[CategorizationModel] = None
    actions: List[ActionModel] = Field(default_factory=list)
    security: Optional[SecurityModel] = None
    created_date: Optional[datetime] = None
    modified_date: Optional[datetime] = None
    default_view: bool = False


class AgentModel(BaseModel):
    """Model representing a Lotus Notes agent."""
    id: str
    name: str
    description: Optional[str] = None
    trigger: Optional[str] = None
    schedule: Optional[str] = None
    target: Optional[str] = None
    script: Optional[str] = None
    script_language: Optional[str] = None
    enabled: bool = True
    security: Optional[SecurityModel] = None
    created_date: Optional[datetime] = None
    modified_date: Optional[datetime] = None


class DocumentModel(BaseModel):
    """Model representing a document."""
    id: str
    form_name: str
    fields: Dict[str, Any] = Field(default_factory=dict)
    attachments: List[str] = Field(default_factory=list)
    created_date: Optional[datetime] = None
    modified_date: Optional[datetime] = None
    author: Optional[str] = None
    readers: List[str] = Field(default_factory=list)


class ResourceModel(BaseModel):
    """Model for application resources (images, files, etc.)."""
    id: str
    name: str
    type: str
    content: Optional[bytes] = None
    file_path: Optional[str] = None
    size: Optional[int] = None
    mime_type: Optional[str] = None


class AccessControlModel(BaseModel):
    """Model for application-level access control."""
    managers: List[str] = Field(default_factory=list)
    designers: List[str] = Field(default_factory=list)
    editors: List[str] = Field(default_factory=list)
    authors: List[str] = Field(default_factory=list)
    readers: List[str] = Field(default_factory=list)
    default_access: AccessLevel = AccessLevel.READER
    enforce_consistent_acl: bool = True


class ApplicationModel(BaseModel):
    """Model representing the complete Lotus Notes application."""
    id: str
    name: str
    description: Optional[str] = None
    version: Optional[str] = None
    created_date: Optional[datetime] = None
    modified_date: Optional[datetime] = None
    access_control: Optional[AccessControlModel] = None
    forms: List[FormModel] = Field(default_factory=list)
    views: List[ViewModel] = Field(default_factory=list)
    agents: List[AgentModel] = Field(default_factory=list)
    documents: List[DocumentModel] = Field(default_factory=list)
    resources: List[ResourceModel] = Field(default_factory=list)
    metadata: Dict[str, Any] = Field(default_factory=dict)

    def get_form_by_name(self, name: str) -> Optional[FormModel]:
        """Get a form by name."""
        for form in self.forms:
            if form.name == name or form.alias == name:
                return form
        return None

    def get_view_by_name(self, name: str) -> Optional[ViewModel]:
        """Get a view by name."""
        for view in self.views:
            if view.name == name or view.alias == name:
                return view
        return None

    def get_documents_by_form(self, form_name: str) -> List[DocumentModel]:
        """Get all documents created with a specific form."""
        return [doc for doc in self.documents if doc.form_name == form_name]

