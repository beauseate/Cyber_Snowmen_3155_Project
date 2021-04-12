Feature: Liking an Event
As a user, I want to support an event I'm attending
by liking it so that others might attend too.

Acceptance Criteria
-I will see feedback that I've liked an event
-I will be able to see people that have liked my Events

Scenario: I want to make my friend's Birthday event more popular so I'll give it a like
    Given an event I wish to like
    When I click the like button
    Then the button turns a different color
    And my name is shown under those who have liked the event

Scenario: I liked an event but now I want to unlike it
    Given an event I wish to unlike
    When I click the like button
    Then the button turns back into the default state
    And my name is removed under those who have liked the event

Background:
    Given an event