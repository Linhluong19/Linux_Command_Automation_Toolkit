import os
import subprocess
import sys
import re 
import json
import datetime
from typing import List, Dict, Optional 



class LinuxCommandToolkit:
    """Documentation for LinuxCommandToolkit class."""

    def __init__(self):
        """Initialize the LinuxCommandToolkit class."""
        self.history = []
        
    
    def _execute_command(self, command: List[str], capture_output: bool = True) -> Dict:
        """
        Execute the command and return the result.

        Args:
            command (str): The command to execute.
            capture_output (bool): If True, return the command output.
        
        Returns:
            Dict: Contains information about the execution result.
        """
        try:
            result = subprocess.run(
                command,
                capture_output=capture_output,
                text=True,
                timeout=30
            )

            output = {
                "command": ' '.join(command),
                'returncode': result.returncode,
                'stdout': result.stdout, #standard output
                'stderr': result.stderr,
                #'timestamp': datetime.now().isoformat(),
                'success': result.returncode == 0
            }

            self.history.append(output)
            return output
        
        except subprocess.TimeoutExpired:
            return {
                "command": ' '.join(command), 
                'error': 'Command timed out (>30 seconds)',
                'success': False
            }
        
    
        except Exception as e:
            return {
                "command": ' '.join(command), 
                'error': str(e),
                'success': False
            }

    def who_am_i(self) -> Dict:
        """Return the current username."""
        # return self._execute_command(['whoami'])
        result = self._execute_command(['whoami'])

        if result['success']:
            result['summary'] = {
                'username': result['stdout'].strip()
            }
    
        return result
    
    def ls(self, path: str = '.',
           long_format: bool = False,
           all_files: bool = False,
           sort_by: Optional[str] = None) -> Dict:
        """List files and directories in the given path.
        
        Args:
            path (str): Path to list. Defaults to the current directory.
            long_format (bool): If True, use long listing format.
            all_files (bool): If True, include hidden files.
            sort_by (Optional[str]): Sorting criteria ('name', 'size', 'time').
        
        Returns:
            Dict: Result of executing the ls command.
        """
        command = ['ls']

        if long_format:
            command.append('-l')
        if all_files:
            command.append('-a')
        if sort_by:
            if sort_by == 'name':
                command.append('-X')
            elif sort_by == 'size':
                command.append('-S')
            elif sort_by == 'time':
                command.append('-t')

        command.append(path)
        return self._execute_command(command)

    def pwd(self) -> Dict:
        """Print working directory.
        
        Returns:
            Dict: Result of executing the pwd command.
        """

        result = self._execute_command(['pwd'])

        if result['success']:
            result['summary'] = {
                'current_directory': result['stdout'].strip()
            }
        return result

    def mkdir(self, dir_name: str, 
              parents: bool = False,
              verbose: bool = False,
              mode: Optional[int] = None) -> Dict:
        """Create a new directory.
        
        Args:
            dir_name (str): Name of the directory to create.
            parents (bool): If True, create parent directories if not exist.
            verbose (bool): If True, display detailed creation information.
            mode (Optional[int]): Permission mode for the new directory (e.g., 0o755).
        
        Returns:
            Dict: Result of executing the mkdir command.
        """
        command = ['mkdir']
        if parents:
            command.append('-p')
        if verbose:
            command.append('-v')
        if mode is not None:
            command.append(f'-m{mode:o}')
        
        command.append(dir_name)
        return self._execute_command(command)
    
    def touch(self, 
              file_name: str, 
              create_new: bool = False,
              verbose: bool = False) -> Dict:
        """Create a new file or update the timestamp of an existing file.
        
        Args:
            file_name (str): Name of the file to create/update.
            create_new (bool): If True, only create if the file does not exist.
            verbose (bool): If True, display detailed output.
        
        Returns:
            Dict: Result of executing the touch command.
        """
        command = ['touch']
        if create_new:
            command.append('-c')
        if verbose:
            command.append('-v')
        
        command.append(file_name)
        return self._execute_command(command)



