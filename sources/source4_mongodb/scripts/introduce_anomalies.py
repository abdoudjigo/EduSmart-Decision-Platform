import json
import random
import copy


INPUT_FILE = "/home/abdoulaye/Documents/Orange Digital center/BI/EduSmart_Decision_Platform/sources/source4_mongodb/json/events.json"
OUTPUT_FILE = "/home/abdoulaye/Documents/Orange Digital center/BI/EduSmart_Decision_Platform/sources/source4_mongodb/json_anomalies/events_anomalies.json"

def introduce_anomalies(events):
    anomalies = []
    for event in events:
        doc = copy.deepcopy(event)
        chance = random.random()
        # ==========================================
        # 1 - Champs manquants
        if chance < 0.10:
            champ = random.choice([
                "student_code",
                "device",
                "app_version",
                "city"
            ])

            doc.pop(champ, None)
        # ==========================================
        # 2 - Valeurs nulles
        if chance < 0.15:
            champ = random.choice([
                "city",
                "country",
                "ip_address"
            ])

            doc[champ] = None
        # ==========================================
        # 3 - Ville mal standardisée
        if chance < 0.20:
            doc["city"] = random.choice([
                "Dakar",
                "DAKAR",
                "dakar",
                "dakarr"
            ])
        # ==========================================
        # 4 - Version application incohérente
        if chance < 0.25:

            doc["app_version"] = random.choice([
                "2.4",
                "2.4.0",
                "v2.4",
                "version2.4"
            ])
        # ==========================================
        # 5 - Système exploitation incohérent
        if chance < 0.30:
            doc["operating_system"] = random.choice([
                "Android",
                "ANDROID",
                "android",
                "IOS"
            ])
        # ==========================================
        # 6 - Adresse IP invalide
        if chance < 0.35:
            doc["ip_address"] = random.choice([
                "999.999.1.1",
                "192.abc.10",
                "invalid_ip"
            ])
        # ==========================================
        # 7 - Durée négative
        if chance < 0.40:
            doc["duration_seconds"] = random.randint(-500,-1)
        anomalies.append(doc)

    # Ajouter quelques doublons
    doublons = random.sample(
        anomalies,
        500
    )
    anomalies.extend(doublons)

    return anomalies


if __name__ == "__main__":
    with open(INPUT_FILE, "r", encoding="utf-8") as file:
        events = json.load(file)

    events_anomalies = introduce_anomalies(events)

    with open(OUTPUT_FILE, "w", encoding="utf-8") as file:
        json.dump(
            events_anomalies,
            file,
            ensure_ascii=False,
            indent=4,
            default=str
        )

    print(len(events_anomalies), "événements avec anomalies générés")