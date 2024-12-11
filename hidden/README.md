# copilot

> [!NOTE]
> As with any GenAI, Copilot is non-deterministic. As such, results you get from Copilot may differ from what I demonstrate.

## Install (for VS Code)
1. Go to Extensions (on Activity Bar)
1. Search for `Copilot`
1. Install
    > You will get both the `Copilot` and `Copilot Chat` extensions installed
1. Using either the pop-up after install or the "Accounts" icon on the Activity Bar, sign into GitHub

Easy as that!

## Familiarize (for VS Code)
After install, Copilot is 100% ready to go. Start coding to use Code completions or click the "Chat" icon on the Activity Bar to use Copilot Chat.

That's all!

## Use
### Code completion <!-- 5 min -->
<!--
Hit on:
- context (file name, existing code, etc.)
  - maybe mention what is used as context and what is not
- how to accept suggestions (tab)
- how to flip through suggestions
- encourages commenting
- show generating boiler plate
  - getters and setters etc.
-->

> [!NOTE]
> Although I don't always explicitly list it, there is an implied acceptance of Copilot's suggestions at the end of each step below.


#### point.py
1. Navigate to point.py
    > file name is part of the context Copilot uses!

##### class point
1. Start a new comment "# create a class..."
    > If the suggestions are wrong or I don't like them, just keep typing!
1. Add "# should include getters, setters and a toString method" to your comment
    > The clearer and more descriptive I am, the more helpful Copilot can be!
1. Type "class Point:" and hit enter
    > Copilot draws on all information in our file to build its context, so it can infer what we want based on what we have already commented and coded. Remember, file name is part of context!
1. Accept all getters, setters and toString
    > Copilot expedites "boring" coding (repetitive, boilerplate tasks). This gives us more time for the tasks and coding we enjoy.
1. Start a new comment "# calculate the..." (we're going to create a distance function)
    > Copilot is, once again, inferring what we might want here based on the context it has.

##### class line
1. Start a new comment "# create a class..."
1. Type "class..."
    > Copilot will use the current context (in this case, the file name, and all comments and code in our current file), to determine how to structure and stylize suggested code. notice how Copilot automatically added getters, setters and a toString method (following the pattern it recognized from above) and it even automatically utilizes the distance method we defined previously.

<!-- ##### from direction to development
1. write a new comment "unit test function to verify line.length == point.distance"
1. hit enter and press tab -->

### Copilot Chat <!-- 10 min -->
<!--
Hit on:
- how context differs from Code completions
  - include how once there are prev messages in a hat, those act as context too
- How to accept changes from chat
- /clear and the `+` button
- history of chats
- models drop down +  attach files
- slash commands, and @'s
-->
#### Generate
> Copilot works on more than just traditional code. Even with operational tasks and files, Copilot can help.

##### Infra as Code
1. Navigate to iac.tf
1. Ask Copilot chat to "write a terraform file that creates a webapp and sql DB in Azure for me"
    > In Copilot Chat, we have various options for how to accepts suggested code.

<!-- ##### .github/workflows/main.yml
1. create a file main.yml
1. ask copilot chat to "write me a starter github actions file" -->

#### Explain
1. Open server.rs
1. Ask Copilot Chat what this file is doing <!-- maybe show #file:server.rs here and show just highlighting and open windows -->
#### Improve
1. Ask Copilot Chat it if there are any ways we can improve the code <!-- maybe talk here about how being specific in our prompt will help give more accurate, reliable answers. the less vague our ask, the better --> <!-- ex. how could I improve this file? I want to make this code run as efficiently as possible and I want to follow best practices -->
1. Ask chat how to implement thread pools and accept changes <!-- this is a good time to show the full overwrite, vs copy paste -->

#### Translate
1. Ask Copilot Chat to turn our rust code into python

#### Brainstorm
1. Ask Copilot Chat: if I'm looking to create a webserver in python, how should I go about it? should I be creating it from scratch like I'm doing here?
1. Ask it about the differences between the different frameworks it suggests.
1. Ask it which to use if I'm looking to run a simple blog server and I don't have much coding experience.

#### Secure
> Copilot can help identify and mitigate security vulnerabilities
1. Navigate to sql.py
1. Ask Copilot Chat to identify any security vulnerabilities it sees


#### @, # and / <!-- 5 min -->
##### \#
We can use `#` to reference files or selections. Essentially, determine what context to use to answer the question we are asking. Note: #web for web search.

1. Try this in chat: 
    - what is the latest version of Node.js?
1. then try this
    - #web what is the latest version of Node.js?

##### @
Called "participants". Use if you're looking to ask about a specific topic or domain. Example @docker. Copilot extensions can also provide more chat participants. Personally I don't use it much but it's there!

##### /
Short hand for common tasks in Copilot. So that I don't have to type out a full paragraph.
- `/tests` - writes tests
- `/explain` - explain code
- `/fix` - fix errors

## FAQ
1. How does GitHub Copilot Chat differ from ChatGPT?
    - GitHub Copilot Chat takes into consideration the context of your codebase and workspace, giving you more tailored solutions grounded in the code that you've already written. ChatGPT does not do this.

## Best Practices
- https://docs.github.com/en/copilot/using-github-copilot/best-practices-for-using-github-copilot