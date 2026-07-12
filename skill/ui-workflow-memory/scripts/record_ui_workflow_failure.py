from _workflow_memory import record_ui_workflow_failure
from _workflow_memory import run_cli

main = record_ui_workflow_failure

if __name__ == "__main__":
    run_cli(main)
