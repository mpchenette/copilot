# GitHub Copilot
> [!NOTE]
> Last updated 05-MAY-2025

This is a repo containing materials that can be used for future Copilot demos.

## Best Practices
![image.png](./docs/images/copilot-best-practices.png)

## [Code Completions](https://code.visualstudio.com/docs/copilot/ai-powered-suggestions)
### Inline suggestions
World's most intelligent autocomplete!

Copilot understands what your intent is via context, like file name, comment contents, surrounding code and other open files in your workspace.

1. `point.py`

Copilot code completions even promotes best practices while you code as comments are one of the primary ways of prompting it!

You can also interact with Copilot code completions (+ more) inside a file in other ways:
- Suggestion Selector
- Completions Panel (Ctrl + Enter)
- Editor Inline Chat (Cmd + I)

### Next Edit Suggestions

1. `point3D.py`

## [Copilot Chat](https://code.visualstudio.com/docs/copilot/chat/copilot-chat)
No need to context switch! Everything I need, in my IDE.

Copilot Chat is also where we can really focus on reducing existing tech debt.

Endless possibilities: Brainstorm, Translate, Review, Document, Clarify, Understand, Optimize, Generate, Secure, Code!


### Chat Commands
Chat commands are a great and easy place to start with Copilot Chat. When in doubt, `/help`!

1. Open `calculator.py` and run `/tests` <!-- (remove floats if they appear) -->
   - Optionally, run `pytest tests/`
1. `@workspace /tests for #file:TaskItem.cs`
   - Make sure the created file is in the `DotnetApp.Tests/Models` directory
   - `dotnet test DotnetApp.Tests/DotnetApp.Tests.csproj`
1. Ask `@vscode Where can I find the setting to render whitespace?`

### Context
Context in Copilot Chat works differently than it did for code completions. Other than what is currently visible in your editor, Copilot Chat requires that we explicitly add all relevant files as context before submitting our prompt. The easiest ways of including files as context are to with drag and drop them into the chat window, or using the `#file:<filename>` tag.

1. Show typing a `#` into chat and reading what each tag specifies

### Possibilities
#### Brainstorm
1. What the best naming convention to use in my .NET project? What's idiomatic?
1. Is it better to use a const or a static variable for something I need to be global in my .NET API?
#### Translate
1. Can you translate this Java file (`point.java`) into Python?
#### Optimize
1. What can I do to improve my .NET app (`DotnetApp`)? I'm preparing it for a production release and need to make sure it's ready.
#### Review
1. Do you see any security vulnerabilities in this code (`sql.py`)?
1. I'm looking to reduce tech debt across my codebase. Is there anything in my .NET app (`DotnetApp`) that I should consider improving or fixing?
#### Understand
1. Can you explain what this file is doing (`server.rs`)?

### Modes
When to use each mode. https://code.visualstudio.com/docs/copilot/chat/copilot-chat#_chat-mode

#### [Ask mode](https://code.visualstudio.com/docs/copilot/chat/chat-ask-mode)

#### [Edit mode](https://code.visualstudio.com/docs/copilot/chat/copilot-edits)
For when you want to Copilot Chat to make suggestions inside your files!

Copilot Edits makes sweeping changes across multiple files quick and easy.

1. "Can you add comments and docstrings to all of the files in `#file:ITaskService.cs`, `#file:CsvTaskService.cs` and `#file:InMemoryTaskService.cs`"

#### [Agent mode](https://code.visualstudio.com/docs/copilot/chat/chat-agent-mode)

## [Configuring Copilot / Customizing Copilot](https://code.visualstudio.com/docs/copilot/copilot-customization)
### Custom instructions
Used to set "rules" you want Copilot to follow for all suggestions. A system prompt of sorts.

Lives under `.github/copilot-instructions.md`.

Examples:
1. Specify packages or frameworks you want Copilot to suggest
   - "Always write my Python unit tests using `pytest`, not `unittest`."
1. Specify (older) versions of languages or frameworks to use
   - "When suggesting .NET code, only suggest code compatible with .NET 8."
   - Note this will not work for versions beyond the model "cut-off" date.
1. Repo-wide standards or expectations for all involved developers
   - "Whenever possible, use recursion."

### Prompt Files

### Public Code Block
If Public Code Block is enabled, if Copilot generates code that closely matches licensed code in the public domain, the response will be blocked. However, there are ways of helping Copilot avoid suggesting public code.

- Refactor / Reframe your prompt
- Ask Copilot to break suggested code into different blocks in its response
- Ask Copilot to only show changed lines of code
- Ask Copilot to just show pseudocode
- Ask Copilot to show the code it suggests in another language
- Ask Copilot to comment out the code it suggests
- Ask Copilot to prepend the code it suggests with something like `##`
- Break your problem into smaller problems

Generally speaking, when we work with our own large, complex, unique codebases, we won't run into this much. This will mostly come into play when we are starting from scratch or asking Copilot for generic examples. The alternative to the Public Code Block is Code Referencing, where Copilot will show the public code anyway and let you know what type of license applies to the repo it is sourced from.

A fairly reliable prompt to use to test Code Referencing (or trigger a public code block) is:
- "generate “void fast_inverse_sqrt” in C"

## Other

### Copilot Code Review

<!-- # Extended Demos
## SonarQube
### SonarQube - Setup
As a prerequisite for this demo, you will need Docker Desktop installed and running.
1. `docker pull sonarqube:community`
1. Follow any steps here that you need: https://docs.sonarsource.com/sonarqube-community-build/try-out-sonarqube/
1. Navigate to http://localhost:9000

### .NET - Setup
As a prerequisite for this demo, you will need a project set-up already inside of SonarQube.

If not yet installed, be sure you have the SonarScanner .NET Core GLobal Tool
1. `dotnet tool install --global dotnet-sonarscanner`
1. `dotnet sonarscanner begin /k:"BofA" /d:sonar.host.url="http://localhost:9000"  /d:sonar.token="sqa_ea0a259ee427f1113d6dc0d0de4f5484ed5d6f62"`
1. `dotnet build DotnetApp/DotnetApp.csproj`
1. `dotnet sonarscanner end /d:sonar.token="sqa_ea0a259ee427f1113d6dc0d0de4f5484ed5d6f62"`

### Fixing Sonar Issues
#### Reliability
1. In SonarQube it is telling me to "Await RunAsync instead" for line 44 of #file:Program.cs. Can you help me fix this?
#### Maintainability
1. In SonarQube it is telling me to "Refactor this method to reduce its Cognitive Complexity from 31 to the 15 allowed" for line 21 of #file:TaskItem.cs. Can you help me fix this?

> Tip: Add a new custom instruction for this: "My team uses SonarQube. Please keep the Cognitive Complexity for all suggested code under 15. In other words, the functions that you suggest need to be very clear and brief in what they do, from a program logic standpoint. Break long, complex functions up into smaller components."

### Code Coverage
1. `dotnet clean DotnetApp/DotnetApp.csproj && dotnet build DotnetApp/DotnetApp.csproj`
1. ``` sh
   dotnet sonarscanner begin /k:"BofA" \
     /d:sonar.host.url="http://localhost:9000" \
     /d:sonar.token="sqa_ea0a259ee427f1113d6dc0d0de4f5484ed5d6f62" \
     /d:sonar.cs.cobertura.reportsPaths="DotnetApp.Tests/TestResults/**/coverage.cobertura.xml" \
     /d:sonar.coverage.exclusions="**Test*.cs,**/*.Tests.cs" \
     /d:sonar.cs.opencover.reportsPaths="DotnetApp.Tests/TestResults/**/coverage.opencover.xml"
   ```
1. `dotnet build DotnetApp/DotnetApp.csproj`
1. `dotnet test DotnetApp.Tests/DotnetApp.Tests.csproj --collect:"XPlat Code Coverage;Format=opencover,cobertura"`
1. `dotnet sonarscanner end /d:sonar.token="sqa_ea0a259ee427f1113d6dc0d0de4f5484ed5d6f62"`

### Misc.
- In the future, Agent mode will be able to iterate on the issues in the dashboard (using the URL) for you!
 -->


## Future
In the future, a decent demo might be to use this commit https://github.com/mpchenette/pong/tree/80dcd03e2cd1e7fe39a044c1fc51cb39ea2b5c2f (FFR: this is the duopong right before I add server side color chainging, right after I changed 127.0.0.1 to 0.0.0.0)to demo agent mode and also repo indexing.

If you have the repo indexed remotely, ask the "ask" mode the following: "it would seem that at the moment the background color changing is a client side change only. is that accurate? how would I make this a change that affects everyone/that everyone can see? that is my goal", and look how fast the response is. This is because of indexing! Even without the file open! No context needed because we have the index.

Now jump to agent mode and ask the same thing. see how much longer it takes. but also see that agent mode makes the change for you. And if agent mode fails like it did for me the first time, you can ask it to iterate!

A good example of when to use each mode and pros/cons and also how knowing the different aspects of Copilot leads to a better experience.

Want to find something that is currently in the code or find where something is? Want to understand how the current logic or implementation works? Ask mode with remote index.

Want to debug something or find where an error or bug stems from? Want to implement a change based on how the current logic functions? Agent mode.