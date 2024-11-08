import asyncio
from prefect import flow, tags
from core.utils import get_contributors, get_repo_info
from utils.prefect import configure_loguru
from settings import config
from loguru import logger


@flow(name=config.app.SLUG, log_prints=False)
async def main(repo_owner: str = "PrefectHQ", repo_name: str = "prefect"):
    """
    Given a GitHub repository, logs the number of stargazers
    and contributors for that repo.
    """
    configure_loguru()

    repo_info = await get_repo_info(repo_owner, repo_name)
    logger.info(f"Stars 🌠 : {repo_info['stargazers_count']}")

    contributors = await get_contributors(repo_info)
    logger.info(f"Number of contributors 👷: {len(contributors)}")


if __name__ == "__main__":
    with tags(f"app:{config.app.SLUG}", f"env:{config.app.ENVIRONMENT}"):
        asyncio.run(main())
