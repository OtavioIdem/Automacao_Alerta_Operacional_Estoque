"""Detecta estoque insuficiente e envia alerta somente mediante autorizacao."""
from __future__ import annotations

import argparse
import csv
import json
import os
from pathlib import Path

import requests


def low_stock(csv_path: Path, columns: dict[str, str]) -> list[dict[str, str]]:
    with csv_path.open(encoding="utf-8-sig", newline="") as file:
        rows = list(csv.DictReader(file))
    required = set(columns.values())
    if not rows or not required.issubset(rows[0]):
        raise ValueError(f"CSV sem as colunas obrigatorias: {sorted(required)}")
    quantity, minimum = columns["quantity"], columns["minimum"]
    return [row for row in rows if float(row[quantity].replace(",", ".")) < float(row[minimum].replace(",", "."))]


def format_message(items: list[dict[str, str]], columns: dict[str, str]) -> str:
    if not items:
        return "Estoque verificado: nenhum item abaixo do minimo."
    lines = ["ALERTA: itens abaixo do estoque minimo:"]
    for item in items:
        lines.append(f"- {item[columns['sku']]} | {item[columns['description']]} | saldo: {item[columns['quantity']]} | minimo: {item[columns['minimum']]}")
    return "\n".join(lines)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--config", type=Path, default=Path("config.json"))
    parser.add_argument("--apply", action="store_true", help="autoriza envio ao webhook")
    args = parser.parse_args()
    config = json.loads(args.config.read_text(encoding="utf-8"))
    items = low_stock(Path(config["input_csv"]), config["columns"])
    message = format_message(items, config["columns"])
    print(message)
    if not args.apply or config.get("dry_run", True):
        print("Simulacao: nenhum webhook foi chamado.")
        return
    url = os.getenv(config["webhook_url_env"])
    if not url:
        raise RuntimeError("URL do webhook ausente na variavel de ambiente configurada.")
    response = requests.post(url, json={"text": message}, timeout=15)
    response.raise_for_status()
    print("Alerta enviado.")


if __name__ == "__main__":
    main()
