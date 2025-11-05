# Deployment Guide - Data Masking & Anonymization Tool

## Pre-Deployment Checklist

Before deploying, ensure you have:

- [ ] Python 3.8 or higher installed
- [ ] pip (Python package manager) available
- [ ] Sufficient disk space (minimum 100MB for dependencies)
- [ ] Network access (for initial package installation)
- [ ] Administrative/sudo privileges (for package installation)

---

## Installation Methods

### Method 1: Automated Setup (Recommended)

#### Linux / macOS
```bash
# Navigate to project directory
cd data-masking-tool

# Make setup script executable
chmod +x setup.sh

# Run setup
./setup.sh
```

#### Windows
```cmd
# Navigate to project directory
cd data-masking-tool

# Run setup
setup.bat
```

### Method 2: Manual Installation

#### Step 1: Install Python Dependencies
```bash
pip install pandas openpyxl Faker cryptography
```

Or use requirements file:
```bash
pip install -r requirements.txt
```

#### Step 2: Verify Installation
```bash
python -c "import pandas, openpyxl, faker, cryptography; print('All dependencies installed!')"
```

#### Step 3: Test Run
```bash
python data_masking_tool.py
```

### Method 3: Virtual Environment (Best Practice)

#### Linux / macOS
```bash
# Create virtual environment
python3 -m venv venv

# Activate virtual environment
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Run application
python data_masking_tool.py
```

#### Windows
```cmd
# Create virtual environment
python -m venv venv

# Activate virtual environment
venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run application
python data_masking_tool.py
```

---

## Post-Installation Verification

### Quick Test
```bash
# Run demonstration script
python test_demo.py
```

Expected output:
- Creates sample data (50 rows)
- Applies various masking types
- Generates comparison report
- Saves two CSV files: sample_original.csv and sample_masked.csv

### GUI Test
```bash
# Launch GUI application
python data_masking_tool.py
```

Verify:
1. Application window opens
2. All tabs are visible (Data Preview, Masking Rules, Processing, Results)
3. Menu bar is accessible
4. "Generate Sample Data" button works
5. Status bar shows "Ready"

---

## Deployment Scenarios

### Scenario 1: Single User Desktop

**Best For**: Individual developers, QA engineers

**Steps**:
1. Install Python 3.8+
2. Run automated setup (setup.sh or setup.bat)
3. Create desktop shortcut (optional)
4. Configure for personal use

**Shortcut Creation**:

Linux/macOS:
```bash
# Create shell script
cat > ~/Desktop/data-masking-tool.sh << 'EOF'
#!/bin/bash
cd /path/to/data-masking-tool
python data_masking_tool.py
EOF

chmod +x ~/Desktop/data-masking-tool.sh
```

Windows:
```
Right-click Desktop → New → Shortcut
Target: C:\Python\python.exe C:\path\to\data-masking-tool\data_masking_tool.py
```

### Scenario 2: Team Environment

**Best For**: Development teams, data teams

**Steps**:
1. Set up on shared network drive or server
2. Install Python on each workstation
3. Use virtual environment for isolation
4. Share masking rule templates (JSON files)
5. Document team-specific workflows

**Shared Configuration**:
```bash
# Network drive structure
\\server\shared\data-masking-tool\
├── app\                    # Application files
│   ├── data_masking_tool.py
│   └── requirements.txt
├── rules\                  # Shared rule templates
│   ├── gdpr_rules.json
│   ├── hipaa_rules.json
│   └── internal_rules.json
├── docs\                   # Documentation
│   ├── README.md
│   └── QUICK_START.md
└── logs\                   # Processing logs (optional)
```

### Scenario 3: Enterprise Deployment

**Best For**: Large organizations, regulated industries

**Steps**:
1. Security review and approval
2. Deploy to secure environment
3. Configure access controls
4. Set up audit logging
5. Create standard operating procedures (SOPs)
6. Train users
7. Monitor usage

**Enterprise Considerations**:
- **Access Control**: Restrict who can use masking tools
- **Audit Trail**: Log all masking operations
- **Key Management**: Use enterprise key management system
- **Data Classification**: Integrate with data classification tools
- **Compliance**: Ensure meets regulatory requirements
- **Support**: Establish internal support process

### Scenario 4: Cloud/Container Deployment

**Best For**: Cloud-native environments, CI/CD pipelines

**Docker Deployment** (Future):
```dockerfile
# Dockerfile (example for future implementation)
FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["python", "data_masking_tool.py"]
```

**Note**: GUI applications in Docker require X11 forwarding or VNC. Consider API version for containerization.

---

## Configuration

### Environment Variables (Optional)

```bash
# Set default batch size
export DATA_MASK_BATCH_SIZE=5000

# Set log level
export DATA_MASK_LOG_LEVEL=INFO

# Set default output directory
export DATA_MASK_OUTPUT_DIR=/path/to/outputs
```

### Configuration File (Future Enhancement)

Example `config.ini`:
```ini
[DEFAULT]
BatchSize = 1000
LogLevel = INFO
OutputDirectory = ./outputs

[Security]
KeyStorageLocation = ./keys
RequireKeyPassword = True

[Compliance]
EnableAuditLog = True
AuditLogPath = ./logs/audit.log
```

---

## Security Hardening

### Best Practices

1. **File Permissions**
   ```bash
   # Restrict access to application directory
   chmod 750 data-masking-tool
   
   # Protect key storage
   chmod 700 keys/
   chmod 600 keys/*.key
   ```

2. **Key Management**
   - Store keys in dedicated key management system
   - Use environment variables for keys (not hardcoded)
   - Rotate keys regularly
   - Limit key access to authorized personnel

3. **Audit Logging**
   ```python
   # Log masking operations
   import logging
   
   logging.basicConfig(
       filename='masking_audit.log',
       level=logging.INFO,
       format='%(asctime)s - %(user)s - %(action)s - %(fields)s'
   )
   ```

4. **Network Isolation**
   - Run on isolated network if handling sensitive data
   - Disable outbound network access if not needed
   - Use VPN for remote access

---

## Troubleshooting Deployment

### Common Issues

#### Issue: Python not found
```bash
# Check Python installation
which python3
python3 --version

# If not installed, install Python 3.8+
# Ubuntu/Debian
sudo apt update
sudo apt install python3 python3-pip

# macOS
brew install python3

# Windows: Download from python.org
```

#### Issue: pip not found
```bash
# Install pip
# Ubuntu/Debian
sudo apt install python3-pip

# macOS
python3 -m ensurepip

# Windows: Should be included with Python
```

#### Issue: Permission denied
```bash
# Use --user flag
pip install --user -r requirements.txt

# Or use virtual environment (recommended)
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

#### Issue: Package installation fails
```bash
# Update pip
pip install --upgrade pip

# Clear cache and retry
pip cache purge
pip install -r requirements.txt

# Install packages individually
pip install pandas
pip install openpyxl
pip install Faker
pip install cryptography
```

#### Issue: Tkinter not available
```bash
# Ubuntu/Debian
sudo apt install python3-tk

# macOS (usually included)
# May need to reinstall Python with Homebrew

# Windows (usually included)
# Ensure "tcl/tk and IDLE" was selected during Python installation
```

#### Issue: GUI doesn't open
```bash
# Check DISPLAY variable (Linux)
echo $DISPLAY

# If empty, set it
export DISPLAY=:0

# For remote sessions, use X11 forwarding
ssh -X user@host
```

---

## Maintenance

### Regular Tasks

**Weekly**:
- [ ] Review processing logs
- [ ] Check disk space
- [ ] Verify backups

**Monthly**:
- [ ] Update dependencies
- [ ] Review masking rules
- [ ] Audit key usage
- [ ] Check for software updates

**Quarterly**:
- [ ] Security review
- [ ] Performance optimization
- [ ] User training refresh
- [ ] Documentation updates

### Updating the Application

```bash
# Backup current installation
cp -r data-masking-tool data-masking-tool.backup

# Download new version
# Extract to data-masking-tool

# Install updated dependencies
pip install -r requirements.txt --upgrade

# Test with demo
python test_demo.py

# If successful, deploy
```

### Monitoring

**Key Metrics**:
- Processing time per file
- Memory usage
- Error rate
- User adoption
- Compliance adherence

**Logging**:
```python
# Enable detailed logging
import logging
logging.basicConfig(
    filename='data_masking.log',
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
```

---

## Backup and Recovery

### What to Backup

- **Application Files**: Keep copy of working version
- **Masking Rules**: Export and backup all rule configurations
- **Encryption Keys**: Secure backup in key management system
- **Reverse Mappings**: Backup if using reversible masking
- **Documentation**: Keep copies of custom procedures
- **Configuration**: Backup any custom configurations

### Backup Strategy

```bash
# Automated backup script
#!/bin/bash

BACKUP_DIR="/backup/data-masking-tool"
DATE=$(date +%Y%m%d)

# Create backup
tar -czf "$BACKUP_DIR/backup-$DATE.tar.gz" \
    data-masking-tool/ \
    --exclude='*.pyc' \
    --exclude='__pycache__'

# Encrypt backup
gpg --encrypt --recipient admin@company.com "$BACKUP_DIR/backup-$DATE.tar.gz"

# Remove old backups (keep last 30 days)
find "$BACKUP_DIR" -name "backup-*.tar.gz.gpg" -mtime +30 -delete
```

---

## Support and Documentation

### Getting Help

1. **Documentation**:
   - README.md - Comprehensive guide
   - QUICK_START.md - Fast setup guide
   - ARCHITECTURE.md - Technical details
   - This file - Deployment guidance

2. **Self-Service**:
   - Check processing logs for errors
   - Review troubleshooting section
   - Test with demo script

3. **Contact Support**:
   - Email: support@monteyai.com
   - Include: Error messages, logs, system info

### Training Resources

**For End Users**:
1. QUICK_START.md (5-minute intro)
2. README.md "Usage Guide" section
3. test_demo.py (hands-on example)

**For Administrators**:
1. ARCHITECTURE.md (technical details)
2. This deployment guide
3. LICENSE.md (policies)

**For Developers**:
1. Source code comments
2. ARCHITECTURE.md
3. Future API documentation

---

## Next Steps After Deployment

1. **Test with Sample Data**
   - Run test_demo.py
   - Generate sample data in GUI
   - Verify all masking types work

2. **Test with Real Data (Small)**
   - Select small dataset (<1000 rows)
   - Apply masking
   - Verify results manually

3. **Create Rule Templates**
   - Define standard masking rules
   - Export to JSON
   - Share with team

4. **Train Users**
   - Conduct training session
   - Provide quick reference guide
   - Set up support channel

5. **Monitor and Optimize**
   - Track usage patterns
   - Identify performance bottlenecks
   - Gather user feedback
   - Plan improvements

6. **Regular Review**
   - Quarterly compliance check
   - Update masking strategies
   - Review security practices

---

## Success Criteria

Deployment is successful when:

- ✅ Application runs without errors
- ✅ All dependencies installed correctly
- ✅ Users can load and mask data
- ✅ Export functions work properly
- ✅ Encryption keys generate successfully
- ✅ Performance meets expectations
- ✅ Users are trained
- ✅ Documentation is accessible
- ✅ Support process is established

---

## Rollback Plan

If deployment fails:

1. **Stop Application**
   ```bash
   pkill -f data_masking_tool.py
   ```

2. **Restore from Backup**
   ```bash
   rm -rf data-masking-tool
   tar -xzf backup.tar.gz
   ```

3. **Verify Previous Version**
   ```bash
   python test_demo.py
   ```

4. **Document Issues**
   - What failed
   - Error messages
   - System state
   - Steps to reproduce

5. **Contact Support**

---

**Deployment Guide Version**: 1.0  
**Last Updated**: November 2024  
**For**: Data Masking & Anonymization Tool v1.0.0

---

**Ready to Deploy?** Follow the checklist above and refer to README.md for usage instructions!
