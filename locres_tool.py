import csv
import os
import subprocess
import sys
import tempfile
import zipfile
from contextlib import contextmanager
from pathlib import Path

import requests
import typer
from pylocres import LocresFile
from rich import print as rprint
from rich.progress import track
from rich.prompt import Confirm

app = typer.Typer(
    help="Unreal Engine Locres Translators Tools: A community tool for extracting and reinserting dialogues/text from Unreal Engine locres files.",
    add_completion=False,
    rich_markup_mode="rich",
    pretty_exceptions_show_locals=False,
)


def get_gradient_colors(num, start="#64c800", end="#c8c800"):
    """Return a gradient of n colors from start to end. Output as RGB tuples if any input is a tuple."""
    s = (
        start
        if isinstance(start, (tuple, list))
        else tuple(int(start[i : i + 2], 16) for i in (1, 3, 5))
    )
    e = (
        end
        if isinstance(end, (tuple, list))
        else tuple(int(end[i : i + 2], 16) for i in (1, 3, 5))
    )
    out_tuple = not (isinstance(start, str) and isinstance(end, str))
    if num < 2:
        return [s] if out_tuple else [f"#{s[0]:02x}{s[1]:02x}{s[2]:02x}"]
    colors = []
    for i in range(num):
        r = int(s[0] + (e[0] - s[0]) * i / (num - 1))
        g = int(s[1] + (e[1] - s[1]) * i / (num - 1))
        b = int(s[2] + (e[2] - s[2]) * i / (num - 1))
        colors.append((r, g, b) if out_tuple else f"#{r:02x}{g:02x}{b:02x}")
    return colors


@contextmanager
def get_u4pak_executable():
    """
    Downloads the u4pak zip from GitHub, extracts it to a temporary directory,
    and yields the path to the correct executable based on the current OS.
    """
    url = "https://github.com/panzi/rust-u4pak/releases/download/v1.4.0/release-v1.4.0.zip"
    with tempfile.TemporaryDirectory() as tmp_dir:
        tmp_dir_path = Path(tmp_dir)
        zip_path = tmp_dir_path / "u4pak.zip"
        rprint(f"[cyan]Downloading u4pak from {url}...[/cyan]")
        response = requests.get(url)
        response.raise_for_status()
        with open(zip_path, "wb") as f:
            f.write(response.content)
        with zipfile.ZipFile(zip_path, "r") as zip_ref:
            zip_ref.extractall(tmp_dir)
        if sys.platform.startswith("win"):
            exec_path = tmp_dir_path / "x86_64-pc-windows-gnu" / "u4pak.exe"
        else:
            exec_path = tmp_dir_path / "x86_64-unknown-linux-gnu" / "u4pak"
            os.chmod(exec_path, 0o755)
        yield exec_path


@app.callback(invoke_without_command=True)
def main() -> None:
    """
    Print the ASCII banner. When the help flag (--help or -h) is used, the
    animated effect from terminaltexteffects is employed; otherwise the banner is printed with a gradient using get_gradient_colors.
    """
    banner_text = r"""
 ██▓     ▒█████   ▄████▄   ██▀███  ▓█████   ██████    ▄▄▄█████▓ ▒█████   ▒█████   ██▓
▓██▒    ▒██▒  ██▒▒██▀ ▀█  ▓██ ▒ ██▒▓█   ▀ ▒██    ▒    ▓  ██▒ ▓▒▒██▒  ██▒▒██▒  ██▒▓██▒
▒██░    ▒██░  ██▒▒▓█    ▄ ▓██ ░▄█ ▒▒███   ░ ▓██▄      ▒ ▓██░ ▒░▒██░  ██▒▒██░  ██▒▒██░
▒██░    ▒██   ██░▒▓▓▄ ▄██▒▒██▀▀█▄  ▒▓█  ▄   ▒   ██▒   ░ ▓██▓ ░ ▒██   ██░▒██   ██░▒██░
░██████▒░ ████▓▒░▒ ▓███▀ ░░██▓ ▒██▒░▒████▒▒██████▒▒     ▒██▒ ░ ░ ████▓▒░░ ████▓▒░░██████▒
░ ▒░▓  ░░ ▒░▒░▒░ ░ ░▒ ▒  ░░ ▒▓ ░▒▓░░░ ▒░ ░▒ ▒▓▒ ▒ ░     ▒ ░░   ░ ▒░▒░▒░ ░ ▒░▒░▒░ ░ ▒░▓  ░
░ ░ ▒  ░  ░ ▒ ▒░   ░  ▒     ░▒ ░ ▒░ ░ ░  ░░ ░▒  ░ ░       ░      ░ ▒ ▒░   ░ ▒ ▒░ ░ ░ ▒  ░
  ░ ░   ░ ░ ░ ▒  ░          ░░   ░    ░   ░  ░  ░       ░      ░ ░ ░ ▒  ░ ░ ░ ▒    ░ ░
    ░  ░    ░ ░  ░ ░         ░        ░  ░      ░                  ░ ░      ░ ░      ░
                 ░
    """
    is_help = any(arg in sys.argv for arg in ["--help", "-h"])
    lines = banner_text.splitlines()
    gradient_colors = get_gradient_colors(len(lines))
    if is_help:
        try:
            from terminaltexteffects.effects.effect_print import Print, PrintConfig
            from terminaltexteffects.engine.terminal import TerminalConfig
            from terminaltexteffects.utils.graphics import Color, Gradient

            effect = Print(banner_text)
            effect.effect_config.print_head_return_speed = (
                PrintConfig.print_head_return_speed * 25
            )
            effect.effect_config.print_speed = PrintConfig.print_speed * 25
            effect.effect_config.final_gradient_direction = Gradient.Direction.VERTICAL
            effect.effect_config.final_gradient_stops = tuple(
                Color(hex_str) for hex_str in reversed(gradient_colors)
            )
            term_conf = TerminalConfig()
            effect.terminal_config = term_conf
            with effect.terminal_output() as terminal:
                for frame in effect:
                    terminal.print(frame)
        except ImportError:
            for line, color in zip(lines, gradient_colors):
                rprint(f"[{color}]{line}[/]")
    else:
        # Static banner printing using gradient
        for line, color in zip(lines, gradient_colors):
            rprint(f"[{color}]{line}[/]")
    rprint(
        "[green]Community tool for extracting and reinserting dialogues/text from Unreal Engine locres files.[/green]\n"
    )


@app.command("decode")
def decode(
    locres_file: Path = typer.Argument(..., help="Input .locres file"),
    output_csv: Path = typer.Argument(..., help="Output CSV file"),
    variables: bool = typer.Option(
        False,
        "--variables",
        "-v",
        help="Include variable column (formatted as <namespace.name|entry.key>)",
    ),
    normalize_newlines: bool = typer.Option(
        False,
        "--normalize-newlines",
        "-n",
        help="Replace '\\r\\n' with '\\n' in translations",
    ),
    escape_newlines: bool = typer.Option(
        False,
        "--escape-newlines",
        "-e",
        help="Escape newline characters (e.g., '\\n' will be converted to '\\\\n') to avoid line breaks in CSV",
    ),
):
    """
    Decode a .locres file into CSV.

    When --variables is used the CSV will have three columns:
      [Variable, Original, Translation]
    Otherwise the CSV will have two columns: [Original, Translation].

    Additional flags allow newline normalization and escaping:
      --normalize-newlines: Replaces '\\r\\n' with '\\n'.
      --escape-newlines: Converts newline characters into escaped representations (e.g., '\\n' becomes '\\\\n').
    """
    try:
        locres = LocresFile()
        locres.read(str(locres_file))
    except Exception as e:
        rprint(f"[bold red]Error reading locres file {locres_file}: {e}[/bold red]")
        raise typer.Exit(code=1)

    seen = set()
    entries = [(namespace, entry) for namespace in locres for entry in namespace]

    with output_csv.open("w", newline="", encoding="utf-8") as csvfile:
        writer = csv.writer(csvfile)
        if variables:
            writer.writerow(["Variable", "Original", "Translation"])
        else:
            writer.writerow(["Original", "Translation"])

        for namespace, entry in track(
            entries, description="[cyan]Exporting translations...[/cyan]"
        ):
            text = entry.translation
            if normalize_newlines:
                text = text.replace("\r\n", "\n")
            if escape_newlines:
                text = text.replace("\n", "\\n")

            if variables:
                variable_key = f"<{namespace.name}|{entry.key}>"
                row_key = (variable_key, text)
                if row_key in seen:
                    continue
                seen.add(row_key)
                writer.writerow([variable_key, text, ""])
            else:
                row_key = (text,)
                if row_key in seen:
                    continue
                seen.add(row_key)
                writer.writerow([text, ""])
    rprint(f"[bold green]CSV exported to[/bold green] [cyan]{output_csv}[/cyan]")


@app.command("encode")
def encode(
    locres_file: Path = typer.Argument(..., help="Input .locres file"),
    csv_file: Path = typer.Argument(..., help="CSV file with translations"),
    output_locres: Path = typer.Argument(..., help="Output updated .locres file"),
    variables: bool = typer.Option(
        False,
        "--variables",
        "-v",
        help="Use variable column for matching translations",
    ),
    normalize_newlines: bool = typer.Option(
        False,
        "--normalize-newlines",
        "-n",
        help="Replace '\\r\\n' with '\\n' in translations before matching",
    ),
    escape_newlines: bool = typer.Option(
        False,
        "--escape-newlines",
        "-e",
        help="Escape newline characters (e.g., '\\n' to '\\\\n') in translations before matching",
    ),
):
    """
    Apply translations from a CSV file to a .locres file and save the updated file.

    When --variables is used the CSV is expected to have three columns:
      [Variable, Original, Translation]
    Otherwise, the CSV must have two columns: [Original, Translation].

    The script converts escaped '\\n' back to newlines for translations unless flags modify behavior.
    """
    translations = {}
    try:
        with csv_file.open("r", newline="", encoding="utf-8") as file:
            reader = csv.reader(file)
            _header = next(reader, None)
            if variables:
                for row in reader:
                    if len(row) >= 3 and row[0] and row[2]:
                        key = row[0]
                        trans = (
                            row[2].replace("\\n", "\n") if escape_newlines else row[2]
                        )
                        translations[key] = trans
            else:
                for row in reader:
                    if len(row) >= 2 and row[0] and row[1]:
                        key = row[0]
                        trans = (
                            row[1].replace("\\n", "\n") if escape_newlines else row[1]
                        )
                        translations[key] = trans
    except Exception as e:
        rprint(f"[bold red]Error reading CSV file {csv_file}: {e}[/bold red]")
        raise typer.Exit(code=1)

    try:
        locres = LocresFile()
        locres.read(str(locres_file))
    except Exception as e:
        rprint(f"[bold red]Error reading locres file {locres_file}: {e}[/bold red]")
        raise typer.Exit(code=1)

    all_entries = [(namespace, entry) for namespace in locres for entry in namespace]
    for namespace, entry in track(
        all_entries, description="[cyan]Applying translations...[/cyan]"
    ):
        if variables:
            key = f"<{namespace.name}|{entry.key}>"
            if key in translations:
                entry.translation = translations[key]
        else:
            text = entry.translation
            if normalize_newlines:
                text = text.replace("\r\n", "\n")
            if escape_newlines:
                text = text.replace("\n", "\\n")
            if text in translations:
                entry.translation = translations[text]
    output_locres.parent.mkdir(parents=True, exist_ok=True)
    try:
        locres.write(str(output_locres))
    except Exception as e:
        rprint(
            f"[bold red]Error writing updated locres file {output_locres}: {e}[/bold red]"
        )
        raise typer.Exit(code=1)
    rprint(
        f"[bold green]Updated locres file saved to[/bold green] [cyan]{output_locres}[/cyan]"
    )


@app.command("u4pak-unpack")
def u4pak_unpack(
    pak_file: Path = typer.Argument(..., help="Input pak file"),
    folder: str = typer.Argument(
        ...,
        help="Folder path within the pak to extract (e.g., ColonyShipGame/Content/Localization)",
    ),
    outdir: Path = typer.Argument(
        ..., help="Output directory where files will be extracted"
    ),
    yes: bool = typer.Option(
        False,
        "--yes",
        "-y",
        help="Skip confirmation prompt for downloading u4pak binary",
    ),
):
    """
    Extract a specific folder from a pak file using u4pak.

    This command downloads the u4pak tool, extracts the executable, and runs:

      u4pak.exe unpack "<pak_file>" "<folder>" --outdir <outdir>
    """
    if not yes:
        if not Confirm.ask(
            "[yellow]This will download and execute the u4pak binary from https://github.com/panzi/rust-u4pak/releases. Continue?[/yellow]"
        ):
            raise typer.Exit(code=1)
    try:
        with get_u4pak_executable() as u4pak:
            cmd = [str(u4pak), "unpack", str(pak_file), folder, "--outdir", str(outdir)]
            rprint(f"[cyan]Running command: {' '.join(cmd)}[/cyan]")
            result = subprocess.run(cmd, capture_output=True, text=True)
            if result.returncode != 0:
                rprint(f"[bold red]Error executing unpack: {result.stderr}[/bold red]")
                raise typer.Exit(code=1)
            else:
                rprint(
                    f"[bold green]Successfully extracted folder to {outdir}[/bold green]"
                )
    except Exception as e:
        rprint(f"[bold red]Error during unpack operation: {e}[/bold red]")
        raise typer.Exit(code=1)


@app.command("u4pak-list")
def u4pak_list(
    pak_file: Path = typer.Argument(..., help="Input pak file"),
    output_txt: Path = typer.Option(
        None,
        "--output",
        "-o",
        help="Optional output text file to save the list",
    ),
    yes: bool = typer.Option(
        False,
        "--yes",
        "-y",
        help="Skip confirmation prompt for downloading u4pak binary",
    ),
):
    """
    List the files contained in a pak file using u4pak.

    This command downloads the u4pak tool, extracts the executable, and runs:

      u4pak.exe list "<pak_file>"

    If --output is specified, the list is saved to the provided text file; otherwise, it is printed to the console.
    """
    if not yes:
        if not Confirm.ask(
            "[yellow]This will download and execute the u4pak binary from https://github.com/panzi/rust-u4pak/releases. Continue?[/yellow]"
        ):
            raise typer.Exit(code=1)
    try:
        with get_u4pak_executable() as u4pak:
            cmd = [str(u4pak), "list", str(pak_file)]
            rprint(f"[cyan]Running command: {' '.join(cmd)}[/cyan]")
            result = subprocess.run(cmd, capture_output=True, text=True)
            if result.returncode != 0:
                rprint(f"[bold red]Error executing list: {result.stderr}[/bold red]")
                raise typer.Exit(code=1)
            output = result.stdout
            if output_txt:
                try:
                    with output_txt.open("w", encoding="utf-8") as f:
                        f.write(output)
                    rprint(f"[bold green]File list saved to {output_txt}[/bold green]")
                except Exception as e:
                    rprint(
                        f"[bold red]Error writing to file {output_txt}: {e}[/bold red]"
                    )
                    raise typer.Exit(code=1)
            else:
                rprint("[green]List of files in pak:[/green]")
                rprint(output)
    except Exception as e:
        rprint(f"[bold red]Error during list operation: {e}[/bold red]")
        raise typer.Exit(code=1)


if __name__ == "__main__":
    app()
