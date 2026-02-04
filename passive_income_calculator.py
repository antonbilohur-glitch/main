#!/usr/bin/env python3
"""
Калькулятор пасивного доходу та плану досягнення фінансової незалежності
Розрахунок для досягнення $3,000/місяць пасивного доходу
"""

from dataclasses import dataclass
from typing import List, Dict
import math


@dataclass
class Investment:
    """Клас для зберігання інформації про інвестицію"""
    name: str
    amount: float
    currency: str
    monthly_income: float
    annual_yield: float


class PassiveIncomeCalculator:
    """Калькулятор пасивного доходу та плану інвестицій"""
    
    def __init__(self, usd_rate: float = 41.0):
        self.usd_rate = usd_rate
        self.target_monthly_income = 3000  # Ціль: $3,000/місяць
        self.monthly_investment = 200  # Планова інвестиція: $200/місяць
        
    def convert_to_usd(self, amount: float, currency: str) -> float:
        """Конвертує суму в долари"""
        if currency.upper() == 'UAH':
            return amount / self.usd_rate
        return amount
    
    def calculate_current_portfolio(self) -> Dict:
        """Розраховує поточний стан портфеля"""
        
        # Поточні інвестиції
        inzhur_reit = Investment(
            name="INZHUR REIT",
            amount=43000,  # грн
            currency="UAH",
            monthly_income=300,  # грн/місяць
            annual_yield=0.0  # розрахуємо
        )
        
        bonds = Investment(
            name="Облігації (UAH)",
            amount=40000,  # грн
            currency="UAH",
            monthly_income=0,  # припустимо 10% річних
            annual_yield=0.10
        )
        
        cash = Investment(
            name="Готівка (USD)",
            amount=1000,  # USD
            currency="USD",
            monthly_income=0,
            annual_yield=0.0
        )
        
        # Конвертуємо все в USD
        inzhur_usd = self.convert_to_usd(inzhur_reit.amount, inzhur_reit.currency)
        bonds_usd = self.convert_to_usd(bonds.amount, bonds.currency)
        cash_usd = cash.amount
        
        # Дохідність INZHUR REIT
        inzhur_monthly_income_usd = self.convert_to_usd(inzhur_reit.monthly_income, "UAH")
        inzhur_annual_yield = (inzhur_monthly_income_usd * 12 / inzhur_usd) * 100
        
        # Дохідність облігацій
        bonds_monthly_income_usd = (bonds_usd * bonds.annual_yield) / 12
        
        # Загальний капітал та дохід
        total_capital_usd = inzhur_usd + bonds_usd + cash_usd
        total_monthly_income_usd = inzhur_monthly_income_usd + bonds_monthly_income_usd
        average_yield = (total_monthly_income_usd * 12 / total_capital_usd) * 100
        
        return {
            'investments': {
                'inzhur_reit': {
                    'amount_uah': inzhur_reit.amount,
                    'amount_usd': inzhur_usd,
                    'monthly_income_uah': inzhur_reit.monthly_income,
                    'monthly_income_usd': inzhur_monthly_income_usd,
                    'annual_yield': inzhur_annual_yield
                },
                'bonds': {
                    'amount_uah': bonds.amount,
                    'amount_usd': bonds_usd,
                    'monthly_income_usd': bonds_monthly_income_usd,
                    'annual_yield': bonds.annual_yield * 100
                },
                'cash': {
                    'amount_usd': cash_usd
                }
            },
            'totals': {
                'capital_usd': total_capital_usd,
                'capital_uah': total_capital_usd * self.usd_rate,
                'monthly_income_usd': total_monthly_income_usd,
                'monthly_income_uah': total_monthly_income_usd * self.usd_rate,
                'annual_income_usd': total_monthly_income_usd * 12,
                'average_yield': average_yield
            }
        }
    
    def calculate_required_capital(self, target_yield: float = 8.0) -> Dict:
        """
        Розраховує необхідний капітал для досягнення цілі
        
        Args:
            target_yield: Очікувана річна дохідність (%)
        """
        required_annual_income = self.target_monthly_income * 12
        required_capital = (required_annual_income / target_yield) * 100
        
        return {
            'target_monthly_income': self.target_monthly_income,
            'target_annual_income': required_annual_income,
            'target_yield': target_yield,
            'required_capital': required_capital
        }
    
    def calculate_investment_plan(
        self,
        current_capital: float,
        required_capital: float,
        monthly_investment: float,
        expected_yield: float = 8.0
    ) -> Dict:
        """
        Розраховує план досягнення цілі з урахуванням складного відсотка
        
        Args:
            current_capital: Поточний капітал
            required_capital: Необхідний капітал
            monthly_investment: Щомісячна інвестиція
            expected_yield: Очікувана річна дохідність (%)
        """
        gap = required_capital - current_capital
        monthly_rate = expected_yield / 100 / 12
        
        # Розрахунок часу до досягнення цілі з урахуванням складного відсотка
        # FV = PV * (1 + r)^n + PMT * [((1 + r)^n - 1) / r]
        # Вирішуємо для n (кількість місяців)
        
        months_needed = 0
        capital = current_capital
        
        results_by_year = []
        
        for month in range(1, 601):  # Максимум 50 років
            # Додаємо дохід від капіталу
            monthly_income = capital * monthly_rate
            capital += monthly_income
            
            # Додаємо щомісячну інвестицію
            capital += monthly_investment
            
            # Зберігаємо результати по роках
            if month % 12 == 0:
                year = month // 12
                annual_income = capital * (expected_yield / 100)
                monthly_passive_income = annual_income / 12
                
                results_by_year.append({
                    'year': year,
                    'month': month,
                    'capital': capital,
                    'monthly_passive_income': monthly_passive_income,
                    'annual_income': annual_income,
                    'progress': (monthly_passive_income / self.target_monthly_income) * 100
                })
            
            # Перевіряємо чи досягли цілі
            if months_needed == 0:
                monthly_passive_income = capital * monthly_rate
                if monthly_passive_income >= self.target_monthly_income:
                    months_needed = month
        
        years_needed = months_needed / 12 if months_needed > 0 else float('inf')
        
        # Альтернативні сценарії
        scenarios = self.calculate_scenarios(current_capital, required_capital, expected_yield)
        
        return {
            'current_capital': current_capital,
            'required_capital': required_capital,
            'gap': gap,
            'monthly_investment': monthly_investment,
            'expected_yield': expected_yield,
            'months_needed': months_needed,
            'years_needed': years_needed,
            'total_invested': current_capital + (monthly_investment * months_needed),
            'results_by_year': results_by_year,
            'scenarios': scenarios
        }
    
    def calculate_scenarios(
        self,
        current_capital: float,
        required_capital: float,
        base_yield: float = 8.0
    ) -> List[Dict]:
        """Розраховує різні сценарії досягнення цілі"""
        scenarios = []
        
        monthly_investments = [100, 200, 300, 500, 1000]
        
        for monthly_inv in monthly_investments:
            months = 0
            capital = current_capital
            monthly_rate = base_yield / 100 / 12
            
            for month in range(1, 601):
                capital += capital * monthly_rate + monthly_inv
                monthly_income = capital * monthly_rate
                
                if monthly_income >= self.target_monthly_income:
                    months = month
                    break
            
            if months > 0:
                scenarios.append({
                    'monthly_investment': monthly_inv,
                    'months_needed': months,
                    'years_needed': months / 12,
                    'total_invested': current_capital + (monthly_inv * months),
                    'final_capital': capital
                })
        
        return scenarios
    
    def print_detailed_report(self):
        """Виводить детальний звіт"""
        print("\n" + "="*80)
        print("💰 КАЛЬКУЛЯТОР ПАСИВНОГО ДОХОДУ")
        print("="*80)
        
        # Поточний портфель
        portfolio = self.calculate_current_portfolio()
        
        print("\n📊 ПОТОЧНИЙ ПОРТФЕЛЬ:")
        print("─" * 80)
        
        inv = portfolio['investments']
        
        print("\n1. INZHUR REIT:")
        print(f"   Сума: {inv['inzhur_reit']['amount_uah']:,.0f} грн (${inv['inzhur_reit']['amount_usd']:,.2f})")
        print(f"   Дивіденди: {inv['inzhur_reit']['monthly_income_uah']:,.0f} грн/міс (${inv['inzhur_reit']['monthly_income_usd']:.2f})")
        print(f"   Дохідність: {inv['inzhur_reit']['annual_yield']:.2f}% річних")
        print(f"   Статус: ✅ Реінвестиція дивідендів (складний відсоток)")
        
        print("\n2. Облігації (UAH):")
        print(f"   Сума: {inv['bonds']['amount_uah']:,.0f} грн (${inv['bonds']['amount_usd']:,.2f})")
        print(f"   Дохід: ${inv['bonds']['monthly_income_usd']:.2f}/міс (орієнтовно)")
        print(f"   Дохідність: {inv['bonds']['annual_yield']:.0f}% річних (припущення)")
        
        print("\n3. Готівка:")
        print(f"   Сума: ${inv['cash']['amount_usd']:,.0f}")
        print(f"   Дохідність: 0% (резерв)")
        
        totals = portfolio['totals']
        
        print("\n" + "─" * 80)
        print("РАЗОМ:")
        print(f"   Загальний капітал: ${totals['capital_usd']:,.2f} ({totals['capital_uah']:,.0f} грн)")
        print(f"   Пасивний дохід: ${totals['monthly_income_usd']:.2f}/міс ({totals['monthly_income_uah']:,.0f} грн)")
        print(f"   Річний дохід: ${totals['annual_income_usd']:,.2f}")
        print(f"   Середня дохідність: {totals['average_yield']:.2f}% річних")
        
        # Ціль
        print("\n" + "="*80)
        print("🎯 ЦІЛЬ:")
        print("─" * 80)
        print(f"   Бажаний пасивний дохід: ${self.target_monthly_income:,.0f}/місяць")
        print(f"   Це річних: ${self.target_monthly_income * 12:,.0f}")
        print(f"   Поточний прогрес: {(totals['monthly_income_usd'] / self.target_monthly_income) * 100:.2f}%")
        
        # Необхідний капітал
        print("\n" + "="*80)
        print("💎 НЕОБХІДНИЙ КАПІТАЛ:")
        print("─" * 80)
        
        for target_yield in [6, 8, 10, 12]:
            required = self.calculate_required_capital(target_yield)
            gap = required['required_capital'] - totals['capital_usd']
            
            print(f"\n   При {target_yield}% річних:")
            print(f"   • Необхідно: ${required['required_capital']:,.0f}")
            print(f"   • Є зараз: ${totals['capital_usd']:,.2f}")
            print(f"   • Не вистачає: ${gap:,.2f}")
        
        # План досягнення
        print("\n" + "="*80)
        print(f"📅 ПЛАН ДОСЯГНЕННЯ (при інвестиції ${self.monthly_investment}/місяць):")
        print("─" * 80)
        
        # Базовий сценарій (8% річних)
        base_required = self.calculate_required_capital(8.0)
        plan = self.calculate_investment_plan(
            totals['capital_usd'],
            base_required['required_capital'],
            self.monthly_investment,
            8.0
        )
        
        print(f"\n📊 БАЗОВИЙ СЦЕНАРІЙ (8% річних):")
        print(f"   Поточний капітал: ${plan['current_capital']:,.2f}")
        print(f"   Необхідний капітал: ${plan['required_capital']:,.0f}")
        print(f"   Не вистачає: ${plan['gap']:,.2f}")
        print(f"   Щомісячна інвестиція: ${plan['monthly_investment']:.0f}")
        
        if plan['years_needed'] != float('inf'):
            print(f"\n   ⏰ Час до досягнення цілі: {plan['years_needed']:.1f} років ({plan['months_needed']} місяців)")
            print(f"   💰 Всього інвестовано: ${plan['total_invested']:,.0f}")
        else:
            print(f"\n   ⚠️ При інвестиції ${self.monthly_investment}/міс ціль недосяжна")
            print(f"   💡 Потрібно більше інвестувати або вища дохідність")
        
        # Прогрес по роках
        print("\n" + "─" * 80)
        print("📈 ПРОГРЕС ПО РОКАХ:")
        print("─" * 80)
        print(f"{'Рік':<6} {'Капітал':<15} {'Дохід/міс':<15} {'% до цілі':<12}")
        print("─" * 80)
        
        for year_data in plan['results_by_year'][:20]:  # Показуємо перші 20 років
            print(f"{year_data['year']:<6} "
                  f"${year_data['capital']:>13,.0f} "
                  f"${year_data['monthly_passive_income']:>13,.2f} "
                  f"{year_data['progress']:>10.1f}%")
            
            if year_data['progress'] >= 100:
                print("─" * 80)
                print(f"✅ ЦІЛЬ ДОСЯГНУТА через {year_data['year']} років!")
                break
        
        # Альтернативні сценарії
        print("\n" + "="*80)
        print("🎲 АЛЬТЕРНАТИВНІ СЦЕНАРІЇ:")
        print("─" * 80)
        print(f"{'Інвестиція/міс':<15} {'Час до цілі':<20} {'Всього інвестовано':<20}")
        print("─" * 80)
        
        for scenario in plan['scenarios']:
            print(f"${scenario['monthly_investment']:<14} "
                  f"{scenario['years_needed']:<19.1f} років "
                  f"${scenario['total_invested']:>18,.0f}")
        
        # Рекомендації
        print("\n" + "="*80)
        print("💡 РЕКОМЕНДАЦІЇ:")
        print("─" * 80)
        
        current_progress = (totals['monthly_income_usd'] / self.target_monthly_income) * 100
        
        if current_progress < 10:
            print("\n   📍 ВИ НА ПОЧАТКУ ШЛЯХУ:")
            print(f"   • Поточний прогрес: {current_progress:.1f}%")
            print(f"   • Фокус на накопичення капіталу")
            print(f"   • Збільшуйте щомісячні інвестиції якщо можливо")
        elif current_progress < 50:
            print("\n   📍 ГАРНИЙ СТАРТ:")
            print(f"   • Поточний прогрес: {current_progress:.1f}%")
            print(f"   • Продовжуйте в тому ж дусі")
            print(f"   • Реінвестуйте всі дивіденди")
        else:
            print("\n   📍 ВИ МАЙЖЕ НА ЦІЛІ:")
            print(f"   • Поточний прогрес: {current_progress:.1f}%")
            print(f"   • Ще трохи!")
        
        print("\n   СТРАТЕГІЯ:")
        print("   1. Реінвестуйте ВСІ дивіденди (складний відсоток)")
        print("   2. Інвестуйте регулярно незалежно від ринку (DCA)")
        print("   3. Диверсифікуйте (не тримайте все в одному активі)")
        print("   4. Збільшуйте інвестиції при зростанні доходу")
        print("   5. Не чіпайте капітал - живіть тільки з дивідендів")
        
        print("\n   ОПТИМАЛЬНИЙ РОЗПОДІЛ:")
        print("   • 50-60% - Дивідендні акції/REIT")
        print("   • 20-30% - Облігації")
        print("   • 10-20% - Готівка/золото")
        
        print("\n" + "="*80)


def main():
    """Головна функція"""
    calculator = PassiveIncomeCalculator(usd_rate=41.0)
    
    print("""
╔═══════════════════════════════════════════════════════════════════════════════╗
║             КАЛЬКУЛЯТОР ФІНАНСОВОЇ НЕЗАЛЕЖНОСТІ                              ║
║           Розрахунок шляху до $3,000/місяць пасивного доходу                 ║
╚═══════════════════════════════════════════════════════════════════════════════╝
    """)
    
    calculator.print_detailed_report()
    
    print("\n💡 Підказка: Редагуйте змінні в коді для ваших даних")
    print("   - usd_rate: курс долара")
    print("   - target_monthly_income: бажаний дохід")
    print("   - monthly_investment: щомісячна інвестиція")


if __name__ == "__main__":
    main()
