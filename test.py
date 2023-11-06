import numpy as np
import tensorflow as tf
import requests


# Beispieldaten zum Lernen (Außentemp/Vorlauf)  (noch einen zweiten graden ausdenken, für raum temp und anhand dessen 3satz)
train_data = np.array([[20,21,0.25], [10,21,0.4375], [0,21,0.5874], [-10,21,0.7125], [-20,21,0.85], [-30,21,1],
                       [20,23,0.15], [10,23,0.33], [0,23,0.47], [-10,23,0.61], [-20,23,0.75], [-30,23,0.9],
                       [20,25,0.05], [10,25,0.23], [0,25,0.37], [-10,25,0.51], [-20,25,0.65], [-30,25,0.8]], dtype=float)  #zum zurückrechnen /0,8 /100
# train_data = np.array([[20,20], [10,35], [0,50], [-10,65], [-20,80], [-30,95]], dtype=float)

# Eingang und Ausgang festlegen
x_train = train_data[:, :2]  # Außentemperatur
y_train = train_data[:, 2]   # Kesseltemp

# Benutzerdefinierte Initialisierungsfunktion (gewichtung zufälig zwischen -1 und 1)
def custom_initializer(shape, dtype=None):
    return tf.constant_initializer(minval = -1, maxval = 1)(shape, dtype)

# Modell erstellen
model = tf.keras.Sequential([
    tf.keras.layers.Dense(units=80, input_shape=[2], activation='relu'),
    tf.keras.layers.Dense(units=80, activation='relu'),
    tf.keras.layers.Dense(units=1, activation='sigmoid')
])

# Modell kompilieren
model.compile(optimizer='adam', loss='binary_crossentropy', metrics=['accuracy'])

# Modell trainieren
model.fit(x_train, y_train, epochs=700)

temperature_celsius = 12
raumTemp = 21

rechnung = np.array([[temperature_celsius,raumTemp]], dtype=float)
ergebnis = model.predict(rechnung)
print("wertergebnis =")
print(ergebnis)

#gehen davon aus, das 80 grad kessel 100% ist
ergebnis = ergebnis * 100  # Mit 100 multiplizieren
ergebnis = ergebnis * 0.8  # Mit 0,8 multiplizieren

print("Ergebnis nach den Berechnungen:", ergebnis)


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


# strg + shift + p