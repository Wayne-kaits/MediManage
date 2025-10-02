#!/usr/bin/env python3
"""
Hospital Management System - Build Test Suite
Publisher: Kaitsnet IT Solutions
Comprehensive testing for Windows desktop application build
"""

import os
import sys
import json
import subprocess
import importlib
from pathlib import Path
from datetime import datetime

class BuildTester:
    """Test suite for build process"""
    
    def __init__(self):
        self.test_results = []
        self.total_tests = 0
        self.passed_tests = 0
        self.failed_tests = 0
        
        # Test configuration
        self.app_name = "Hospital Management System"
        self.app_version = "1.0.0"
        self.publisher = "Kaitsnet IT Solutions"
        
        # Required files
        self.required_files = [
            "desktop_app.py",
            "patient_management.py", 
            "appointment_management.py",
            "billing_management.py",
            "lab_management.py",
            "reports_management.py",
            "user_management.py",
            "setup.py",
            "build_installer.py",
            "requirements.txt"
        ]
        
        # Required imports
        self.required_imports = [
            ("tkinter", "Required"),
            ("sqlite3", "Required"),
            ("hashlib", "Required"),
            ("datetime", "Required"),
            ("pathlib", "Required"),
            ("json", "Required"),
            ("os", "Required"),
            ("sys", "Required"),
            ("tkcalendar", "Optional"),
            ("matplotlib", "Optional"),
            ("pandas", "Optional"),
            ("PIL", "Optional")
        ]
        
        # Config files
        self.config_files = [
            "build_config.json",
            "installer_config.json",
            "version_info.py",
            "BUILD_INSTRUCTIONS.md"
        ]
    
    def log_test(self, test_name, status, details=""):
        """Log test result"""
        self.total_tests += 1
        if status == "PASS":
            self.passed_tests += 1
            print(f"[PASS] {test_name}")
            if details:
                print(f"    Details: {details}")
        else:
            self.failed_tests += 1
            print(f"[FAIL] {test_name}")
            if details:
                print(f"    Details: {details}")
        
        self.test_results.append({
            "test": test_name,
            "status": status,
            "details": details
        })
    
    def test_python_availability(self):
        """Test Python availability"""
        try:
            version = sys.version
            self.log_test("Python available", "PASS", version)
            return True
        except Exception as e:
            self.log_test("Python available", "FAIL", str(e))
            return False
    
    def test_pyinstaller_availability(self):
        """Test PyInstaller availability"""
        try:
            import PyInstaller
            version = PyInstaller.__version__
            self.log_test("PyInstaller available", "PASS", version)
            return True
        except ImportError:
            self.log_test("PyInstaller available", "FAIL", "PyInstaller not installed")
            return False
    
    def test_source_files(self):
        """Test if all source files exist"""
        for file_name in self.required_files:
            file_path = Path(__file__).parent / file_name
            if file_path.exists():
                self.log_test(f"Source file: {file_name}", "PASS")
            else:
                self.log_test(f"Source file: {file_name}", "FAIL", f"File not found: {file_path}")
    
    def test_imports(self):
        """Test if required imports work"""
        for module_name, importance in self.required_imports:
            try:
                if module_name == "PIL":
                    import PIL
                    version = PIL.__version__
                elif module_name == "matplotlib":
                    import matplotlib
                    version = matplotlib.__version__
                elif module_name == "pandas":
                    import pandas
                    version = pandas.__version__
                elif module_name == "tkcalendar":
                    import tkcalendar
                    version = "1.6.1"  # Default version
                else:
                    module = importlib.import_module(module_name)
                    version = "Available"
                
                self.log_test(f"Import {module_name}", "PASS", f"{importance} - {version}")
            except ImportError as e:
                if importance == "Required":
                    self.log_test(f"Import {module_name}", "FAIL", f"{importance} - {str(e)}")
                else:
                    self.log_test(f"Import {module_name}", "FAIL", f"{importance} - will be included in build")
            except Exception as e:
                self.log_test(f"Import {module_name}", "FAIL", f"Error: {str(e)}")
    
    def test_config_files(self):
        """Test configuration files"""
        for file_name in self.config_files:
            file_path = Path(__file__).parent / file_name
            if file_path.exists():
                self.log_test(f"Config file: {file_name}", "PASS")
                
                # Test JSON validity for JSON files
                if file_name.endswith('.json'):
                    try:
                        with open(file_path, 'r') as f:
                            json.load(f)
                        self.log_test(f"JSON valid: {file_name}", "PASS")
                    except json.JSONDecodeError as e:
                        self.log_test(f"JSON valid: {file_name}", "FAIL", f"Invalid JSON: {str(e)}")
            else:
                self.log_test(f"Config file: {file_name}", "FAIL", f"File not found: {file_path}")
    
    def test_installer_file(self):
        """Test if installer file exists"""
        installer_name = f"HospitalManagementSystem_v{self.app_version}_Setup.exe"
        installer_path = Path(__file__).parent / "dist" / installer_name
        
        if installer_path.exists():
            self.log_test("Installer file exists", "PASS", str(installer_path))
            
            # Test installer properties
            try:
                size_mb = installer_path.stat().st_size / (1024 * 1024)
                self.log_test("Installer properties", "PASS", f"Size: {size_mb:.1f} MB")
            except Exception as e:
                self.log_test("Installer properties", "FAIL", f"Error reading properties: {str(e)}")
        else:
            self.log_test("Installer file exists", "FAIL", f"Not found: {installer_path}")
            self.log_test("Installer properties", "FAIL", "Installer not found")
    
    def test_build_process(self):
        """Test the build process"""
        print("\nTesting build process...")
        
        try:
            # Run build script
            build_script = Path(__file__).parent / "build_installer.py"
            if build_script.exists():
                result = subprocess.run([sys.executable, str(build_script)], 
                                      capture_output=True, text=True, timeout=300)
                
                if result.returncode == 0:
                    self.log_test("Build process", "PASS", "Build completed successfully")
                else:
                    self.log_test("Build process", "FAIL", f"Build failed: {result.stderr}")
            else:
                self.log_test("Build process", "FAIL", "Build script not found")
        except subprocess.TimeoutExpired:
            self.log_test("Build process", "FAIL", "Build timed out after 5 minutes")
        except Exception as e:
            self.log_test("Build process", "FAIL", f"Build error: {str(e)}")
    
    def generate_report(self):
        """Generate test report"""
        report = f"""Hospital Management System - Build Test Report
Publisher: {self.publisher}
Test Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
============================================================

"""
        
        for result in self.test_results:
            status = result["status"]
            test_name = result["test"]
            details = result["details"]
            
            report += f"[{status}] {test_name}\n"
            if details:
                report += f"    Details: {details}\n"
            report += "\n"
        
        # Summary
        success_rate = (self.passed_tests / self.total_tests * 100) if self.total_tests > 0 else 0
        
        report += f"""SUMMARY
--------------------
Total Tests: {self.total_tests}
Passed: {self.passed_tests}
Failed: {self.failed_tests}
Success Rate: {success_rate:.1f}%

"""
        
        # Recommendations
        if self.failed_tests > 0:
            report += "RECOMMENDATIONS\n"
            report += "---------------\n"
            
            for result in self.test_results:
                if result["status"] == "FAIL":
                    test_name = result["test"]
                    if "Import" in test_name and "matplotlib" in test_name:
                        report += f"• {test_name}: Install matplotlib with 'pip install matplotlib==3.7.2'\n"
                    elif "Import" in test_name and "PyInstaller" in test_name:
                        report += f"• {test_name}: Install PyInstaller with 'pip install pyinstaller'\n"
                    elif "Source file" in test_name:
                        report += f"• {test_name}: Ensure all source files are present in the directory\n"
                    elif "Installer file" in test_name:
                        report += f"• {test_name}: Run the build process to create the installer\n"
                    else:
                        report += f"• {test_name}: Check the specific error and resolve accordingly\n"
        
        return report
    
    def save_report(self, report):
        """Save test report to file"""
        report_file = Path(__file__).parent / "test_report.txt"
        with open(report_file, 'w') as f:
            f.write(report)
        print(f"\nTest report saved to: {report_file}")
    
    def run_all_tests(self):
        """Run all tests"""
        print(f"Running {self.app_name} Build Tests")
        print("=" * 50)
        
        # Basic tests
        self.test_python_availability()
        self.test_pyinstaller_availability()
        
        # File tests
        self.test_source_files()
        self.test_config_files()
        
        # Import tests
        self.test_imports()
        
        # Installer tests
        self.test_installer_file()
        
        # Build process test (optional)
        # self.test_build_process()
        
        # Generate and save report
        report = self.generate_report()
        print(report)
        self.save_report(report)
        
        return self.failed_tests == 0

def main():
    """Main test function"""
    tester = BuildTester()
    success = tester.run_all_tests()
    
    if success:
        print("\n✅ All tests passed! Build environment is ready.")
        return 0
    else:
        print(f"\n❌ {tester.failed_tests} test(s) failed. Please fix the issues above.")
        return 1

if __name__ == "__main__":
    exit(main())