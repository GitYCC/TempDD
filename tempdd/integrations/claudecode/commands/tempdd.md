# TempDD Claude-Code Command

Follow these steps:

1.  **Execute Command**: Run `tempdd ai "$ARGUMENTS"`
2.  **Get Instruction**: Get the AI execution instruction from the command's standard output.
3.  **Strict Execution**: Follow the retrieved instruction exactly, without adding any extra operations.

Note: The format is `tempdd ai "<stage> <action>"`, for example:
- `tempdd ai "prd build"`
- `tempdd ai "arch build"`
- `tempdd ai "tasks build"`
- `tempdd ai "tasks run"`
