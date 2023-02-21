from strawberry.utils import files_utils
from strawberry.consts import FormatConsts
import sys
import re


class TemplateParser:
    def __init__(self):
        pass

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
            var_string = f"{FormatConsts.TEMPLATE_VAR_START}{context_var}{FormatConsts.TEMPLATE_VAR_END}"
            template = template.replace(var_string, context[context_var])

        return template

    def merge_with_parent_template(self, template):
        first_row = template.split("\n")[0].strip()

        if first_row.startswith(FormatConsts.BASE_TEMPLATE_DEFINE):
            base_template_path = first_row.split()[-1]
            base_template_content = files_utils.get_file_content(base_template_path)

            if base_template_content:
                template = template.replace(f"{FormatConsts.BASE_TEMPLATE_DEFINE} {base_template_path}", "")

                base_template_sections_slots = self.get_sections_slots_from_template(base_template_content)
                template_sections = self.get_sections_from_template(template)

                template = self.process_sections(template,
                                                 base_template_content,
                                                 template_sections,
                                                 base_template_sections_slots)

        return template

    def process_sections(self, template, base_template, template_sections, sections_slots_names):
        splitted_template = template.split("\n")

        for template_section_name in template_sections:
            template_section = template_sections.get(template_section_name)

            if template_section_name in sections_slots_names:
                base_section_slot_name = f"{FormatConsts.TEMPLATE_SECTION_SLOT} {template_section_name}"
                templ_between = splitted_template[template_section["start"]: template_section["end"] + 1]

                base_template = re.sub(f"{base_section_slot_name}\n", "\n".join(templ_between), base_template)

                sections_slots_names.remove(template_section_name)

        base_template = self.clear_section_slots(base_template, sections_slots_names)

        return base_template

    def get_sections_from_template(self, template):
        sections = {}
        section_name = None
        section_start = None

        for row_id, row in enumerate(template.split("\n")):
            stripped_row = row.strip()

            if stripped_row.startswith(FormatConsts.TEMPLATE_SECTION_START):
                section_name = stripped_row.split()[-1]
                section_start = row_id + 1

            if stripped_row == f"{FormatConsts.TEMPLATE_SECTION_END} {section_name}":
                section_end = row_id - 1

                if section_name and section_start:
                    sections[section_name] = {
                        "start": section_start,
                        "end": section_end,
                    }

        return sections

    def get_sections_slots_from_template(self, template):
        sections_slots = []

        for row_id, row in enumerate(template.split("\n")):
            stripped_row = row.strip()

            if stripped_row.startswith(FormatConsts.TEMPLATE_SECTION_START):
                sections_slots.append(stripped_row.split()[-1])

        return sections_slots

    def clear_section_slots(self, template, slots_names):
        for name in slots_names:
            template = template.replace(f"{FormatConsts.TEMPLATE_SECTION_SLOT} {name}", "")

        return template
