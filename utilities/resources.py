class ApiResources:
    # GET APIs
    get_update_body = 'f"automation/adaccount/{context.ad_account_id}/tactic/{context.tactic_id}"'

    # POST APIs

    # PUT APIs

    # DELETE API's
    tactic_validation = 'f"adaccount/{context.ad_account_id}/tacticvalidation"'
    create_tactic = 'f"adaccount/{context.ad_account_id}/tactic"'
    update_tactic = 'f"adaccount/{context.ad_account_id}/tactic"'
    get_tactic_data = 'f"adaccount/{context.ad_account_id}/tactic/{context.tactic_id}"'
    tactic_on_off = 'f"adaccount/{context.ad_account_id}/tactic/{context.tactic_id}/status/{context.status}"'
    error_date_logs = 'f"adaccount/{context.ad_account_id}/tactic/{context.tactic_id}/task/{context.task_id}/errors"'
    tactic_overview = 'f"adaccount/{context.ad_account_id}/tactics?page=1&page_size=10"'
    search_tactic = 'f"adaccount/{context.ad_account_id}/tactics?name={search_query}&page_size={page_size}&page={page}"'
    delete_tactic = 'f"adaccount/{context.ad_account_id}/tactic/{context.tactic_id}"'
    task_overview = 'f"adaccount/{context.ad_account_id}/tactic/{context.tactic_id}/tasks"'
    task_logs = 'f"adaccount/{context.ad_account_id}/tactic/{context.tactic_id}/task/{context.task_id}/logs"'
    datelogs = 'f"adaccount/{context.ad_account_id}/tactic/{context.tactic_id}/task/{context.task_id}/log_date/' \
               '{context.pipeline_id}/datelogs"'
    create_filtergroups = 'f"adaccount/{context.ad_account_id}/level/{context.level}/filtergroups"'
    get_filtergroups = 'f"adaccount/{context.ad_account_id}/level/{context.level}/filtergroups"'
    delete_filtergroups = 'f"adaccount/{context.ad_account_id}/filtergroups/{context.filtergroups_id}"'
