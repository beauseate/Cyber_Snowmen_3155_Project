Feature: User can log in to their account
As a user, I want the website to remember my events
and RSVPs by having an account.

Acceptance Criteria
-I am able to see myself logged in under my name
-I can log out of my account

Scenario: I want to post an event so I need to log in
    Given I have created an account
    When I enter my account detials to log in
    Then I press the log in button
    And I am taken to the home page where I can see and create events

Scenario: I want to log out of my account to switch to a new one
    Given I am logged in to my account
    When I find the option to log out of my account
    Then I press the log out button
    And I am taken back to the user log in page

Background:
    Given I have created an account