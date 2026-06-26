try:
  import subprocess, os, sys, json, time, msvcrt
  import discord
  from utils.cloner import Cloner
  from utils.panel import show_banner, show_settings, show_result, show_error
  from discord import Client
  from rich.progress import Progress, BarColumn, TextColumn
  from rich.live import Live
  from rich.table import Table
  from rich.panel import Panel as RichPanel

  from rich.text import Text
  from rich.style import Style
  from rich.console import Group
except Exception:
  print("Installing Requirements...")
  subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
  os.execl(sys.executable, sys.executable, *sys.argv)

import logging
logging.getLogger("discord").setLevel(logging.CRITICAL)

with open("./utils/config.json", "r") as f:
  CONFIG = json.load(f)

def getkey():
  return msvcrt.getwch()

def ask_yes_no(prompt):
  sys.stdout.write(f"{prompt} [y/n] ")
  sys.stdout.flush()
  while True:
    k = getkey().lower()
    if k in ('y', 'n'):
      sys.stdout.write(k + '\n')
      return k == 'y'

def ask_input(prompt):
  sys.stdout.write(prompt)
  sys.stdout.flush()
  chars = []
  while True:
    k = msvcrt.getwch()
    if k == '\r':
      sys.stdout.write('\n')
      break
    elif k == '\b' or k == '\x7f':
      if chars:
        chars.pop()
        sys.stdout.write('\b \b')
    elif k == '\x03':
      raise KeyboardInterrupt
    else:
      chars.append(k)
      sys.stdout.write(k)
    sys.stdout.flush()
  return ''.join(chars)

def save_config(key, value):
  CONFIG[key] = value
  with open("./utils/config.json", "w") as f:
    json.dump(CONFIG, f, indent=4)

def get_token():
  if CONFIG.get("token"):
    return CONFIG["token"]
  show_banner()
  print()
  token = ask_input("> Token: ")
  save_config("token", token)
  return token

def get_settings():
  while True:
    show_banner()
    show_settings()
    print()
    if not ask_yes_no("Ayarları değiştir?"):
      break
    show_banner()
    for key, label in [("categories", "Kategoriler"), ("channels", "Kanallar"), ("roles", "Roller"), ("emojis", "Emojiler")]:
      val = ask_yes_no(f"{label} kopyalansın?")
      CONFIG["copy_settings"][key] = val
    save_config("copy_settings", CONFIG["copy_settings"])

def get_server_ids():
  show_banner()
  print()
  target = ask_input("Hedef sunucu ID (yeni oluşturduğun): ")
  show_banner()
  print()
  source = ask_input("Kopyalanacak sunucu ID: ")
  return target, source

async def run_cloner(client, target_id, source_id):
  guild_to = client.get_guild(int(target_id))
  guild_from = client.get_guild(int(source_id))
  if not guild_to or not guild_from:
    return "Sunucu bulunamadı! ID'leri kontrol et.", False

  start_time = time.time()
  on_style = Style(color="green", bold=True)
  off_style = Style(color="red", bold=True)
  labels = {"roles": "Roller", "categories": "Kategoriler", "channels": "Kanallar", "emojis": "Emojiler"}

  settings_table = Table(show_header=True, header_style="bold cyan", box=None)
  settings_table.add_column("Kopyalanacak", style="white", width=20)
  settings_table.add_column("Durum", justify="center", width=10)
  active_keys = []
  for key, label in labels.items():
    val = CONFIG["copy_settings"].get(key, True)
    settings_table.add_row(label, Text("AÇIK" if val else "KAPALI", style=on_style if val else off_style))
    if val:
      active_keys.append(key)

  info_table = Table(show_header=False, box=None)
  info_table.add_column(style="bold yellow", width=10)
  info_table.add_column(style="white")
  info_table.add_row("Hedef:", str(guild_to))
  info_table.add_row("Kaynak:", str(guild_from))
  info_table.add_row("Hesap:", str(client.user))
  info_panel = RichPanel(info_table, title="[bold]Kopyalama", border_style="green")

  roles_list = [r for r in guild_from.roles if r.name != "@everyone"]
  total = 1 + len(guild_to.channels)
  if "roles" in active_keys:
    total += len(roles_list)
  if "categories" in active_keys:
    total += len(guild_from.categories)
  if "channels" in active_keys:
    total += len(guild_from.text_channels) + len(guild_from.voice_channels)
  if "emojis" in active_keys:
    total += len(guild_from.emojis)

  progress = Progress(
    TextColumn("[bold cyan]{task.description}"),
    BarColumn(bar_width=40),
    TextColumn("[progress]{task.completed}/{task.total}"),
  )
  task = progress.add_task("Başlatılıyor...", total=total)
  done = 0

  def on_progress(stage, current, total_items):
    nonlocal done
    new_done = done + current
    progress.update(task, completed=new_done, description=f"[bold yellow]{stage}")

  combined = Group(settings_table, info_panel, RichPanel(progress, border_style="cyan"))
  with Live(combined, refresh_per_second=10):
    await Cloner.guild_create(guild_to, guild_from, on_progress)
    done += 1

    await Cloner.channels_delete(guild_to, on_progress)
    done += len(guild_to.channels)

    if "roles" in active_keys:
      await Cloner.roles_create(guild_to, guild_from, on_progress)
      done += len(roles_list)

    if "categories" in active_keys:
      await Cloner.categories_create(guild_to, guild_from, on_progress)
      done += len(guild_from.categories)

    if "channels" in active_keys:
      await Cloner.channels_create(guild_to, guild_from, on_progress)
      done += len(guild_from.text_channels) + len(guild_from.voice_channels)

    if "emojis" in active_keys:
      await Cloner.emojis_create(guild_to, guild_from, on_progress)
      done += len(guild_from.emojis)

    progress.update(task, completed=total, description="[bold green]Tamamlandı")
    time.sleep(0.5)

  elapsed = round(time.time() - start_time, 2)
  return f"Tamamlandı! ({elapsed}s)", True

def main():
  token = get_token()
  get_settings()
  target_id, source_id = get_server_ids()

  show_banner()
  print("\nBağlanıyor...")
  client = Client(bot=False)

  @client.event
  async def on_ready():
    msg, ok = await run_cloner(client, target_id, source_id)
    if ok:
      show_result(msg, True)
    else:
      show_error(msg)

  client.run(token)

if __name__ == "__main__":
  try:
    main()
  except KeyboardInterrupt:
    print("\nİptal edildi.")
  except Exception as e:
    show_error(str(e))