Feature: Tactic creation Step 1 API testing

  Background:
        Given I set base REST API url and headers correctly
  @smoke
  Scenario: API Step 1
        Given Execute test case po_01
            And I Set posts api endpoint to create_step_1 endpoint
        When Set the body of request
            And Perfrom post
        Then Validate HTTP response code
            And Validate error
         Then Extract tactic Id
            And Delete the tactic


        Scenario Outline: API Step 1: Validate if "status" accepts <status>
        Given Execute test case <test_case>
            And I Set posts api endpoint to create_step_1 endpoint
        When Set the body of request
            And Perfrom post
        Then Validate HTTP response code
            And Validate error
        Then Validate if is status <status>
            And Delete the tactic
      Examples:
        | test_case | status |
        | po_02     |  draft |
        | po_03     |  on    |
        | po_04     |  off   |
        | po_05     | null   |
        | po_06     | ['"xyz" is not a valid choice.'] |


