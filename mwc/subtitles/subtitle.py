from pathlib import Path

import srt,logging

from mwc.cfg import load_config

log = logging.getLogger(__name__)
CONFIG = load_config()


class Subtitle:

    def __init__(self, subtitle_id, language, srt_file):
        self.subtitle_id = subtitle_id
        self.srt_location = Path(CONFIG['SRT_FOLDER']) / f"{self.subtitle_id}.srt"
        self.language = language
        self.file = srt_file

    def get_lines(self):
        lines = srt.parse(srt.make_legal_content(self.file.read()))
        self.file.seek(0)
        return lines

    def is_valid(self):
        try:
            self.get_lines()
            return True
        except srt.SRTParseError as error:
            if "Sorry, maximum download count for IP" in str(error):
                log.error("Error: reason='API limit reached'")
                return False
            logger.error("Error: reason='%s'", error)
            return False

    def save_srt_file(self):
        with open(self.srt_location, "w") as srtf:
            srtf.write(self.file.read())

    @classmethod
    def get_from_movie(cls, movie):
        subtitle_id = movie.srt_file.split('/')[-1].replace('.srt', '')
        return cls(subtitle_id, movie.language_id, open(movie.srt_file))
