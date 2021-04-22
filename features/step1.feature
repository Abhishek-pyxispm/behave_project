Feature: Tactic creation Step 1 API testing

  Background:
        Given I set base REST API url and headers correctly
  @smoke
  Scenario: API Step 1
        Given I Set posts api endpoint to Step 1 endpoint
        When set the body of request to po_01
            And perfrom post
        Then I receive valid HTTP response code as 200
            And validate error is False
         Then Extract tactic Id

    Scenario: API Step 1: Validate if "status" accepts "draft"
        Given I Set posts api endpoint to Step 1 endpoint
        When set the body of request to po_02
            And perfrom post
        Then I receive valid HTTP response code as 200
            And validate error is False
        Then validate if is status draft

  Scenario: API Step 1: Validate if "status" accepts "on"
        Given I Set posts api endpoint to Step 1 endpoint
        When set the body of request to po_03
            And perfrom post
        Then I receive valid HTTP response code as 200
            And validate error is False
        Then validate if is status on


  Scenario: API Step 1: Validate if "status" accepts "off"
        Given I Set posts api endpoint to Step 1 endpoint
        When set the body of request to po_04
            And perfrom post
        Then I receive valid HTTP response code as 200
            And validate error is False
        Then validate if is status off


  Scenario: API Step 1: Validate if "status" accepts null
        Given I Set posts api endpoint to Step 1 endpoint
        When set the body of request to po_05
            And perfrom post
        Then I receive valid HTTP response code as 200
            And validate error is False
        Then validate if is status null


  Scenario: API Step 1: Validate if "status" accepts invalid value
        Given I Set posts api endpoint to Step 1 endpoint
        When set the body of request to po_06
            And perfrom post
        Then I receive valid HTTP response code as 400
            And validate error is True
