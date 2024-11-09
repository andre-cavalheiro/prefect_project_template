import logging

from settings import config
from prefect.runner.storage import GitRepository
from prefect_github import GitHubCredentials
from prefect import flow

logger = logging.getLogger(config.app.SLUG)

if __name__ == "__main__":
    logger.info("Starting deployment script")

    # Set up Git repository source
    logger.info("Configuring Git repository source")
    branch = "main" if config.app.is_production else "develop"
    source = GitRepository(
        url=config.git.REPOSITORY_LINK,
        credentials=GitHubCredentials.load(config.blocks.GITHUB_CREDENTIALS),
        branch=branch,
    )
    logger.info(
        "Git repository configured: %s on branch %s", config.git.REPOSITORY_LINK, branch
    )

    # Load flow from source
    logger.info("Loading flow from source")
    try:
        flow = flow.from_source(
            source=source,
            entrypoint="src/main.py:main",
        )
        logger.info("Flow loaded successfully from source")
    except Exception as e:
        logger.error("Failed to load flow from source: %s", e)
        raise

    # Deploy the flow
    logger.info("Starting deployment of flow")
    try:
        flow.deploy(
            name=config.app.ENVIRONMENT,
            build=True,  # Build a new image for the flow
            push=True,  # Push the built image to a registry
            work_pool_name=config.prefect.WORK_POOL,
            cron=config.prefect.CRON_SCHEDULE,
            tags=["app:%s" % config.app.SLUG, "env:%s" % config.app.ENVIRONMENT],
            job_variables={"env": {"APP_ENVIRONMENT": "%s" % config.app.ENVIRONMENT}},
            parameters={},
        )
        logger.info("Deployment successful for environment: %s", config.app.ENVIRONMENT)
    except Exception as e:
        logger.error("Deployment failed: %s", e)
        raise
