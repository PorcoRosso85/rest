import logging

import pytest

# ロガーを作成します。
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

# ログレベルとプレフィックスのマッピングを定義します。
log_levels = {
    logging.DEBUG: "[DEBUG]",
    logging.INFO: "[INFO]",
    logging.WARNING: "[WARNING]",
    logging.ERROR: "[ERROR]",
    logging.CRITICAL: "[CRITICAL]",
}


class LevelFilter(logging.Filter):
    def __init__(self, level):
        self.level = level

    def filter(self, record):
        return record.levelno == self.level


# 各ログレベルに対してハンドラを作成し、ログメッセージのフォーマットを設定します。
for log_level, prefix in log_levels.items():
    handler = logging.StreamHandler()
    formatter = logging.Formatter(
        f"\n {prefix} %(message)s"
    )  # プレフィックスを設定します。
    handler.setFormatter(formatter)
    handler.setLevel(log_level)
    handler.addFilter(LevelFilter(log_level))  # フィルターを追加します。
    logger.addHandler(handler)


class TestLogger:
    def test_正常系_ロガーを使用する場合(self):
        """ロガーを使用する場合"""
        logger.debug("デバッグメッセージ")
        logger.info("情報メッセージ")
        logger.warning("警告メッセージ")
        logger.error("エラーメッセージ")
        logger.critical("致命的なエラーメッセージ")


class ExceptionProcessor:
    """このクラスは例外を処理するためのクラスです。
    例外が発生した際
    - ログに例外を出力します。
    - 例外が返却されます。
    -
    このクラスを使用することでログを出力しつつ、返却された例外を処理することができます。
    """

    def __init__(self, logger: logging.Logger) -> None:
        self.logger = logger

    def process(self, e: Exception) -> Exception:
        """例外を処理します。
        Args:
            e (Exception): 例外
        Returns:
            Exception: 例外
        """
        self.logger.exception(e)
        return e


class TestExceptionProcessor:
    @pytest.fixture
    def exception_processor(self):
        return ExceptionProcessor(logger)

    def test_正常系_例外を処理する場合(self, exception_processor):
        """例外を処理する場合"""
        e = Exception("エラーが発生しました。")
        with pytest.raises(Exception):
            raise exception_processor.process(e)
