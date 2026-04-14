from __future__ import annotations

from dataclasses import dataclass, field

from albion_factory.craftcalc.models import CraftCalculationRequest, CraftCalculationResult, CraftRuleSet


@dataclass
class ProfitCalculationInput:
    request: CraftCalculationRequest
    material_cost: float
    output_price: float
    rules: CraftRuleSet
    focus_discount: float = 0.0


class ProfitEngine:
    """Initial profitability engine for craft calculator MVP.

    Phase 4 scope:
    - total craft cost
    - focus-adjusted cost
    - net revenue after fees/taxes
    - net profit
    - profit margin
    - break-even price
    """

    def calculate(self, data: ProfitCalculationInput) -> CraftCalculationResult:
        adjusted_input_cost = max(0.0, data.material_cost - data.focus_discount)
        total_cost = adjusted_input_cost + data.rules.crafting_fee + data.rules.usage_fee

        tax_multiplier = 1.0 - data.rules.sales_tax if data.request.include_taxes else 1.0
        net_revenue = data.output_price * tax_multiplier
        estimated_profit = net_revenue - total_cost
        profit_margin = (estimated_profit / total_cost) if total_cost > 0 else 0.0
        break_even_price = total_cost / tax_multiplier if tax_multiplier > 0 else total_cost

        notes: list[str] = []
        if data.request.use_focus:
            notes.append("Focus-adjusted cost applied")
        if data.request.include_taxes:
            notes.append("Taxes included in net revenue")

        return CraftCalculationResult(
            item_id=data.request.item_id,
            city=data.request.city,
            estimated_input_cost=round(total_cost, 2),
            estimated_output_value=round(net_revenue, 2),
            estimated_profit=round(estimated_profit, 2),
            profit_margin=round(profit_margin, 4),
            break_even_price=round(break_even_price, 2),
            notes=notes,
        )