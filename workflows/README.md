# Lobster Workflows

This directory contains [Lobster](https://github.com/openclaw/lobster) workflow definitions for the vfinance-news skill.

## Available Workflows

### `briefing.yaml` - Market Briefing with Approval

Generates a market briefing with an approval gate.

**Usage:**
```bash
# Run via Lobster CLI
lobster "workflows.run --file ~/projects/vfinance-news-openclaw-skill/workflows/briefing.yaml"

# With custom args
lobster "workflows.run --file workflows/briefing.yaml --args-json '{\"lang\":\"en\"}'"
```

**Arguments:**
| Arg | Default | Description |
|-----|---------|-------------|
| `lang` | `de` | Language: `en` or `de` |
| `fast` | `false` | Use fast mode (shorter timeouts) |

**Examples:**
```bash
lobster "workflows.run --file workflows/briefing.yaml"
```

**Flow:**
1. **Generate** - Runs local `.venv` CLI to produce briefing JSON
2. **Validate** - Enforces deterministic structured output
3. **Approve** - Halts for human review (shows briefing preview)

**Requirements:**
- Repo-local `.venv` with package installed (`pip install -e .`)
- `jq` for JSON parsing

## Adding to Lobster Registry

To make these workflows available as named workflows in Lobster:

```typescript
// In lobster/src/workflows/registry.ts
export const workflowRegistry = {
  // ... existing workflows
  'vfinance.briefing': {
    name: 'vfinance.briefing',
    description: 'Generate market briefing with approval gate',
    argsSchema: {
      type: 'object',
      properties: {
        lang: { type: 'string', enum: ['en', 'de'], default: 'de' },
        fast: { type: 'boolean', default: false },
      },
    },
    examples: [
      { args: { lang: 'de' }, description: 'German briefing' },
    ],
    sideEffects: [],
  },
};
```

## Why Lobster?

Using Lobster instead of direct cron execution provides:

- **Approval gates** - Review briefing before completion
- **Resumability** - If interrupted, continue from last step
- **Token efficiency** - One workflow call vs. multiple LLM tool calls
- **Determinism** - Same inputs = same outputs
