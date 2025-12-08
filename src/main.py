import click
from pathlib import Path
from jinja2 import Environment, FileSystemLoader
from src.FileServices.Group import Group


@click.group()
@click.version_option(version="0.0.1")
def cli():
    """PyTeambook: CLI tool to generate ICPC Team Reference Documents"""
    pass


@cli.command()
@click.argument(
    "input_dir", type=click.Path(exists=True, file_okay=False, path_type=Path)
)
@click.option(
    "-o",
    "--output",
    type=click.Path(path_type=Path),
    default="output.tex",
    help="Output LaTeX file path",
)
@click.option("-t", "--team-name", default="Team Name", help="Team name for header")
@click.option(
    "-u", "--university", default="University", help="University name for header"
)
@click.option(
    "-c",
    "--columns",
    type=click.IntRange(1, 3),
    default=2,
    help="Number of columns (1=portrait, 2-3=landscape)",
)
@click.option(
    "-p",
    "--paper",
    type=click.Choice(["a4", "letter", "legal"]),
    default="a4",
    help="Paper size (a4/letter/legal)",
)
@click.option(
    "-i",
    "--image",
    type=click.Path(exists=True, dir_okay=False, path_type=Path),
    default=None,
    help="Cover image (jpg/png only)",
)
def build(
    input_dir: Path,
    output: Path,
    team_name: str,
    university: str,
    columns: int,
    paper: str,
    image: Path,
):
    """
    Build a Team Reference Document from a directory of code files.

    INPUT_DIR: Directory containing organized code files (.cpp, .java, .py)
    """
    try:
        if image:
            if image.suffix.lower() not in [".jpg", ".jpeg", ".png"]:
                click.echo(
                    f"Error: Image must be JPG or PNG format, got: {image.suffix}",
                    err=True,
                )
                raise click.Abort()
            image_path = image.absolute()
            click.echo(f"Using cover image: {image.name}")
        else:
            image_path = None

        click.echo(f"Scanning directory: {input_dir}")

        group = Group(input_dir)

        if not group.hierarchy:
            click.echo("No code files found in the directory", err=True)
            return

        click.echo(
            f"✓ Found {sum(len(files) for _, subs in group.hierarchy for _, files in subs)} code files"
        )

        template_dir = Path(__file__).parent / "templates"
        env = Environment(loader=FileSystemLoader(str(template_dir)))
        template = env.get_template("default.tex")

        click.echo("Rendering LaTeX template...")

        def latex_escape(text):
            return text.replace("_", r"\_").replace("#", r"\#").replace("&", r"\&")

        orientation = "landscape" if columns >= 2 else "portrait"

        latex_content = template.render(
            hierarchy=group.hierarchy,
            team_name=latex_escape(team_name),
            university=latex_escape(university),
            columns=columns,
            orientation=orientation,
            paper=paper,
            cover_image=str(image_path) if image_path else None,
            open=open,
        )

        output.write_text(latex_content, encoding="utf-8")
        click.echo(f"Generated: {output.absolute()}")
        click.echo(f"Layout: {columns} column(s), {orientation}, {paper.upper()}")
        click.echo(f"\nCompile with: pdflatex -shell-escape {output.name}")

    except Exception as e:
        click.echo(f"Error: {e}", err=True)
        raise click.Abort()


@cli.command()
def info():
    """Display project information and requirements"""
    click.echo("""
PyTeambook v0.0.1
─────────────────────────────────────────────
ICPC Team Reference Document Generator

Requirements:
  • Python 3.9+
  • LaTeX distribution (TeXLive/MikTeX)
  • Pygments (for syntax highlighting)

Supported Languages:
  • C++ (.cpp, .cc, .cxx, .h, .hpp)
  • Python (.py)
  • Java (.java)
  • Bash (.sh, .bash)

Directory Structure:
  codes/
  ├── Section1/
  │   ├── Subsection1/
  │   │   ├── algorithm1.cpp
  │   │   └── algorithm2.cpp
  │   └── algorithm3.cpp
  └── Section2/
      └── algorithm4.py

Usage:
  pyteambook build ./codes -o teambook.tex
  pdflatex -shell-escape teambook.tex
    """)


if __name__ == "__main__":
    cli()
