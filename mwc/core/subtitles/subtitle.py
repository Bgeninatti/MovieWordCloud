import re
import string

import srt

import attr


class SubtitleError(Exception):
    ...


@attr.s
class Subtitle:

    subtitle_id: int = attr.ib()
    language: str = attr.ib()
    content: str = attr.ib(converter=srt.make_legal_content)
    xmltag_regex = attr.ib(default=re.compile(r'(<[^>]+>)'))
    excluded_chars = attr.ib(default=string.punctuation + "¡¿1234567890\\\"")
    filename: str = attr.ib(init=False)

    def __attrs_post_init__(self):
        try:
            self.lines = list(srt.parse(self.content))
        except srt.SRTParseError:
            raise SubtitleError(
                f'Invalid subtitle: subtitle_id={self.subtitle_id} language={self.language}'
            )
        self.filename = self.build_filename(self.subtitle_id)

    @staticmethod
    def build_filename(subtitle_id):
        return f'{subtitle_id}.srt'

    def _tokenize_text(self, text):
        # Find and remove all xml tags <i>, <font>, etc
        tags = set(self.xmltag_regex.findall(text))
        for tag in tags:
            text = text.replace(tag, '')
        # Remove punctuation and other stuff
        excluded_chars = str.maketrans('', '', self.excluded_chars)
        words = text.translate(excluded_chars) \
            .strip() \
            .lower() \
            .replace('\n', ' ')
        # Remove duplicated spaces
        words = re.sub(' +', ' ', words)
        return words

    def get_words(self):
        lines = [line.content for line in self.lines]
        return self._tokenize_text(' '.join(lines))
