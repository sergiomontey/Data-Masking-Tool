"""
Test script for Data Masking & Anonymization Tool
Demonstrates various masking techniques programmatically
"""

import pandas as pd
from faker import Faker
import hashlib
from cryptography.fernet import Fernet

def create_sample_data():
    """Create sample dataset for testing"""
    faker = Faker()
    
    data = {
        'employee_id': [f'EMP{i:04d}' for i in range(1, 21)],
        'first_name': [faker.first_name() for _ in range(20)],
        'last_name': [faker.last_name() for _ in range(20)],
        'email': [faker.email() for _ in range(20)],
        'phone': [faker.phone_number() for _ in range(20)],
        'ssn': [faker.ssn() for _ in range(20)],
        'salary': [faker.random_int(40000, 150000) for _ in range(20)],
        'date_of_birth': [faker.date_of_birth(minimum_age=25, maximum_age=65) for _ in range(20)],
        'address': [faker.address().replace('\n', ', ') for _ in range(20)],
        'department': [faker.random_element(['Engineering', 'Sales', 'Marketing', 'HR', 'Finance']) for _ in range(20)]
    }
    
    return pd.DataFrame(data)

def full_mask(value):
    """Full masking - replace all with asterisks"""
    return '*' * len(str(value))

def partial_mask(value, keep_first=0, keep_last=4):
    """Partial masking - keep first and last characters"""
    s = str(value)
    if len(s) <= keep_first + keep_last:
        return '*' * len(s)
    return s[:keep_first] + '*' * (len(s) - keep_first - keep_last) + s[-keep_last:]

def email_mask(email):
    """Mask email keeping format"""
    if '@' in email:
        local, domain = email.split('@', 1)
        if len(local) > 2:
            masked_local = local[0] + '*' * (len(local) - 2) + local[-1]
        else:
            masked_local = '*' * len(local)
        return f"{masked_local}@{domain}"
    return '*' * len(email)

def phone_mask(phone):
    """Mask phone keeping last 4 digits"""
    digits = ''.join(filter(str.isdigit, str(phone)))
    if len(digits) >= 4:
        return '*' * (len(str(phone)) - 4) + str(phone)[-4:]
    return '*' * len(str(phone))

def ssn_mask(ssn):
    """Mask SSN keeping last 4 digits"""
    digits = ''.join(filter(str.isdigit, str(ssn)))
    if len(digits) >= 4:
        return '***-**-' + digits[-4:]
    return '*' * len(str(ssn))

def hash_value(value):
    """One-way hash"""
    return hashlib.sha256(str(value).encode()).hexdigest()[:16]

def demonstrate_masking():
    """Demonstrate various masking techniques"""
    print("=" * 80)
    print("DATA MASKING & ANONYMIZATION TOOL - DEMONSTRATION")
    print("=" * 80)
    print()
    
    # Create sample data
    print("1. Creating sample data...")
    df = create_sample_data()
    print(f"   Created {len(df)} employee records")
    print()
    
    # Display original data
    print("2. Original Data (first 5 rows):")
    print("-" * 80)
    print(df.head().to_string())
    print()
    
    # Create masked dataframe
    print("3. Applying masking rules...")
    masked_df = df.copy()
    
    # Apply different masking strategies
    print("   - Hashing employee_id")
    masked_df['employee_id'] = df['employee_id'].apply(hash_value)
    
    print("   - Masking first_name (full)")
    masked_df['first_name'] = df['first_name'].apply(full_mask)
    
    print("   - Masking last_name (partial)")
    masked_df['last_name'] = df['last_name'].apply(lambda x: partial_mask(x, 1, 1))
    
    print("   - Masking email (format-preserving)")
    masked_df['email'] = df['email'].apply(email_mask)
    
    print("   - Masking phone (keep last 4)")
    masked_df['phone'] = df['phone'].apply(phone_mask)
    
    print("   - Masking SSN (keep last 4)")
    masked_df['ssn'] = df['ssn'].apply(ssn_mask)
    
    print("   - Masking salary (full)")
    masked_df['salary'] = df['salary'].apply(full_mask)
    
    print("   - Masking address (partial)")
    masked_df['address'] = df['address'].apply(lambda x: partial_mask(x, 0, 10))
    
    print("   - Date of birth shifted by 30 days")
    masked_df['date_of_birth'] = pd.to_datetime(df['date_of_birth']) + pd.Timedelta(days=30)
    
    print()
    
    # Display masked data
    print("4. Masked Data (first 5 rows):")
    print("-" * 80)
    print(masked_df.head().to_string())
    print()
    
    # Show comparison
    print("5. Side-by-Side Comparison (Row 1):")
    print("-" * 80)
    print(f"{'Field':<20} {'Original':<35} {'Masked':<35}")
    print("-" * 80)
    for col in df.columns:
        orig = str(df[col].iloc[0])[:30]
        mask = str(masked_df[col].iloc[0])[:30]
        print(f"{col:<20} {orig:<35} {mask:<35}")
    print()
    
    # Statistics
    print("6. Masking Statistics:")
    print("-" * 80)
    print(f"   Total records processed: {len(df)}")
    print(f"   Fields masked: {len(df.columns)}")
    print(f"   Original data size: {df.memory_usage(deep=True).sum() / 1024:.2f} KB")
    print(f"   Masked data size: {masked_df.memory_usage(deep=True).sum() / 1024:.2f} KB")
    print()
    
    # Save results
    print("7. Saving results...")
    df.to_csv('/home/claude/sample_original.csv', index=False)
    masked_df.to_csv('/home/claude/sample_masked.csv', index=False)
    print("   ✓ Original data saved to: sample_original.csv")
    print("   ✓ Masked data saved to: sample_masked.csv")
    print()
    
    print("=" * 80)
    print("DEMONSTRATION COMPLETE")
    print("=" * 80)
    print()
    print("Next steps:")
    print("1. Run 'python data_masking_tool.py' to use the GUI application")
    print("2. Load sample_original.csv to see the data")
    print("3. Configure your own masking rules")
    print("4. Compare with sample_masked.csv to see results")
    print()

if __name__ == "__main__":
    demonstrate_masking()