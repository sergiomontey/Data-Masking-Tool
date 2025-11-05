# Data Masking Tool - Architecture & Technical Documentation

## System Architecture

### High-Level Architecture

```
┌─────────────────────────────────────────────────────────┐
│                    User Interface (Tkinter)              │
│  ┌──────────┬──────────┬────────────┬─────────────┐    │
│  │  Data    │ Masking  │ Processing │   Results   │    │
│  │ Preview  │  Rules   │            │             │    │
│  └──────────┴──────────┴────────────┴─────────────┘    │
└─────────────────────────────────────────────────────────┘
                          ▼
┌─────────────────────────────────────────────────────────┐
│              Core Application Logic                      │
│  ┌──────────────────────────────────────────────────┐  │
│  │  Data Loading │ Rule Management │ Processing     │  │
│  └──────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────┘
                          ▼
┌─────────────────────────────────────────────────────────┐
│                 Masking Engine                           │
│  ┌──────────────────────────────────────────────────┐  │
│  │  Full  │ Partial │ Fake │ Hash │ Encrypt │ etc.  │  │
│  └──────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────┘
                          ▼
┌─────────────────────────────────────────────────────────┐
│              External Libraries                          │
│  ┌──────────────────────────────────────────────────┐  │
│  │ Pandas │ Faker │ Cryptography │ OpenPyXL        │  │
│  └──────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────┘
```

## Component Breakdown

### 1. User Interface Layer

**Technology**: Tkinter (Python standard library)

**Components**:
- **Main Window**: Root application window with menu bar
- **Tab Navigation**: 4-tab notebook interface
  - Data Preview Tab
  - Masking Rules Tab
  - Processing Tab
  - Results Tab
- **Status Bar**: Real-time status updates
- **Dialogs**: File selection, confirmations, error messages

**Key Features**:
- Responsive layout with expandable panels
- Scrollable text areas for large data
- Progress indicators
- Keyboard shortcuts support

### 2. Data Management Layer

**Responsibilities**:
- File I/O operations (CSV, Excel)
- Data validation and preprocessing
- Memory management for large datasets
- Sample data generation

**Key Classes/Methods**:
```python
- load_csv(): Import CSV files
- load_excel(): Import Excel files
- generate_sample_data(): Create test datasets
- update_data_view(): Refresh UI with current data
- save_masked_data(): Export processed data
```

**Data Flow**:
```
User File → Pandas DataFrame → In-Memory Processing → Output File
```

### 3. Rule Management Layer

**Responsibilities**:
- Define masking rules per field
- Store rule configurations
- Import/Export rule templates
- Validate rule compatibility

**Rule Structure**:
```json
{
  "field_name": {
    "type": "masking_type",
    "options": {
      "key": "value"
    }
  }
}
```

**Supported Rule Types**:
1. Full Masking
2. Partial Masking
3. Format-Preserving Encryption
4. Fake Data Replacement
5. Hash (One-way)
6. Reversible (with key)
7. Email Masking
8. Phone Masking
9. SSN Masking
10. Date Shifting
11. Number Randomization

### 4. Masking Engine

**Core Function**: `mask_value(value, rule, field_name)`

**Processing Pipeline**:
```
Input Value → Type Detection → Rule Application → Output Value
```

**Masking Algorithms**:

#### Full Masking
- Replace all characters with asterisks
- Maintains string length
- Use case: Credit cards, passwords

#### Partial Masking
- Keep first N and last M characters
- Mask middle section
- Use case: Account numbers, IDs

#### Fake Data Replacement
- Intelligent field detection
- Context-aware fake data
- Use case: Names, addresses, emails

#### Hash (One-way)
- SHA-256 hashing
- Truncated to 16 characters
- Irreversible transformation
- Use case: Unique identifiers

#### Format-Preserving Encryption
- Fernet symmetric encryption
- Maintains data type
- Reversible with key
- Use case: Sensitive data with recovery needs

#### Email Masking
- Format: `j***n@example.com`
- Preserves domain
- Masks username intelligently

#### Phone Masking
- Keeps last 4 digits
- Masks remaining characters
- Format: `***-***-4567`

#### SSN Masking
- Standard format: `***-**-6789`
- Keeps last 4 digits
- GDPR/HIPAA compliant

#### Date Shifting
- Shifts dates by N days
- Maintains date format
- Preserves temporal relationships

#### Number Randomization
- Adds random noise (±10%)
- Maintains realistic ranges
- Preserves statistical properties

### 5. Encryption & Security Layer

**Components**:
- Key generation (Fernet)
- Symmetric encryption
- Hash generation
- Secure key storage recommendations

**Security Features**:
```python
- generate_key(): Create cryptographic keys
- Fernet encryption for reversible masking
- SHA-256 hashing for one-way operations
- Secure random number generation
```

**Key Management**:
- Keys stored separately from data
- User-controlled key generation
- Optional key export
- Reverse mapping for decryption

### 6. Batch Processing Layer

**Features**:
- Configurable batch sizes
- Progress tracking
- Memory-efficient processing
- Large file support (millions of rows)

**Processing Strategy**:
```python
if batch_processing_enabled:
    for chunk in chunked_dataframe(batch_size):
        process_chunk(chunk)
        update_progress()
else:
    process_all_at_once()
```

## Data Flow Diagrams

### Complete Processing Flow

```
┌─────────────┐
│  Load Data  │
└──────┬──────┘
       ▼
┌─────────────────┐
│  Validate Data  │
└──────┬──────────┘
       ▼
┌─────────────────────┐
│  Configure Rules    │
│  (per field)        │
└──────┬──────────────┘
       ▼
┌─────────────────────┐
│  Apply Masking      │
│  (batch or full)    │
└──────┬──────────────┘
       ▼
┌─────────────────────┐
│  Generate Outputs   │
│  - Masked Data      │
│  - Reverse Mapping  │
│  - Rules Export     │
└─────────────────────┘
```

### Masking Process per Row

```
For each row in dataset:
  For each field with masking rule:
    1. Get field value
    2. Check if null/empty
    3. Apply masking algorithm
    4. Store reverse mapping (if applicable)
    5. Update masked dataframe
  Next field
Next row
```

## Performance Considerations

### Memory Management

**Strategies**:
- Chunked processing for large files
- Garbage collection between batches
- Efficient data types (Pandas optimization)
- Lazy evaluation where possible

**Benchmarks** (approximate):
- Small files (<10K rows): <1 second
- Medium files (10K-100K rows): 5-30 seconds
- Large files (100K-1M rows): 30-180 seconds
- Very large files (>1M rows): Use batch processing

### Optimization Techniques

1. **Vectorized Operations**: Use Pandas apply() instead of loops
2. **Type Inference**: Automatic data type detection
3. **Selective Column Loading**: Load only necessary columns
4. **Batch Processing**: Process in chunks for memory efficiency
5. **Parallel Processing**: Future enhancement for multi-core

## Security Architecture

### Threat Model

**Protected Against**:
- Accidental data exposure
- Unauthorized data access
- Data correlation attacks
- Pattern-based re-identification

**User Responsibilities**:
- Secure key storage
- Access control to reverse mappings
- Secure disposal of original data
- Compliance verification

### Encryption Flow

```
Original Data → Encryption Key → Fernet Cipher → Encrypted Data
                       ↓
              Reverse Mapping Storage
                       ↓
              Secure Key Storage
```

### Best Practices Implemented

1. **Key Generation**: Cryptographically secure random keys
2. **Separation of Concerns**: Keys stored separately from data
3. **Hashing**: One-way SHA-256 for irreversible masking
4. **Format Preservation**: Maintain data usability
5. **Audit Trail**: Processing logs for compliance

## Extensibility

### Adding New Masking Types

```python
# In mask_value() method:
elif masking_type == 'Custom Type':
    # Implement custom logic
    return custom_mask_function(value, options)
```

### Plugin Architecture (Future)

```python
# Proposed structure
class MaskingPlugin:
    def mask(self, value, options):
        pass
    
    def unmask(self, value, key):
        pass
```

## Error Handling

### Strategy

1. **Graceful Degradation**: Continue processing on non-critical errors
2. **User Feedback**: Clear error messages with remediation steps
3. **Logging**: Detailed process logs for debugging
4. **Validation**: Pre-process validation to catch issues early

### Common Errors & Handling

```python
try:
    # Data processing
except FileNotFoundError:
    # Show file selection dialog
except pd.errors.EmptyDataError:
    # Alert user about empty file
except MemoryError:
    # Suggest batch processing
except Exception as e:
    # Log error and show user-friendly message
```

## Testing Strategy

### Unit Tests (Future Enhancement)

```python
- test_full_masking()
- test_partial_masking()
- test_encryption()
- test_hash_generation()
- test_fake_data_generation()
- test_batch_processing()
```

### Integration Tests

- End-to-end data processing
- File I/O operations
- Rule import/export
- Large file handling

### Manual Testing Checklist

- [ ] Load CSV files
- [ ] Load Excel files
- [ ] Generate sample data
- [ ] Apply each masking type
- [ ] Batch processing with large files
- [ ] Export masked data
- [ ] Import/export rules
- [ ] Generate and use encryption keys
- [ ] Compare original vs masked
- [ ] Export reverse mappings

## Compliance Considerations

### GDPR Compliance

**Relevant Articles**:
- Article 5: Data minimization
- Article 25: Data protection by design
- Article 32: Security of processing

**Tool Capabilities**:
- Pseudonymization (reversible masking)
- Anonymization (one-way hashing)
- Data minimization (selective masking)
- Purpose limitation (test/dev environments)

### HIPAA Compliance (Healthcare)

**Safe Harbor Method**:
- Remove 18 types of identifiers
- SSN masking
- Date shifting
- Geographic information masking

**Tool Support**:
- PHI field identification
- De-identification techniques
- Audit logging

### Industry Best Practices

1. **Data Classification**: Identify sensitive fields
2. **Risk Assessment**: Evaluate re-identification risks
3. **Documentation**: Maintain masking policies
4. **Regular Review**: Update masking rules
5. **Access Control**: Limit key distribution

## Future Enhancements

### Phase 2 Features

1. **Database Connectivity**
   - Direct database masking
   - SQL query support
   - Real-time masking

2. **Advanced Algorithms**
   - Differential privacy
   - K-anonymity
   - T-closeness

3. **Machine Learning**
   - Auto-detect sensitive fields
   - Suggest masking strategies
   - Pattern learning

4. **API Development**
   - RESTful API
   - Programmatic access
   - Integration capabilities

5. **Cloud Integration**
   - AWS S3 support
   - Azure Blob storage
   - Google Cloud Storage

6. **Enhanced UI**
   - Data profiling dashboard
   - Visual rule builder
   - Masking preview

7. **Compliance Reporting**
   - GDPR compliance report
   - HIPAA audit trail
   - Custom reports

8. **Performance**
   - Multi-threading
   - GPU acceleration
   - Distributed processing

## Deployment

### Standalone Application

Current deployment model:
- Python script execution
- Local installation
- Desktop application

### Future Deployment Options

1. **Executable Package**
   - PyInstaller bundle
   - Single-file executable
   - No Python installation required

2. **Docker Container**
   - Containerized application
   - Platform-independent
   - Easy deployment

3. **Web Application**
   - Browser-based UI
   - Server-side processing
   - Multi-user support

## Maintenance

### Version Control

- Semantic versioning (MAJOR.MINOR.PATCH)
- Changelog maintenance
- Backward compatibility

### Updates & Patches

- Security patches: Immediate
- Feature updates: Quarterly
- Major versions: Annually

### Support

- Documentation updates
- Bug fixes
- Feature requests
- Community support

---

## Technical Specifications

**Language**: Python 3.8+  
**GUI Framework**: Tkinter  
**Data Processing**: Pandas 2.0+  
**Encryption**: Cryptography library (Fernet)  
**Fake Data**: Faker library  
**File Formats**: CSV, Excel (XLSX, XLS)  
**Platform**: Cross-platform (Windows, macOS, Linux)  
**License**: Proprietary/Custom

---

**Document Version**: 1.0  
**Last Updated**: 2024  
**Author**: MonteyAI LLC
