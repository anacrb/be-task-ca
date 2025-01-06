# Backend Task - Clean Architecture

This project is a very naive implementation of a simple shop system. It mimics in its structure a real world example of a service that was prepared for being split into microservices and uses the current Helu backend tech stack.

## Goals

Please answer the following questions:

1. Why can we not easily split this project into two microservices?
    This project uses a single database for both User and Item, which creates challenges when dividing the system into 
    separate microservices. To achieve separation, the database would need to be split or each microservice would need 
    controlled access to only its relevant data.

    Additionally, the User use case has direct access to the Item functionality, leading to tight coupling between the 
    two domains. Separating them would require implementing an inter-service(REST, gRPC, or message queues) 
    communication mechanism to handle interactions between the services.

    Lastly, there are shared components that both services rely on. This could be addressed by extracting the shared 
    functionality into a separate shared library, allowing both microservices to reuse the logic without direct 
    dependency on one another.

2. Why does this project not adhere to the clean architecture even though we have separate modules for api, repositories, usecases and the model?
    The current architecture lacks the proper abstraction and separation of concerns required by clean architecture. 
    Specifically:

   - Decouple Use Cases: The User use case is directly coupled with the Item model, which introduces unnecessary 
   dependencies between unrelated parts of the system. Each use case should focus on its own specific responsibilities 
   and communicate through abstractions or clearly defined interfaces. This will prevent changes in one area 
   (e.g., the Item model) from affecting unrelated use cases like User.

   - Introduce Repository Interfaces: The use case layer should interact with the persistence layer through repository 
   interfaces, not directly with the database or ORM. This abstraction will decouple the business logic from the 
   underlying database implementation.

   - Use Domain Entities: Models should represent domain entities that encapsulate business logic and remain independent 
   of the database. Database-specific models should be confined to the persistence layer.

   - Restrict Framework-Specific Code: Framework-specific code (like FastAPI exceptions) should be restricted to the 
   API layer. The core business logic should raise generic, application-specific exceptions that can later be translated 
   by the outer layer.

   - Ensure Separation of Concerns: Each layer should have a clear and distinct responsibility. Business logic, 
   database operations, and API handling should not overlap, ensuring a modular and maintainable architecture.

3. What would be your plan to refactor the project to stick to the clean architecture?
    To refactor the project to adhere to the clean architecture principles, I would follow these steps:

   - Introduce Repository Interfaces: Replace direct database interactions in use cases with repository interfaces in 
   the core layer. Database-specific implementations should reside in the persistence layer, adhering to the dependency 
   inversion principle.

   - Decouple Use Cases from Models: Refactor tightly coupled use cases (e.g., User use case with Item model) by 
   introducing domain-specific abstractions. Ensure use cases operate independently within their contexts.

   - Define Domain Entities: Replace SQL-tied models with domain-specific entities encapsulating business logic. Keep 
   database models confined to the persistence layer and ensure the use cases interact only with the domain entities.

   - Confine Framework-Specific Code: Move framework-specific logic (e.g., FastAPI exceptions) to the API layer. The 
   use cases should raise application-specific exceptions that are translated in the outer layer.

   - Improve Layer Separation: Clarify boundaries between layers by ensuring business logic resides in use cases, 
   database interactions in repositories, and framework-specific code in the API layer.

   - Use Incremental Refactoring: Tackle one use case at a time, applying the above principles iteratively to ensure 
   minimal disruption and maintain functionality during the refactoring process.

4. How can you make dependencies between modules more explicit?
    To make dependencies between modules more explicit, I would follow these practices:

   - Use Interfaces and Dependency Injection: Clearly define and inject dependencies like repositories or services.
   
   - Enforce Layer Boundaries: Maintain clear responsibilities for each layer and ensure dependencies flow inward.
   
   - Leverage Type Annotations and Documentation: Use type hints and document module dependencies to clarify relationships.
   
   - Visualize and Monitor Dependencies: Use diagrams and linting tools to track and enforce dependency rules.

*Please do not spend more than 2-3 hours on this task.*

Stretch goals:
* Fork the repository and start refactoring
* Write meaningful tests
* Replace the SQL repository with an in-memory implementation

## References
* [Clean Architecture by Uncle Bob](https://blog.cleancoder.com/uncle-bob/2012/08/13/the-clean-architecture.html)
* [Clean Architecture in Python](https://www.youtube.com/watch?v=C7MRkqP5NRI)
* [A detailed summary of the Clean Architecture book by Uncle Bob](https://github.com/serodriguez68/clean-architecture)

## How to use this project

If you have not installed poetry you find instructions [here](https://python-poetry.org/).

1. `docker-compose up` - runs a postgres instance for development
2. `poetry install` - install all dependency for the project
3. `poetry run schema` - creates the database schema in the postgres instance
4. `poetry run start` - runs the development server at port 8000
5. `/postman` - contains an postman environment and collections to test the project

## Other commands

* `poetry run graph` - draws a dependency graph for the project
* `poetry run tests` - runs the test suite
* `poetry run lint` - runs flake8 with a few plugins
* `poetry run format` - uses isort and black for autoformating
* `poetry run typing` - uses mypy to typecheck the project

## Specification - A simple shop

* As a customer, I want to be able to create an account so that I can save my personal information.
* As a customer, I want to be able to view detailed product information, such as price, quantity available, and product description, so that I can make an informed purchase decision.
* As a customer, I want to be able to add products to my cart so that I can easily keep track of my intended purchases.
* As an inventory manager, I want to be able to add new products to the system so that they are available for customers to purchase.