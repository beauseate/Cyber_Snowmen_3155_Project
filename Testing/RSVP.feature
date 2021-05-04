Feature: RSVP to an event
    An RSVP button near an event for me to let the creator know I've RSVPed.


    
Acceptance Criteria
-I am able to RSVP to an event to let the organizer know that I will be attending.
-I am able to manage my RSVP selections 

Scenario: I need to RSVP for the cat event so I can pet ALL the cats. 
    Given the event exists
    When I press RSVP
    Then I am registered for the event
    And I can view my name next to the event in the RSVP section


Scenario: I need to un-RSVP to an event. I learned I have cat allergies and can no longer go.
    Given I RSVPed to the event
    When I click UN-RSVP it takes me off the event listing
    Then I am unresgistered for the event
    And I won't be able to see my name next to the event in the RSVP section

Background: 
    Given I am logged into my account.