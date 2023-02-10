class ParserBase:
    @staticmethod
    def parse(template):
        return template


class VariablesParser:
    @staticmethod
    def parse(template, context):
        var_start = "{{"
        var_end = "}}"

        for context_var in context:
            var_string = f"{var_start}{context_var}{var_end}"
            template = template.replace(var_string, context[context_var])

        return template
