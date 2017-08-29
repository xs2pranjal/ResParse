"""

Main program

"""

import converter
import annotations_parser
import details_parser as dp
import language_parser as lp
import pandas as pd

import dirpath
import configurations

class ResParse():
    def __init__(self, name, path = dirpath.RESUMEPATH):
        self.path = path + '/' + name

        if self.exists():
            self.extract()
        else:
            raise OSError("There is no file found at " + self.path)

    def exists(self):
        return configurations.isfile(self.path)

    # Extracts raw text from resume
    # Supports Doc, PDF, Docx
    def extract(self):
        if self.path.find(".pdf"|".doc"|".docx") != -1:
            self.raw_text = converter.document_to_txt(self.path)

        if self.raw_text is not '':
            self.parse()
        else:
            raise ValueError("Error extracting resume text.")

    def parse(self):
        self.URLs = annotations_parser.fetch_pdf_urls(self.path)
        self.name = lp.fetch_name(self.raw_text)
        self.emails = dp.fetch_email(self.raw_text)
        self.phone_numbers = dp.fetch_phone(self.raw_text)
        self.experience = dp.calculate_experience(self.raw_text)
        self.cleaned_resume = lp.clean_resume(self.raw_text)
        self.skills = dp.fetch_skills(self.cleaned_resume)
        (self.qualifications,self.degree_info) = dp.fetch_qualifications(
            self.raw_text)
        self.job_roles, self.category = dp.fetch_roles(self.cleaned_resume)
        self.current_employers,self.employers = lp.fetch_employers(
            self.raw_text,self.job_positions)
        self.extra_info = dp.fetch_extra(self.raw_text)
        out= pd.DataFrame({
            "name" : self.name,
            "experience" : self.experience,
            "address" : self.address,
            "phone_numbers" : self.phone_numbers,
            "emails" : self.emails,
            "urls" : self.URLs,
            "skills" : self.skills,
            "jobs" : self.job_positions,
            "job category" : self.category,
            "employers" : self.employers,
            "current_employers" : self.current_employers,
            "qualifications" : self.qualifications,
            "extra_info" : self.extra_info})
        out.to_csv("Parsed_Resume.csv", index = False)


    # TODO: Add more fetch here
    def show(self):
        return {
            "name" : self.name,
            "experience" : self.experience,
            "phone_numbers" : self.phone_numbers,
            "emails" : self.emails,
            "urls" : self.URLs,
            "skills" : self.skills,
            "jobs" : self.job_positions,
            "job category" : self.category,
            "employers" : self.employers,
            "current_employers" : self.current_employers,
            "qualifications" : self.qualifications,
            "extra_info" : self.extra_info
        }
 