Feature: RAG Question Answering
  As a student using the assistant
  I want to ask questions about course topics
  So that I get accurate answers from the knowledge base

  Scenario: Health check returns ok
    Given the server is running
    When I request GET "/health"
    Then the response status is 200
    And the response field "status" equals "ok"

  Scenario: Question about RAG is answered from the knowledge base
    Given the server is running
    When user "student-01" asks "Que es RAG en el curso?"
    Then the response status is 200
    And the answer contains "RAG recupera"
    And the sources include "rag"
    And context_used is empty

  Scenario: Question about CAG is answered from the knowledge base
    Given the server is running
    When user "student-02" asks "Que es CAG?"
    Then the response status is 200
    And the answer contains "contexto persistente"
    And the sources include "cag"

  Scenario: Question with no matching content returns fallback message
    Given the server is running
    When user "student-03" asks "IPv6 Fibonacci Merkle Huffman"
    Then the response status is 200
    And the answer contains "No encontre informacion"

  Scenario: Ask endpoint requires both user_id and question
    Given the server is running
    When I post to "/api/ask" with body {"user_id": "x"}
    Then the response status is 400
    And the response field "error" equals "user_id and question are required"
