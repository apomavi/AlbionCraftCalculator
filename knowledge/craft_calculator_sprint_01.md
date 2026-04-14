# Albion Online Craft Calculator — Sprint 1 Foundation

## Goal
İlk sprintte craft calculator için domain foundation kurulur.

## Scope
- item / recipe / price / rule domain modelleri
- tek item için calculation request/result şeması
- future resolver/cost engine için temel tipler

## Non-Goals
- tam UI
- tam recipe graph çözümü
- gerçek canlı hesap motoru
- batch profitability

## Agent Responsibilities

### Lead
- sprint scope
- acceptance criteria
- sequencing

### Researcher
- data source inventory
- recipe/price/rule ihtiyaçları

### Coder
- domain models
- package structure
- calculator engine scaffold

### Tester
- schema smoke tests
- import validation

### Validator
- sprint output contract kontrolü

## Acceptance Criteria
- `src/albion_factory/craftcalc/` paketi oluşmuş olmalı
- domain modelleri import edilebilir olmalı
- compile hatası olmamalı
- sprint notu repo içinde kayıtlı olmalı