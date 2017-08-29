
"""

A utility to fetch details from the txt format of the resume

"""
import re
import pickle
import logging
from datetime import date
import configurations as regex

import dirpath

logging.basicConfig(level=logging.DEBUG)

"""

Utility function that fetches emails in the resume.
Params: resume_text type: string
returns: list of emails

"""
def fetch_email(resume_text):
  try:
    regular_expression = re.compile(regex.email, re.IGNORECASE)
    emails = []
    result = re.search(regular_expression, resume_text)
    while result:
      emails.append(result.group())
      resume_text = resume_text[result.end():]
      result = re.search(regular_expression, resume_text)
    return emails
  except Exception as exception_instance:
    logging.error('Issue parsing email: ' + str(exception_instance))
    return []


"""

Utility function that fetches phone number in the resume.
Params: resume_text type: string
returns: phone number type:string

"""
def fetch_phone(resume_text):
  try:
    regular_expression = re.compile(regex.get_phone(3, 3, 10), re.IGNORECASE)
    result = re.search(regular_expression, resume_text)
    phone = ''
    if result:
      result = result.group()
      for part in result:
        if part:
          phone += part
    if phone is '':
      for i in range(1, 10):
        for j in range(1, 10-i):
          regular_expression =re.compile(regex.get_phone(i, j, 10), re.IGNORECASE)
          result = re.search(regular_expression, resume_text)
          if result:
            result = result.groups()
            for part in result:
              if part:
                phone += part
          if phone is not '':
            return phone
    return phone
  except Exception as exception_instance:
    logging.error('Issue parsing phone number: ' + resume_text +
      str(exception_instance))
    return None



"""

Utility Function that calculates experience in the resume text
params: resume_text type:string
returns: experience type:int

"""
def calculate_experience(resume_text):
  #
  def get_month_index(month):
    month_dict = {'jan':1, 'feb':2, 'mar':3, 'apr':4, 'may':5, 'jun':6, 'jul':7, 'aug':8, 'sep':9, 'oct':10, 'nov':11, 'dec':12}
    return month_dict[month.lower()]

  try:
    experience = 0
    start_month = -1
    start_year = -1
    end_month = -1
    end_year = -1
    regular_expression = re.compile(regex.date_range, re.IGNORECASE)
    regex_result = re.search(regular_expression, resume_text)
    while regex_result:
      date_range = regex_result.group()
      year_regex = re.compile(regex.year)
      year_result = re.search(year_regex, date_range)
      if (start_year == -1) or (int(year_result.group()) <= start_year):
        start_year = int(year_result.group())
        month_regex = re.compile(regex.months_short, re.IGNORECASE)
        month_result = re.search(month_regex, date_range)
        if month_result:
          current_month = get_month_index(month_result.group())
          if (start_month == -1) or (current_month < start_month):
            start_month = current_month
      if date_range.lower().find('present') != -1:
        end_month = date.today().month # current month
        end_year = date.today().year # current year
      else:
        year_result = re.search(year_regex, date_range[year_result.end():])
        if (end_year == -1) or (int(year_result.group()) >= end_year):
          end_year = int(year_result.group())
          month_regex = re.compile(regex.months_short, re.IGNORECASE)
          month_result = re.search(month_regex, date_range)
          if month_result:
            current_month = get_month_index(month_result.group())
            if (end_month == -1) or (current_month > end_month):
              end_month = current_month
      resume_text = resume_text[regex_result.end():]
      regex_result = re.search(regular_expression, resume_text)

    return end_year - start_year  # Use the obtained month attribute
  except Exception as exception_instance:
    logging.error('Issue calculating experience: '+str(exception_instance))
    return None


"""

Utility function that fetches Job Position from the resume.
Params: cleaned_resume Type: string
returns: job_positions Type:List

"""
def fetch_roles(cleaned_resume):
  positions_path = dirpath.PKGPATH + '/data/job_positions/positions'
  with open(positions_path, 'rb') as fp:
    jobs = pickle.load(fp)

  job_positions = []
  positions = []
  for job in jobs.keys():
    job_regex = r'[^a-zA-Z]'+job+r'[^a-zA-Z]'
    regular_expression = re.compile(job_regex, re.IGNORECASE)
    regex_result = re.search(regular_expression, cleaned_resume)
    if regex_result:
      positions.append(regex_result.start())
      job_positions.append(job.capitalize())
  job_positions = [job for (pos, job) in sorted(zip(positions, job_positions))]

  # For finding the most frequent job category
  hash_jobs = {}
  for job in job_positions:
    if jobs[job.lower()] in hash_jobs.keys():
      hash_jobs[jobs[job.lower()]] += 1
    else:
      hash_jobs[jobs[job.lower()]] = 1

  # To avoid the "Other" category and 'Student' category from
  # becoming the most frequent one.
  if 'Student' in hash_jobs.keys():
    hash_jobs['Student'] = 0
  hash_jobs['Other'] = -1

  return (job_positions, max(hash_jobs, key=hash_jobs.get).capitalize())


"""

Utility function that fetches degree and degree-info from the resume.
Params: resume_text Type: string
returns:
degree Type: List of strings
info Type: List of strings

"""
def fetch_qualifications(resume_text):
  degree_path = dirpath.PKGPATH + '/data/qualifications/degree'
  with open(degree_path, 'rb') as fp:
    qualifications = pickle.load(fp)

  degree = []
  for qualification in qualifications:
    qual_regex = r'[^a-zA-Z]'+qualification+r'[^a-zA-Z]'
    regular_expression = re.compile(qual_regex, re.IGNORECASE)
    regex_result = re.search(regular_expression, resume_text)
    while regex_result:
      degree.append(qualification)
      resume_text = resume_text[regex_result.end():]
      regex_result = re.search(regular_expression, resume_text)
  all_qualifications = [deg for (deg, qual) in sorted(zip(degree, qualifications))]

  # For finding the highest Qualification
  hash_degree = {}
  for deg in all_qualifications:
    if qualifications[deg.lower()] in hash_degree.keys():
      hash_degree[qualifications[g=deg.lower()]] += 1
    else:
      hash_degree[qualifications[deg.lower()]] = 1
  return (all_qualifications, max(hash_degree, key=hash_degree.get).capitalize())

"""

Utility function that fetches the skills from resume
Params: cleaned_resume Type: string
returns: skill_set Type: List

"""
def fetch_skills(cleaned_resume):
  with open(dirpath.PKGPATH + '/data/skills/skills', 'rb') as fp:
    skills = pickle.load(fp)

  skill_set = []
  for skill in skills:
    skill = ' '+skill+' '
    if skill.lower() in cleaned_resume:
      skill_set.append(skill)
  return skill_set


"""

Utility function that fetches extra information from the resume.
Params: resume_text Type: string
returns: extra_information Type: List of strings

"""
def fetch_extra(resume_text):
  with open(dirpath.PKGPATH + '/data/extra/extra', 'rb') as fp:
    extra = pickle.load(fp)

  extra_information = []
  for info in extra:
    extra_regex = r'[^a-zA-Z]'+info+r'[^a-zA-Z]'
    regular_expression = re.compile(extra_regex, re.IGNORECASE)
    regex_result = re.search(regular_expression, resume_text)
    while regex_result:
      extra_information.append(info)
      resume_text = resume_text[regex_result.end():]
      regex_result = re.search(regular_expression, resume_text)
  return extra_information
