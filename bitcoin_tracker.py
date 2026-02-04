#!/usr/bin/env python3
"""
Скрипт для моніторингу ціни біткоїна та виявлення інвестиційних можливостей
на основі аналізу попередження Майкла Б'юррі
"""

import requests
import json
from datetime import datetime
import time
from typing import Dict, List, Tuple


class BitcoinTracker:
    """Клас для відстеження ціни біткоїна та аналізу інвестиційних можливостей"""
    
    def __init__(self):
        self.api_url = "https://api.coingecko.com/api/v3"
        
        # Критичні рівні з аналізу Б'юррі
        self.critical_levels = {
            'current_resistance': 73000,
            'warning_level_1': 70000,
            'warning_level_2': 65000,
            'warning_level_3': 60000,
            'burry_target': 55000,
            'capitulation': 50000,
            'strong_buy_1': 50000,
            'strong_buy_2': 45000,
            'extreme_buy': 40000
        }
        
    def get_btc_price(self) -> Dict:
        """Отримує поточну ціну біткоїна та додаткові дані"""
        try:
            response = requests.get(
                f"{self.api_url}/simple/price",
                params={
                    'ids': 'bitcoin',
                    'vs_currencies': 'usd',
                    'include_market_cap': 'true',
                    'include_24hr_vol': 'true',
                    'include_24hr_change': 'true'
                },
                timeout=10
            )
            response.raise_for_status()
            data = response.json()['bitcoin']
            
            return {
                'price': data['usd'],
                'market_cap': data['usd_market_cap'],
                'volume_24h': data['usd_24h_vol'],
                'change_24h': data['usd_24h_change'],
                'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            }
        except Exception as e:
            print(f"❌ Помилка отримання даних: {e}")
            return None
    
    def get_fear_greed_index(self) -> Dict:
        """Отримує індекс страху та жадібності"""
        try:
            response = requests.get(
                "https://api.alternative.me/fng/",
                timeout=10
            )
            response.raise_for_status()
            data = response.json()['data'][0]
            
            return {
                'value': int(data['value']),
                'classification': data['value_classification']
            }
        except Exception as e:
            print(f"⚠️ Не вдалося отримати індекс страху/жадібності: {e}")
            return None
    
    def analyze_opportunity(self, price: float) -> Tuple[str, str, List[str]]:
        """
        Аналізує поточну ціну та визначає інвестиційну можливість
        
        Returns:
            Tuple[signal, risk_level, recommendations]
        """
        recommendations = []
        
        if price >= self.critical_levels['current_resistance']:
            signal = "🔴 НЕБЕЗПЕЧНА ЗОНА"
            risk_level = "ВИСОКИЙ РИЗИК"
            recommendations = [
                "❌ Не купувати біткоїн",
                "✅ Розглянути шорт-позиції через пут-опціони",
                "✅ Інвестувати в золото/срібло",
                "✅ Шортити криптокомпанії (MSTR, MARA, RIOT)",
                "💰 Накопичувати готівку для майбутніх покупок"
            ]
            
        elif price >= self.critical_levels['warning_level_1']:
            signal = "🟠 ЗОНА ПОПЕРЕДЖЕННЯ"
            risk_level = "ПІДВИЩЕНИЙ РИЗИК"
            recommendations = [
                "⚠️ Утримуватись від покупок",
                "✅ Підготувати шорт-стратегію",
                "✅ Збільшити позиції в золоті",
                "📊 Моніторити відтоки з ETF",
                "💰 Зберігати 30-40% готівки"
            ]
            
        elif price >= self.critical_levels['warning_level_3']:
            signal = "🟡 ЗОНА СПОСТЕРЕЖЕННЯ"
            risk_level = "СЕРЕДНІЙ РИЗИК"
            recommendations = [
                "👀 Уважно спостерігати за ринком",
                "⏳ Чекати подальшого зниження",
                "✅ Продовжувати DCA в золото",
                "📈 Готуватися до можливих покупок",
                "💰 Тримати 40-50% готівки"
            ]
            
        elif price >= self.critical_levels['burry_target']:
            signal = "🟢 ЗОНА ІНТЕРЕСУ"
            risk_level = "ПОМІРНИЙ РИЗИК"
            recommendations = [
                "💎 Розглянути початок накопичення (10-20% капіталу)",
                "⏰ Використовувати DCA стратегію",
                "✅ Продовжувати тримати золото",
                "📊 Моніторити хешрейт мережі",
                "🎯 Підготувати план для рівня $50k"
            ]
            
        elif price >= self.critical_levels['capitulation']:
            signal = "🟢 ЗОНА КАПІТУЛЯЦІЇ"
            risk_level = "СЕРЕДНІЙ РИЗИК - МОЖЛИВІСТЬ"
            recommendations = [
                "💎 АКТИВНО КУПУВАТИ (20-30% капіталу)",
                "🎯 Основна зона накопичення за Б'юррі",
                "⚠️ Чекати стабілізації хешрейту",
                "📊 Моніторити банкрутства майнерів",
                "✅ Зберігати резерв для $45k"
            ]
            
        elif price >= self.critical_levels['strong_buy_2']:
            signal = "🟢🟢 СИЛЬНА ЗОНА ПОКУПКИ"
            risk_level = "НИЖЧИЙ РИЗИК - ВИСОКА МОЖЛИВІСТЬ"
            recommendations = [
                "💎💎 АГРЕСИВНО КУПУВАТИ (30-40% капіталу)",
                "🎯 Історично сильний рівень підтримки",
                "✅ Ймовірне формування дна",
                "📈 Довгостроковий потенціал 100-200%",
                "⏰ Продовжувати DCA"
            ]
            
        else:  # price < 40000
            signal = "🟢🟢🟢 ЕКСТРЕМАЛЬНА МОЖЛИВІСТЬ"
            risk_level = "НИЗЬКИЙ РИЗИК - МАКСИМАЛЬНА МОЖЛИВІСТЬ"
            recommendations = [
                "💎💎💎 МАКСИМАЛЬНА ПОКУПКА (до 50% капіталу)",
                "🎯 Історичний шанс купівлі",
                "✅ Висока ймовірність дна",
                "📈 Потенціал 200-400%",
                "🚀 Довгостроковий HODLing"
            ]
        
        return signal, risk_level, recommendations
    
    def calculate_potential_profit(self, current_price: float) -> Dict:
        """Розраховує потенційний прибуток для різних сценаріїв"""
        scenarios = {
            'conservative': 75000,  # Повернення до попереднього рівня
            'moderate': 100000,     # Новий ATH
            'optimistic': 150000,   # Бичачий сценарій
            'extreme': 200000       # Екстремальний бичачий ринок
        }
        
        profits = {}
        for scenario, target_price in scenarios.items():
            profit_percent = ((target_price - current_price) / current_price) * 100
            profits[scenario] = {
                'target_price': target_price,
                'profit_percent': round(profit_percent, 2)
            }
        
        return profits
    
    def get_risk_indicators(self, data: Dict) -> Dict:
        """Аналізує індикатори ризику"""
        price = data['price']
        change_24h = data['change_24h']
        
        indicators = {
            'volatility': 'ВИСОКА' if abs(change_24h) > 5 else 'ПОМІРНА' if abs(change_24h) > 2 else 'НИЗЬКА',
            'trend': 'ВЕДМЕЖИЙ' if change_24h < -2 else 'БИЧАЧИЙ' if change_24h > 2 else 'БОКОВИЙ',
            'distance_from_burry_target': round(((price - self.critical_levels['burry_target']) / self.critical_levels['burry_target']) * 100, 2),
            'distance_from_capitulation': round(((price - self.critical_levels['capitulation']) / self.critical_levels['capitulation']) * 100, 2)
        }
        
        return indicators
    
    def print_detailed_analysis(self, data: Dict):
        """Виводить детальний аналіз"""
        if not data:
            return
        
        price = data['price']
        signal, risk_level, recommendations = self.analyze_opportunity(price)
        potential_profits = self.calculate_potential_profit(price)
        risk_indicators = self.get_risk_indicators(data)
        fear_greed = self.get_fear_greed_index()
        
        print("\n" + "="*80)
        print("📊 АНАЛІЗ БІТКОЇНА ЗА МЕТОДОЛОГІЄЮ МАЙКЛА Б'ЮРРІ")
        print("="*80)
        
        print(f"\n⏰ Час: {data['timestamp']}")
        print(f"\n💰 ПОТОЧНА ЦІНА: ${price:,.2f}")
        print(f"📈 Зміна за 24г: {data['change_24h']:.2f}%")
        print(f"📊 Обсяг за 24г: ${data['volume_24h']:,.0f}")
        print(f"🏦 Ринкова капіталізація: ${data['market_cap']:,.0f}")
        
        if fear_greed:
            print(f"\n🎭 Індекс страху/жадібності: {fear_greed['value']}/100 ({fear_greed['classification']})")
        
        print(f"\n{signal}")
        print(f"⚠️ Рівень ризику: {risk_level}")
        
        print("\n📍 КРИТИЧНІ РІВНІ ЦІНИ:")
        for level_name, level_price in self.critical_levels.items():
            distance = ((price - level_price) / level_price) * 100
            status = "✅" if price > level_price else "⬇️"
            print(f"  {status} {level_name.replace('_', ' ').title()}: ${level_price:,.0f} ({distance:+.2f}%)")
        
        print("\n🔍 ІНДИКАТОРИ РИЗИКУ:")
        print(f"  • Волатильність: {risk_indicators['volatility']}")
        print(f"  • Тренд: {risk_indicators['trend']}")
        print(f"  • Відстань до цілі Б'юррі ($55k): {risk_indicators['distance_from_burry_target']:+.2f}%")
        print(f"  • Відстань до капітуляції ($50k): {risk_indicators['distance_from_capitulation']:+.2f}%")
        
        print("\n💡 РЕКОМЕНДАЦІЇ:")
        for i, rec in enumerate(recommendations, 1):
            print(f"  {i}. {rec}")
        
        print("\n🎯 ПОТЕНЦІЙНИЙ ПРИБУТОК ПРИ ПОКУПЦІ:")
        for scenario, data in potential_profits.items():
            print(f"  • {scenario.upper()}: ${data['target_price']:,.0f} (+{data['profit_percent']:.2f}%)")
        
        print("\n💼 АЛЬТЕРНАТИВНІ ІНВЕСТИЦІЇ:")
        print("  🥇 Золото - РЕКОМЕНДОВАНО (захисний актив)")
        print("  🥈 Срібло - РЕКОМЕНДОВАНО (захисний актив)")
        print("  📉 Шорт MSTR - Розглянути (якщо BTC < $70k)")
        print("  📉 Шорт майнери - Розглянути (якщо BTC < $60k)")
        
        print("\n" + "="*80)
        print("⚠️ ВАЖЛИВО: Це не фінансова порада. Завжди проводьте власне дослідження!")
        print("="*80 + "\n")
    
    def monitor(self, interval: int = 300):
        """
        Постійний моніторинг ціни біткоїна
        
        Args:
            interval: Інтервал між запитами в секундах (за замовчуванням 5 хвилин)
        """
        print("🚀 Запуск моніторингу біткоїна...")
        print(f"⏰ Інтервал оновлення: {interval} секунд")
        print("⌨️  Натисніть Ctrl+C для зупинки\n")
        
        try:
            while True:
                data = self.get_btc_price()
                if data:
                    self.print_detailed_analysis(data)
                
                time.sleep(interval)
        except KeyboardInterrupt:
            print("\n\n👋 Моніторинг зупинено.")
    
    def single_check(self):
        """Одноразова перевірка ціни"""
        data = self.get_btc_price()
        if data:
            self.print_detailed_analysis(data)


def main():
    """Головна функція"""
    import sys
    
    tracker = BitcoinTracker()
    
    print("""
╔═══════════════════════════════════════════════════════════════════════════════╗
║                   BITCOIN TRACKER - BURRY ANALYSIS EDITION                    ║
║                   Моніторинг біткоїна на основі аналізу                      ║
║                      попередження Майкла Б'юррі                               ║
╚═══════════════════════════════════════════════════════════════════════════════╝
    """)
    
    if len(sys.argv) > 1 and sys.argv[1] == "--monitor":
        # Режим постійного моніторингу
        interval = int(sys.argv[2]) if len(sys.argv) > 2 else 300
        tracker.monitor(interval)
    else:
        # Одноразова перевірка
        tracker.single_check()
        
        print("\n💡 Підказка: Запустіть з прапором --monitor для постійного моніторингу:")
        print("   python bitcoin_tracker.py --monitor [інтервал_у_секундах]")
        print("   Приклад: python bitcoin_tracker.py --monitor 300")


if __name__ == "__main__":
    main()
