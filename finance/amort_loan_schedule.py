"""
Show schedule of an amortizable loan.

"""

from dataclasses import dataclass
from typing import List


# some class
@dataclass
class MonthlyPay:
    month_id: int
    interest_pay: float
    capital_pay: float
    remaining_capital: float
    monthly_pay: float


# some functions
def build_amort_sched_l(amount_eur: float, percent_by_year: float, nb_months: int) -> List[MonthlyPay]:
    """ Generate an amortization schedule list from amount, percent and delay of credit. """
    # annual interest rate (example: 12%) -> monthly rate (example: 0.01)
    monthly_rate = (percent_by_year / 100) / 12
    # calculate monthly payment using the loan payment formula
    monthly_pay = (amount_eur * monthly_rate) / (1 - (1 + monthly_rate)**-nb_months)
    # build schedule list
    remaining_capital = amount_eur
    amort_sched_l = []
    for month_id in range(1, nb_months + 1):
        interest_pay = remaining_capital * monthly_rate
        captital_pay = monthly_pay - interest_pay
        remaining_capital -= captital_pay
        mp = MonthlyPay(month_id=month_id, interest_pay=interest_pay, capital_pay=captital_pay, remaining_capital=remaining_capital, monthly_pay=monthly_pay)
        amort_sched_l.append(mp)
    # return the amortization schedule list
    return amort_sched_l


if __name__ == '__main__':
    print(f"{'#':>3s} {'interest':>8s} {'capital':>8s} {'remaining':>10s} {'pay':>8s}")
    for mp in build_amort_sched_l(amount_eur=50_000, percent_by_year=3.0, nb_months=3*12):
        print(f"{mp.month_id:3d} {mp.interest_pay:>8.2f} {mp.capital_pay:>8.2f} {mp.remaining_capital:>10.2f} {mp.monthly_pay:>8.2f}")
