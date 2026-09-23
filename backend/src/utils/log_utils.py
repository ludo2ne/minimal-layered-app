import logging
from functools import wraps

from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(name)-25s %(levelname)-7s - %(message)s",
    datefmt="%d/%m/%Y %H:%M:%S",
)


def initialize_logs(name: str):
    """Initialise un logger simple pour l'application"""
    logging.info("-" * 50)
    logging.info(f"Starting {name}")
    logging.info("-" * 50)


def get_logger(module_name: str, max_size: int = 25):
    """Retourne un logger avec un nom raccourci"""
    if len(module_name) <= max_size:
        return logging.getLogger(module_name)

    parts = module_name.split(".")
    short_prefix = [p[0] for p in parts[:-1]]
    short_name = ".".join(short_prefix + [parts[-1]])
    return logging.getLogger(short_name)


class LogIndentation:
    """Gère l'indentation des logs"""

    current_indentation = 0
    indentation_size = 2

    @classmethod
    def increase_indentation(cls):
        cls.current_indentation += 1

    @classmethod
    def decrease_indentation(cls):
        cls.current_indentation -= 1

    @classmethod
    def get_indentation(cls):
        return " " * cls.indentation_size * cls.current_indentation


def log(func):
    """Décorateur pour logger les entrées/sorties des méthodes"""
    SENSITIVE_KEYWORDS = {"password", "passwd", "pwd", "pass", "token", "secret", "key"}

    @wraps(func)
    def wrapper(*args, **kwargs):
        if args and hasattr(args[0], "__class__"):
            logger = get_logger(f"{args[0].__class__.__module__}")
        else:
            logger = logging.getLogger(__name__)

        LogIndentation.increase_indentation()
        indentation = LogIndentation.get_indentation()

        method_name = func.__name__
        param_names = func.__code__.co_varnames[1 : func.__code__.co_argcount]
        args_list = []

        # Traitement des args
        for i, arg in enumerate(args[1:]):
            if i >= len(param_names):
                break
            param_name = param_names[i].lower()
            args_list.append(
                "*****" if any(k in param_name for k in SENSITIVE_KEYWORDS) else str(arg)
            )

        # Traitement des kwargs
        for k, v in kwargs.items():
            args_list.append(
                "*****" if any(k2 in k.lower() for k2 in SENSITIVE_KEYWORDS) else str(v)
            )

        args_tuple = tuple(args_list)
        logger.info(f"{indentation}{method_name}{args_tuple} - START")

        result = func(*args, **kwargs)

        logger.info(f"{indentation}{method_name}{args_tuple} - END")

        # Formatage de la sortie
        if isinstance(result, (list, dict)):
            result_str = f"{type(result).__name__}({len(result)} items)"
        elif isinstance(result, str) and len(result) > 50:
            result_str = result[:50] + "..."
        else:
            result_str = str(result)

        logger.info(f"{indentation}  └─> Output: {result_str}")
        LogIndentation.decrease_indentation()
        return result

    return wrapper


class LogMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        method = request.method
        path = str(request.url.path)
        logging.info(f"{method} {path} - START")
        try:
            response = await call_next(request)
            logging.info(f"{method} {path} - END [Status: {response.status_code}]")
            return response
        except Exception as e:
            logging.error(f"{method} {path} - FAILED [Status: 500] Error: {str(e)}")
            raise e
