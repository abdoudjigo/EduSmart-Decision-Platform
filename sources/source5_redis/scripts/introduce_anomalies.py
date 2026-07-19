import json
import random
import copy


INPUT_FILE = "/home/abdoulaye/Documents/Orange Digital center/BI/EduSmart_Decision_Platform/sources/source5_redis/data/redis_data.json"
OUTPUT_FILE = "/home/abdoulaye/Documents/Orange Digital center/BI/EduSmart_Decision_Platform/sources/source5_redis/data_anomalies/redis_data_anomalies.json"


def introduce_anomalies(data):
    anomalies = {}
    for key, value in data.items():
        doc = copy.deepcopy(value)
        chance = random.random()

        # valeurs manquantes
        if chance < 0.10:
            doc.pop(
                random.choice(
                    list(doc.keys())
                ),
                None
            )

        # valeurs nulles
        if chance < 0.20:
            champ = random.choice(
                list(doc.keys())
            )

            doc[champ] = None

        # appareil incohérent
        if "device" in doc and chance < 0.30:
            doc["device"] = random.choice(
                [
                    "Mobile",
                    "mobile",
                    "Téléphone",
                    "PHONE"
                ]
            )


        # statut incorrect
        if "status" in doc and chance < 0.40:
            doc["status"] = random.choice(
                [
                    "ONLINE",
                    "offline",
                    "unknown"
                ]
            )

        anomalies[key] = doc
    return anomalies


if __name__ == "__main__":
    with open(INPUT_FILE, "r",encoding="utf-8") as file:
        data = json.load(file)
    data_anomalies = introduce_anomalies(data)

    with open(OUTPUT_FILE, "w", encoding="utf-8") as file:
        json.dump(
            data_anomalies,
            file,
            indent=4,
            ensure_ascii=False
        )
    print(len(data_anomalies),"clés Redis avec anomalies générées")