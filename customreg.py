#from pathlib import Path
#print('Running' if __name__ == '__main__' else 'Importing', Path(__file__).resolve())

from presidio_analyzer import AnalyzerEngine, Pattern, PatternRecognizer
from typing import Optional,List,Tuple
text = 'my passport is 1200101756875'

analyzer = AnalyzerEngine()


class Th_passport_recognizer(PatternRecognizer):
    PATTERNS =[Pattern("Passport (week)", 
                r"\b[a-zA-z]{2}\d{7}\b", 0.6)]
    CONTEXT = ['Passport','passport#','passport number']
    def __init__(
        self,
        patterns: Optional[List[Pattern]] = None,
        context: Optional[List[str]] = None,
        supported_language: str = "en",
        supported_entity: str = "TH_PASSPORT",
    ):
        patterns = patterns if patterns else self.PATTERNS
        context = context if context else self.CONTEXT
        super().__init__(
            supported_entity=supported_entity,
            patterns=patterns,
            context=context,
            supported_language=supported_language,
        )    

class Th_phone_recognizer(PatternRecognizer):
    PATTERNS = [
        Pattern(
            "Phone (strong)",
            r"\b[0-9]{3}([\/]|[\-]){1}[0-9]{3}[\-]{1}[0-9]{4}\b",
            0.9,
        ),
        Pattern("Phone (medium)", r"\b[0-9]{3}([\/]|[\-]){1}[0-9]{7}\b", 0.85),
        Pattern("Phone (weak)", r"\b[0]{1}[0-9]{8,9}\b", 0.05),
    ]

    CONTEXT = ["phone", "number", "telephone", "cell", "mobile", "call"]

    def __init__(
        self,
        patterns: Optional[List[Pattern]] = None,
        context: Optional[List[str]] = None,
        supported_language: str = "en",
        supported_entity: str = "TH_PHONE_NUMBER",
    ):
        patterns = patterns if patterns else self.PATTERNS
        context = context if context else self.CONTEXT
        super().__init__(
            supported_entity=supported_entity,
            patterns=patterns,
            context=context,
            supported_language=supported_language,
        )

class Th_ID_recognizer(PatternRecognizer):
    PATTERNS = [
        Pattern(
            "Citizen ID (strong)",
            r"\b[1-8]{1}[\-|\s]{1}([0-6]{1}\d{1}|[7]{1}[0-7]{1})\d{2}[\-|\s]{1}\d{5}[\-|\s]{1}\d{2}[\-|\s]{1}\d{1}\b",
            0.7
        ),
        Pattern(
            "Citizen ID (weak)",
            r"\b[1-8]{1}\d{12}\b",
            0.05
        )
    ]

    # pylint: disable=line-too-long,abstract-method
    CONTEXT = ["citizen id", "id number"]

    def __init__(
        self,
        patterns=None,
        context=None,
        supported_language="en",
        supported_entity="TH_ID",
        replacement_pairs=None,
    ):
        """
            :param replacement_pairs: list of tuples to replace in the string.
                ( default: [("-", ""), (" ", "")] )
                i.e. remove dashes and spaces from the string during recognition.
        """
        self.replacement_pairs = replacement_pairs if replacement_pairs else [
            ("-", ""), (" ", "")]
        context = context if context else self.CONTEXT
        patterns = patterns if patterns else self.PATTERNS
        super().__init__(
            supported_entity=supported_entity,
            patterns=patterns,
            context=context,
            supported_language=supported_language,
        )

    def validate_result(self, pattern_text):
        sanitized_value = self.__sanitize_value(
            pattern_text, self.replacement_pairs)
        checksum = self.__id_checksum(sanitized_value)
        return checksum

    @staticmethod
    def __id_checksum(sanitized_value):
        sums = 0

        def digits_of(n):
            # (โยน string แล้วหั่นทีละตัว return array ที่เป็น int)
            return [int(d) for d in str(n)]
        digits = digits_of(sanitized_value)  # (ได้เลข 13 ตัว)
        digit2 = digits[:12]  # (เอาแค่เลข 12 ตัวแรก)

        for d in range(12):
            sums += (digit2[d]) * (13-d)
        return (11 - sums % 11) % 10 == digits[12]

    @staticmethod
    def __sanitize_value(text, replacement_pairs):
        for search_string, replacement_string in replacement_pairs:
            text = text.replace(search_string, replacement_string)
        return text


#analyzer.registry.add_recognizer(Th_passport_recognizer())
#analyzer.registry.add_recognizer(Th_phone_recognizer())
#analyzer.registry.add_recognizer(Th_ID_recognizer())

#analyzer_results = analyzer.analyze(text=text, entities=['TH_PASSPORT','TH_PHONE_NUMBER','TH_ID'], language='en')

#print(analyzer_results)