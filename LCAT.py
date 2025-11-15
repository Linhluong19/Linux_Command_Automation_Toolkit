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

    def cd(self, 
           path: str = None) -> Dict:
        """Change the current directory."""
        try: 
            if path is None or path == "~":
                path = os.path.expanduser("~")
            elif path == '.':
                # cd . -> Directory remains the same
                path = os.getcwd() 
            elif path == '..':
                path = os.path.dirname(os.getcwd())
            
            os.chdir(path)
            current = os.getcwd()
            result = {
                "command": f"cd {path}",
                "success": True,
                "summary": {
                    "current_directory": current,
                }
            }
        except Exception as e:
            return {
                "command": f"cd {path}",
                "success": False,
                "error": str(e)
            }
        self.history.append(result)
        return result
    
    def rm(self, 
           paths = List[str],
           # Recursively delete directory …
           recursive: bool = False,
           # Force delete without prompting.
           force: bool = False,
           interactive: bool = False,
           verbose: bool = False,
           dir_mode: bool = False) -> Dict:
        
        """Xoá tệp hoặc thư mục.
        Args:
            paths (List[str]): List of files or directories to delete.
            (-r) recursive (bool): If True, delete directories recursively.
            (-f) force (bool): If True, ignore warnings and errors during deletion.
            (-i) interactive (bool): If True, prompt for confirmation before deleting.
            (-v) verbose (bool): If True, display detailed output during deletion.
            (-d) dir_mode (bool): If True, treat the target as a directory rather than a file.
        Returns:
            Dict: The execution result returned by the rm operation
        """
        command = ['rm']
        if recursive:
            command.append('-r')
        if force:
            command.append('-f')
        if interactive:
            command.append('-i')
        if verbose:
            command.append('-v')
        if dir_mode:
            command.append('-d')
        
        command.extend(paths)
        return self._execute_command(command)

    def chmod(self, 
              path: str,
              mode: str,
              recursive: bool = False,
              verbose: bool = False) -> Dict:
        """Change the permissions of a file or directory.
        Args:
            path (str): The path to the file or directory.
            mode (str): The new permission setting (e.g., '755', 'u+rwx').
            recursive (bool): If True, apply the permission change recursively.
            verbose (bool): If True, display detailed output during the operation.
        
        Returns:
            Dict: The result of executing the chmod command.
        """
        command = ['chmod']
        if recursive:
            command.append('-r')
        if verbose:
            command.append('-v')
        
        command.extend([mode, path])

        return self._execute_command(command)
    
    def chown(self,
              path: str,
              owner: str,
              group: Optional[str] = None,
              recursive: bool = False) -> Dict:
        """Change the owner and group of a file or directory.

            Args:
                path (str): The path to the file or directory.
                owner (str): The new owner.
                group (Optional[str]): The new group.
                recursive (bool): If True, apply the change recursively.
            
            Returns:
                Dict: The result of executing the chown command.
            """

        command = ['chown']
        if recursive:
            command.append('-R')
        if group:
            command.append(f"{owner}:{group}")
        else:
            command.append(owner)
        
        command.append(path)
        return self._execute_command(command)
    
    def ps(self,
        filter: Optional[str] = None,
        show_all: bool = False,
        format_fields: Optional[List[str]] = None) -> Dict:
        """List running processes.

            Args:
                filter (Optional[str]): Filter processes by name or PID.
                show_all (bool): If True, display all processes.
                format_fields (Optional[List[str]]): Specific fields to display.
            
            Returns:
                Dict: The result of executing the ps command.
            """

        command = ['ps']
        if show_all:
            command.append('-e')
        if filter:
            command.extend(['-C', filter])
        if format_fields:
            command.extend(['-o', ','.join(format_fields)])

        return self._execute_command(command)
        
    def kill(self, pid: int, signal: str = 'TERM') -> Dict: 
        """Kill a process by PID.

            Args:
                pid (int): The Process ID to terminate.
                signal (str): The signal to send (default is 'TERM').
            
            Returns:
                Dict: The result of executing the kill command.
            """

        command = ['kill', f'-{signal}', str(pid)]
        return self._execute_command(command)

