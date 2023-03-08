import datetime
import requests
import io
import csv

# Define the base URL for the CSV file download
base_url = "https://ptax.bcb.gov.br/ptax_internet/consultaBoletim.do"

# Define the start and end dates for the period you want to download
today = datetime.date.today()
yesterday = today - datetime.timedelta(days=1)

data_ini = yesterday.strftime("%d/%m/%Y")
data_fim = today.strftime("%d/%m/%Y")

# Define the URL parameters for the CSV file download
url_params = {
    "method": "gerarCSVFechamentoMoedaNoPeriodo",
    "ChkMoeda": "61",
    "DATAINI": data_ini,
    "DATAFIM": data_fim,
}

# Build the full URL for the CSV file download
url = base_url + "?" + "&".join(f"{k}={v}" for k, v in url_params.items())

# Make a GET request to download the CSV file
response = requests.get(url)

# Parse the CSV file content
content = response.content.decode('utf-8')
csv_data = list(csv.reader(io.StringIO(content), delimiter=';'))

# Extract the exchange rate for today and yesterday
today_rate = float(csv_data[-1][4].replace(',', '.'))
yesterday_rate = float(csv_data[-2][4].replace(',', '.'))

# Calculate and print the exchange rate ratio
exchange_rate_ratio = today_rate / yesterday_rate
if(exchange_rate_ratio == 0.97):
    print("Tanto faz o cartão\n")
elif(exchange_rate_ratio > 0.97):
    print("Vai com o BTG\n")
else:
    print("Melhor usar o Nu\n")
print(f"BTG: {yesterday_rate*1.061:.2f}\nNubank: {today_rate*1.0938:.2f}")
