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
        """Thay đổi thư mục hiện tại."""
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
           # Xoá đè quy dir ..
           recursive: bool = False,
           # Force xoá và không hỏi
           force: bool = False,
           interactive: bool = False,
           verbose: bool = False,
           dir_mode: bool = False) -> Dict:
        
        """Xoá tệp hoặc thư mục.
        Args:
            paths (List[str]): Danh sách các tệp hoặc thư mục cần xoá.
            (-r) recursive (bool): Nếu True, xoá đệ quy các thư mục.
            (-f) force (bool): Nếu True, bỏ qua các cảnh báo và lỗi.
            (-i) interactive (bool): Nếu True, hỏi xác nhận trước khi xoá.
            (-v) verbose (bool): Nếu True, hiển thị thông tin chi tiết khi xoá.
            (-d) dir_mode (bool): Nếu True, xoá thư mục thay vì tệp.
        Returns:
            Dict: Kết quả thực thi lệnh rm.
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
        """Thay đổi quyền truy cập của tệp hoặc thư mục.
        Args:
            path (str): Đường dẫn đến tệp hoặc thư mục.
            mode (str): Quyền truy cập mới (ví dụ: '755', 'u+rwx').
            recursive (bool): Nếu True, thay đổi quyền truy cập đệ quy.
            verbose (bool): Nếu True, hiển thị thông tin chi tiết khi thay đổi.
        
        Returns:
            Dict: Kết quả thực thi lệnh chmod.
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
        """Thay đổi chủ sở hữu và nhóm của tệp hoặc thư mục.
        Args:
            path (str): Đường dẫn đến tệp hoặc thư mục.
            owner (str): Chủ sở hữu mới.
            group (Optional[str]): Nhóm mới.
            recursive (bool): Nếu True, thay đổi đệ quy.
        Returns:
            Dict: Kết quả thực thi lệnh chown.
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
        """"Liệt kê các tiến trình đang chạy.
        Args:
            filter (Optional[str]): Lọc tiến trình theo tên hoặc PID.
            show_all (bool): Nếu True, hiển thị tất cả tiến trình.
            format_fields (Optional[List[str]]): Các trường để hiển thị.
        Returns:
            Dict: Kết quả thực thi lệnh ps.
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
            pid (int): Process ID to kill.
            signal (str): Signal to send (default is 'TERM').
        Returns:
            Dict: Kết quả thực thi lệnh kill.
        """
        command = ['kill', f'-{signal}', str(pid)]
        return self._execute_command(command)

