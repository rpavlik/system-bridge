"""System Bridge: Server Handler - TTS"""
from plyer import tts
from sanic.request import Request
from sanic.response import HTTPResponse, json


def tts_say(message: str):
    """Say a message"""
    tts.speak(message)


async def handler_tts(
    request: Request,
) -> HTTPResponse:
    """Send a TTS message."""
    if "message" not in request.json:
        return json(
            {
                "message": "No message provided",
            },
            status=400,
        )

    tts_say(request.json["message"])

    return json(
        {
            "message": "Keypress sent",
            "key": request.json["key"],
        }
    )
