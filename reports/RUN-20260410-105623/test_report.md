# Test Report

## verdict
Failed: Eşleşen test komutu bulunamadı. `pytest` komutu sistemde mevcut değil. 

## commands_run
- git diff --name-only HEAD~1 HEAD
- pytest scripts/import_items.py scripts/import_prices.py sql/001_create_core_tables.sql reference/city_bonuses.csv reference/focus_rules.csv reference/market_fees.csv

## findings
- pytest komutu çalıştırılamadı
