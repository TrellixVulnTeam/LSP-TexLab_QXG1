from .const import ARCH
from .const import PLATFORM
from .const import PLUGIN_NAME
from .const import PLATFORM_ARCH_TO_TARBALL
from .const import SERVER_VERSION
from .const import SETTINGS_FILENAME
from functools import lru_cache
from LSP.plugin.core.typing import Optional
import os
import sublime


@lru_cache()
def get_plugin_storage_dir() -> str:
    """Gets this plugin's storage dir."""

    return os.path.abspath(os.path.join(sublime.cache_path(), "..", "Package Storage", PLUGIN_NAME))


@lru_cache()
def get_server_download_url(version: str, platform: str, arch: str) -> Optional[str]:
    """
    Gets the LSP server download URL.

    :param      version:   The LSP server version
    :param      platform:  The platform ("osx", "linux" or "windows")
    :param      arch:      The arch ("x32", "x64" or "arm64")
    """

    settings = sublime.load_settings(SETTINGS_FILENAME)
    url = settings.get("lsp_server_download_url", "")  # type: str
    tarball = PLATFORM_ARCH_TO_TARBALL.get("{}_{}".format(platform, arch), "")

    if not (url and tarball):
        return None

    return url.format_map(
        {
            "version": version,
            "version_without_v": version.lstrip("v"),
            "tarball": tarball,
        }
    )


@lru_cache()
def get_server_dir() -> str:
    """Gets the server directory."""

    server_dir = "{}-{}~{}".format(PLATFORM, ARCH, SERVER_VERSION)

    return os.path.join(get_plugin_storage_dir(), server_dir)


@lru_cache()
def get_default_server_bin_path() -> str:
    """Gets the default LSP server binary path."""
    return os.path.join(
        get_server_dir(),
        "texlab.exe" if PLATFORM == "windows" else "texlab",
    )
