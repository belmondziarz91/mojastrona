import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime, timedelta

# Definicja akcji i ich ilości
portfolio = {
    "XTB.WA": 14,
    "DNP.WA": 1,
    "ZABKA.WA": 15,
    "MBR.WA": 1,
    "PKN.WA": 10,
    "KTY.WA": 1,
    "CPS.WA": 25,
    "DGN.WA": 6,
    "ASEE.WA": 8,
    "ALE.WA": 10,
    "APR.WA": 20,
    "KRU.WA": 1,
    "ELT.WA": 10
}

start_date = (datetime.today() - timedelta(days=365)).strftime('%Y-%m-%d')
end_date = datetime.today().strftime('%Y-%m-%d')

# Pobranie danych dla S&P 500
sp500 = yf.download("^GSPC", start=start_date, end=end_date)
print(f"Dostępne kolumny dla S&P 500: {sp500.columns}")

# Wybór odpowiednich kolumn z MultiIndex
if ("Adj Close", "^GSPC") in sp500.columns:
    sp500 = sp500[("Adj Close", "^GSPC")]
elif ("Close", "^GSPC") in sp500.columns:
    sp500 = sp500[("Close", "^GSPC")]
else:
    raise ValueError("Brak dostępnych danych zamknięcia dla S&P 500")

portfolio_data = {}

for ticker, shares in portfolio.items():
    data = yf.download(ticker, start=start_date, end=end_date)
    print(f"Dostępne kolumny dla {ticker}: {data.columns}")

    if ("Adj Close", ticker) in data.columns:
        portfolio_data[ticker] = data[("Adj Close", ticker)]
    elif ("Close", ticker) in data.columns:
        portfolio_data[ticker] = data[("Close", ticker)]
    else:
        print(f"Brak danych 'Close' dla {ticker}, pomijam.")

# Sprawdzenie, czy portfolio_data zawiera jakiekolwiek dane
if not portfolio_data:
    print("Brak dostępnych danych dla portfela. Skrypt zakończony.")
    exit()

# Tworzenie DataFrame z dostępnymi danymi
portfolio_df = pd.DataFrame(portfolio_data)

# Usunięcie brakujących wartości i ponowne sprawdzenie, czy dane istnieją
portfolio_df.dropna(how='all', inplace=True)
if portfolio_df.empty:
    print("Brak ważnych danych do analizy portfela. Skrypt zakończony.")
    exit()

# Obliczenie wartości portfela w czasie
portfolio_value = (portfolio_df * pd.Series({k: v for k, v in portfolio.items() if k in portfolio_df.columns})).sum(axis=1)
initial_value = portfolio_value.iloc[0]
portfolio_return = (portfolio_value / initial_value - 1) * 100

# Obliczenie zwrotu S&P 500
sp500_return = (sp500 / sp500.iloc[0] - 1) * 100

# Wykres
plt.figure(figsize=(12, 6))
plt.plot(portfolio_return, label="Zwrot Portfela")
plt.plot(sp500_return, label="Zwrot S&P 500", linestyle="dashed")
plt.xlabel("Data")
plt.ylabel("Zwrot (%)")
plt.title("Porównanie zwrotu portfela inwestycyjnego i S&P 500")
plt.legend()
plt.grid()
plt.show()
