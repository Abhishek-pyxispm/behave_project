import json

from behave import given, when, then
import requests

import utilities.rw_csv as csv
from utilities.resources import ApiResources
from utilities.log import custom_logger as log

log = log()
log.info("\n\n")


@given(u'I set base REST API url and headers correctly')
def setup_baseurl(context):
    try:
        context.baseURL = context.config.userdata.get("base_url", "url")
        context.headers = {"token": context.config.userdata.get("access_token", "token"),
                           "content-type": "application/json"}
        context.ad_account_id = context.config.userdata.get("account_id", "1001")
        log.info(f"Base URL set to : {context.baseURL}")
        log.info(f"Headers set to : {context.headers}")
        log.info(f"account_id set to : {context.ad_account_id}")
    except Exception as e:
        log.exception(str(e))
        raise e


@given(u'Set csv path to {csv_file_path}')
def set_csv_path(context, csv_file_path='data/PO_API Automation - Sheet1.csv'):
    try:
        context.csv_file_path = csv_file_path
        log.info(f"CSV path set to: {context.csv_file_path}")
    except Exception as e:
        log.exception(str(e))
        raise e


@given(u'Execute test case {testcase_id}')
def get_testcase_data(context, testcase_id):
    try:
        context.testcase_id = testcase_id
        # Fetching all data from the provided testcase_id from the CSV file
        context.row = csv.read_csv(testcase_id, key="row", csv_file_path=context.csv_file_path)
        try:
            # Check if CSV file returned any error
            if context.row["error"]:
                raise context.row["error_msg"]
        except Exception as e:
            # If the error is not raised for "error" key not in row (context.row["error"]) log and raise error message
            if "error" not in str(e):
                log.exception(e)
                raise e
        log.info(f'<{context.testcase_id}> - CSV File row data: {context.row}')
    except Exception as e:
        log.exception(str(e))
        raise e


@when(u'I set level to {level}')
def set_level(context, level=None):
    try:
        if level is not None:
            context.level = level.lower()
            log.info(f"<{context.testcase_id}> - Level set to : {context.level}")
    except Exception as e:
        log.exception(str(e))
        raise e


@when(u'I set api endpoint to {endpoint}')
def set_endpoint(context, endpoint):
    try:
        context.endpoint_name = endpoint
        context.endpoint = f"ApiResources.{endpoint}"
        context.endpoint = eval(eval(f'{context.endpoint}'))
        log.info(f"<{context.testcase_id}> - Endpoint set to {context.endpoint_name}: {context.endpoint}")
    except Exception as e:
        log.exception(str(e))
        raise e


@when(u'Set the body of request to {body}')
def set_body(context, body):
    try:
        # Set body to blank
        if body.lower() == 'blank':
            context.body = "{}"

        # Set body to update
        elif body.lower() == 'update body':
            # Set body for update
            get_update_body(context)

        # Set body from CSV file
        else:
            context.body = context.row[body.capitalize()]

        log.info(f"<{context.testcase_id}> - Body set to: {context.body}")
    except Exception as e:
        log.exception(str(e))
        raise e


# HTTP request methods

@when(u'Perform get')
def perform_get(context):
    try:
        log.info(f"<{context.testcase_id}> - Performing GET")
        context.response = requests.get(context.baseURL + context.endpoint, headers=context.headers)
        log.info(f'<{context.testcase_id}> - GET Response: {context.response.json()}')
    except Exception as e:
        log.exception(str(e))
        raise e


@when(u'Perform post')
def perform_post(context):
    try:
        log.info(f"<{context.testcase_id}> - Performing post")
        context.response = requests.post(context.baseURL + context.endpoint, data=context.body.encode('utf-8'),
                                         headers=context.headers)
        log.info(f'<{context.testcase_id}> - POST Response: {context.response.json()}')
        if str(context.endpoint_name) == "create_tactic" and context.response.json()["data"]["success"]:
            get_tactic_id(context)
            context.tactic = True
        elif str(context.endpoint_name) == "create_step_1":
            context.tactic = False

        if str(context.endpoint_name) == "create_filtergroups" and not context.response.json()["error"]:
            get_filtergroups_data(context)

    except Exception as e:
        log.exception(str(e))
        raise e


@when(u'Perform put')
def perform_put(context):
    try:
        log.info(f"<{context.testcase_id}> - Performing PUT")
        context.response = requests.put(context.baseURL + context.endpoint, data=context.body.encode('utf-8'),
                                        headers=context.headers)
        log.info(f'<{context.testcase_id}> - PUT Response: {context.response.json()}')
    except Exception as e:
        log.exception(str(e))
        raise e


@when(u'Perform delete')
def perform_delete(context):
    try:
        log.info(f"<{context.testcase_id}> - Performing DELETE")
        context.response = requests.delete(context.baseURL + context.endpoint, headers=context.headers)
        log.info(f'<{context.testcase_id}> - GET Response: {context.response.json()}')
    except Exception as e:
        log.exception(str(e))
        raise e


@then(u'Validate HTTP response code {response_from}')
def validate_response_code(context, response_from):
    try:
        # Get response code from CSV file if input is "from csv" else take the provided input value.
        context.response_code = context.row["Expected status code"] if response_from == "from csv" else response_from
        log.info(f"<{context.testcase_id}> - Actual Response Code: {context.response.status_code}")
        log.info(f"<{context.testcase_id}> - Expected Response Code: {context.response_code}")
        assert str(context.response.status_code) == context.response_code, \
            (f"<{context.testcase_id}> - Actual Response Code({context.response.status_code}) does not matches "
             f"Expected Response Code({context.response_code})")
    except AssertionError as e:
        log.exception(e)
        raise e
    except Exception as e:
        log.exception(str(e))
        raise e


@then(u'Validate error {error_from}')
def validate_response_error(context, error_from):
    try:
        # Get expected_error_code from CSV file if input is "from csv" else take the provided input value.
        expected_error_code = context.row["Error"] if error_from == "from csv" else error_from.lower()
        context.actual_err_code = context.response.json()["error"]
        # csv.read_csv(context.testcase_id, key="Error")
        log.info(f'<{context.testcase_id}> - Actual Error Code: {context.actual_err_code}')
        log.info(f'<{context.testcase_id}> - Expected Error Code: {expected_error_code}')
        assert str(context.response.json()["error"]).lower() == expected_error_code.lower(), \
            (f'<{context.testcase_id}> - Actual Error Code ({context.response.json()["error"]})'
                f' does not matches Expected Error Code ({expected_error_code})')
    except AssertionError as e:
        log.exception(e)
        raise e
    except Exception as e:
        log.exception(str(e))
        raise e


@then(u'Get tactic Id')
def get_tactic_id(context):
    try:
        context.tactic_id = context.response.json()["data"]["tactic_id"]
        print(f'<{context.testcase_id}> - Tactic Id: {context.tactic_id}')
        log.info(f'<{context.testcase_id}> - Tactic Id: {context.tactic_id}')
    except Exception as e:
        log.exception(str(e))
        raise e


@then(u'Get filtergroups data')
def get_filtergroups_data(context):
    try:
        context.filtergroups_id = context.response.json()["data"]["id"]
        context.filtergroups_filter_name = context.response.json()["data"]["filter_name"]
        context.filtergroups_auth_user = context.response.json()["data"]["auth_user"]
        context.filtergroups_filters = context.response.json()["data"]["filters"]
        context.filtergroups_level = context.response.json()["data"]["level"]
        context.filtergroups_ad_account_id = context.response.json()["data"]["ad_account_id"]
        log.info(f'<{context.testcase_id}> - Filtergroups Id: {context.filtergroups_id}')
    except Exception as e:
        log.exception(str(e))
        raise e


# validate tactic status from get call
@then(u'Validate the status')
def validate_status(context):
    try:
        if context.tactic:
            set_endpoint(context, "get_tactic_data")
            perform_get(context)
            context.actual_status = context.response.json()["data"]["status"]
            context.expected_status = context.row['Validate']
            log.info(f'<{context.testcase_id}> - Tactic status: {context.actual_status}')
            assert str(context.actual_status).lower() == context.expected_status.lower(), \
                f'<{context.testcase_id}> - Actual Tactic status ({context.actual_status}) does not matches Expected ' \
                f'Error Code ({context.expected_status}) '
        else:
            log.info(f'<{context.testcase_id}> - Validate the status Response: STEP SKIPPED. The tactic was not created\
            , So there is no tactic to Validate the status.')
    except AssertionError as e:
        log.exception(e)
        raise e
    except Exception as e:
        log.exception(str(e))
        raise e


@then(u'Validate the date_schedule')
def validate_date_schedule(context):
    try:
        if context.tactic:
            set_endpoint(context, "get_tactic_data")
            perform_get(context)
            context.actual_date_schedule = context.response.json()["data"]["tactic_json"]["date_schedule"]
            context.expected_date_schedule = context.row['Validate']
            log.info(f'<{context.testcase_id}> - Tactic status: {context.actual_date_schedule}')
            assert str(context.actual_date_schedule).lower() == context.expected_date_schedule.lower(), \
                f'<{context.testcase_id}> - Actual Tactic status ({context.actual_date_schedule}) does not matches ' \
                f'Expected Error Code ({context.expected_date_schedule}) '
        else:
            log.info(f'<{context.testcase_id}> - Validate the date_schedule Response: STEP SKIPPED. The tactic was not\
             created, So there is no tactic to Validate the date_schedule.')
    except AssertionError as e:
        log.exception(e)
        raise e
    except Exception as e:
        log.exception(str(e))
        raise e


@then(u'Validate the {date}')
def validate_date(context, date):
    try:
        if context.tactic:
            set_endpoint(context, "get_tactic_data")
            perform_get(context)
            context.actual_date = context.response.json()["data"][date]
            context.expected_date = context.row['Validate']
            log.info(f'<{context.testcase_id}> - Tactic status: {context.actual_date}')
            assert str(context.actual_date).lower() == context.expected_date.lower(), \
                f'<{context.testcase_id}> - Actual Tactic status ({context.actual_date}) does not matches Expected ' \
                f'Error Code ({context.expected_date}) '
        else:
            log.info(f'<{context.testcase_id}> - Validate the date_schedule Response: STEP SKIPPED. The tactic was not\
             created, So there is no tactic to Validate the {date}.')
    except AssertionError as e:
        log.exception(e)
        raise e
    except Exception as e:
        log.exception(str(e))
        raise e


@then(u'Delete the tactic')
def del_tactic(context):
    try:
        if context.tactic:
            context.del_response = requests.delete(
                context.baseURL + f"adaccount/{context.ad_account_id}/tactic/{context.tactic_id}",
                headers=context.headers)
            log.info(f'<{context.testcase_id}> - DELETE Response: {context.del_response.json()}')
        else:
            log.info(f'<{context.testcase_id}> - DELETE Response: STEP SKIPPED. The tactic was not created, So there is\
             no tactic to delete.')

    except Exception as e:
        log.exception(str(e))
        raise e


@then(u'Validate success {success_source}')
def validate_success(context, success_source="from csv"):
    try:
        context.actual_status = context.response.json()["data"]["success"]
        context.expected_status = context.row['Validate'] if success_source == "from csv" else success_source

        log.info(f'<{context.testcase_id}> - Actual success status: {context.actual_status}')
        log.info(f'<{context.testcase_id}> - Expected success status: {context.expected_status}')

        assert str(context.actual_status).lower() == context.expected_status.lower(), \
            f'<{context.testcase_id}> - Actual success status ({context.actual_status}) does not matches Expected ' \
            f'success status ({context.expected_status}) '

    except AssertionError as e:
        log.exception(e)
        raise e
    except Exception as e:
        log.exception(str(e))
        raise e


@then(u'validate pages')
def validate_pages(context):
    try:
        context.actual_pages = context.response.json()["data"]["pages"]
        log.info(f'<{context.testcase_id}> - Actual number of pages: {context.actual_pages}')
        log.info(f'<{context.testcase_id}> - Expected number of pages: value greater than 0')
        assert context.actual_pages != 0, f'<{context.testcase_id}> - Actual number of pages ({context.actual_pages})' \
                                          f' does not matches Expected number of pages that is greater than 0'
    except AssertionError as e:
        log.exception(e)
        raise e
    except Exception as e:
        log.exception(str(e))
        raise e


@then(u'validate page_size')
def validate_page_size(context):
    try:
        context.actual_page_size = context.response.json()["data"]["page_size"]
        log.info(f'<{context.testcase_id}> - Actual Page size: {context.actual_page_size}')
        log.info(f'<{context.testcase_id}> - Expected Page size: 10')
        assert context.actual_page_size == "10" and context.actual_page_size is not None, \
            (f'<{context.testcase_id}> - Actual Page size ({context.actual_page_size}) does not matches Expected Page '
             f'size (10)')
    except AssertionError as e:
        log.exception(e)
        raise e
    except Exception as e:
        log.exception(str(e))
        raise e


@then(u'validate current_page')
def validate_current_page(context):
    try:
        context.current_page = context.response.json()["data"]["current_page"]
        log.info(f'<{context.testcase_id}> - Actual current page: {context.current_page}')
        log.info(f'<{context.testcase_id}> - Expected current page: 1')
        assert context.current_page == "1", f'<{context.testcase_id}> - Actual current page ({context.current_page}) ' \
                                            f'does not matches Expected current page 1.'
    except AssertionError as e:
        log.exception(e)
        raise e
    except Exception as e:
        log.exception(str(e))
        raise e


@then(u'validate total count of tactic on overview')
def validate_count(context):
    try:
        context.tactic_count = context.response.json()["data"]["count"]
        log.info(f'<{context.testcase_id}> - Actual total count of tactic on the overview: {context.tactic_count}')
        log.info(f'<{context.testcase_id}> - Expected total count of tactic on the overview: value greater than 0.')
        assert context.tactic_count != 0, f'<{context.testcase_id}> - Actual total count of tactic on the overview ' \
                                          f'({context.tactic_count}), does not matches Expected total count of tactic' \
                                          f' on the overview (value greater than 0) '
    except AssertionError as e:
        log.exception(e)
        raise e
    except Exception as e:
        log.exception(str(e))
        raise e


@then(u'Validate tactic id from {get_tacticid}')
def validate_tactic_id(context, get_tacticid):
    try:
        # If input is "overview" then get tactic id from tactic overview api response
        # Else get tactic id from GET tactic data api response
        context.id = context.response.json()["data"]["results"][0]["id"] if get_tacticid.lower() == "overview" else \
            context.response.json()["data"]["id"]
        log.info(f'<{context.testcase_id}> - Actual tactic id: {context.id}')
        log.info(f'<{context.testcase_id}> - Expected tactic id: {context.tactic_id}')
        assert context.tactic_id == context.id, f'<{context.testcase_id}> - Actual tactic id from overview is ' \
                                                f'({context.id}), does not matches Expected tactic id after tactic ' \
                                                f'creation({context.tactic_id}) '
    except AssertionError as e:
        log.exception(e)
        raise e
    except Exception as e:
        log.exception(str(e))
        raise e


@then(u'Validate message {message}')
def validate_massage(context, message):
    try:
        context.message = context.response.json()["message"]
        log.info(f'<{context.testcase_id}> - Actual message : {context.tactic_id}')
        log.info(f'<{context.testcase_id}> - Expected message : {message}')
        assert message == context.message, f'<{context.testcase_id}> - Actual message ({context.message}), does not ' \
                                           f'matches Expected message({message}) '
    except AssertionError as e:
        log.exception(e)
        raise e
    except Exception as e:
        log.exception(str(e))
        raise e


@then(u'Validate if tactic status is {check_status} on overview')
def validate_tactic_status(context, check_status):
    try:
        context.actual_tactic_status = context.response.json()["data"]["results"][0]["status"]
        log.info(f'<{context.testcase_id}> - Actual tactic status: {context.actual_tactic_status}')
        log.info(f'<{context.testcase_id}> - Expected tactic status: {check_status}')
        assert context.actual_tactic_status == check_status.lower(), \
            f'<{context.testcase_id}> - Actual tactic status from overview:  ({context.actual_tactic_status}) does ' \
            f'not matches Expected tactic status ({check_status})'
    except AssertionError as e:
        log.exception(e)
        raise e
    except Exception as e:
        log.exception(str(e))
        raise e


@given(u'Set tactic status to {tactic_status}')
def set_tactic_status(context, tactic_status):
    try:

        assert tactic_status.lower() in ("off", "on"), f'<{context.testcase_id}> - "{tactic_status}" is a Invalid ' \
                                                       f'Input. Please enter a valid status on or off. '
        context.status = tactic_status.lower()
    except AssertionError as e:
        log.exception(e)
        raise e
    except Exception as e:
        log.exception(str(e))
        raise e


@then(u'Validate if filtergroups {key} is {expected_result} from {filtergroups_source}')
def validate_filtergroups(context, key='id', expected_result='present', filtergroups_source="from csv"):
    try:
        key = key.lower()
        assert key in ("id", "filter_name", "auth_user", "filters", "level", "ad_account_id"), \
            f'<{context.testcase_id}> - "{key}" is a Invalid Valid input for "key". Please enter a valid input "id", ' \
            f'"filter_name", "auth_user", "filters", "level" or "ad_account_id".'

        check_filtergroups_value = eval("context.filtergroups_" + key)

        if filtergroups_source.lower() == "from csv":
            context.filtergroups_id = context.row['Validate']

        filtergroup_value = False
        # Iterate through the filtergroups present in the GET filtergroup response and check for filtergroups_value
        for filtergroups in context.response.json()['data']:
            if check_filtergroups_value == filtergroups[key]:
                filtergroup_value = True
                break

        if expected_result.lower() == 'present':
            assert filtergroup_value, f'<{context.testcase_id}> - Filtergroup {key}: "{check_filtergroups_value}" is ' \
                                      f'not present in the GET filtergroup response. '
            log.info(
                f'<{context.testcase_id}> - Filtergroup {key}: "{check_filtergroups_value}" is present '
                f'in the GET filtergroup response.')
        elif expected_result.lower() == 'not present':
            assert not filtergroup_value, f'<{context.testcase_id}> - Filtergroup {key}: "{check_filtergroups_value}"' \
                                          f' is present in the GET filtergroup response. '
            log.info(f'<{context.testcase_id}> - Filtergroup {key}: "{check_filtergroups_value}" is not '
                     f'present in the GET filtergroup response.')
        else:
            assert False, log.exception(f'<{context.testcase_id}> - "{expected_result}" is a Invalid Valid input for '
                                        f'expected_result. Please enter a valid input "present" or "not present".')

    except AssertionError as e:
        log.exception(e)
        raise e
    except Exception as e:
        log.exception(str(e))
        raise e


@given(u'Set tactic id to {tactic_id} and task id to {task_id}')
def set_tactic_task_id(context, tactic_id='', task_id=''):
    try:
        context.tactic_id = int(tactic_id)
        context.task_id = int(task_id)
        log.info(f'<{context.testcase_id}> - Tactic id is set to: "{context.tactic_id}"')
        log.info(f'<{context.testcase_id}> - Task id is set to: "{context.task_id}"')
    except AssertionError as e:
        log.exception(e)
        raise e
    except Exception as e:
        log.exception(str(e))
        raise e


@then(u'Validate if {key} is {expected_result} on task overview')
def validate_filtergroups(context, key='id', expected_result=None):
    try:
        key = key.lower()
        assert key in ("id", "condition", "filtered_ids", "applied_to", "task_results", "task", "task_type",
                       "task_checked_status", "tactic_name", "error", "action_execution_frequency"), \
            f'<{context.testcase_id}> - "{key}" is a Invalid Valid input for "key". Please enter a valid input "id", ' \
            f'"condition", "filtered_ids", "applied_to", "task_results", "task", "task_type", "task_checked_status", ' \
            f'"tactic_name", "error", "action_execution_frequency".'

        check_value = False
        # Iterate through the tasks present in the GET task overview response and check for filtergroups_value
        for overview_tasks in context.response.json()['data']:
            if context.task_id == overview_tasks['id']:
                check_value = True
                log.info(f'<{context.testcase_id}> - Actual "{key}" value: {overview_tasks[key]}')
                log.info(f'<{context.testcase_id}> - Expected "{key}" value: {expected_result}')
                assert str(expected_result).lower() == str(overview_tasks[key]).lower(), \
                    f'<{context.testcase_id}> - Actual "{key}" from the task overview ({overview_tasks[key]}) does ' \
                    f'not matches Expected "{key}" value ({expected_result}) '

        assert check_value, f'<{context.testcase_id}> - Task Id: "{context.task_id}" Not found in the Task Overview ' \
                            f'of Tactic id: {context.tactic_id} '
    except AssertionError as e:
        log.exception(e)
        raise e
    except Exception as e:
        log.exception(str(e))
        raise e


@then(u'Validate if {key} is {expected_result} on task logs')
def validate_filtergroups(context, key='id', expected_result=None):
    try:
        key = key.lower()
        assert key in ("changed", "condition", "date", "last_checked", "pipeline_id", "rule_results", "task"), \
            f'<{context.testcase_id}> - "{key}" is a Invalid Valid input for "key". Please enter a valid input ' \
            f'"changed", "condition", "date", "last_checked", "pipeline_id", "rule_results", "task". '

        # Save pipeline id
        context.pipeline_id = context.response.json()["data"][0]["pipeline_id"]

        log.info(f'<{context.testcase_id}> - Actual "{key}" value: {context.response.json()["data"][0][key]}')
        log.info(f'<{context.testcase_id}> - Expected "{key}" value: {expected_result}')

        assert str(expected_result).lower() == str(context.response.json()["data"][0][key]).lower(), \
            f'<{context.testcase_id}> - Actual "{key}" from the task logs last execution ' \
            f'({context.response.json()["data"][0][key]}) does not matches Expected "{key}" value ({expected_result})'

    except AssertionError as e:
        log.exception(e)
        raise e
    except Exception as e:
        log.exception(str(e))
        raise e


@then(u'Validate if {key} is {expected_result} on task datelogs')
def validate_filtergroups(context, key=None, expected_result=None):
    try:
        key = key.lower()
        assert key in ("concept_id", "concept_name", "details"), f'<{context.testcase_id}> - "{key}" is a Invalid ' \
                                                                 f'Valid input for "key". Please enter a valid input ' \
                                                                 f'"concept_id", "concept_name", "details". '

        log.info(f'<{context.testcase_id}> - Actual "{key}" value: {context.response.json()["data"][0][key]}')
        log.info(f'<{context.testcase_id}> - Expected "{key}" value: {expected_result}')

        assert str(expected_result).lower() == str(context.response.json()["data"][0][key]).lower(), \
            f'<{context.testcase_id}> - Actual "{key}" from the task datelogs last execution ' \
            f'({context.response.json()["data"][0][key]}) does not matches Expected "{key}" value ({expected_result}) '

    except AssertionError as e:
        log.exception(e)
        raise e
    except Exception as e:
        log.exception(str(e))
        raise e


@when(u'Get body for update for tactic id {tactic_id}')
def get_update_body(context, tactic_id=None):
    """
    Set body for update tactic

    Performs GET (get_update_body) operation and saves body to context.body for performing update tactic operation

    :param context:
    :param tactic_id: string (default None), tactic id that needs to be updated
    :return:
    """
    # Set body for update
    temp_endpoint = context.endpoint

    if tactic_id is not None:
        context.tactic_id = tactic_id

    set_endpoint(context, "get_update_body")
    perform_get(context)
    context.endpoint = temp_endpoint
    if context.response.json()["error"]:
        log.error(f'<{context.testcase_id}> -Received Error for tactic id: {tactic_id} :: '
                  f'Error Message: {context.response.json()["message"]}')
    elif not context.response.json()["error"]:
        context.body = json.dumps(context.response.json()["data"])
        log.info(f"<{context.testcase_id}> - Body set to: {context.body}")
