class ApiResources:
    create_step_1 = 'f"adaccount/{context.account_id}/tactic"'
    # create_step_1 = "adaccount/{context.account_id}/tactic"
    create_step_2 = 'f"adaccount/{context.account_id}/tactic/{context.tactic_id}/filters"'
    tactic_on_off = 'f"adaccount/{context.ad_account_id}/tactic/{context.tactic_id}/status/{status}"'
    error_date_logs = 'f"adaccount/{context.ad_account_id}/tactic/{context.tactic_id}/task/{context.task_id}/errors"'
    tactic_overview = 'f"adaccount/{context.ad_account_id}/tactics"'
    search_tactic = 'f"adaccount/{context.ad_account_id}/tactics?name={search_query}&page_size={page_size}&page={page}"'
    delete_tactic = 'f"adaccount/{context.ad_account_id}/tactic/{context.tactic_id}"'
    task_overview = 'f"adaccount/{context.ad_account_id}/tactic/{context.tactic_id}/tasks"'
    task_logs = 'f"adaccount/{context.ad_account_id}/tactic/{context.tactic_id}/task/{context.task_id}/logs"'


