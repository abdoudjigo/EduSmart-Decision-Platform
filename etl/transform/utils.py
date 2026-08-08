import re
import pandas as pd


def clean_text(value):
    """
    Supprime les espaces inutiles.
    Retourne None si la valeur est vide.
    """
    if pd.isna(value):
        return None

    value = str(value).strip()

    if value == "":
        return None

    return value


def format_name(value):
    """
    Met en forme un nom ou prénom.
    Exemple :
    abdoulaye   -> Abdoulaye
    JEAN DUPONT -> Jean Dupont
    """
    value = clean_text(value)

    if value is None:
        return None

    return value.title()


def is_valid_email(email):
    """
    Vérifie qu'une adresse email est valide.
    """
    email = clean_text(email)

    if email is None:
        return False

    pattern = r"^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$"

    return re.match(pattern, email) is not None


def remove_duplicates(df):
    """
    Supprime les doublons.
    """
    return df.drop_duplicates()


def normalize_gender(value):
    """
    Uniformise le sexe.
    """
    value = clean_text(value)
    if value is None:
        return None
    value = value.upper()
    if value in ["M", "MALE", "HOMME", "GARÇON", "GARCON", "1"]:
        return "M"
    if value in ["F", "FEMALE", "FEMME", "FILLE", "0"]:
        return "F"
    return None


def is_future_date(date_value):
    """
    Vérifie si une date est dans le futur.
    """
    try:

        date = pd.to_datetime(date_value)

        return date > pd.Timestamp.today()

    except Exception:

        return True

def remove_missing_values(df):
    """
    Supprime les lignes contenant au moins une valeur manquante.
    """
    return df.dropna()


def count_missing_values(df):
    """
    Compte le nombre total de valeurs manquantes.
    """
    return df.isna().sum().sum()