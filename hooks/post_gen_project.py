#!/usr/bin/env python3
"""
Post-generation hook for cookiecutter template.

This hook removes entity-specific files when include_entity_example is "no".
"""

import os
import sys


def main() -> None:
    """Remove entity-specific files if include_entity_example is 'no'."""
    # Cookiecuter passes context as JSON in the first command-line argument
    # or we can check environment variables
    
    # Try to get context from command line args (cookiecutter 1.7+)
    context_json = None
    if len(sys.argv) > 1:
        context_json = sys.argv[1]
    else:
        # Try environment variable (cookiecutter 2.0+)
        context_json = os.environ.get("COOKIECUTTER_CONTEXT", "")
    
    include_entity = "no"  # Default to "no"
    
    if context_json:
        try:
            import json
            context = json.loads(context_json)
            # Context structure: {"cookiecutter": {"include_entity_example": "no", ...}}
            cookiecutter_vars = context.get("cookiecutter", {})
            include_entity = cookiecutter_vars.get("include_entity_example", "no")
        except (json.JSONDecodeError, KeyError, AttributeError):
            # If parsing fails, default to "no"
            include_entity = "no"
    
    # If include_entity_example is "no", remove entity-specific files
    if include_entity == "no":
        entity_files = [
            "app/services/entity_service.py",
            "app/schemas/entity.py",
            "app/api/v1/endpoints/entities.py",
            "tests/unit/domain/test_entity.py",
            "tests/unit/services/test_entity_service.py",
            "tests/unit/api/test_entity_endpoint.py",
            "tests/integration/test_entity_flow.py",
            "tests/unit/repositories/test_memory_repository.py",
        ]
        
        project_root = os.getcwd()
        removed_count = 0
        
        for file_path in entity_files:
            full_path = os.path.join(project_root, file_path)
            if os.path.exists(full_path):
                try:
                    os.remove(full_path)
                    removed_count += 1
                except OSError as e:
                    print(f"Warning: Could not remove {file_path}: {e}", file=sys.stderr)
        
        if removed_count > 0:
            print(f"Removed {removed_count} entity example file(s) (include_entity_example='no')")


if __name__ == "__main__":
    main()
