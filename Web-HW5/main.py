import aiohttp
import asyncio
import sys
from datetime import datetime, timedelta

async def fetch_exchange_rates(date):
    url = f"https://api.privatbank.ua/p24api/exchange_rates?json&date={date}"
    async with aiohttp.ClientSession(connector=aiohttp.TCPConnector(ssl=False)) as session:
        async with session.get(url) as response:
            data = await response.json()
            rates = {rate['currency']: {'sale': rate['saleRateNB'], 'purchase': rate['purchaseRateNB']} for rate in data['exchangeRate'] if rate.get('currency') in ['EUR', 'USD']}
            return {date: rates}

async def get_currency_rates(days):
    tasks = []
    dates = []

    # Отримання дат за останні `days` днів
    for i in range(1, days + 1):
        date = (datetime.now() - timedelta(days=i)).strftime('%d.%m.%Y')
        dates.append(date)

    # Виклик асинхронних запитів для отримання курсів валют для кожної дати
    for date in dates:
        tasks.append(fetch_exchange_rates(date))

    return await asyncio.gather(*tasks)

async def main(days):
    currency_rates = await get_currency_rates(days)
    return currency_rates

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python main.py <days>")
        sys.exit(1)

    try:
        days = int(sys.argv[1])
        if days > 10:
            print("Error: You can only query exchange rates for up to 10 days.")
            sys.exit(1)
    except ValueError:
        print("Error: Invalid number of days.")
        sys.exit(1)

    result = asyncio.run(main(days))
    print(result)
