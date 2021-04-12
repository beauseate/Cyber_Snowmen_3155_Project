Feature: Deleting an event
As a user I need to be able to delete an event if something 
occurs that would cause it to need to be cancelled. 

Acceptance Criteria
-I will see my event is actually created and displayed publically
-  Once deleted we will see that the event is no longer avaliable 
-I will recieve a notice that the event was successfully deleted

Scenario: I made my baseball event but its gonna storm severely so I need to cancel it 
    Given my event exists
    When I press delete
    Then the event deletes
    And I recieve a notice

Scenario: I tried to delete an event I already deleted
        Given my event has been deleted or does not exists
        When I try to delete
        Then a message appears 
        And the user notified it doesn't exists
Background: 
    Given User loged in
