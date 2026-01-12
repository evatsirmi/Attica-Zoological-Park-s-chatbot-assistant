# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/custom-actions


# This is a simple example for a custom action which utters "Hello World!"

from typing import Any, Text, Dict, List
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
import os
import requests



ATTICA_PARK_STOP_CODES = ["440119"]  #το id της στάσης

class ActionOasaArrivals(Action):

    def name(self) -> Text:
        return "action_oasa_arrivals"

    def run(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any]
    ) -> List[Dict[Text, Any]]:

        # dictionary route_code -> line_descr
        route_to_line = {}

        #  περιγραφές γραμμών για κάθε στάση
        for stop_id in ATTICA_PARK_STOP_CODES:
            try:
                url_lines = f"http://telematics.oasa.gr/api/?act=webRoutesForStop&p1={stop_id}"
                resp_lines = requests.get(url_lines, timeout=5)
                resp_lines.raise_for_status()
                data_lines = resp_lines.json()
                for item in data_lines:
                    route_to_line[item.get("RouteCode")] = item.get("LineDescr", "Άγνωστη γραμμή")
            except Exception as e:
                dispatcher.utter_message(
                    text=f"Πρόβλημα κατά την ανάκτηση των γραμμών για stop {stop_id}."
                )

        all_buses = []

        #  live arrivals
        for stop_id in ATTICA_PARK_STOP_CODES:
            try:
                url = f"http://telematics.oasa.gr/api/?act=getStopArrivals&p1={stop_id}"
                resp = requests.get(url, timeout=5)
                resp.raise_for_status()
                data = resp.json()
                if data:
                    all_buses.extend(data)
            except requests.exceptions.Timeout:
                dispatcher.utter_message(
                    text=f"Η σύνδεση με το σύστημα συγκοινωνιών καθυστέρησε για stop {stop_id}."
                )
            except requests.exceptions.RequestException:
                dispatcher.utter_message(
                    text=f"Παρουσιάστηκε πρόβλημα επικοινωνίας με το σύστημα συγκοινωνιών για stop {stop_id}."
                )

        if not all_buses:
            dispatcher.utter_message(
                text="Δεν βρέθηκαν διαθέσιμες πληροφορίες για τα λεωφορεία αυτή τη στιγμή."
            )
            return []

        # μήνυμα για τον χρήστη
        message = "Επόμενα λεωφορεία κοντά στο Αττικό Ζωολογικό Πάρκο:\n"

        # Εμφανίζουμε max 5 συνολικά
        for bus in all_buses[:5]:
            route_code = bus.get("route_code")
            line_descr = route_to_line.get(route_code, "Άγνωστη γραμμή")
            minutes = bus.get("btime2", "?")
            message += f"- Γραμμή {line_descr}: σε {minutes} λεπτά\n"

        dispatcher.utter_message(text=message)

        return []
    



class ActionWeather(Action):

    def name(self) -> Text:
        return "action_weather"

    def run(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any]
    ) -> List[Dict[Text, Any]]:

        #i found the coordinates in the park's website
        lat = 37.9890184
        lon = 23.910875

        API_KEY = os.getenv("OPENWEATHER_API_KEY")

        url = (
            f"https://api.openweathermap.org/data/2.5/weather"
            f"?lat={lat}&lon={lon}&units=metric&lang=el&appid={API_KEY}"
        )

        try:
            response = requests.get(url, timeout=5)
            response.raise_for_status()
            data = response.json()

            description = data["weather"][0]["description"]
            temperature = data["main"]["temp"]

            message = (
                f"Καιρός στο Αττικό Ζωολογικό Πάρκο:\n"
                f"- Συνθήκες: {description}\n"
                f"- Θερμοκρασία: {temperature}°C\n"
            )

          
            desc = description.lower()

            if "βροχή" in desc:
                message += "\n Βρέχει — καλύτερα να έρθεις στο Αττικό πάρκο μία άλλη μέρα."
            elif temperature > 28:
                message += "\n Πολλή ζέστη — πάρε μαζί σου καπέλο και αντιηλιακό!."
            elif temperature < 10:
                message += "\n Πολύ κρύο — ντύσου ζεστά."
            else:
                message += "\n Ο καιρός φαίνεται κατάλληλος για επίσκεψη."

            dispatcher.utter_message(text=message)

        except requests.exceptions.RequestException:
            dispatcher.utter_message(
                text= "Λυπάμαι, δεν μπόρεσα να λάβω πληροφορίες αυτή τη στιγμή. Προσπάθησε ξανά αργότερα"
            )

        return []
    




class ActionAnimalSchedule(Action):

    def name(self) -> Text:
        return "action_animal_schedule"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        # Map intents to responses
        schedules = {
            "ask_bird_show": " Πτήση Πτηνών: 11:30, 14:00",
            "ask_elephants": " Ελέφαντες: 12:30 (μόνο Σάββατο & Κυριακή)",
            "ask_lemurs": " Λεμούριοι: 12:45, 16:00",
            "ask_chimps": " Χιμπατζήδες: 13:45",
            "ask_penguins": " Αφρικανικοί Πιγκουίνοι: 14:00",
            "ask_dolphins": " Χώρος Δελφινιών: 11:00–12:30, 13:00–14:30, 15:00–16:30"
        }

        # Get the last intent detected
        intent = tracker.latest_message['intent'].get('name')
        response = schedules.get(intent, "Δεν έχω πληροφορίες για αυτό το ζώο.")

        dispatcher.utter_message(text=response)
        return []
