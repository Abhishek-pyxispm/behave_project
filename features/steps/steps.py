from behave import given, when, then
import requests
import utilities.rw_csv as csv
from utilities.log import custom_logger as log

log = log()


@given(u'I set base REST API url and headers correctly')
def setup_baseurl(context):
    context.baseURL = context.config.userdata.get("base_url", "url")
    context.headers = {"token": context.config.userdata.get("access_token", "token"),
                       "content-type": "application/json"}
    context.account_id = context.config.userdata.get("account_id", "1001")
    log.info(f"Base URL set to : {context.baseURL}")
    log.info(f"Headers set to : {context.headers}")
    log.info(f"account_id set to : {context.account_id}")


@given(u'I Set posts api endpoint to Step 1 endpoint')
def step1_endpoint(context):
    context.endpoint = f"adaccount/{context.account_id}/tactic"
    log.info(f"Endpoint set to : {context.endpoint}")



@when(u'set the body of request to {testcase_name}')
def set_body(context, testcase_name):
    # context.body = "{\r\n\t\"status\": \"draft\",\r\n\t\"date_schedule\": \"continuously\",\r\n\t\"level\": \"campaign\",\r\n\t\"action_execution_frequency\": \"28\",\r\n\r\n\t\"tasks\": [{\r\n\t\t\"task\": \"add_to_name\",\r\n\t\t\"meta_data\": {\r\n\t\t\t\"text\": \"_test 1\"\r\n\t\t},\r\n\t\t\"conditions\": {\r\n\t\t\t\"child_conditions\": [{\r\n\t\t\t\t\"name\": \"fb_primary_impressions\",\r\n\t\t\t\t\"time\": \"yesterday\",\r\n\t\t\t\t\"condition\": \">=\",\r\n\t\t\t\t\"value\": 0,\r\n\t\t\t\t\"absolute_value\": 0,\r\n\t\t\t\t\"rel_child\": \"AND\",\r\n\t\t\t\t\"aggregate\": \"\",\r\n\t\t\t\t\"child_conditions\": [],\r\n\t\t\t\t\"child_groups\": []\r\n\t\t\t}],\r\n\t\t\t\"child_groups\": []\r\n\t\t}\r\n\t}, {\r\n\t\t\"task\": \"remove_from_name\",\r\n\t\t\"meta_data\": {\r\n\t\t\t\"text\": \"_test 1\"\r\n\t\t},\r\n\t\t\"conditions\": {\r\n\t\t\t\"child_conditions\": [{\r\n\t\t\t\t\"name\": \"fb_primary_impressions\",\r\n\t\t\t\t\"time\": \"yesterday\",\r\n\t\t\t\t\"condition\": \">=\",\r\n\t\t\t\t\"value\": 0,\r\n\t\t\t\t\"absolute_value\": 0,\r\n\t\t\t\t\"rel_child\": \"AND\",\r\n\t\t\t\t\"aggregate\": \"\",\r\n\t\t\t\t\"child_conditions\": [],\r\n\t\t\t\t\"child_groups\": []\r\n\t\t\t}],\r\n\t\t\t\"child_groups\": []\r\n\t\t}\r\n\t}],\r\n\t\"setup_type\": \"exp\",\r\n\t\"task_sequence\": null,\r\n\t\"objective\": \"\"\r\n}"
    context.testcase_name = testcase_name
    context.body = csv.read_csv(testcase_name, key="Test Data")
    log.info(f"Test case name: {context.testcase_name}")
    log.info(f"Body set to: {context.body}")


@when(u'perfrom post')
def perform_post(context):
    log.info("Performing post")
    context.response = requests.post(context.baseURL + context.endpoint, data=context.body, headers=context.headers)
    log.info(f'Response: {context.response.json()}')


@then(u'I receive valid HTTP response code as {code}')
def validateResponseCode(context, code):
    # Response code from CSV
    context.response_code = csv.read_csv(context.testcase_name, key="Expected status code")
    log.info(f"Actule Response Code: {context.response.status_code}")
    log.info(f"Expected Response Code: {context.response_code}")
    assert str(context.response.status_code) == context.response_code, \
        log.exception(f"Actule Response Code({context.response.status_code}) does not matches Expected Response Code({context.response_code})")


@then(u'validate error is {err_code}')
def validate_response_error(context, err_code):
    err_code = csv.read_csv(context.testcase_name, key="Error")
    log.info(f'Actule Error Code: {context.response.json()["error"]}')
    log.info(f'Expected Error Code: {err_code}')
    assert str(context.response.json()["error"]).lower() == err_code.lower(), \
        log.exception(f'Actule Error Code ({context.response.json()["error"]} does not matches Expected Error Code ({err_code})')


@then(u'Extract tactic Id')
def step_impl(context):
    context.tactic_id = context.response.json()["data"]["id"]
    print(f'Tactic Id: {context.tactic_id}')
    log.info(f'Tactic Id: {context.tactic_id}')


@then(u'validate if is status {status}')
def step_impl(context, status):
    context.status = context.response.json()["data"]["status"]
    print(f'Tactic status: {context.status}')
    log.info(f'Tactic status: {context.status}')
    assert str(context.status).lower() == status.lower(), \
        log.exception(f'Actule Tactic status ({context.status} does not matches Expected Error Code ({status})')
