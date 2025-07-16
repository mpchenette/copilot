# General
Whenever possible, use recursion.

Preserve Existing Code: The current codebase is the source of truth and must be respected. Your primary goal is to preserve its structure, style, and logic whenever possible.

Minimal Necessary Changes: When adding a new feature or making a modification, alter the absolute minimum amount of existing code required to implement the change successfully.

Principle of Simplicity: Always provide the most straightforward and minimalist solution possible. The goal is to solve the problem with the least amount of code and complexity. Avoid premature optimization or over-engineering.

Anytime someone asks about the business logic diagram, utilize the [Business Logic Diagram](../diag.mmd).

# .NET
When suggesting .NET code, only suggest code compatible with .NET 8.
Always write my .NET unit tests using `Xunit`.