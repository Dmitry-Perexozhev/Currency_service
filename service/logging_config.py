import logging
import os

LOG_DIR = os.path.join(os.path.dirname(__file__), "logs")
os.makedirs(LOG_DIR, exist_ok=True)

def init_logger(debug: bool, logfile: str = "app.log"):
    root_logger = logging.getLogger()
    root_logger.setLevel(logging.DEBUG if debug else logging.INFO)

    # Удаляем старые обработчики
    for handler in root_logger.handlers[:]:
        root_logger.removeHandler(handler)

    formatter = logging.Formatter("%(asctime)s | %(levelname)s | %(name)s | %(message)s")

    file_handler = logging.FileHandler(logfile, mode="w")
    file_handler.setFormatter(formatter)
    root_logger.addHandler(file_handler)

    if debug:
        console_handler = logging.StreamHandler()
        console_handler.setFormatter(formatter)
        root_logger.addHandler(console_handler)

# _logger: logging.Logger | None = None
#
# def init_logger(debug: bool, log_file: str = "__main__.log"):
#     global _logger
#
#     _logger.setLevel(logging.DEBUG if debug else logging.INFO)
#
#     formatter = logging.Formatter("%(asctime)s | %(levelname)s | %(name)s | %(message)s")
#
#     file_handler = logging.FileHandler(os.path.join(LOG_DIR, log_file), mode="w")
#     file_handler.setFormatter(formatter)
#     _logger.addHandler(file_handler)
#
#     if debug:
#         console_handler = logging.StreamHandler()
#         console_handler.setFormatter(formatter)
#         _logger.addHandler(console_handler)
#
# def get_logger(name: str = "") -> logging.Logger:
#     if _logger is None:
#         raise RuntimeError("Logger not initialized. Call init_logger(debug) first.")
#     return logging.getLogger(name)  # <-- создаём логгер напрямую, без getChild




# def get_logger(name: str, log_file: str, debug: bool = False) -> logging.Logger:
#     logger = logging.getLogger(name)
#     logger.setLevel(logging.DEBUG if debug else logging.INFO)
#
#     # Чтобы избежать дублирования хендлеров при повторном вызове
#     if not logger.handlers:
#         # Файловый хендлер
#         file_handler = logging.FileHandler(os.path.join(LOG_DIR, log_file), mode='w')
#         file_handler.setLevel(logging.DEBUG)  # Всегда логируем всё в файл
#         file_handler.setFormatter(logging.Formatter(
#             "%(asctime)s | %(levelname)s | %(name)s | %(message)s"
#         ))
#         logger.addHandler(file_handler)
#
#         # Консольный хендлер, только если debug=True
#         if debug:
#             console_handler = logging.StreamHandler()
#             console_handler.setLevel(logging.DEBUG)
#             console_handler.setFormatter(logging.Formatter(
#                 "%(asctime)s | %(levelname)s | %(name)s | %(message)s"
#             ))
#             logger.addHandler(console_handler)
#
#     return logger