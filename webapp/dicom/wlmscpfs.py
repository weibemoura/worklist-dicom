import os
from struct import pack

from decouple import config

# https://www.dicomlibrary.com/dicom/dicom-tags/
# https://support.dcmtk.org/docs/wlmscpfs.html


def __calculate_space_list(values):
    size = 8
    for value in values:
        size += len(value) + 8

        if len(value) % 2 != 0:
            size += 1

    return size


def __write_code(file, code):
    for base in code.split(","):
        file.write(pack("H", int(base, 16)))


def __write_datatype(file, datatype):
    if datatype:
        file.write(datatype.encode())


def __write_property(file, code, datatype, content):
    __write_code(file, code)
    __write_datatype(file, datatype)

    if isinstance(content, str):
        if len(content) % 2 != 0 and datatype != "UI":
            content += " "

        content = content.encode()
        file.write(pack("I", len(content))[:2])
        file.write(content)
    else:
        file.write(pack("I", content))


def __write_sequence(file, code, datatype, values=[]):
    __write_code(file, code)
    __write_datatype(file, datatype)

    size = __calculate_space_list(values)

    file.write(bytes([0, 0]))
    file.write(pack("I", size))

    __write_code(file, "FFFE,E000")
    file.write(pack("I", size - 8))


def clear_file_wl():
    dir_worklist = config("WORKLIST_DIR")
    for item in os.listdir(dir_worklist):
        if item.endswith(".wl"):
            os.remove(os.path.join(dir_worklist, item))


def write_file_wl(worklists):
    header = open(config("HEADER_FILE"), "rb").read(360)

    dir_worklist = config("WORKLIST_DIR")
    for worklist in worklists:
        file_worklist = os.path.join(dir_worklist, f"{worklist.patient_id}.wl")
        with open(file_worklist, "wb") as f:
            f.write(header)

            __write_property(f, "0008,0005", "CS", "ISO_IR 192")

            __write_property(f, "0008,0020", "DA", worklist.study_date)
            __write_property(f, "0008,0030", "TM", worklist.study_time)
            __write_property(f, "0008,0050", "SH", worklist.accession_number)
            __write_property(f, "0008,0080", "LO", worklist.institution_name)
            __write_property(f, "0008,0081", "ST", worklist.institution_address)

            __write_property(f, "0010,0010", "PN", worklist.patient_name)
            __write_property(f, "0010,0020", "LO", worklist.patient_id)
            __write_property(f, "0010,0030", "DA", worklist.patient_birthdate)
            __write_property(f, "0010,0040", "CS", worklist.patient_sex)
            __write_property(f, "0010,1020", "DS", worklist.patient_size)
            __write_property(f, "0010,1030", "DS", worklist.patient_weight)
            __write_property(f, "0010,1040", "ST", worklist.patient_address)
            __write_property(f, "0010,2000", "LO", worklist.medical_alerts)
            __write_property(f, "0010,2110", "LO", worklist.contrast_allergies)
            __write_property(f, "0020,000d", "UI", worklist.study_instance_uid)
            __write_property(f, "0032,1032", "PN", worklist.requesting_physician)
            __write_property(
                f, "0032,1060", "LO", worklist.requested_procedure_description
            )

            values = [
                worklist.modality,
                worklist.requested_contrast_agent,
                worklist.scheduled_station_aetitle,
                worklist.scheduled_procedure_step_startdate,
                worklist.scheduled_procedure_step_starttime,
                worklist.scheduled_procedure_step_enddate,
                worklist.scheduled_procedure_step_endtime,
                worklist.scheduled_performing_physician_name,
                worklist.scheduled_procedure_step_description,
                worklist.scheduled_procedure_step_id,
                worklist.scheduled_station_name,
                worklist.scheduled_procedure_step_location,
                worklist.pre_medication,
                worklist.scheduled_procedure_step_status,
            ]
            __write_sequence(f, "0040,0100", "SQ", values=values)
            __write_property(f, "0008,0060", "CS", worklist.modality)
            __write_property(f, "0032,1070", "LO", worklist.requested_contrast_agent)
            __write_property(f, "0040,0001", "AE", worklist.scheduled_station_aetitle)
            __write_property(
                f, "0040,0002", "DA", worklist.scheduled_procedure_step_startdate
            )
            __write_property(
                f, "0040,0003", "TM", worklist.scheduled_procedure_step_starttime
            )
            __write_property(
                f, "0040,0004", "DA", worklist.scheduled_procedure_step_enddate
            )
            __write_property(
                f, "0040,0005", "TM", worklist.scheduled_procedure_step_endtime
            )
            __write_property(
                f, "0040,0006", "PN", worklist.scheduled_performing_physician_name
            )
            __write_property(
                f, "0040,0007", "LO", worklist.scheduled_procedure_step_description
            )
            __write_property(f, "0040,0009", "SH", worklist.scheduled_procedure_step_id)
            __write_property(f, "0040,0010", "SH", worklist.scheduled_station_name)
            __write_property(
                f, "0040,0011", "SH", worklist.scheduled_procedure_step_location
            )
            __write_property(f, "0040,0012", "LO", worklist.pre_medication)
            __write_property(
                f, "0040,0020", "CS", worklist.scheduled_procedure_step_status
            )

            __write_property(f, "0040,1001", "SH", "5000")
