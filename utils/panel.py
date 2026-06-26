from rich.console import Console, Group
from rich.table import Table
from rich.text import Text
from rich.style import Style
from rich.panel import Panel as RichPanel
from rich.progress import Progress, BarColumn, TextColumn, SpinnerColumn
from rich.live import Live
from rich.layout import Layout
import json, time

console = Console()

BANNER = """[bold cyan]
   ╔══════════════════════════════════════╗
   ║                                      ║
   ║       DISCORD SERVER CLONER v3       ║
   ║                                      ║
   ╚══════════════════════════════════════╝
[/bold cyan]"""

def clear_screen():
    import os
    os.system('cls' if os.name == 'nt' else 'clear')

def show_banner():
    clear_screen()
    console.print(BANNER, justify="center")

def show_settings():
    with open("./utils/config.json", "r") as f:
        data = json.load(f)
    on = Style(color="green", bold=True)
    off = Style(color="red", bold=True)
    labels = {"categories": "Kategoriler", "channels": "Kanallar", "roles": "Roller", "emojis": "Emojiler"}
    table = Table(show_header=True, header_style="bold cyan", box=None)
    table.add_column("Ayarlar", style="white", width=20)
    table.add_column("Durum", justify="center", width=10)
    for key, label in labels.items():
        val = data["copy_settings"].get(key, True)
        table.add_row(label, Text("AÇIK" if val else "KAPALI", style=on if val else off))
    console.print(RichPanel(table, title="[bold]Kopyalama Ayarları", border_style="cyan"))

def show_progress(guild_from, guild_to, user):
    with open("./utils/config.json", "r") as f:
        data = json.load(f)
    on = Style(color="green", bold=True)
    off = Style(color="red", bold=True)
    labels = {"categories": "Kategoriler", "channels": "Kanallar", "roles": "Roller", "emojis": "Emojiler"}
    table = Table(show_header=True, header_style="bold cyan", box=None)
    table.add_column("Kopyalanacak", style="white", width=20)
    table.add_column("Durum", justify="center", width=10)
    for key, label in labels.items():
        val = data["copy_settings"].get(key, True)
        table.add_row(label, Text("AÇIK" if val else "KAPALI", style=on if val else off))
    info = Table(show_header=False, box=None)
    info.add_column(style="bold yellow", width=10)
    info.add_column(style="white")
    info.add_row("Hedef:", str(guild_to))
    info.add_row("Kaynak:", str(guild_from))
    info.add_row("Hesap:", str(user))
    console.print(table)
    console.print(RichPanel(info, title="[bold]Kopyalama", border_style="green"))

def show_result(message, success=True):
    color = "green" if success else "red"
    console.print(RichPanel(f"[bold {color}]{message}[/]", border_style=color))

def show_error(message):
    console.print(RichPanel(f"[bold red]{message}[/]", border_style="red"))