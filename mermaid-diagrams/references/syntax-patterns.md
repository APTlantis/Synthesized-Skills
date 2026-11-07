# Syntax patterns and semantic checks

The bundled `.mmd` examples are original, conservative samples. They are starting points, not schemas. Validate using the destination's Mermaid version. Follow the linked official type documentation for syntax beyond these patterns.

## Flowcharts

Use `flowchart TD` or `flowchart LR`, IDs separate from labels (`request["Receive request"]`), and labeled decision edges (`decision -->|Yes| proceed`). A decision shape does not create branches automatically. Define the rejected path too when required. Use `subgraph ... end` for meaningful groups.

Avoid bare lowercase `end` as a node token; use an ID such as `finish_step` and an appropriate display label. Adjacent `o` or `x` after an edge can be interpreted as a special arrow terminator: use spaces and explicit node definitions. Quotes and entity codes help with punctuation, but escaping is diagram-type-specific. Do not mechanically apply HTML escaping to an entire diagram. See [flowchart.mmd](../examples/flowchart.mmd).

## Sequence diagrams

Declare `participant` or `actor` order explicitly when needed and use aliases for display names. `A->>B: message` and `B-->>A: reply` are useful conventional patterns; line style alone does not establish synchronous semantics. Choose an asynchronous arrow form only after checking the type's documentation and intended meaning.

Use `alt` / `else` / `end` for alternative branches, `opt` for optional work, and `loop` for repetition. Keep activations balanced if used. A sequence diagram represents interaction order, not a precise elapsed-time scale. Do not depict an optional action as unconditional. See [sequence.mmd](../examples/sequence.mmd).

## State diagrams

Use `stateDiagram-v2` and `[*]` for initial or final pseudo-states. A transition's label should identify its trigger or condition. Distinguish a state's name from an action performed while moving between states. Composite states are not a substitute for documenting an undefined transition. Check reachable states and intended terminal behavior. See [state.mmd](../examples/state.mmd).

## Classes

`Base <|-- Derived` shows inheritance with the triangle at the base. `Whole *-- Part` shows composition at the whole end; choose aggregation or association only if that is the intended relationship. Use explicit multiplicities when known. A class name or member label is not proof of implementation: use inspected code or supplied facts when documenting a real system. See [classes.mmd](../examples/classes.mmd).

## Entity relationships

Read both ends of a relationship: `||` means exactly one, `o|` zero or one, `o{` zero or many, and `|{` one or many, with mirrored left-hand forms. For example, `ACCOUNT ||--o{ SESSION : owns` means an account can own zero or many sessions and each session has exactly one account. The connecting solid/dashed form distinguishes identifying/non-identifying relationships; choose it from the model, not as decoration. Do not infer optionality or identification from a foreign-key name alone. See [entities.mmd](../examples/entities.mmd).

## Gantt

Set `dateFormat`, stable task IDs, and explicit starts or `after` dependencies. Distinguish input parsing (`dateFormat`) from displayed ticks (`axisFormat`). On compatible versions, use `tickInterval 1day` when automatic sub-day ticks repeat the same displayed date; the sample uses this v10.3.0+ feature. Excluded days affect scheduling; do not assume durations are business days. Confirm supplied dates and calendar conventions. A Gantt illustration does not validate feasibility or automatically solve resource constraints. See [schedule.mmd](../examples/schedule.mmd).

## Layout and debugging

Layout is algorithmic and type-dependent. Changing direction, declaration order, group membership, or label length can change positions. Use an alternative layout only when installed and supported by the host. Inspect subgraph links before expecting a nested direction to hold. Avoid fragile invisible edges unless their purpose is documented and semantic interpretation remains clear.

When a syntax error points at an arrow or closing keyword, check the preceding line for an unclosed delimiter. Isolate labels with punctuation and code-like text. When valid syntax looks wrong, review semantics and layout separately before changing grammar. Keep failure fixtures outside deliverable diagrams.
