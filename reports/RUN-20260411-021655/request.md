# Craft Calculator Phase 3 — Price Resolver

## Context

- İş problemi:
  Şehir bazlı fiyat çözümleyici katmanı kurmak.

## Goal

- Beklenen sonuç:
  current price kullanım mantığı ve eksik fiyat fallback tasarımı netleşsin.
  şehir bazlı alış/satış price resolver contract'ı oluşsun.

## Constraints

- önce current price, sonra fallback
- history/trend sonraya kalabilir

## Output Expectation

- price resolver scope
- price source selection kuralları
- missing data fallback kuralları

## Functional Coverage

- city bazlı sell/buy seçim mantığı
- quality etkisi için veri şekli
- retrieved_at / freshness alanları
- veri kaynağı güveni
- missing price fallback

## Acceptance Focus

- current price resolver tek item hesap motoruna bağlanabilecek kadar net olmalı
- buy order vs sell order kullanım kuralı yazılmalı