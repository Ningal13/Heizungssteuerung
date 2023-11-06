import requests

# API-Anfrage senden
url = "https://api.openweathermap.org/data/2.5/forecast"
params = {
    "q": "Krefeld",
    "appid": "e344fc9861dff7289176537e2060d323"
}

response = requests.get(url, params=params)

# JSON-Daten abrufen
data = response.json()

# Heutiges Datum im Format "YYYY-MM-DD"
heutiges_datum = data['list'][0]['dt_txt'][:10]

# Temperaturen für den heutigen Tag speichern
temperaturen = []

for eintrag in data['list']:
    datum_und_zeit = eintrag['dt_txt']
    temperatur_in_kelvin = eintrag['main']['temp']
    
    if datum_und_zeit.startswith(heutiges_datum):
        temperatur_in_celsius = temperatur_in_kelvin - 273.15
        temperaturen.append({
            'Uhrzeit': datum_und_zeit[11:],
            'Temperatur_in_Celsius': temperatur_in_celsius
        })

# Ergebnisse anzeigen
for eintrag in temperaturen:
    print(f"Uhrzeit: {eintrag['Uhrzeit']}, Temperatur (Celsius): {eintrag['Temperatur_in_Celsius']:.2f} °C")
