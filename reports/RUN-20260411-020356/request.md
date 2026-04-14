# Craft Calculator Phase 1 — Domain Foundation

## Context

- İş problemi:
  Albion Online craft calculator için temel domain yapısını request-temelli akışla başlatmak.
- Mevcut durum:
  İlk foundation dosyaları açıldı ancak fazların CrewAI üzerinden sistematik yürütülmesi gerekiyor.
- İlgili dosyalar:
  - `src/albion_factory/craftcalc/`
  - `knowledge/craft_calculator_sprint_01.md`

## Goal

- Beklenen sonuç:
  Domain foundation için net lead/research/validation çıktısı üretmek.
- Başarı kriteri:
  - item / recipe / price / rule / calculation modeli kapsamı netleşsin
  - sonraki implementation adımı netleşsin

## Constraints

- Dokunulmayacak alanlar:
  - request/run/report append-only akışı
- Riskli noktalar:
  - veri modelinin yanlış soyutlanması
  - static/live ayrımının bulanık kalması
- Kullanılabilecek kaynaklar:
  - repo içi craftcalc foundation
  - AODP ve resmi Albion kaynakları

## Output Expectation

- İstenen çıktı formatı:
  - Lead: scope / risks / next task
  - Researcher: source inventory / findings / constraints / sources
  - Validator: correctness / risky areas / required fixes / commit ready
- Test beklentisi:
  - compile/import smoke test planı
- Commit beklentisi:
  - henüz büyük implementasyon değil, foundation doğrulama