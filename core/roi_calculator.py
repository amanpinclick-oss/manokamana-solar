from typing import Dict

class ROICalculator:
    """
    Utility for solar financial projections in the Indian market.
    Calculates CAPEX, monthly savings, and payback period.
    """

    def __init__(self, cost_per_kw: float = 60000.0, units_per_kw_monthly: float = 120.0, rate_per_unit: float = 8.0):
        self.cost_per_kw = cost_per_kw
        self.units_per_kw_monthly = units_per_kw_monthly
        self.rate_per_unit = rate_per_unit
        # CO2 Factor: ~0.82 kg per kWh for Indian grid
        self.co2_factor_kg_per_kwh = 0.82

    def calculate(self, roof_size_sqft: float, monthly_bill_inr: float) -> Dict[str, float]:
        """
        Performs ROI calculation based on roof size and electricity bill.
        """
        # 1kW needs ~100 sq ft
        recommended_capacity_kw = roof_size_sqft / 100
        
        # Limit capacity based on bill (don't over-install)
        # Assuming system should cover ~90% of bill
        needed_capacity_kw = (monthly_bill_inr * 0.9) / (self.units_per_kw_monthly * self.rate_per_unit)
        
        final_capacity_kw = min(recommended_capacity_kw, needed_capacity_kw)
        
        capex = final_capacity_kw * self.cost_per_kw
        monthly_savings = final_capacity_kw * self.units_per_kw_monthly * self.rate_per_unit
        
        payback_years = capex / (monthly_savings * 12) if monthly_savings > 0 else 0
        
        # CO2 Calculation
        annual_generation_kwh = final_capacity_kw * self.units_per_kw_monthly * 12
        annual_co2_offset_tons = (annual_generation_kwh * self.co2_factor_kg_per_kwh) / 1000

        return {
            "capacity_kw": round(final_capacity_kw, 2),
            "capex_estimate": round(capex, 2),
            "monthly_savings": round(monthly_savings, 2),
            "payback_years": round(payback_years, 2),
            "roi_percentage": round((monthly_savings * 12 / capex) * 100, 2) if capex > 0 else 0,
            "annual_co2_offset_tons": round(annual_co2_offset_tons, 2)
        }
