# Craft Calculator Phase 2 — Recipe Resolver

## Context

- İş problemi:
  Tek bir item için recipe tree çözümleyebilecek temel resolver katmanını kurmak.

## Goal

- Beklenen sonuç:
  Recipe resolver için ilk teknik tasarım ve implementation scope oluşsun.
- Başarı kriteri:
  - input/output contract net olsun
  - recursive çözümleme gereksinimleri yazılsın
  - recipe -> ingredient tree çözümü için veri akışı netleşsin
  - missing recipe / missing ingredient handling kuralları netleşsin

## Constraints

- scope dışı UI yok
- canlı veri fetch yok

## Output Expectation

- resolver planı
- riskler
- test senaryoları

## Functional Coverage

- item -> recipe çözümleme
- recipe -> ingredient listesi çözümleme
- recursive cost-tree için temel yapı
- missing node handling
- cycle/invalid recipe riskleri

## Acceptance Focus

- tek item için recipe çözümü yapılabilecek kadar net domain ve servis contract'ı oluşmalı
- resolver gelecekte price katmanına bağlanabilecek şekilde tasarlanmalı