Feature: The program must get monthly metrics from i-DE

Scenario: The program login into i-DE
    Given credentials
    When the program starts
    Then the program get a right response
