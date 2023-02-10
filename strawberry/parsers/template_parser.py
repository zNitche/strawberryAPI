from strawberry.utils import files_utils
import sys


class TemplateParser:
    def __init__(self):
        self.base_template_define_start = "#BASE"

        self.var_start = "{{"
        self.var_end = "}}"

        self.template_section_start = "#SECTION"
        self.template_section_end = "#END"

    def parse_template(self, template_content, context):
        try:
            template_content = self.merge_with_parent_template(template_content)
            template_content = self.parse_variables(template_content, context)

        except Exception as e:
            print(f"Exception during parsing template")
            sys.print_exception(e)

        return template_content

    def parse_variables(self, template, context):
        for context_var in context:
            var_string = f"{self.var_start}{context_var}{self.var_end}"
            template = template.replace(var_string, context[context_var])

        return template

    def merge_with_parent_template(self, template):
        first_row = template.split("\n")[0].strip()

        if first_row.startswith(self.base_template_define_start):
            base_template_path = first_row.split()[-1]
            base_template_content = files_utils.get_file_content(base_template_path)

            if base_template_content:
                template = template.replace(f"{self.base_template_define_start} {base_template_path}", "")

                base_template_sections = self.get_sections_from_template(base_template_content)
                template_sections = self.get_sections_from_template(template)

                template = self.process_sections(template,
                                                 base_template_content,
                                                 template_sections,
                                                 base_template_sections)

        return template

    def process_sections(self, template, base_template, template_sections, base_sections):
        splitted_base_template = base_template.split("\n")
        splitted_template = template.split("\n")

        for template_section_name in template_sections:
            template_section = template_sections.get(template_section_name)
            base_section = base_sections.get(template_section_name)

            if base_section:
                templ_between = splitted_template[template_section["start"]: template_section["end"]]

                splitted_base_template = splitted_base_template[:(base_section["start"] - 1)] + \
                                         templ_between + \
                                         splitted_base_template[(base_section["end"] + 2):]

        return "\n".join(splitted_base_template)

    def get_sections_from_template(self, template):
        sections = {}
        section_name = None
        section_start = None

        for row_id, row in enumerate(template.split("\n")):
            stripped_row = row.strip()

            if stripped_row.startswith(self.template_section_start):
                section_name = stripped_row.split()[-1]
                section_start = row_id + 1

            if stripped_row == f"{self.template_section_end} {section_name}":
                section_end = row_id - 1

                if section_name and section_start:
                    sections[section_name] = {
                        "start": section_start,
                        "end": section_end,
                    }

        return sections
