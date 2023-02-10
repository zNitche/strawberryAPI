from strawberry.parsers.workers import template_parsers as parsers
import sys


class TemplateParser:
    def __init__(self):
        self.parsers = [
            parsers.VariablesParser
        ]

    def parse_template(self, template_content, context):
        for parser in self.parsers:
            try:
                template_content = parser.parse(template_content, context)
            except Exception as e:
                print(f"Exception during parsing template using {parser.__name__}")
                sys.print_exception(e)

        return template_content
