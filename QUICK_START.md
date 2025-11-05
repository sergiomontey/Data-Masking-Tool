# Quick Start Guide - Data Masking Tool

## 5-Minute Getting Started

### Step 1: Install (2 minutes)
```bash
# Install dependencies
pip install -r requirements.txt

# Run the application
python data_masking_tool.py
```

### Step 2: Try It Out (3 minutes)

1. **Generate Sample Data**
   - Click "Generate Sample Data" button
   - You'll get 50 rows with names, emails, phones, SSNs, etc.

2. **Apply Quick Masking**
   - Go to "Masking Rules" tab
   - Select all fields (Ctrl+A or Cmd+A)
   - Choose "Fake Data Replacement"
   - Click "Add Rule"

3. **Process & View**
   - Go to "Processing" tab
   - Click "Apply Masking Rules"
   - Go to "Results" tab to see masked data

4. **Compare**
   - Click "Compare Original vs Masked"
   - See side-by-side comparison

That's it! You've masked your first dataset.

## Common Workflows

### Workflow 1: Quick Anonymization
```
Load Data → Select All Fields → Choose "Fake Data" → Apply → Save
```

### Workflow 2: Selective Masking
```
Load Data → Select Specific Fields → Configure Each → Apply → Save
```

### Workflow 3: GDPR Compliance
```
Load Data → Mask PII Fields → Hash IDs → Save + Export Rules
```

### Workflow 4: Reversible Testing
```
Load Data → Generate Key → Use "Reversible" → Apply → Export Mapping
```

## Field Selection Tips

### Keyboard Shortcuts
- `Ctrl+Click` / `Cmd+Click`: Select multiple fields
- `Shift+Click`: Select range of fields
- `Ctrl+A` / `Cmd+A`: Select all fields

### Smart Selection
1. **PII Fields**: email, phone, ssn, name
2. **Sensitive**: salary, address, DOB
3. **Identifiers**: employee_id, customer_id

## Masking Strategy Guide

### For Different Data Types

**Text Fields (names, addresses)**
- Use: Fake Data Replacement or Partial Masking
- Why: Maintains readability while protecting privacy

**Email Addresses**
- Use: Email Masking
- Why: Shows format but hides identity

**Phone Numbers**
- Use: Phone Masking
- Why: Keeps last 4 digits for reference

**IDs/Keys**
- Use: Hash (One-way)
- Why: Consistent, irreversible, unique

**Dates**
- Use: Date Shifting
- Why: Maintains relationships while changing values

**Numbers (salary, amounts)**
- Use: Number Randomization
- Why: Preserves range while changing exact values

**Highly Sensitive**
- Use: Full Masking or Reversible
- Why: Maximum protection with optional recovery

## Pro Tips

### 1. Test First
Always run on sample data before production:
```
Generate Sample Data → Configure → Test → Verify → Apply to Real Data
```

### 2. Save Your Rules
Export rules for reuse:
```
File → Export Rules → Save as "pii_masking_rules.json"
```

### 3. Document Your Keys
For reversible masking:
```
1. Generate Key
2. Screenshot or copy to secure location
3. Never commit to version control
4. Share via secure channel only
```

### 4. Batch Large Files
For files > 100k rows:
```
Enable Batch Processing → Set size to 5000 → Monitor progress
```

### 5. Verify Results
Always check:
```
Compare Original vs Masked → Spot check random rows → Verify format
```

## Real-World Examples

### Example 1: Customer Database
```json
{
  "customer_name": {"type": "Fake Data Replacement"},
  "email": {"type": "Email Masking"},
  "phone": {"type": "Phone Masking"},
  "credit_card": {"type": "Full Masking (****)"},
  "address": {"type": "Partial Masking", "options": {"keep_first": 0, "keep_last": 5}}
}
```

### Example 2: Employee Records
```json
{
  "employee_id": {"type": "Hash (One-way)"},
  "full_name": {"type": "Fake Data Replacement"},
  "ssn": {"type": "SSN Masking"},
  "salary": {"type": "Number Randomization"},
  "hire_date": {"type": "Date Shifting", "options": {"shift_days": 90}}
}
```

### Example 3: Medical Records (Reversible)
```json
{
  "patient_id": {"type": "Reversible (with key)", "options": {"key": "your-key"}},
  "patient_name": {"type": "Reversible (with key)", "options": {"key": "your-key"}},
  "diagnosis": {"type": "Reversible (with key)", "options": {"key": "your-key"}},
  "dob": {"type": "Date Shifting", "options": {"shift_days": 180}}
}
```

## Troubleshooting Quick Fixes

### Problem: Can't see my fields
**Fix**: Make sure data is loaded (check Data Preview tab)

### Problem: Masking is too slow
**Fix**: Enable batch processing, increase batch size

### Problem: Need to recover data
**Fix**: Use "Export Reverse Mapping" (only works with Reversible masking)

### Problem: Wrong masking applied
**Fix**: Clear rules and start over, or remove specific rule

### Problem: File won't load
**Fix**: Check file format (CSV or Excel), ensure no password protection

## Next Steps

1. ✅ Complete this quick start
2. 📖 Read full README.md for advanced features
3. 🧪 Test with your own data
4. 💾 Save your masking configurations
5. 🔒 Set up secure key management

## Need More Help?

- Check the README.md for detailed documentation
- Review the processing log for error details
- Test with sample data to understand behavior

---

**Remember**: Always verify masked data before using in production!
