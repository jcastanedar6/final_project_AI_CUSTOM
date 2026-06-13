Feature: CAG Context Storage and Personalisation
  As a student using the assistant
  I want my preferences to be remembered across questions
  So that responses adapt to my learning style

  Scenario: Save a user context preference
    Given the server is running
    When I save context for user "bdd-ana" key "preferred_style" value "explicaciones con analogias"
    Then the response status is 201
    And the response field "saved" equals true

  Scenario: Retrieve all saved context for a user
    Given the server is running
    And user "bdd-carlos" has context "topic" set to "arquitectura de software"
    When I retrieve context for user "bdd-carlos"
    Then the response status is 200
    And the context list contains key "topic" with value "arquitectura de software"

  Scenario: Context key is overwritten when saved again
    Given the server is running
    And user "bdd-marta" has context "nivel" set to "avanzado"
    When I save context for user "bdd-marta" key "nivel" value "principiante"
    And I retrieve context for user "bdd-marta"
    Then the context list contains key "nivel" with value "principiante"
    And the context list has exactly 1 item for key "nivel"

  Scenario: User context influences the answer
    Given the server is running
    And user "bdd-luis" has context "audience" set to "explicar como principiante"
    When user "bdd-luis" asks "Que es CAG?"
    Then the response status is 200
    And the answer contains "principiante"
    And the context_used includes "audience"

  Scenario: Users have isolated context stores
    Given the server is running
    And user "bdd-alice" has context "lang" set to "ingles"
    When I retrieve context for user "bdd-bob"
    Then the context list is empty
