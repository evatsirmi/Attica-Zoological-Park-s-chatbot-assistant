# My Project

This chatbot is designed for visitors of the Attica Zoological Park in Greece.

The motivation behind this choice is that visitors typically need practical, real-time information before and during their visit, such as transportation, weather conditions, and activity schedules and ticket prices. This is particularly crucial for this park, since it is located in the outer suburbs of Athens where weather and transportation information might be challlenging to acquire.
Therefore, the goal is to improve the visitor experience by providing instant, accurate, and context-aware information, all in a single chatbot.

## About
The chatbot implements the following core scenarios:

    1.Bus Arrival Information (OASA Live Data)

Users can ask:

“Πότε έρχεται το λεωφορείο;"

The chatbot:

Connects to the OASA Telematics API

Retrieves live arrival data for bus stop 440119,which is the closest to the park

Converts route codes into meaningful route descriptions

Displays how many minutes remain until each bus arrives

It also includes some general information about the bus route that could help the user

This demonstrates the chatbot’s ability to use real-time external data, while it also gives meaningful feedback to the user when there is not avaliable information for some reason.

    2.Weather at Attica Park

Users can ask:

“What is the weather like at Attica Park now?”

The chatbot:

Connects to the OpenWeather API

Uses the park’s geographic coordinates, as given in its website

Returns:

Weather description

Temperature

And gives meaningful advise to the potential visitors based on the weather conditions:

For instance:
If it is raining → advises against visiting

It also provides the user useful feedback when data is not avaliable for some reason.

    3.Animal Schedule (Simulated Task Execution)

Users can ask questions as:

“Πότε είναι οι ελέφαντες;”

These responses come from a mock database inside ActionAnimalSchedule, not from an external API.

This fulfills the Simulated Task Execution requirement:

The chatbot behaves as if it has access to a real animal schedule system, allowing testing of logic and conversation flow before real data sources are available.

    4.Ticket Price Information (NLU-based Static Knowledge)

The chatbot provides detailed ticket pricing for Attica Zoological Park using intent-based Natural Language Understanding (NLU).

Instead of using an external API or database, ticket prices are implemented as structured static knowledge inside the NLU and domain configuration, as described in the park's website.
This is appropriate because ticket prices are stable, publicly available, do not change in real time.

Users can ask questions as:

“Πόσο κάνουν τα εισιτήρια;”

The chatbot uses multiple specialized intents to distinguish what the user is asking for, since there are many ticket types available.

## Data sources

| Feature          | Data Source                | Purpose                                  |
| ---------------- | ---------------------      | ---------------------------------------- |
| Bus arrivals     | OASA Telematics API        | Provides real-time public transport data |
| Weather          | OpenWeather API            | Provides live weather information        |
| Animal schedules | Simulated (Mock data)      | Provides info found in the park's website|   |
| Ticket prices    | NLU-based Static Knowledge | Provides info found in the park's website|

## Challenges and solutions

    1. Bus stop without live data

One stop (440218) did not return live bus information because it belongs to a circular route.
Solution: The chatbot uses stop 440119, in which passenger can both get and leave the park since it's a circular route and it has live data .

    2. Route codes instead of names

The OASA API returns numeric route_code values instead of route names.
Solution: The webRoutesForStop endpoint is used to map route codes to real route descriptions.

    3. Weather API authentication

The OpenWeather API requires an API key and activation time.
Solution: Environment variables were used and the key was tested after activation.

    4. YAML formatting errors

Long Greek texts caused syntax errors in domain.yml.
Solution: Proper quoting and validation with YAML checkers.

## Environment

The OpenWeather API key must be stored as an environment variable.

Linux / Mac:

export OPENWEATHER_API_KEY="YOUR_API_KEY"


Windows:

setx OPENWEATHER_API_KEY "YOUR_API_KEY"


Run the bot:

rasa run actions

## Example Runs

    1. Bus Information

User:

Πότε έρχεται το λεωφορείο;

Bot:


Έχε υπόψη σου ότι το δρομολόγιο εκτελείται από τις 7:45 π.μ. έως τις 20:40 μ.μ.
Η κυκλική διαδρομή μπορεί να σε φέρει στο Αττικό πάρκο από Δουκ. Πλακεντίας ή να σε πάρει από το πάρκο και να σε επιστρέψει εκεί.
Επόμενα λεωφορεία κοντά στο Αττικό Ζωολογικό Πάρκο:
    - Γραμμή ΣΤ. ΔΟΥΚ. ΠΛΑΚΕΝΤΙΑΣ - ΠΑΛΛΗΝΗ - ΕΚΠΤ. ΧΩΡΙΟ ΣΠΑΤΑ (ΚΥΚΛΙΚΗ): σε 5 λεπτά

    
    2. Weather

User: 

Τι καιρό έχει τώρα;

Bot:

Weather at Attica Zoological Park:

Καιρός στο Αττικό Ζωολογικό Πάρκο:
- Συνθήκες: ελαφρές νεφώσεις
- Θερμοκρασία: 12.76°C
Ο καιρός φαίνεται κατάλληλος για επίσκεψη.


        3. Animal Schedule


User:

 Πρόγραμμα για πιγκουίνους;

Bot:

Αφρικανικοί Πιγκουίνοι: 14:00

    4. Tickets:

User:  Πόσο κάνουν τα εισιτήρια;

Τα εισιτήρια για εσάς είναι:
Γενική είσοδος: 25€
Παιδιά 3-12 ετών: 19€
Κάτω των 3 ετών: Δωρεάν



