import logging

# ロガーを作成します。
logger = logging.getLogger(__name__)

# ログレベルとプレフィックスのマッピングを定義します。
log_levels = {
    logging.DEBUG: "[DEBUG]",
    logging.INFO: "[INFO]",
    logging.WARNING: "[WARNING]",
    logging.ERROR: "[ERROR]",
    logging.CRITICAL: "[CRITICAL]",
}

# 各ログレベルに対してハンドラを作成し、ログメッセージのフォーマットを設定します。
for log_level, prefix in log_levels.items():
    handler = logging.StreamHandler()
    formatter = logging.Formatter(
        f"\n {prefix} %(message)s"
    )  # プレフィックスを設定します。
    handler.setFormatter(formatter)
    handler.setLevel(log_level)
    logger.addHandler(handler)

# ログレベルを設定します。
logger.setLevel(logging.DEBUG)


# def test_logger(caplog):
#     # ロガーを設定します。
#     logger = logging.getLogger("app.utils")
#     logger.setLevel(logging.DEBUG)

#     # ハンドラを設定します。
#     handler = logging.StreamHandler()
#     formatter = logging.Formatter("[%(levelname)s] %(message)s")
#     handler.setFormatter(formatter)
#     logger.addHandler(handler)

#     # ログを出力します。
#     logger.debug("This is a debug message.")
#     assert "[DEBUG] This is a debug message" in caplog.text

#     logger.info("This is an info message.")
#     assert "[INFO] This is an info message" in caplog.text

#     logger.warning("This is a warning message.")
#     assert "[WARNING] This is a warning message" in caplog.text

#     logger.error("This is an error message.")
#     assert "[ERROR] This is an error message" in caplog.text

#     logger.critical("This is a critical message.")
#     assert "[CRITICAL] This is a critical message" in caplog.textt
