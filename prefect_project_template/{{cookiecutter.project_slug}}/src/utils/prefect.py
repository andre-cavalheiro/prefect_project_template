from prefect import get_run_logger
from settings import config


def configure_loguru() -> None:
    """
    Source: https://discourse.prefect.io/t/can-i-use-loguru-logs-in-prefect-flows/140

    Redirect loguru logging messages to the prefect run logger.
    This function should be called from within a Prefect task or flow before calling any module that uses loguru.
    This function can be safely called multiple times.

    Example Usage:
    from prefect import flow
    from loguru import logger
    from prefect_utils import configure_loguru # import this function in your flow from your module
    @flow()
    def myflow():
        logger.info("This is hidden from the Prefect UI")
        configure_loguru()
        logger.info("This shows up in the Prefect UI")
    """
    # import here for distributed execution because loguru cannot be pickled.
    from loguru import logger  # pylint: disable=import-outside-toplevel

    run_logger = get_run_logger()
    logger.remove()
    logger.add(
        run_logger.debug,
        filter=lambda record: record["level"].name == "DEBUG",
        level="TRACE",
        format=config.logging.FORMAT,
    )
    logger.add(
        run_logger.warning,
        filter=lambda record: record["level"].name == "WARNING",
        level="TRACE",
        format=config.logging.FORMAT,
    )
    logger.add(
        run_logger.error,
        filter=lambda record: record["level"].name == "ERROR",
        level="TRACE",
        format=config.logging.FORMAT,
    )
    logger.add(
        run_logger.critical,
        filter=lambda record: record["level"].name == "CRITICAL",
        level="TRACE",
        format=config.logging.FORMAT,
    )
    logger.add(
        run_logger.info,
        filter=lambda record: record["level"].name
        not in ["DEBUG", "WARNING", "ERROR", "CRITICAL"],
        level="TRACE",
        format=config.logging.FORMAT,
    )
