import subprocess
import tempfile
import os


class PythonTool:

    name = "python_executor"

    description = """
    Executes Python code and returns output.
    """

    def execute(self, code: str):

        with tempfile.NamedTemporaryFile(
            mode="w",
            suffix=".py",
            delete=False
        ) as temp_file:

            temp_file.write(code)

            temp_path = temp_file.name

        try:

            result = subprocess.run(
                ["python", temp_path],
                capture_output=True,
                text=True,
                timeout=10
            )

            return {
                "success": True,
                "stdout": result.stdout,
                "stderr": result.stderr
            }

        except Exception as e:

            return {
                "success": False,
                "error": str(e)
            }

        finally:

            os.remove(temp_path)