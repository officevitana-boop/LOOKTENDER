# Tender Supplier Search

Система пошуку тендерів за **замовником** або **постачальником/виробником**.

## Що реалізовано
- Імпорт тендерів з TSV-файлу.
- Пошук за частиною назви замовника.
- Пошук за частиною назви постачальника.
- Фільтр за діапазоном очікуваної вартості.
- Вивід ключових полів: замовник, постачальник, вартість, важливі дати, статус, посилання.

## Запуск
```bash
python3 src/tender_search.py --supplier "Кукла"
python3 src/tender_search.py --customer "УКРГАЗВИДОБУВАННЯ"
python3 src/tender_search.py --min-value 100000 --max-value 250000
```

## Джерело даних
За замовчуванням використовується файл:

`data/tenders.tsv`

За потреби можна передати інший файл:

```bash
python3 src/tender_search.py --supplier "ВІТАНА" --data-file /path/to/file.tsv
```

## Тести
```bash
python3 -m unittest tests/test_tender_search.py
```
