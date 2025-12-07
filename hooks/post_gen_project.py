#!/usr/bin/env python3
"""
Post-generation hook for cookiecutter template.

This hook removes entity-specific files when include_entity_example is "no".
"""

import os
import sys


def main() -> None:
    """Remove entity-specific files if include_entity_example is 'no'."""
    import json
    
    include_entity = None  # Will be set from context, None means "don't remove"
    
    # Try multiple methods to get the context value
    # Method 1: Command line argument (cookiecutter 1.7+)
    # Cookiecuter passes context as JSON string in sys.argv[1]
    if len(sys.argv) > 1:
        try:
            # The context might be passed as a JSON string directly
            context_str = sys.argv[1]
            # Try parsing as JSON
            if context_str.startswith('{'):
                context = json.loads(context_str)
                cookiecutter_vars = context.get("cookiecutter", {})
                include_entity = cookiecutter_vars.get("include_entity_example", None)
            # Or it might be a file path
            elif os.path.exists(context_str):
                with open(context_str, "r", encoding="utf-8") as f:
                    context = json.load(f)
                    cookiecutter_vars = context.get("cookiecutter", {})
                    include_entity = cookiecutter_vars.get("include_entity_example", None)
        except (json.JSONDecodeError, KeyError, AttributeError, OSError):
            pass
    
    # Method 2: Environment variables (cookiecutter may set these)
    if include_entity is None:
        # Check for COOKIECUTTER_CONTEXT environment variable
        context_json = os.environ.get("COOKIECUTTER_CONTEXT", "")
        if context_json:
            try:
                context = json.loads(context_json)
                cookiecutter_vars = context.get("cookiecutter", {})
                include_entity = cookiecutter_vars.get("include_entity_example", None)
            except (json.JSONDecodeError, KeyError, AttributeError):
                pass
        
        # Also check for direct environment variable (some cookiecutter versions)
        if include_entity is None:
            include_entity = os.environ.get("COOKIECUTTER_INCLUDE_ENTITY_EXAMPLE", None)
    
    # Method 3: Read from .cookiecutter.json file in project root (fallback)
    if include_entity is None:
        cookiecutter_json_path = os.path.join(os.getcwd(), ".cookiecutter.json")
        if os.path.exists(cookiecutter_json_path):
            try:
                with open(cookiecutter_json_path, "r", encoding="utf-8") as f:
                    context = json.load(f)
                    cookiecutter_vars = context.get("cookiecutter", {})
                    include_entity = cookiecutter_vars.get("include_entity_example", None)
            except (json.JSONDecodeError, KeyError, AttributeError, OSError):
                pass
    
    # Method 4: Heuristic detection from generated files (fallback)
    # If we can't get context from cookiecutter, check if entity code exists in generated files
    # When include_entity_example == "no", the template doesn't include EntityService imports
    if include_entity is None:
        container_path = os.path.join(os.getcwd(), "app", "core", "container.py")
        if os.path.exists(container_path):
            try:
                with open(container_path, "r", encoding="utf-8") as f:
                    container_content = f.read()
                    # If EntityService is not imported, include_entity_example was "no"
                    if "from app.services.entity_service import EntityService" not in container_content:
                        include_entity = "no"
            except OSError:
                pass
    
    # Normalize to lowercase for case-insensitive comparison
    # Only remove files if explicitly set to "no" (case-insensitive)
    # If context parsing failed or value is "yes"/None, keep the files
    if include_entity and include_entity.lower().strip() == "no":
        entity_files = [
            "app/services/entity_service.py",
            "app/schemas/entity.py",
            "app/api/v1/endpoints/entities.py",
            "tests/unit/domain/test_entity.py",
            "tests/unit/services/test_entity_service.py",
            "tests/unit/api/test_entity_endpoint.py",
            "tests/integration/test_entity_flow.py",
            # Note: tests/unit/repositories/test_memory_repository.py is NOT removed
            # because it's conditionally included in the template and will be empty/commented
            # when include_entity_example == "no"
        ]
        
        project_root = os.getcwd()
        removed_count = 0
        not_found_count = 0
        
        for file_path in entity_files:
            full_path = os.path.join(project_root, file_path)
            if os.path.exists(full_path):
                try:
                    os.remove(full_path)
                    removed_count += 1
                except OSError as e:
                    print(f"Warning: Could not remove {file_path}: {e}", file=sys.stderr)
            else:
                not_found_count += 1
        
        if removed_count > 0:
            print(f"Removed {removed_count} entity example file(s) (include_entity_example='no')")
        if not_found_count > 0:
            # Only print if we expected to remove files but some weren't found
            # This helps debug path issues
            pass


if __name__ == "__main__":
    main()
