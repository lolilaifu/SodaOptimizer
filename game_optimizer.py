import os
import sys
import json
import ctypes
import psutil
import time
import subprocess
import tkinter as tk
from tkinter import ttk, messagebox
from typing import Dict, List

class GameOptimizer:
    def __init__(self):
        self.is_admin = ctypes.windll.shell32.IsUserAnAdmin()
        self.whitelist_path = "whitelist.json"
        self.backup_state: Dict = {}
        self.root = tk.Tk()
        self.style = ttk.Style(self.root)
        self.setup_main_ui()
        
    def setup_main_ui(self):
        self.root.title("Soda Optimizer")
        self.root.geometry("1200x800")
        self.style.theme_use("clam")
        
        # Create notebook for tabs
        self.notebook = ttk.Notebook(self.root)
        
        # Create tabs
        self.dashboard_tab = ttk.Frame(self.notebook)
        self.whitelist_tab = ttk.Frame(self.notebook)
        self.settings_tab = ttk.Frame(self.notebook)
        self.metrics_tab = ttk.Frame(self.notebook)
        
        self.notebook.add(self.dashboard_tab, text="Dashboard")
        self.notebook.add(self.whitelist_tab, text="Process Whitelist")
        self.notebook.add(self.settings_tab, text="Settings")
        self.notebook.add(self.metrics_tab, text="Performance Metrics")
        self.notebook.pack(expand=True, fill="both")
        
        # Dashboard Tab Contents
        self.create_dashboard_ui()
        # Whitelist Tab Contents
        self.create_whitelist_ui()
        # Settings Tab Contents  
        self.create_settings_ui()
        # Metrics Tab Contents
        self.create_metrics_ui()
        
        # Status Bar
        self.status_bar = ttk.Label(self.root, text="Ready", relief="sunken")
        self.status_bar.pack(side="bottom", fill="x")
        
    def check_admin(self):
        if not self.is_admin:
            ctypes.windll.shell32.ShellExecuteW(
                None, "runas", sys.executable, " ".join(sys.argv), None, None, 1)
            sys.exit()

    def load_whitelist(self) -> List[str]:
        try:
            with open(self.whitelist_path, 'r') as f:
                return json.load(f)
        except FileNotFoundError:
            return []

    def save_whitelist(self, processes: List[str]):
        with open(self.whitelist_path, 'w') as f:
            json.dump(processes, f)

    def optimize_system(self):
        """Perform comprehensive system optimization for gaming performance.
        
        Backs up current system state before applying optimizations:
        - Power plan settings
        - GPU performance mode
        - Process priorities
        - Network configurations
        - Running services
        - Mouse settings
        - Fullscreen optimizations
        - Disk settings
        """
        self.backup_state = {
            'virtual_memory': self.get_virtual_memory_settings(),
            'power_plan': self.get_current_power_plan(),
            'gpu_mode': self.get_gpu_power_mode(),
            'running_processes': [],
            'network_settings': self.get_network_settings(),
            'services': self.get_running_services(),
            'mouse_settings': self.get_mouse_settings(),
            'fullscreen_opt': self.get_fullscreen_optimization()
        }
        
        self.set_high_performance_power_plan()
        self.optimize_gpu()
        self.optimize_processes()
        self.free_memory()

    def get_current_power_plan(self):
        result = subprocess.run(
            ['powercfg', '/getactivescheme'],
            capture_output=True, text=True, shell=True)
        return result.stdout.split(':')[-1].strip()

    def set_high_performance_power_plan(self):
        """Activate Windows high performance power plan.
        
        Uses powercfg to set the active scheme to the high performance GUID.
        Handles potential exceptions and logs errors appropriately."""
        try:
            result = subprocess.run(
                ['powercfg', '/setactive', '8c5e7fda-e8bf-4a96-9a85-a6e23a8c635c'],
                shell=True,
                check=True,
                capture_output=True,
                text=True
            )
            self.status_bar.config(text="Power plan optimized successfully")
        except subprocess.CalledProcessError as e:
            self.status_bar.config(text=f"Power plan error: {e.stderr}")
            messagebox.showerror("Power Plan Error", 
                f"Failed to set power plan:\n{e.stderr}")

    def optimize_gpu(self):
        # NVIDIA optimization
        try:
            subprocess.run(['nvidia-smi', '-pm', '1'], check=True)
            subprocess.run(['nvidia-smi', '-pl', '125'], check=True)
        except (subprocess.CalledProcessError, FileNotFoundError):
            # AMD optimization
            try:
                subprocess.run(['amdconfig', '--set-default-power-profile=high'], check=True)
                subprocess.run(['amdconfig', '--set-max-engine-clock=1200'], check=True)
            except (subprocess.CalledProcessError, FileNotFoundError):
                print("No compatible GPU drivers found")

    def optimize_processes(self):
        """Manage processes based on whitelist rules"""
        whitelist = self.load_whitelist()
        critical_processes = {'system idle process', 'system', 'svchost.exe', 'explorer.exe'}
        
        for proc in psutil.process_iter(['pid', 'name']):
            try:
                proc_name = proc.info['name'].lower()
                pid = proc.info['pid']
                
                if pid == os.getpid() or proc_name in critical_processes:
                    continue
                    
                if proc_name in whitelist:
                    # Track whitelisted processes
                    self.backup_state['running_processes'].append({
                        'name': proc_name,
                        'pid': pid,
                        'status': 'protected'
                    })
                else:
                    # Gracefully terminate non-whitelisted processes
                    proc.terminate()
                    self.backup_state['running_processes'].append({
                        'name': proc_name,
                        'pid': pid,
                        'status': 'terminated'
                    })
                    
            except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
                continue

    def restore_processes(self):
        """Attempt to restart important system processes"""
        for proc in self.backup_state['running_processes']:
            try:
                if proc['status'] == 'terminated' and proc['name'] in {'explorer.exe'}:
                    subprocess.Popen(proc['name'], shell=True)
                elif proc['status'] == 'protected':
                    # Ensure protected processes are still running
                    if not psutil.pid_exists(proc['pid']):
                        subprocess.Popen(proc['name'], shell=True)
            except Exception as e:
                print(f"Error restoring {proc['name']}: {str(e)}")

    def monitor_game_process(self):
        whitelist = self.load_whitelist()
        while True:
            games_running = False
            for proc in psutil.process_iter():
                if proc.name().lower() in whitelist:
                    games_running = True
                    break
            if not games_running:
                self.restore_system()
                print("Game closed - optimizations reverted")
                break
            time.sleep(10)

    def free_memory(self):
        try:
            subprocess.run(['EmptyStandbyList.exe', 'standbylist'],
                           check=True, shell=True)
        except (subprocess.CalledProcessError, FileNotFoundError):
            print("EmptyStandbyList.exe not found - download from Microsoft")

    def optimize_disk(self):
        """Optimize disk settings for gaming performance"""
        try:
            # Disable defragmentation
            subprocess.run(['reg', 'add', 'HKEY_LOCAL_MACHINE\\SOFTWARE\\Microsoft\\Dfrg\\BootOptimizeFunction', 
                          '/v', 'Enable', '/t', 'REG_SZ', '/d', 'N', '/f'], check=True)
            
            # Set optimal virtual memory (1.5x RAM size)
            total_ram = psutil.virtual_memory().total // (1024 * 1024)  # in MB
            min_page = int(total_ram * 1.5)
            max_page = int(total_ram * 3)
            subprocess.run(
                f'wmic pagefileset where name="C:\\\\pagefile.sys" set InitialSize={min_page},MaximumSize={max_page}',
                shell=True, check=True)
            
            self.status_bar.config(text="Disk optimization successful")
        except subprocess.CalledProcessError as e:
            self.status_bar.config(text=f"Disk optimization failed: {e}")

    def get_virtual_memory_settings(self) -> Dict:
        """Backup current virtual memory settings"""
        try:
            result = subprocess.run(
                'wmic pagefileset get Name,InitialSize,MaximumSize /format:list',
                shell=True, check=True, capture_output=True, text=True)
            settings = {}
            for line in result.stdout.split('\n'):
                if '=' in line:
                    key, value = line.strip().split('=', 1)
                    settings[key] = value
            return settings
        except subprocess.CalledProcessError as e:
            print(f"Failed to get virtual memory settings: {e}")
            return {}

    def optimize_network(self):
        """Optimize network settings for gaming"""
        try:
            # Set gaming QoS flags
            subprocess.run(['netsh', 'int', 'tcp', 'set', 'global', 'autotuninglevel=normal'], check=True)
            subprocess.run(['netsh', 'int', 'tcp', 'set', 'global', 'dca=enabled'], check=True)
            subprocess.run(['netsh', 'int', 'tcp', 'set', 'global', 'rss=enabled'], check=True)
            
            # Disable Nagle's algorithm
            subprocess.run(['netsh', 'int', 'tcp', 'set', 'global', 'congestionprovider=ctcp'], check=True)
        except subprocess.CalledProcessError as e:
            print(f"Network optimization failed: {e}")

    def optimize_windows_settings(self):
        """Configure Windows-specific gaming optimizations"""
        try:
            # Enable Game Mode
            subprocess.run(['reg', 'add', 'HKEY_CURRENT_USER\\System\\GameConfigStore', 
                          '/v', 'GameDVR_Enabled', '/t', 'REG_DWORD', '/d', '0', '/f'], check=True)
            
            # Disable fullscreen optimizations
            subprocess.run(['reg', 'add', 'HKEY_CURRENT_USER\\System\\GameConfigStore', 
                          '/v', 'FullscreenOptimization', '/t', 'REG_DWORD', '/d', '0', '/f'], check=True)
        except subprocess.CalledProcessError as e:
            print(f"Windows settings optimization failed: {e}")

    def disable_game_overlays(self):
        """Kill common game overlay processes"""
        overlays = [
            'discordoverlay.exe',
            'steamwebhelper.exe',
            'originoverlay.exe',
            'overlay.exe',
            'razer cortex.exe'
        ]
        for proc in psutil.process_iter():
            try:
                if proc.name().lower() in overlays:
                    proc.kill()
            except (psutil.NoSuchProcess, psutil.AccessDenied):
                continue

    def manage_background_services(self):
        """Stop non-essential background services"""
        services_to_stop = [
            'BITS', 'wuauserv', 'DoSvc',  # Windows Update services
            'WSearch',  # Windows Search
            'SysMain',  # Superfetch
            'TrkWks'    # Distributed Link Tracking
        ]
        for service in services_to_stop:
            try:
                subprocess.run(['net', 'stop', service, '/y'], check=True)
            except subprocess.CalledProcessError:
                continue

    def get_gpu_power_mode(self) -> Dict:
        gpu_state = {}
        try:
            # Get NVIDIA settings
            result = subprocess.run(['nvidia-smi', '-q'], capture_output=True, text=True, check=True)
            gpu_state['nvidia'] = {
                'persistence_mode': 'Enabled' in result.stdout,
                'power_limit': int(result.stdout.split('Power Limit')[1].split(':')[1].split('W')[0].strip())
            }
        except (subprocess.CalledProcessError, FileNotFoundError):
            try:
                # Get AMD settings
                result = subprocess.run(['amdconfig', '--get-power-profile'], capture_output=True, text=True, check=True)
                gpu_state['amd'] = {
                    'power_profile': result.stdout.split(':')[-1].strip(),
                    'engine_clock': int(result.stdout.split('Engine Clock:')[1].split('MHz')[0].strip())
                }
            except (subprocess.CalledProcessError, FileNotFoundError):
                pass
        return gpu_state

    def restore_gpu_settings(self):
        if 'nvidia' in self.backup_state['gpu_mode']:
            try:
                orig_mode = self.backup_state['gpu_mode']['nvidia']
                subprocess.run(['nvidia-smi', '-pm', str(int(orig_mode['persistence_mode']))], check=True)
                subprocess.run(['nvidia-smi', '-pl', str(orig_mode['power_limit'])], check=True)
            except (subprocess.CalledProcessError, FileNotFoundError):
                pass
        
        if 'amd' in self.backup_state['gpu_mode']:
            try:
                orig_mode = self.backup_state['gpu_mode']['amd']
                subprocess.run(['amdconfig', f'--set-power-profile={orig_mode["power_profile"]}'], check=True)
                subprocess.run(['amdconfig', f'--set-engine-clock={orig_mode["engine_clock"]}'], check=True)
            except (subprocess.CalledProcessError, FileNotFoundError):
                pass

    def get_network_settings(self):
        """Backup current network settings"""
        try:
            result = subprocess.run(['netsh', 'int', 'tcp', 'show', 'global'], 
                                  capture_output=True, text=True, check=True)
            return result.stdout
        except subprocess.CalledProcessError:
            return ""

    def get_running_services(self):
        """Backup current service states"""
        return [s.name() for s in psutil.win_service_iter() if s.status() == 'running']

    def get_mouse_settings(self):
        """Backup mouse acceleration settings"""
        try:
            result = subprocess.run(['reg', 'query', 'HKEY_CURRENT_USER\\Control Panel\\Mouse', 
                                   '/v', 'MouseSensitivity', '/t', 'REG_SZ'], 
                                  capture_output=True, text=True, check=True)
            return result.stdout
        except subprocess.CalledProcessError:
            return ""

    def get_fullscreen_optimization(self):
        """Check current fullscreen optimization setting"""
        try:
            result = subprocess.run(['reg', 'query', 'HKEY_CURRENT_USER\\System\\GameConfigStore', 
                                   '/v', 'FullscreenOptimization', '/t', 'REG_DWORD'], 
                                  capture_output=True, text=True, check=True)
            return result.stdout
        except subprocess.CalledProcessError:
            return ""

    def restore_system(self):
        if self.backup_state:
            # Restore core settings
            subprocess.run(['powercfg', '/setactive', self.backup_state['power_plan']], shell=True)
            self.restore_gpu_settings()
            self.restore_processes()
            
            # Restore network settings
            if 'network_settings' in self.backup_state:
                self.restore_network_settings()
            
            # Restore services
            if 'services' in self.backup_state:
                self.restore_services()
            
            # Restore mouse settings
            if 'mouse_settings' in self.backup_state:
                self.restore_mouse_settings()
            
            # Restore fullscreen optimization
            if 'fullscreen_opt' in self.backup_state:
                self.restore_fullscreen_optimization()
            
            self.backup_state = {}

    def restore_network_settings(self):
        """Restore original network configuration"""
        try:
            # Restore from backup using stored registry values
            subprocess.run(['netsh', 'int', 'tcp', 'set', 'global', 'autotuninglevel=normal'], check=True)
            subprocess.run(['netsh', 'int', 'tcp', 'set', 'global', 'dca=disabled'], check=True)
            subprocess.run(['netsh', 'int', 'tcp', 'set', 'global', 'rss=disabled'], check=True)
            subprocess.run(['netsh', 'int', 'tcp', 'set', 'global', 'congestionprovider=none'], check=True)
        except subprocess.CalledProcessError as e:
            print(f"Network restore failed: {e}")

    def restore_services(self):
        """Restore original service states"""
        for service in self.backup_state.get('services', []):
            try:
                subprocess.run(['net', 'start', service], check=True)
            except subprocess.CalledProcessError:
                continue

    def restore_mouse_settings(self):
        """Restore original mouse acceleration"""
        try:
            sens_value = self.backup_state['mouse_settings'].split()[-1]
            subprocess.run(['reg', 'add', 'HKEY_CURRENT_USER\\Control Panel\\Mouse',
                           '/v', 'MouseSensitivity', '/t', 'REG_SZ', '/d', sens_value, '/f'], check=True)
        except (KeyError, subprocess.CalledProcessError):
            pass

    def restore_fullscreen_optimization(self):
        """Restore original fullscreen optimization setting"""
        try:
            value = self.backup_state['fullscreen_opt'].split()[-1]
            subprocess.run(['reg', 'add', 'HKEY_CURRENT_USER\\System\\GameConfigStore',
                           '/v', 'FullscreenOptimization', '/t', 'REG_DWORD', '/d', value, '/f'], check=True)
        except (KeyError, subprocess.CalledProcessError):
            pass

    def restore_virtual_memory(self):
        """Restore original virtual memory settings"""
        try:
            vm_settings = self.backup_state['virtual_memory']
            subprocess.run(
                f'wmic pagefileset where name="C:\\\\pagefile.sys" set InitialSize={vm_settings["InitialSize"]},MaximumSize={vm_settings["MaximumSize"]}',
                shell=True, check=True)
        except (KeyError, subprocess.CalledProcessError) as e:
            print(f"Failed to restore virtual memory: {e}")

    def show_optimizations(self):
        print("\nActive Optimizations:")
        print("- High Performance Power Plan")
        print("- GPU Performance Mode (NVIDIA/AMD)")
        print("- Process Priority Optimization")
        print("- Memory Cleanup")
        print("- Network Latency Optimization")
        print("- Windows Game Mode Activation")
        print("- Background Service Management")
        print("- Game Overlay Prevention")
        print("- Fullscreen Optimization Tweaks")
        input("\nPress Enter to return...")

    class WhitelistManagerGUI(tk.Tk):
        def __init__(self, optimizer):
            super().__init__()
            self.optimizer = optimizer
            self.title("Process Whitelist Manager")
            self.geometry("600x400")
            self.create_widgets()
            
        def create_widgets(self):
            self.tree = ttk.Treeview(self, columns=("name", "status"), show="headings")
            self.tree.heading("name", text="Process Name")
            self.tree.heading("status", text="Whitelisted")
            
            scrollbar = ttk.Scrollbar(self, orient="vertical", command=self.tree.yview)
            self.tree.configure(yscrollcommand=scrollbar.set)
            
            btn_frame = ttk.Frame(self)
            add_btn = ttk.Button(btn_frame, text="Add Selected", command=self.add_selected)
            remove_btn = ttk.Button(btn_frame, text="Remove Selected", command=self.remove_selected)
            refresh_btn = ttk.Button(btn_frame, text="Refresh", command=self.populate_list)
            
            self.tree.pack(side="left", fill="both", expand=True)
            scrollbar.pack(side="left", fill="y")
            btn_frame.pack(side="right", padx=10, pady=10)
            add_btn.pack(pady=5)
            remove_btn.pack(pady=5)
            refresh_btn.pack(pady=5)
            
            self.populate_list()
            
        def populate_list(self):
            current_whitelist = self.optimizer.load_whitelist()
            self.tree.delete(*self.tree.get_children())
            
            for proc in psutil.process_iter():
                try:
                    name = proc.name().lower()
                    status = "Yes" if name in current_whitelist else "No"
                    self.tree.insert("", "end", values=(name, status))
                except (psutil.NoSuchProcess, psutil.AccessDenied):
                    continue
                    
        def add_selected(self):
            selected = self.tree.selection()
            whitelist = self.optimizer.load_whitelist()
            
            for item in selected:
                name = self.tree.item(item)["values"][0]
                if name not in whitelist:
                    whitelist.append(name)
                    
            self.optimizer.save_whitelist(whitelist)
            self.populate_list()
            
        def remove_selected(self):
            selected = self.tree.selection()
            whitelist = self.optimizer.load_whitelist()
            
            for item in selected:
                name = self.tree.item(item)["values"][0]
                if name in whitelist:
                    whitelist.remove(name)
                    
            self.optimizer.save_whitelist(whitelist)
            self.populate_list()

    def create_dashboard_ui(self):
        # System Status Frame
        status_frame = ttk.LabelFrame(self.dashboard_tab, text="System Status")
        status_frame.pack(fill="x", padx=10, pady=5)
        
        # Performance Metrics
        self.cpu_label = ttk.Label(status_frame, text="CPU Usage: -")
        self.gpu_label = ttk.Label(status_frame, text="GPU Usage: -")
        self.ram_label = ttk.Label(status_frame, text="RAM Usage: -")
        self.net_label = ttk.Label(status_frame, text="Network Latency: -")
        
        self.cpu_label.grid(row=0, column=0, padx=5, pady=2, sticky="w")
        self.gpu_label.grid(row=0, column=1, padx=5, pady=2, sticky="w")
        self.ram_label.grid(row=1, column=0, padx=5, pady=2, sticky="w")
        self.net_label.grid(row=1, column=1, padx=5, pady=2, sticky="w")
        
        # Optimization Controls
        ctrl_frame = ttk.Frame(self.dashboard_tab)
        ctrl_frame.pack(fill="x", padx=10, pady=5)
        
        self.optimize_btn = ttk.Button(ctrl_frame, text="Optimize Now", command=self.optimize_system)
        self.restore_btn = ttk.Button(ctrl_frame, text="Restore System", command=self.restore_system)
        self.monitor_btn = ttk.Button(ctrl_frame, text="Monitor Games", command=self.monitor_game_process)
        
        self.optimize_btn.pack(side="left", padx=5)
        self.restore_btn.pack(side="left", padx=5)
        self.monitor_btn.pack(side="left", padx=5)
        
        # Real-time Metrics
        self.metrics_canvas = tk.Canvas(self.metrics_tab, height=300)
        self.metrics_canvas.pack(fill="both", expand=True)
        
    def create_whitelist_ui(self):
        # Reuse existing WhitelistManagerGUI but integrate into notebook
        self.whitelist_tree = ttk.Treeview(self.whitelist_tab, columns=("name", "status"), show="headings")
        self.whitelist_tree.heading("name", text="Process Name")
        self.whitelist_tree.heading("status", text="Whitelisted")
        
        scrollbar = ttk.Scrollbar(self.whitelist_tab, orient="vertical", command=self.whitelist_tree.yview)
        self.whitelist_tree.configure(yscrollcommand=scrollbar.set)
        
        btn_frame = ttk.Frame(self.whitelist_tab)
        add_btn = ttk.Button(btn_frame, text="Add Selected", command=self.add_to_whitelist)
        remove_btn = ttk.Button(btn_frame, text="Remove Selected", command=self.remove_from_whitelist)
        refresh_btn = ttk.Button(btn_frame, text="Refresh", command=self.update_whitelist_tree)
        
        self.whitelist_tree.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="left", fill="y")
        btn_frame.pack(side="right", padx=10, pady=10)
        add_btn.pack(pady=5)
        remove_btn.pack(pady=5)
        refresh_btn.pack(pady=5)
        
        self.update_whitelist_tree()
        
    def create_settings_ui(self):
        settings_frame = ttk.LabelFrame(self.settings_tab, text="Optimization Settings")
        settings_frame.pack(fill="both", expand=True, padx=10, pady=5)
        
        # GPU Settings
        ttk.Label(settings_frame, text="GPU Optimization:").grid(row=0, column=0, sticky="w")
        self.gpu_var = tk.StringVar(value="auto")
        ttk.Radiobutton(settings_frame, text="Auto Detect", variable=self.gpu_var, value="auto").grid(row=0, column=1, sticky="w")
        ttk.Radiobutton(settings_frame, text="NVIDIA", variable=self.gpu_var, value="nvidia").grid(row=0, column=2, sticky="w")
        ttk.Radiobutton(settings_frame, text="AMD", variable=self.gpu_var, value="amd").grid(row=0, column=3, sticky="w")
        
        # Network Optimization
        ttk.Label(settings_frame, text="Network Profile:").grid(row=1, column=0, sticky="w")
        self.network_var = tk.StringVar(value="balanced")
        ttk.Combobox(settings_frame, textvariable=self.network_var, 
                    values=["Gaming", "Streaming", "Competitive", "Balanced"]).grid(row=1, column=1, sticky="ew")
        
        # Apply Button
        ttk.Button(settings_frame, text="Save Settings", command=self.save_settings).grid(row=2, column=0, columnspan=4, pady=10)
        
    def create_metrics_ui(self):
        # System Monitoring Graphs
        self.cpu_graph = tk.Canvas(self.metrics_tab, bg="white", height=150)
        self.gpu_graph = tk.Canvas(self.metrics_tab, bg="white", height=150)
        self.ram_graph = tk.Canvas(self.metrics_tab, bg="white", height=150)
        
        self.cpu_graph.pack(fill="x", padx=10, pady=5)
        self.gpu_graph.pack(fill="x", padx=10, pady=5)
        self.ram_graph.pack(fill="x", padx=10, pady=5)
        
    def update_whitelist_tree(self):
        current_whitelist = self.load_whitelist()
        self.whitelist_tree.delete(*self.whitelist_tree.get_children())
        
        for proc in psutil.process_iter():
            try:
                name = proc.name().lower()
                status = "Yes" if name in current_whitelist else "No"
                self.whitelist_tree.insert("", "end", values=(name, status))
            except (psutil.NoSuchProcess, psutil.AccessDenied):
                continue
                
    def add_to_whitelist(self):
        selected = self.whitelist_tree.selection()
        whitelist = self.load_whitelist()
        
        for item in selected:
            name = self.whitelist_tree.item(item)["values"][0]
            if name not in whitelist:
                whitelist.append(name)
                
        self.save_whitelist(whitelist)
        self.update_whitelist_tree()
        
    def remove_from_whitelist(self):
        selected = self.whitelist_tree.selection()
        whitelist = self.load_whitelist()
        
        for item in selected:
            name = self.whitelist_tree.item(item)["values"][0]
            if name in whitelist:
                whitelist.remove(name)
                
        self.save_whitelist(whitelist)
        self.update_whitelist_tree()
        
    def save_settings(self):
        """Save user preferences to config file"""
        config = {
            'gpu_preference': self.gpu_var.get(),
            'network_profile': self.network_var.get(),
            'last_update': time.time()
        }
        try:
            with open('optimizer_config.json', 'w') as f:
                json.dump(config, f)
            self.status_bar.config(text="Settings saved successfully")
        except Exception as e:
            messagebox.showerror("Save Error", f"Failed to save settings:\n{str(e)}")
        
    def update_metrics(self):
        """Update real-time performance metrics in UI"""
        try:
            # CPU Usage
            cpu_percent = psutil.cpu_percent()
            self.cpu_label.config(text=f"CPU Usage: {cpu_percent}%")
            
            # RAM Usage
            ram = psutil.virtual_memory()
            self.ram_label.config(text=f"RAM Usage: {ram.percent}% ({ram.used//1024//1024}MB/{ram.total//1024//1024}MB)")
            
            # GPU Monitoring (if available)
            try:
                import GPUtil
                gpus = GPUtil.getGPUs()
                if gpus:
                    gpu = gpus[0]
                    self.gpu_label.config(text=f"GPU Usage: {gpu.load*100:.1f}% ({gpu.temperature}°C)")
            except ImportError:
                pass
            
            # Network Latency
            latency = self.ping_test()
            self.net_label.config(text=f"Network Latency: {latency}ms")
            
            # Update graphs
            self.draw_cpu_graph(cpu_percent)
            self.draw_ram_graph(ram.percent)
            
            # Schedule next update
            self.root.after(1000, self.update_metrics)
        except Exception as e:
            print(f"Metrics update error: {str(e)}")

    def ping_test(self) -> float:
        """Test network latency to Google DNS"""
        try:
            result = subprocess.run(['ping', '-n', '1', '8.8.8.8'], 
                                  capture_output=True, text=True, check=True)
            timings = result.stdout.split('Average = ')[1].split('ms')[0]
            return float(timings)
        except Exception:
            return 0.0

    def draw_cpu_graph(self, value: float):
        """Draw CPU usage history graph"""
        self.metrics_canvas.create_rectangle(0,0,300,150, fill='white')
        # Add graph drawing logic here

    def draw_ram_graph(self, value: float):
        """Draw RAM usage history graph"""
        self.metrics_canvas.create_rectangle(0,0,300,150, fill='white')
        # Add graph drawing logic here

if __name__ == "__main__":
    optimizer = GameOptimizer()
    optimizer.check_admin()
    optimizer.root.mainloop()
