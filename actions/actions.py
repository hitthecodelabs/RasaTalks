# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/custom-actions

from typing import Any, Text, Dict, List

from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.events import SlotSet, SessionStarted, ActionExecuted, EventType
import requests

class AccionClima(Action):
    def name(self):
        return "action_clima"
    
    def run(self, dispatcher, tracker, domain):
        city = tracker.get_slot("ciudad")

        APIKEY = "57ed2d85181443d5aa1222521242102"
        APIURL = f'http://api.weatherapi.com/v1/current.json?key={APIKEY}&q={city.capitalize()}&aqi=no'

        response = requests.get(APIURL)

        if not response:
            message = "Algo salió mal. Intente más tarde."
            dispatcher.utter_message(text=message)
            return []

        data = response.json()
        # print(data)

        data_actual = data['current']
        temperatura = data_actual['temp_c'] ### grandos centigrados

        location = data['location']
        city = location['name']
        region = location['region']
        country = location['country']
        datetime_str = location['localtime']
        clima_actual = data_actual['condition']['text']
        icono_clima = "https:" + data_actual['condition']['icon']

        info = f"""Ciudad: {city} | Provincia: {region} | Pais: {country} | Hora: {datetime_str} | Temperatura Actual: {temperatura}ºC | Condición Actual: {clima_actual}"""

        # response = f"It's currently {weather}, {temp}'C in {place}."
        dispatcher.utter_message(text=info)
        # dispatcher.utter_message(text="test")
        
        # Enviar la imagen del ícono del clima
        # dispatcher.utter_message(image=icono_clima)

        return [SlotSet('ciudad', city)]

