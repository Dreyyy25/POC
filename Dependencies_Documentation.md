# Dependencies

PydanticAI uses a dependency injection system to provide data and services to your agent's system prompts, tools, and result validators.

Matching PydanticAI's design philosophy, our dependency system tries to use existing best practices in Python development rather than inventing esoteric "magic." This makes dependencies type-safe, understandable, easier to test, and ultimately easier to deploy in production.

## Defining Dependencies

Dependencies can be any Python type. While in simple cases, you might be able to pass a single object as a dependency (e.g., an HTTP connection), dataclasses are generally a convenient container when your dependencies include multiple objects.

Here's an example of defining an agent that requires dependencies.

(Note: dependencies aren't actually used in this example, see [Accessing Dependencies](#accessing-dependencies) below)

### `unused_dependencies.py`

```python
from dataclasses import dataclass
import httpx
from pydantic_ai import Agent

@dataclass
class MyDeps:  
    api_key: str
    http_client: httpx.AsyncClient

agent = Agent(
    'openai:gpt-4o',
    deps_type=MyDeps,  
)

async def main():
    async with httpx.AsyncClient() as client:
        deps = MyDeps('foobar', client)
        result = await agent.run(
            'Tell me a joke.',
            deps=deps,  
        )
        print(result.data)
        #> Did you hear about the toothpaste scandal? They called it Colgate.
```

(This example is complete; it can be run "as is" — you'll need to add `asyncio.run(main())` to run `main`.)

## Accessing Dependencies

Dependencies are accessed through the `RunContext` type; this should be the first parameter of system prompt functions, etc.

### `system_prompt_dependencies.py`

```python
from dataclasses import dataclass
import httpx
from pydantic_ai import Agent, RunContext

@dataclass
class MyDeps:
    api_key: str
    http_client: httpx.AsyncClient

agent = Agent(
    'openai:gpt-4o',
    deps_type=MyDeps,
)

@agent.system_prompt  
async def get_system_prompt(ctx: RunContext[MyDeps]) -> str:  
    response = await ctx.deps.http_client.get(  
        'https://example.com',
        headers={'Authorization': f'Bearer {ctx.deps.api_key}'},  
    )
    response.raise_for_status()
    return f'Prompt: {response.text}'

async def main():
    async with httpx.AsyncClient() as client:
        deps = MyDeps('foobar', client)
        result = await agent.run('Tell me a joke.', deps=deps)
        print(result.data)
        #> Did you hear about the toothpaste scandal? They called it Colgate.
```

(This example is complete; it can be run "as is" — you'll need to add `asyncio.run(main())` to run `main`.)

## Asynchronous vs. Synchronous Dependencies

System prompt functions, function tools, and result validators are all run in the async context of an agent run.

If these functions are not coroutines (e.g., `async def`), they are called with `run_in_executor` in a thread pool. It's therefore marginally preferable to use async methods where dependencies perform I/O, although synchronous dependencies should work fine too.

### `sync_dependencies.py`

```python
from dataclasses import dataclass
import httpx
from pydantic_ai import Agent, RunContext

@dataclass
class MyDeps:
    api_key: str
    http_client: httpx.Client  

agent = Agent(
    'openai:gpt-4o',
    deps_type=MyDeps,
)

@agent.system_prompt
def get_system_prompt(ctx: RunContext[MyDeps]) -> str:  
    response = ctx.deps.http_client.get(
        'https://example.com', headers={'Authorization': f'Bearer {ctx.deps.api_key}'}
    )
    response.raise_for_status()
    return f'Prompt: {response.text}'

async def main():
    deps = MyDeps('foobar', httpx.Client())
    result = await agent.run(
        'Tell me a joke.',
        deps=deps,
    )
    print(result.data)
    #> Did you hear about the toothpaste scandal? They called it Colgate.
```

(This example is complete; it can be run "as is" — you'll need to add `asyncio.run(main())` to run `main`.)

## Full Example

Dependencies can be used in system prompts, tools, and result validators.

### `full_example.py`

```python
from dataclasses import dataclass
import httpx
from pydantic_ai import Agent, ModelRetry, RunContext

@dataclass
class MyDeps:
    api_key: str
    http_client: httpx.AsyncClient

agent = Agent(
    'openai:gpt-4o',
    deps_type=MyDeps,
)

@agent.system_prompt
async def get_system_prompt(ctx: RunContext[MyDeps]) -> str:
    response = await ctx.deps.http_client.get('https://example.com')
    response.raise_for_status()
    return f'Prompt: {response.text}'

@agent.tool  
async def get_joke_material(ctx: RunContext[MyDeps], subject: str) -> str:
    response = await ctx.deps.http_client.get(
        'https://example.com#jokes',
        params={'subject': subject},
        headers={'Authorization': f'Bearer {ctx.deps.api_key}'},
    )
    response.raise_for_status()
    return response.text

@agent.result_validator  
async def validate_result(ctx: RunContext[MyDeps], final_response: str) -> str:
    response = await ctx.deps.http_client.post(
        'https://example.com#validate',
        headers={'Authorization': f'Bearer {ctx.deps.api_key}'},
        params={'query': final_response},
    )
    if response.status_code == 400:
        raise ModelRetry(f'invalid response: {response.text}')
    response.raise_for_status()
    return final_response

async def main():
    async with httpx.AsyncClient() as client:
        deps = MyDeps('foobar', client)
        result = await agent.run('Tell me a joke.', deps=deps)
        print(result.data)
        #> Did you hear about the toothpaste scandal? They called it Colgate.
```

## Overriding Dependencies

When testing agents, it's useful to be able to customize dependencies.

### `test_joke_app.py`

```python
from joke_app import MyDeps, application_code, joke_agent

class TestMyDeps(MyDeps):  
    async def system_prompt_factory(self) -> str:
        return 'test prompt'

async def test_application_code():
    test_deps = TestMyDeps('test_key', None)  
    with joke_agent.override(deps=test_deps):  
        joke = await application_code('Tell me a joke.')  
    assert joke.startswith('Did you hear about the toothpaste scandal?')
```
