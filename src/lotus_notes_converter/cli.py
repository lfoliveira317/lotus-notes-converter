"""
Command Line Interface for the Lotus Notes to React Converter.
"""

import logging
import sys
from pathlib import Path
from typing import Optional

import click
from rich.console import Console
from rich.logging import RichHandler
from rich.progress import Progress, SpinnerColumn, TextColumn
from rich.panel import Panel
from rich.text import Text

from .converter import NotesConverter
from .exceptions import LotusConverterError


console = Console()


def setup_logging(verbose: bool = False) -> None:
    """Setup logging configuration."""
    level = logging.DEBUG if verbose else logging.INFO
    
    logging.basicConfig(
        level=level,
        format="%(message)s",
        datefmt="[%X]",
        handlers=[RichHandler(console=console, rich_tracebacks=True)]
    )


@click.group()
@click.option('--verbose', '-v', is_flag=True, help='Enable verbose logging')
@click.pass_context
def cli(ctx: click.Context, verbose: bool) -> None:
    """Lotus Notes to React Converter - Convert NSF files to React applications."""
    ctx.ensure_object(dict)
    ctx.obj['verbose'] = verbose
    setup_logging(verbose)


@cli.command()
@click.argument('nsf_file', type=click.Path(exists=True, path_type=Path))
@click.argument('output_dir', type=click.Path(path_type=Path))
@click.option('--template-dir', '-t', type=click.Path(exists=True, path_type=Path),
              help='Custom template directory')
@click.option('--force', '-f', is_flag=True, help='Overwrite existing output directory')
@click.pass_context
def convert(ctx: click.Context, nsf_file: Path, output_dir: Path, 
           template_dir: Optional[Path], force: bool) -> None:
    """Convert a Lotus Notes NSF file to a React application."""
    
    try:
        # Display conversion info
        console.print(Panel.fit(
            f"[bold blue]Lotus Notes to React Converter[/bold blue]\n\n"
            f"[bold]Input:[/bold] {nsf_file}\n"
            f"[bold]Output:[/bold] {output_dir}\n"
            f"[bold]Template:[/bold] {template_dir or 'Default'}",
            title="Conversion Settings"
        ))
        
        # Check if output directory exists
        if output_dir.exists() and not force:
            if not click.confirm(f"Output directory {output_dir} exists. Continue?"):
                console.print("[yellow]Conversion cancelled.[/yellow]")
                return
        
        # Initialize converter
        converter = NotesConverter(template_dir)
        
        # Run conversion with progress indicator
        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            console=console
        ) as progress:
            
            task = progress.add_task("Converting NSF file...", total=None)
            
            try:
                app_model = converter.convert(nsf_file, output_dir)
                progress.update(task, description="Conversion completed!")
                
                # Display success message
                console.print(Panel.fit(
                    f"[bold green]✓ Conversion Successful![/bold green]\n\n"
                    f"[bold]Application:[/bold] {app_model.name}\n"
                    f"[bold]Forms:[/bold] {len(app_model.forms)}\n"
                    f"[bold]Views:[/bold] {len(app_model.views)}\n"
                    f"[bold]Documents:[/bold] {len(app_model.documents)}\n\n"
                    f"[bold]Next steps:[/bold]\n"
                    f"1. cd {output_dir}\n"
                    f"2. npm install\n"
                    f"3. npm start",
                    title="Conversion Results"
                ))
                
            except LotusConverterError as e:
                progress.update(task, description="Conversion failed!")
                console.print(f"[bold red]Error:[/bold red] {e}")
                sys.exit(1)
                
    except Exception as e:
        console.print(f"[bold red]Unexpected error:[/bold red] {e}")
        if ctx.obj.get('verbose'):
            console.print_exception()
        sys.exit(1)


@cli.command()
@click.argument('nsf_file', type=click.Path(exists=True, path_type=Path))
def analyze(nsf_file: Path) -> None:
    """Analyze an NSF file and display its structure."""
    
    try:
        console.print(f"[bold blue]Analyzing NSF file:[/bold blue] {nsf_file}")
        
        # Initialize parser
        from .parser import NSFParser
        parser = NSFParser()
        
        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            console=console
        ) as progress:
            
            task = progress.add_task("Analyzing NSF structure...", total=None)
            
            try:
                app_model = parser.parse_file(nsf_file)
                progress.update(task, description="Analysis completed!")
                
                # Display analysis results
                console.print(Panel.fit(
                    f"[bold]Application Name:[/bold] {app_model.name}\n"
                    f"[bold]Description:[/bold] {app_model.description or 'N/A'}\n"
                    f"[bold]Created:[/bold] {app_model.created_date or 'N/A'}\n"
                    f"[bold]Modified:[/bold] {app_model.modified_date or 'N/A'}\n\n"
                    f"[bold]Forms:[/bold] {len(app_model.forms)}\n"
                    f"[bold]Views:[/bold] {len(app_model.views)}\n"
                    f"[bold]Documents:[/bold] {len(app_model.documents)}\n"
                    f"[bold]Resources:[/bold] {len(app_model.resources)}",
                    title="NSF Analysis Results"
                ))
                
                # Display forms
                if app_model.forms:
                    console.print("\n[bold blue]Forms:[/bold blue]")
                    for form in app_model.forms:
                        console.print(f"  • {form.name} ({len(form.fields)} fields)")
                
                # Display views
                if app_model.views:
                    console.print("\n[bold blue]Views:[/bold blue]")
                    for view in app_model.views:
                        console.print(f"  • {view.name} ({len(view.columns)} columns)")
                
            except LotusConverterError as e:
                progress.update(task, description="Analysis failed!")
                console.print(f"[bold red]Error:[/bold red] {e}")
                sys.exit(1)
                
    except Exception as e:
        console.print(f"[bold red]Unexpected error:[/bold red] {e}")
        sys.exit(1)


@cli.command()
def version() -> None:
    """Display version information."""
    from . import __version__, __author__
    
    console.print(Panel.fit(
        f"[bold blue]Lotus Notes to React Converter[/bold blue]\n\n"
        f"[bold]Version:[/bold] {__version__}\n"
        f"[bold]Author:[/bold] {__author__}\n\n"
        f"A tool for converting Lotus Notes applications to modern React applications.",
        title="Version Information"
    ))


def main() -> None:
    """Main entry point for the CLI."""
    cli()


if __name__ == '__main__':
    main()

