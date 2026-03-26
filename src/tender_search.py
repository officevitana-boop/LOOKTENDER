#!/usr/bin/env python3
"""Пошук тендерів за замовником або постачальником."""

from __future__ import annotations

import argparse
import csv
import sqlite3
from pathlib import Path
from typing import Iterable

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_DATA_FILE = ROOT / "data" / "tenders.tsv"


def _connect() -> sqlite3.Connection:
    conn = sqlite3.connect(":memory:")
    conn.row_factory = sqlite3.Row
    conn.execute(
        """
        CREATE TABLE tenders (
            customer TEXT NOT NULL,
            contacts TEXT,
            expected_value REAL,
            link TEXT,
            important_date TEXT,
            auction_date TEXT,
            supplier TEXT,
            estimation_status TEXT,
            action_status TEXT,
            docs_check TEXT,
            result TEXT,
            manager TEXT
        )
        """
    )
    return conn


def load_tenders(conn: sqlite3.Connection, data_file: Path = DEFAULT_DATA_FILE) -> None:
    with data_file.open("r", encoding="utf-8") as f:
        reader = csv.DictReader(f, delimiter="\t")
        rows = [
            (
                row["Замовник"],
                row["Контакти"],
                float(row["Очікувана_вартість"]),
                row["Посилання"],
                row["Важлива_дата"],
                row["Аукціон"],
                row["Постачальник"],
                row["Прорахунок"],
                row["Дія"],
                row["Перевірка_документів"],
                row["Результат"],
                row["Менеджер"],
            )
            for row in reader
        ]

    conn.executemany(
        """
        INSERT INTO tenders (
            customer, contacts, expected_value, link, important_date,
            auction_date, supplier, estimation_status, action_status,
            docs_check, result, manager
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """,
        rows,
    )


def search_tenders(
    conn: sqlite3.Connection,
    *,
    customer: str | None = None,
    supplier: str | None = None,
    min_value: float | None = None,
    max_value: float | None = None,
) -> Iterable[sqlite3.Row]:
    where_parts: list[str] = []
    values: list[object] = []

    if customer:
        where_parts.append("customer LIKE ?")
        values.append(f"%{customer}%")

    if supplier:
        where_parts.append("supplier LIKE ?")
        values.append(f"%{supplier}%")

    if min_value is not None:
        where_parts.append("expected_value >= ?")
        values.append(min_value)

    if max_value is not None:
        where_parts.append("expected_value <= ?")
        values.append(max_value)

    where_clause = ""
    if where_parts:
        where_clause = "WHERE " + " AND ".join(where_parts)

    return conn.execute(
        f"""
        SELECT customer, supplier, expected_value, important_date, auction_date,
               action_status, link
        FROM tenders
        {where_clause}
        ORDER BY important_date
        """,
        values,
    )


def _render(results: Iterable[sqlite3.Row]) -> str:
    lines = []
    for row in results:
        lines.append(
            " | ".join(
                [
                    row["customer"],
                    row["supplier"],
                    f"{row['expected_value']:.2f}",
                    row["important_date"] or "—",
                    row["auction_date"] or "—",
                    row["action_status"] or "—",
                    row["link"],
                ]
            )
        )
    return "\n".join(lines) if lines else "Нічого не знайдено."


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Система пошуку товарів/тендерів за виробником або постачальником"
    )
    parser.add_argument("--customer", help="Частина назви замовника")
    parser.add_argument("--supplier", help="Частина назви постачальника/виробника")
    parser.add_argument("--min-value", type=float, help="Мінімальна очікувана вартість")
    parser.add_argument("--max-value", type=float, help="Максимальна очікувана вартість")
    parser.add_argument(
        "--data-file",
        type=Path,
        default=DEFAULT_DATA_FILE,
        help="TSV-файл з тендерами",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    conn = _connect()
    load_tenders(conn, args.data_file)
    results = search_tenders(
        conn,
        customer=args.customer,
        supplier=args.supplier,
        min_value=args.min_value,
        max_value=args.max_value,
    )
    print(_render(results))


if __name__ == "__main__":
    main()
