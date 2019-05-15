import random as _random
import time as _time
from datetime import datetime as _datetime, timedelta as _timedelta

import names as _names

from dicom.worklist import Worklist as _Worklist


def year_to_days(year):
    return year * 365


def generate_worklist(count=10):
    list_sex = ["male", "female"]
    list_modality = [
        ["MR", "CT Left Shoulder"],
        ["CT", "CT Brain"],
        ["MR", "MRI Left Shoulder"],
        ["RF", "Left Leg DSA"],
        ["CT", "MRI Left Shoulder"],
        ["US", "US Left Shoulder"],
        ["RF", "Right Leg DSA"],
        ["NM", "CEqual 1 Day"],
        ["CR", "CR Brain"],
    ]

    timestamp = int(_time.time())
    birthdate = _datetime.utcnow() - _timedelta(days=year_to_days(55))

    worklists = []
    for x in range(count):
        worklist = _Worklist()
        worklist.create_sample()

        timestamp += 1
        sex = _random.choice(list_sex)

        date = _datetime.utcnow()
        date += _timedelta(seconds=_random.randint(10, 300))

        worklist.study_date = date.strftime("%Y%m%d")
        worklist.study_time = date.strftime("%H%M%S")
        # worklist.accession_number = str(timestamp)
        worklist.accession_number = f"000{timestamp}"

        worklist.patient_id = f"{timestamp}"
        worklist.patient_name = _names.get_full_name(gender=sex).replace(" ", "^")
        worklist.patient_sex = sex[0].upper()
        worklist.patient_size = str(_random.randint(120, 200) / 100)
        worklist.patient_weight = str(_random.randint(65, 115))
        worklist.patient_birthdate = (birthdate + _timedelta(days=year_to_days(_random.randint(5, 25)))).strftime(
            "%Y%m%d"
        )
        worklist.patient_address = "patient@patient.com"

        modality = _random.choice(list_modality)
        worklist.modality = modality[0]
        worklist.requesting_physician = "Dr(a) " + _names.get_full_name()
        worklist.requested_procedure_description = modality[1]
        worklist.study_instance_uid = f"1.2.276.0.{timestamp}.3.2.101"

        date += _timedelta(minutes=_random.randint(10, 300))
        worklist.scheduled_procedure_step_startdate = date.strftime("%Y%m%d")
        worklist.scheduled_procedure_step_starttime = date.strftime("%H%M%S")
        date += _timedelta(minutes=_random.randint(10, 300))
        worklist.scheduled_procedure_step_enddate = date.strftime("%Y%m%d")
        worklist.scheduled_procedure_step_endtime = date.strftime("%H%M%S")

        worklists.append(worklist)

    return worklists
