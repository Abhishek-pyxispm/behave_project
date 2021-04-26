Feature: Tactic creation Step 1 API testing

  Background:
        Given I set base REST API url and headers correctly
  @smoke
  Scenario: API Step 1
        Given Execute test case po_01
            And I Set posts api endpoint to Step 1 endpoint
        When set the body of request
            And perfrom post
        Then Validate HTTP response code
            And Validate error
         Then Extract tactic Id
            And delete the tactic


        Scenario Outline: API Step 1: Validate if "status" accepts <status>
        Given Execute test case <test_case>
            And I Set posts api endpoint to Step 1 endpoint
        When set the body of request
            And perfrom post
        Then Validate HTTP response code
            And Validate error
        Then validate if is status <status>
            And delete the tactic
      Examples:
        | test_case | status |
        | po_02     |  draft |
        | po_03     |  on    |
        | po_04     |  off   |
        | po_05     | null   |
        | po_06     | ['"xyz" is not a valid choice.'] |


