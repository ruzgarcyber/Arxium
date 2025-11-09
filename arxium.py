# --- Arxium --- Lightweight, Pentest Tool Launcher ---

import json
import os
import subprocess
import sys
import shutil
import argparse
import traceback
from rich.console import Console
from rich.table import Table
from rich.panel import Panel

TOOL_DOSYASI = 'tools.json'

def tool_yukle():
    if not os.path.exists(TOOL_DOSYASI):
        with open(TOOL_DOSYASI, "w", encoding="utf-8") as f:
            json.dump({"tools": [], "favorites": []}, f, indent=2, ensure_ascii=False)
        print("[+] tools.json dosyası oluşturuldu.")
    else:
        print("[+] Tool dosyası zaten mevcut.")
    with open(TOOL_DOSYASI, "r", encoding="utf-8") as f:
        data = json.load(f)
    tools = data.get("tools", [])
    favorites = data.get("favorites", [])
    return tools, favorites


def tool_calistir(cmd, tool_id="tool"):
    try:
        subprocess.run(cmd, shell=True)
        print(f"[+] {tool_id} başarıyla çalıştırıldı.")
    except Exception as e:
        print(f"[-] Hata: {e}")


def kontrol_et(tool):
    cevap = input("İstediğiniz Tool'u giriniz: ")
    if os.path.exists(TOOL_DOSYASI):
        print(f"[+] {cevap} kontrol ediliyor...")
    else:
        print("[-] Tool dosyası yoktur.")


def cikis():
    cevap = input("Çıkmak istiyor musunuz? (Y/N): ").strip().lower()
    if cevap == "y":
        print("Çıkılıyor...")
        sys.exit(0)
    else:
        print("Programda kalınıyor.")


def kontrol():
    if os.path.exists(TOOL_DOSYASI):
        print("[+] Toollar yüklü! İstediğiniz Toolları kullanabilirsiniz.")
    else:
        print("[-] Toollar yüklü değil. Gerekli olan toolları indiriniz.")


YAPIMCI = "ruzgarcyber (Rüzgar Umut Gündoğan)"
BANNER = r"""
    _  ____  _  _  _  _  _ 
   /_\|_  / / \/ \/ \/ \/ |
  / _ \ / /  \  /\  /\  /| |
 /_/ \_\/___\/_/\/_/\/_/ |_| 
   Arxium — Minimal CLI Tool Launcher
"""

console = Console()

def build_tools_table(tools, favorites):
    table = Table(title="Available Tools")
    table.add_column("#", style="bold", width=4)
    table.add_column("ID", style="magenta", no_wrap=True)
    table.add_column("Name", style="green")
    table.add_column("Description", style="white")
    table.add_column("Cmd Template", style="blue")

    for i, t in enumerate(tools, start=1):
        tid = t.get("id", "")
        name = t.get("name", "")
        desc = t.get("description", "")
        cmd = t.get("cmd_template", "")
        fav_mark = "★" if tid in favorites else ""
        short_cmd = (cmd if len(cmd) <= 60 else cmd[:57] + "...")
        table.add_row(str(i), tid, f"{name} {fav_mark}", desc, short_cmd)
    return table

def banner_yazdir():
    CYAN = "\033[96m"
    RESET = "\033[0m"
    print(CYAN + BANNER + RESET)
    print(f"Yapımcı: {YAPIMCI}")
    print("-" * 48 + "\n")


def main():
    parser = argparse.ArgumentParser(
        prog="arxium",
        description="Arxium — Minimal CLI Tool Launcher (Gerçek hedefler üzerinde denemeyiniz!!)"
    )
    parser.add_argument("-l", "--list", action="store_true", help="List available tools and exit")
    parser.add_argument("-t", "--tool", type=str, metavar="TOOL_ID",
                        help="Run tool by id (non-interactive if --arg provided for placeholders)")
    parser.add_argument("--arg", action="append", metavar="KEY=VALUE",
                        help="Provide placeholder values for the tool template (can be repeated). Example: --arg target=10.10.10.10")
    parser.add_argument("--no-logs", action="store_true", help="Disable logging of runs")
    parser.add_argument("--fav", type=str, metavar="TOOL_ID", help="Toggle favorite for TOOL_ID")
    parser.add_argument("--version", action="store_true", help="Show version and exit")

    args = parser.parse_args()

    banner_yazdir()
    kontrol()
    tools, favorites = tool_yukle()

    if args.list:
        if not tools:
            console.print("[yellow]tools.json içinde hiç tool yok.[/yellow]")
        else:
            table = build_tools_table(tools, favorites)
            console.print(table)
        return

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        traceback.print_exc()
    finally:
        input("\nProgram bitti. Kapatmak için ENTER'a basın...")