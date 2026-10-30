"""Reglas de evaluación e integración con Google Gemini."""

import os
from dotenv import load_dotenv
from google import genai

load_dotenv()

SALARIO_ANUAL_MINIMO = 300_000


def evaluar_solicitud(edad: int, salario_mensual: float) -> dict:
    salario_anual = salario_mensual * 12
    cumple_edad = edad >= 18
    cumple_salario = salario_anual >= SALARIO_ANUAL_MINIMO

    if cumple_edad and cumple_salario:
        return {
            "califica": True,
            "motivo": (
                f"Cumple los criterios bancarios: edad mínima de 18 años "
                f"y salario anual de RD${salario_anual:,.2f}."
            )
        }

    motivos = []

    if not cumple_edad:
        motivos.append("No cumple la edad mínima de 18 años.")

    if not cumple_salario:
        motivos.append(
            f"El salario anual es RD${salario_anual:,.2f}; "
            f"el mínimo requerido es RD${SALARIO_ANUAL_MINIMO:,.2f}."
        )

    return {
        "califica": False,
        "motivo": " ".join(motivos)
    }


def generar_explicacion_ia(solicitud) -> str:
    api_key = os.getenv("GEMINI_API_KEY")

    if not api_key:
        raise RuntimeError(
            "Falta GEMINI_API_KEY. Configura tu clave en el archivo .env."
        )

    cliente = genai.Client(api_key=api_key)

    instrucciones = (
        "Eres un asistente educativo de Banco Talendig. "
        "Explica en lenguaje claro si la solicitud cumple los criterios "
        "de edad mínima de 18 años y salario anual mínimo de RD$300,000. "
        "Recomienda orientativamente una cuenta de ahorro o corriente "
        "según el perfil del solicitante. "
        "No inventes tasas, comisiones ni beneficios. "
        "Aclara que el análisis es educativo y no representa una "
        "aprobación bancaria ni una decisión financiera real."
    )

    mensaje = (
        f"{instrucciones}\n\n"
        f"Datos de la solicitud:\n"
        f"Nombre ficticio: {solicitud.nombre}\n"
        f"Edad: {solicitud.edad}\n"
        f"Salario mensual: RD${solicitud.salario_mensual:,.2f}\n"
        f"Tipo de cuenta: {solicitud.tipo_cuenta}\n"
        f"Resultado de evaluación: "
        f"{'Cumple' if solicitud.califica else 'No cumple'}\n"
        f"Motivo: {solicitud.motivo_evaluacion}\n\n"
        "Genera una explicación breve y una recomendación orientativa."
    )

    respuesta = cliente.models.generate_content(
        model=os.getenv("GEMINI_MODEL", "gemini-2.5-flash"),
        contents=mensaje
    )

    texto = respuesta.text

    return texto.strip() if texto else "La IA no devolvió una explicación."