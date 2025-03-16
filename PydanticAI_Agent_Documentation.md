# Agents

## Introduction

Agents are PydanticAI's primary interface for interacting with LLMs.

In some use cases, a single Agent will control an entire application or component, but multiple agents can also interact to embody more complex workflows.

The Agent class has full API documentation, but conceptually you can think of an agent as a container for:

| Component                  | Description                                                                                               |
| -------------------------- | --------------------------------------------------------------------------------------------------------- |
| System prompt(s)           | A set of instructions for the LLM written by the developer.                                               |
| Function tool(s)           | Functions that the LLM may call to get information while generating a response.                           |
| Structured result type     | The structured datatype the LLM must return at the end of a run, if specified.                            |
| Dependency type constraint | System prompt functions, tools, and result validators may all use dependencies when they're run.          |
| LLM model                  | Optional default LLM model associated with the agent. Can also be specified when running the agent.       |
| Model Settings             | Optional default model settings to help fine-tune requests. Can also be specified when running the agent. |

In typing terms, agents are generic in their dependency and result types, e.g., an agent which required dependencies of type `Foobar` and returned results of type `list[str]` would have type `Agent[Foobar, list[str]]`. In practice, you shouldn't need to care about this, but it allows your IDE to assist with type correctness and static type checking.

## Example: Simulating a Roulette Wheel

### `roulette_wheel.py`

```python
from pydantic_ai import Agent, RunContext

roulette_agent = Agent(  
    'openai:gpt-4o',
    deps_type=int,
    result_type=bool,
    system_prompt=(
        'Use the `roulette_wheel` function to see if the '
        'customer has won based on the number they provide.'
    ),
)

@roulette_agent.tool
async def roulette_wheel(ctx: RunContext[int], square: int) -> str:  
    """Check if the square is a winner"""
    return 'winner' if square == ctx.deps else 'loser'

# Run the agent
success_number = 18  
result = roulette_agent.run_sync('Put my money on square eighteen', deps=success_number)
print(result.data)  
#> True

result = roulette_agent.run_sync('I bet five is the winner', deps=success_number)
print(result.data)
#> False
```

## Agents are Designed for Reuse, Like FastAPI Apps

Agents are intended to be instantiated once (frequently as module globals) and reused throughout your application, similar to a small FastAPI app or an `APIRouter`.

## Running Agents

There are four ways to run an agent:

- `agent.run()` — A coroutine which returns a `RunResult` containing a completed response.
- `agent.run_sync()` — A synchronous function which returns a `RunResult` containing a completed response (internally, this just calls `loop.run_until_complete(self.run())`).
- `agent.run_stream()` — A coroutine which returns a `StreamedRunResult`, allowing streaming of responses as an async iterable.
- `agent.iter()` — A context manager which returns an `AgentRun`, an async iterable over the agent's underlying graph nodes.

### Example Usage

### `run_agent.py`

```python
from pydantic_ai import Agent

agent = Agent('openai:gpt-4o')

result_sync = agent.run_sync('What is the capital of Italy?')
print(result_sync.data)
#> Rome

async def main():
    result = await agent.run('What is the capital of France?')
    print(result.data)
    #> Paris

    async with agent.run_stream('What is the capital of the UK?') as response:
        print(await response.get_data())
        #> London
```

## Iterating Over an Agent's Graph

Each Agent in PydanticAI uses `pydantic-graph` to manage execution flow. `pydantic-graph` is a generic, type-centric library for building and running finite state machines in Python.

If you need deeper insight or control over execution, `Agent.iter()` returns an `AgentRun`, which you can async-iterate over or manually drive node-by-node via `next()`.

### Example: Using `async for` with `iter`

### `agent_iter_async_for.py`

```python
from pydantic_ai import Agent

agent = Agent('openai:gpt-4o')

async def main():
    nodes = []
    async with agent.iter('What is the capital of France?') as agent_run:
        async for node in agent_run:
            nodes.append(node)
    print(nodes)
    print(agent_run.result.data)
    #> Paris
```

### Example: Driving Iteration Manually with `.next()`

### `agent_iter_next.py`

```python
from pydantic_ai import Agent
from pydantic_graph import End

agent = Agent('openai:gpt-4o')

async def main():
    async with agent.iter('What is the capital of France?') as agent_run:
        node = agent_run.next_node  
        all_nodes = [node]

        while not isinstance(node, End):  
            node = await agent_run.next(node)  
            all_nodes.append(node)  

        print(all_nodes)
```

## Streaming

### `streaming.py`

```python
import asyncio
from dataclasses import dataclass
from datetime import date
from pydantic_ai import Agent
from pydantic_ai.tools import RunContext

@dataclass
class WeatherService:
    async def get_forecast(self, location: str, forecast_date: date) -> str:
        return f'The forecast in {location} on {forecast_date} is 24°C and sunny.'

weather_agent = Agent[WeatherService, str](
    'openai:gpt-4o',
    deps_type=WeatherService,
    result_type=str,
    system_prompt='Providing a weather forecast at the locations the user provides.',
)

@weather_agent.tool
async def weather_forecast(ctx: RunContext[WeatherService], location: str, forecast_date: date) -> str:
    return await ctx.deps.get_forecast(location, forecast_date)

async def main():
    user_prompt = 'What will the weather be like in Paris on Tuesday?'
    async with weather_agent.iter(user_prompt, deps=WeatherService()) as run:
        async for node in run:
            print(node)

if __name__ == '__main__':
    asyncio.run(main())
```

## Additional Configuration: Usage Limits

PydanticAI offers a `UsageLimits` structure to limit usage (tokens and/or requests) on model runs.

### Example: Restricting Response Tokens

```python
from pydantic_ai import Agent
from pydantic_ai.exceptions import UsageLimitExceeded
from pydantic_ai.usage import UsageLimits

agent = Agent('anthropic:claude-3-5-sonnet-latest')

result_sync = agent.run_sync(
    'What is the capital of Italy? Answer with just the city.',
    usage_limits=UsageLimits(response_tokens_limit=10),
)
print(result_sync.data)
#> Rome
print(result_sync.usage())
"""
Usage(requests=1, request_tokens=62, response_tokens=1, total_tokens=63, details=None)
"""

try:
    result_sync = agent.run_sync(
        'What is the capital of Italy? Answer with a paragraph.',
        usage_limits=UsageLimits(response_tokens_limit=10),
    )
except UsageLimitExceeded as e:
    print(e)
    #> Exceeded the response_tokens_limit of 10 (response_tokens=32)
```

Restricting the number of requests can be useful in preventing infinite loops or excessive tool calling:

```python
from typing_extensions import TypedDict

from pydantic_ai import Agent, ModelRetry
from pydantic_ai.exceptions import UsageLimitExceeded
from pydantic_ai.usage import UsageLimits


class NeverResultType(TypedDict):
    """
    Never ever coerce data to this type.
    """

    never_use_this: str


agent = Agent(
    'anthropic:claude-3-5-sonnet-latest',
    retries=3,
    result_type=NeverResultType,
    system_prompt='Any time you get a response, call the `infinite_retry_tool` to produce another response.',
)


@agent.tool_plain(retries=5)  
def infinite_retry_tool() -> int:
    raise ModelRetry('Please try again.')


try:
    result_sync = agent.run_sync(
        'Begin infinite retry loop!', usage_limits=UsageLimits(request_limit=3)  
    )
except UsageLimitExceeded as e:
    print(e)
    #> The next request would exceed the request_limit of 3
```

Model (Run) Settings
PydanticAI offers a settings.ModelSettings structure to help you fine tune your requests. This structure allows you to configure common parameters that influence the model's behavior, such as temperature, max_tokens, timeout, and more.

There are two ways to apply these settings: 1. Passing to run{_sync,_stream} functions via the model_settings argument. This allows for fine-tuning on a per-request basis. 2. Setting during Agent initialization via the model_settings argument. These settings will be applied by default to all subsequent run calls using said agent. However, model_settings provided during a specific run call will override the agent's default settings.

For example, if you'd like to set the temperature setting to 0.0 to ensure less random behavior, you can do the following:

```python
from pydantic_ai import Agent

agent = Agent('openai:gpt-4o')

result_sync = agent.run_sync(
    'What is the capital of Italy?', model_settings={'temperature': 0.0}
)
print(result_sync.data)
#> Rome
```

### Model specific settings
If you wish to further customize model behavior, you can use a subclass of ModelSettings, like GeminiModelSettings, associated with your model of choice.

For example:

```python
from pydantic_ai import Agent, UnexpectedModelBehavior
from pydantic_ai.models.gemini import GeminiModelSettings

agent = Agent('google-gla:gemini-1.5-flash')

try:
    result = agent.run_sync(
        'Write a list of 5 very rude things that I might say to the universe after stubbing my toe in the dark:',
        model_settings=GeminiModelSettings(
            temperature=0.0,  # general model settings can also be specified
            gemini_safety_settings=[
                {
                    'category': 'HARM_CATEGORY_HARASSMENT',
                    'threshold': 'BLOCK_LOW_AND_ABOVE',
                },
                {
                    'category': 'HARM_CATEGORY_HATE_SPEECH',
                    'threshold': 'BLOCK_LOW_AND_ABOVE',
                },
            ],
        ),
    )
except UnexpectedModelBehavior as e:
    print(e)  
    """
    Safety settings triggered, body:
    <safety settings details>
    """
```

### Runs vs. Conversations
An agent run might represent an entire conversation — there's no limit to how many messages can be exchanged in a single run. However, a conversation might also be composed of multiple runs, especially if you need to maintain state between separate interactions or API calls.

Here's an example of a conversation comprised of multiple runs:

```python
from pydantic_ai import Agent

agent = Agent('openai:gpt-4o')

# First run
result1 = agent.run_sync('Who was Albert Einstein?')
print(result1.data)
#> Albert Einstein was a German-born theoretical physicist.

# Second run, passing previous messages
result2 = agent.run_sync(
    'What was his most famous equation?',
    message_history=result1.new_messages(),  
)
print(result2.data)
#> Albert Einstein's most famous equation is (E = mc^2).
```

(This example is complete, it can be run "as is")

### Type safe by design
PydanticAI is designed to work well with static type checkers, like mypy and pyright.

#### Typing is (somewhat) optional
PydanticAI is designed to make type checking as useful as possible for you if you choose to use it, but you don't have to use types everywhere all the time.

That said, because PydanticAI uses Pydantic, and Pydantic uses type hints as the definition for schema and validation, some types (specifically type hints on parameters to tools, and the result_type arguments to Agent) are used at runtime.

We (the library developers) have messed up if type hints are confusing you more than helping you, if you find this, please create an issue explaining what's annoying you!

In particular, agents are generic in both the type of their dependencies and the type of results they return, so you can use the type hints to ensure you're using the right types.

Consider the following script with type mistakes:

```python
from dataclasses import dataclass

from pydantic_ai import Agent, RunContext

@dataclass
class User:
    name: str

agent = Agent(
    'test',
    deps_type=User,  
    result_type=bool,
)

@agent.system_prompt
def add_user_name(ctx: RunContext[str]) -> str:  
    return f"The user's name is {ctx.deps}."

def foobar(x: bytes) -> None:
    pass

result = agent.run_sync('Does their name start with "A"?', deps=User('Anne'))
foobar(result.data)  
```

Running mypy on this will give the following output:

```shell
➤ uv run mypy type_mistakes.py
type_mistakes.py:18: error: Argument 1 to "system_prompt" of "Agent" has incompatible type "Callable[[RunContext[str]], str]"; expected "Callable[[RunContext[User]], str]"  [arg-type]
type_mistakes.py:28: error: Argument 1 to "foobar" has incompatible type "bool"; expected "bytes"  [arg-type]
Found 2 errors in 1 file (checked 1 source file)
```

Running pyright would identify the same issues.

### System Prompts
System prompts might seem simple at first glance since they're just strings (or sequences of strings that are concatenated), but crafting the right system prompt is key to getting the model to behave as you want.

Generally, system prompts fall into two categories:

- **Static system prompts:** These are known when writing the code and can be defined via the `system_prompt` parameter of the `Agent` constructor.
- **Dynamic system prompts:** These depend in some way on context that isn't known until runtime, and should be defined via functions decorated with `@agent.system_prompt`.

You can add both to a single agent; they're appended in the order they're defined at runtime.

Here's an example using both types of system prompts:

```python
from datetime import date

from pydantic_ai import Agent, RunContext

agent = Agent(
    'openai:gpt-4o',
    deps_type=str,  
    system_prompt="Use the customer's name while replying to them.",  
)

@agent.system_prompt  
def add_the_users_name(ctx: RunContext[str]) -> str:
    return f"The user's name is {ctx.deps}."

@agent.system_prompt
def add_the_date() -> str:  
    return f'The date is {date.today()}.'

result = agent.run_sync('What is the date?', deps='Frank')
print(result.data)
#> Hello Frank, the date today is 2032-01-02.
```

(This example is complete, it can be run "as is")

