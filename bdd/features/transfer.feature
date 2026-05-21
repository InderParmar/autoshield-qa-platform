Feature: Fund Transfer
    As a logged-in ParaBank customer
    I want to transfer funds between my accounts
    So that I can manage my money

    Scenario: Valid transfer shows success confirmation
        Given I am logged into Parabank
        When I navigate to transfer funds page
        And I transfer funds between two accounts
        Then I should see a transfer success message

    Scenario: Transfer page loads correctly
        Given I am logged into Parabank
        When I navigate to transfer funds page
        Then the transfer page should be displayed