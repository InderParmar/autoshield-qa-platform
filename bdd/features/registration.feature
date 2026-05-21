Feature: User Registration
    As a new customer
    I want to register for a ParaBank account
    So that I can access banking services

    Scenario: Valid registration shows welcome message
        Given I am on the Parabank registration page
        When I fill in the registration form with valid data
        Then I should see a welcome message with my username

    Scenario: Duplicate username shows an error
        Given I am on the Parabank registration page
        When I register with a username which already exists
        Then I should see a duplicate username error