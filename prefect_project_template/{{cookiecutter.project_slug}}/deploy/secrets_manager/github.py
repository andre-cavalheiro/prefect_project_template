from settings import config

from github import Github
from github import GithubException
import base64
import nacl.encoding
import nacl.public

from loguru import logger


def _upsert_github_secret(
    repo_name: str,
    secret_name: str,
    secret_value: str,
    token: str = config.git.ACCESS_TOKEN.get_secret_value(),
):
    """
    Upserts (inserts or updates) a GitHub secret in a repository.
    :param repo_name: Repository name in the format 'owner/repo'.
    :param secret_name: The name of the secret to create or update.
    :param secret_value: The value of the secret to store.
    :param token: GitHub personal access token with repo access.
    """
    github = Github(token)
    repo = github.get_repo(repo_name)

    # Retrieve the public key
    public_key = repo.get_actions_public_key()
    encrypted_value = _encrypt_secret(public_key.key, secret_value)

    # Upsert the secret
    try:
        repo.create_secret(secret_name, encrypted_value, public_key.key_id)
        logger.info(f"Secret '{secret_name}' upserted in {repo_name}.")
    except GithubException as e:
        logger.error(f"Error upserting secret: {e}")


def _encrypt_secret(public_key: str, secret_value: str) -> str:
    """Encrypt the secret value using the repository's public key."""
    public_key = nacl.public.PublicKey(
        base64.b64decode(public_key), nacl.encoding.RawEncoder
    )
    sealed_box = nacl.public.SealedBox(public_key)
    encrypted = sealed_box.encrypt(secret_value.encode("utf-8"))
    return base64.b64encode(encrypted).decode("utf-8")
