Feature: User Login
    As a ParaBank customer
    I want to log into my account
    So that I can access my banking services

    Scenario: Valid credentials redirect to accounts overview
        Given I am on the Parabank login page
        When I enter valid username and password
        Then I should be redirected to the accounts overview page

    Scenario: Invalid credentials show an error message
        Given I am on the Parabank login page
        When I enter invalid username and password
        Then I should see a login error message

    Scenario: Empty credentials show an error message
        Given I am on the Parabank login page
        When I submit the login form with empty credentials
        Then I should see a login error message