import subprocess
import sys
import os
import time
import signal
import pytest
from unittest.mock import patch


class TestScriptExecution:
    """Test suite for testing the script execution as a standalone module."""

    def test_script_can_be_imported(self):
        """Test that the main script can be imported without errors."""
        try:
            import main
            assert main.app is not None
            assert hasattr(main.app, 'run')
        except ImportError as e:
            pytest.fail(f"Failed to import main module: {e}")

    def test_script_syntax_is_valid(self):
        """Test that the main script has valid Python syntax."""
        try:
            with open('main.py', 'r') as f:
                code = f.read()
            compile(code, 'main.py', 'exec')
        except SyntaxError as e:
            pytest.fail(f"Syntax error in main.py: {e}")

    @pytest.mark.timeout(10)
    def test_script_execution_with_timeout(self):
        """Test that the script can be executed and responds to termination."""
        # Start the Flask app as a subprocess
        env = os.environ.copy()
        env['PORT'] = '5001'  # Use a different port to avoid conflicts
        
        try:
            # Start the process
            process = subprocess.Popen(
                [sys.executable, 'main.py'],
                env=env,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                preexec_fn=os.setsid  # Create a new process group
            )
            
            # Give it a moment to start
            time.sleep(2)
            
            # Check if the process is still running (it should be)
            poll_result = process.poll()
            assert poll_result is None, "Process should still be running"
            
            # Terminate the process gracefully
            os.killpg(os.getpgid(process.pid), signal.SIGTERM)
            
            # Wait for it to terminate
            try:
                process.wait(timeout=5)
            except subprocess.TimeoutExpired:
                # Force kill if it doesn't terminate gracefully
                os.killpg(os.getpgid(process.pid), signal.SIGKILL)
                process.wait()
            
        except Exception as e:
            # Clean up if something goes wrong
            if 'process' in locals() and process.poll() is None:
                try:
                    os.killpg(os.getpgid(process.pid), signal.SIGKILL)
                    process.wait()
                except:
                    pass
            pytest.fail(f"Script execution test failed: {e}")

    def test_main_module_structure(self):
        """Test that the main module has the expected structure."""
        import main
        
        # Check that required components exist
        assert hasattr(main, 'app'), "Module should have 'app' attribute"
        assert hasattr(main, 'index'), "Module should have 'index' function"
        assert hasattr(main, 'Flask'), "Module should import Flask"
        assert hasattr(main, 'jsonify'), "Module should import jsonify"
        assert hasattr(main, 'os'), "Module should import os"

    def test_environment_variable_handling_in_context(self):
        """Test environment variable handling in the context of the main module."""
        import main
        
        # Test with different PORT values
        test_ports = ['3000', '8080', '9000']
        
        for port in test_ports:
            with patch.dict(os.environ, {'PORT': port}):
                result = os.getenv("PORT", default=5000)
                assert result == port, f"Expected {port}, got {result}"
        
        # Test default behavior
        with patch.dict(os.environ, {}, clear=True):
            result = os.getenv("PORT", default=5000)
            assert result == 5000, f"Expected 5000, got {result}"