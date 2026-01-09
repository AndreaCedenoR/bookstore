import requests

def get_exchange_rate():
    """
    Consulta la tasa de cambio USD -> EUR (o la moneda local deseada).
    """
    url = "https://api.exchangerate-api.com/v4/latest/USD"
    try:
        response = requests.get(url, timeout=5)
        response.raise_for_status()
        data = response.json()
        # Retornamos la tasa para EUR como ejemplo de moneda local
        return data['rates'].get('EUR', 0.85)
    except Exception:
        # Si la API falla, usamos la tasa por defecto (0.85) según el requerimiento
        return 0.85