import click
import logging

from mwc.core.cfg import load_config

from .service import SubtitlesService

log = logging.getLogger(__name__)
CONFIG = load_config()


@click.command()
@click.argument('srt_folder', type=str, default=CONFIG['SRT_FOLDER'])
@click.argument('language', type=str, default=CONFIG['DEFAULT_LANGUAGE_ID'])
def download_missing_subtitles(srt_folder, language):
    """
    Downloads subtitles for movies in the local database that doesn't have one yet.
    """
    service = SubtitlesService(srt_folder=srt_folder, language=language)
    service.sync()
