# Category Page Schema Generator

Automatically generate LLM-optimized JSON-LD structured data for category pages from CSV data.

## Features

- ✅ Generates complete schema.org markup for educational category pages
- ✅ Supports multiple courses per category
- ✅ LLM-optimized with natural language context
- ✅ Includes FAQs, breadcrumbs, and rich metadata
- ✅ Validates schema structure
- ✅ Exports clean, formatted JSON files

## 📍 Step-by-Step Setup Instructions
### Step 1: Download & Extract

1. **Download**  the ZIP file I created: category-schema-generator.zip
   [category-schema-generator.zip](https://github.com/user-attachments/files/22752973/category-schema-generator.zip)

2. **Extract it** to a location on your computer, for example:

 - Windows:
   ```
   C:\Users\YourName\Documents\schema-generator\
   ```
 - Mac: 
```
/Users/YourName/Documents/schema-generator/
```
 - Or anywhere you prefer!

### Directory Structure

Create this folder structure:

```
your-project/
├── schema_generator.py
├── requirements.txt
├── schema_data/           # Your CSV files go here
│   ├── 01_organization_variables.csv
│   ├── 02_category_pages.csv
│   ├── 03_category_about_topics.csv
│   ├── 04_courses_master_list.csv
│   ├── 05_course_topics.csv
│   ├── 06_area_served.csv
│   ├── 07_categories_tags.csv
│   └── 08_faqs.csv
└── output/                # Generated schemas will appear here
```

### Prepare Your CSV Files

1. **Export the spreadsheet sheets** as individual CSV files
2. **Name them exactly** as shown above (01-08)
3. **Place them** in the `schema_data/` directory

### Step 2: Open Terminal/Command Prompt

**On Windows:**
 - Press ```Win + R```
 - Type ```cmd``` and press Enter
 - OR right-click in the extracted folder and select "Open in Terminal" (Windows 11)

**On Mac:**
- Press ```Cmd + Space```
- Type "Terminal" and press Enter
- OR right-click the folder and select "New Terminal at Folder"

### Step 3: Navigate to the Directory
In the terminal, type:
**Windows:**
```bash
cd C:\Users\YourName\Documents\schema-generator
```
**Mac/Linux:**
```bash
cd /Users/YourName/Documents/schema-generator
```
(Replace with your actual path)

### Step 4: Run the Script
```bash
python quick_start.py
```
Or if you have Python 3 specifically:
```bash
python3 quick_start.py
```

## Installation

1. **Install Python 3.8+** (if not already installed)

2. **Install dependencies:**
```bash
pip install -r requirements.txt
```


## Usage

### Generate All Category Schemas

```bash
python schema_generator.py
```

This will:
- Read all CSV files from `./schema_data/`
- Generate a JSON schema file for each category
- Save files to `./output/` directory

### Generate Schema for Specific Category

```python
from schema_generator import SchemaGenerator

# Initialize
generator = SchemaGenerator(data_directory="./schema_data")
generator.load_data()

# Generate for specific category
schema = generator.generate_schema_for_category("defensive-driving")

# Save to file
import json
with open("defensive-driving-schema.json", "w") as f:
    json.dump(schema, f, indent=2)
```

## Output

The script generates JSON files like:

- `defensive-driving_schema.json`
- `drivers-ed_schema.json`
- `real-estate_schema.json`
- etc.

Each file contains complete, ready-to-use JSON-LD markup.

## Implementation

### Copy to Your Website

1. **Open the generated JSON file** (e.g., `defensive-driving_schema.json`)
2. **Copy the entire JSON content**
3. **Paste into your HTML** within the `<head>` section:

```html
<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@graph": [
    ... paste your generated schema here ...
  ]
}
</script>
```

### For CMS Integration

If you're using a CMS like WordPress, Craft, or custom platform:

1. **Create a custom field** for schema markup
2. **Paste the generated JSON** into that field
3. **Ensure it outputs** in the `<head>` section

### Validate Your Schema

After implementation, validate using:
- [Google Rich Results Test](https://search.google.com/test/rich-results)
- [Schema.org Validator](https://validator.schema.org/)

## CSV File Reference

### Required Files

| File | Description |
|------|-------------|
| `01_organization_variables.csv` | Global organization info (same for all pages) |
| `02_category_pages.csv` | Category page metadata and URLs |
| `03_category_about_topics.csv` | 3 key topics per category |
| `04_courses_master_list.csv` | All course details |
| `05_course_topics.csv` | 8 topics taught per course |
| `06_area_served.csv` | Geographic areas where courses are available |
| `07_categories_tags.csv` | Category classification tags |
| `08_faqs.csv` | Frequently asked questions per category |

### CSV Format Notes

- **Encoding:** UTF-8
- **Delimiter:** Comma (,)
- **Headers:** First row must contain column names exactly as specified
- **Empty values:** Use empty string or leave blank (not "N/A" unless specified)

## Customization

### Change Data Directory

```python
generator = SchemaGenerator(data_directory="./my_custom_folder")
```

### Change Output Directory

```python
generator.generate_all_schemas(output_dir="./my_output_folder")
```

### Add Custom Validation

```python
schema = generator.generate_schema_for_category("defensive-driving")
warnings = generator.validate_schema(schema)

if warnings:
    print("⚠️ Validation warnings:")
    for warning in warnings:
        print(f"  • {warning}")
```

## Troubleshooting

### "FileNotFoundError: CSV file not found"

**Solution:** Ensure all 8 CSV files are in the `schema_data/` directory with exact names.

### "Category ID not found"

**Solution:** Check that your Category ID in `02_category_pages.csv` matches the IDs used in other CSV files.

### "KeyError: Column not found"

**Solution:** Verify your CSV files have all required columns with exact spelling.

### Schema validation errors

**Solution:** 
1. Check for missing required fields in CSV
2. Verify URLs are complete (include https://)
3. Ensure ISO 8601 date formats (YYYY-MM-DD)
4. Check that duration codes use proper format (PT#H)

## Examples

### Example 1: Generate Single Category

```python
from schema_generator import SchemaGenerator
import json

generator = SchemaGenerator()
generator.load_data()

# Generate for drivers ed
schema = generator.generate_schema_for_category("drivers-ed")

# Pretty print to console
print(json.dumps(schema, indent=2))
```

### Example 2: Validate Before Saving

```python
from schema_generator import SchemaGenerator
import json

generator = SchemaGenerator()
generator.load_data()

category_id = "real-estate"
schema = generator.generate_schema_for_category(category_id)

# Validate
warnings = generator.validate_schema(schema)
if warnings:
    print(f"Warnings for {category_id}:")
    for w in warnings:
        print(f"  • {w}")
else:
    # Save if valid
    with open(f"{category_id}_schema.json", "w") as f:
        json.dump(schema, f, indent=2)
    print(f"✓ {category_id} schema saved")
```

### Example 3: Batch Generate with Progress

```python
from schema_generator import SchemaGenerator
import json
import os

generator = SchemaGenerator()
generator.load_data()

output_dir = "./output"
os.makedirs(output_dir, exist_ok=True)

categories = generator.category_data['Category ID'].tolist()

for i, category_id in enumerate(categories, 1):
    print(f"[{i}/{len(categories)}] Generating {category_id}...")
    
    try:
        schema = generator.generate_schema_for_category(category_id)
        
        filename = f"{output_dir}/{category_id}_schema.json"
        with open(filename, 'w') as f:
            json.dump(schema, f, indent=2)
        
        print(f"  ✓ Saved to {filename}")
    except Exception as e:
        print(f"  ✗ Error: {e}")

print("\nDone!")
```

## Advanced Usage

### Custom Schema Modifications

You can extend the `SchemaGenerator` class to add custom schema properties:

```python
from schema_generator import SchemaGenerator

class CustomSchemaGenerator(SchemaGenerator):
    def generate_course_schema(self, course_row, category_row):
        # Call parent method
        schema = super().generate_course_schema(course_row, category_row)
        
        # Add custom properties
        schema['customProperty'] = "custom value"
        
        return schema

# Use custom generator
generator = CustomSchemaGenerator()
generator.load_data()
schema = generator.generate_schema_for_category("defensive-driving")
```

### Integration with Build Pipeline

Add to your build process:

```bash
# In your build script or CI/CD pipeline
python schema_generator.py

# Then copy outputs to your web directory
cp output/*.json ../public/schemas/
```

## Support

For issues or questions:
1. Check the CSV file format matches the template
2. Verify all required columns exist
3. Review error messages for specific issues
4. Validate generated JSON at schema.org/validator

## License

Internal use for Aceable Technical SEO team.

## Version History

- **v1.0.0** (2025-01-07) - Initial release
  - Support for all 6 category types
  - Complete schema.org markup
  - LLM optimization
  - FAQ integration

