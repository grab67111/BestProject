from fastapi.templating import Jinja2Templates

from .config.lazy import settings

from .recognizers.yandex.adapter import YandexAdapter
from .recognizers.kaldi.adapter import KaldiAdapter
from .ws.connection import ConnectionManager


templates = Jinja2Templates(settings.BASE_DIR / 'templates')
SPEECHKITS = {
    'yandex': {
        'adapter': YandexAdapter(settings.YANDEX_API_KEY),
        'format': 'ogg'
    },
    'kaldi': {
        'adapter': KaldiAdapter(),
        'format': 'mp3'
    }
}
ws_manager = ConnectionManager()