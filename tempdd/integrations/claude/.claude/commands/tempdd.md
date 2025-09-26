# TempDD Command Entrypoint

Follow these steps:

1.  **Check Arguments**: If `$ARGUMENTS` is "help" or empty, run `tempdd help` to get the output content and display the output with preferred language. Then stop - do not execute further steps.
2.  **Execute Command**: Otherwise, run `tempdd ai "$ARGUMENTS"`
3.  **Get Instruction**: Get the AI execution instruction from the command's standard output.
4.  **Strict Execution**: Follow the retrieved instruction exactly, without adding any extra operations.

Note: The format is `tempdd ai "<stage> <action>"`, for example:
- `tempdd ai "prd build"`
- `tempdd ai "arch build"`
- `tempdd ai "tasks build"`
- `tempdd ai "tasks run"`
