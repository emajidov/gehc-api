import os
from datetime import datetime
import logging

CODING_SYTEM = os.getenv("CODING_SYSTEM", "http://loinc.org")


def process_units(unit, value):
    if unit == "cm":
        return unit.replace("cm", "m"), .01 * value
    if unit == "lb":
        return unit.replace("lb", "kg"), .45 * value
    if unit == "g/dl" or unit == "g/dL":
        return "kg/l", .001 * 10 * value

    if unit == "mg/dl" or unit == "mg/dL":
        return "kg/l", .001 * .001 * 10 * value
    else:
        return unit, value


def get_measurement(observation, entry=None):
    if not entry:
        entry = observation
    value = {}
    measurement_coding = []
    code = observation.get("code", {})
    codings = code.get("coding", [])
    for coding in codings:
        if CODING_SYTEM in coding.get("system", ""):
            measurement_coding.append(coding)

    value["observationId"] = entry.get("id")
    value["patientId"] = entry.get("subject", {}).get("reference", "/").split("/")[1]
    if entry.get("performer"):
        value["performerId"] = entry.get("performer")[0].get("reference", "/").split("/")[1]
    measurement = observation.get("valueQuantity", {})
    value["measurementCoding"] = measurement_coding
    value["measurementUnit"], value["measurementValue"] = process_units(measurement.get("unit", ""),
                                                                        measurement.get("value", ""))
    value["measurementDate"] = entry.get("issued", "")
    value["dateFetched"] = datetime.now().strftime("%Y-%m-%dT%H:%M:%SZ")
    return value


def map_input(entry):
    try:
        observation = entry.get("resource")
        # some observations could have two different measurements therefore we need to check component exist
        if "component" in observation:
            for sub_observation in observation.get("component", []):
                value = get_measurement(sub_observation, observation)
                return value
        else:
            value = get_measurement(observation)
            return value
    except Exception as e:
        logging.info("Error happened while processing the input entry")
        logging.debug(f"{e}")


def map_inputs(input_data):
    result = []
    try:
        for entry in input_data:
            value = map_input(entry)
            result.append(value)
    except Exception as e:
        logging.info("Error happened while processing the input entry")
        logging.debug(f"{e}")
    return result
