# Toyota Copilot Session - 12/11 - Tech Debt Reduction with Copilot

## Steps

To reduce technical debt with copilot, we will:
1. Refactor
1. Document (via comments, READMEs, etc.)
1. Future-proof (e.g., write unit tests)
1. Optimize (for memory and time complexity)
1. Secure

### Code Documentation
1. what does this file do? (server.py)
1. can you write some docstrings and comments for this file?
1. what are some ways I could improve this implementation?

or I could get more specific

1. what are some ways I could optimize this code? (with respect to the threads and memory and time efficiency)

1. what are some things that might potentially go wrong with this implementation?
1. can you suggest fixes for the things that might go wrong?
similar results to above. proof that there is more than one way to go about tech debt reduction with copilot.

1. what are some thing I may want to think about to help future-proof this code?

### Code Translation
1. Can you translate this code to Java for me?
1. Do the same concerns from my python implementation apply for my new Java implementation?

### Unit Test Generation
Copilot will have a much easier time writing unit tests for your code when your code is amply commented. Context is very important for successful interactions with Copilot!

1. can you help me write docstrings and comments for my code?
1. @workspace /tests use the unittest package. validate both success and failure, and include edge cases.

### Understand Code
What does this regex string capture?