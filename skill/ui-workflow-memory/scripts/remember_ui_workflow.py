from _workflow_memory import remember_ui_workflow
from _workflow_memory import run_cli

main = remember_ui_workflow

if __name__ == "__main__":
    run_cli(main)
