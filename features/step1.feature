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
        | po_07     |
#    Scenario: API Step 1: Validate if "status" accepts "draft"
#        Given Execute test case po_02
#            And I Set posts api endpoint to Step 1 endpoint
#        When set the body of request
#            And perfrom post
#        Then Validate HTTP response code
#            And Validate error
#        Then validate if is status draft
#            And delete the tactic



#  Scenario: API Step 1: Validate if "status" accepts "on"
#        Given Execute test case po_03
#            And I Set posts api endpoint to Step 1 endpoint
#        When set the body of request
#            And perfrom post
#        Then Validate HTTP response code
#            And Validate error
#        Then validate if is status on
#            And delete the tactic
#
#  Scenario: API Step 1: Validate if "status" accepts "off"
#        Given Execute test case po_04
#            And I Set posts api endpoint to Step 1 endpoint
#        When set the body of request
#            And perfrom post
#        Then Validate HTTP response code
#            And Validate error
#        Then validate if is status off
#            And delete the tactic
#
#
#  @test
#  Scenario: API Step 1: Validate if "status" accepts null
#        Given Execute test case po_05
#            And I Set posts api endpoint to Step 1 endpoint
#        When set the body of request
#            And perfrom post
#        Then Validate HTTP response code
#            And Validate error
#        Then Validate if is status null
#            And delete the tactic


#  @test
#  Scenario: API Step 1: Validate if "status" accepts invalid value
#        Given Execute test case po_061
#            And I Set posts api endpoint to Step 1 endpoint
#        When set the body of request to po_061
#            And perfrom post
#        Then Validate HTTP response code
#            And Validate error
#            And delete the tactic

