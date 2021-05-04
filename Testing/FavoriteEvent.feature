Feature: Favoritinging an Event
As a user, I want to support an event I'm attending
by favoriting it so that others might attend too.

Acceptance Criteria
-I will see feedback that I've favorited an event
-I will be able to see people that have favorited my Events

Scenario: I want to make my friend's Birthday event more popular so I'll give it a favorite
    Given an event I wish to favorite
    When I click the favorite button
    Then the button turns a different color
    And there is a notification that I've favorited the event

Scenario: I favorited an event but now I want to unfavorite it
    Given an event I wish to unfavorite
    When I click the unfavorite button
    Then the button turns back into the default state
    And there is a notification that I've unfavorited the event

Background:
    Given an event