import json
import os
import numpy as np


def convert_numpy_types(obj):
    """
    Convertit les types numpy/pandas
    vers des types compatibles JSON
    """

    if isinstance(obj, np.integer):
        return int(obj)

    if isinstance(obj, np.floating):
        return float(obj)

    if isinstance(obj, np.ndarray):
        return obj.tolist()

    return obj


def save_quality_report(source, table, stats):

    report = {
        "source": source,
        "table": table,
        "quality": stats
    }

    # Conversion des types numpy
    report = json.loads(
        json.dumps(
            report,
            default=convert_numpy_types
        )
    )

    os.makedirs(
        "etl/logs/quality_reports",
        exist_ok=True
    )

    path = f"etl/logs/quality_reports/{source}_{table}_quality.json"

    with open(path, "w", encoding="utf-8") as file:
        json.dump(
            report,
            file,
            indent=4,
            ensure_ascii=False
        )

    print(f"Rapport qualité généré : {path}")