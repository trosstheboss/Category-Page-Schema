# Complete Usage Guide

## Table of Contents
1. [Getting Started](#getting-started)
2. [Preparing Your Data](#preparing-your-data)
3. [Running the Generator](#running-the-generator)
4. [Implementing on Your Website](#implementing-on-your-website)
5. [Troubleshooting](#troubleshooting)
6. [Advanced Workflows](#advanced-workflows)

---

## Getting Started

### Prerequisites
- Python 3.8 or higher
- Excel or Google Sheets (for managing CSV data)
- Text editor (for reviewing JSON output)

### Installation

**Option 1: Quick Start (Recommended)**
```bash
# Run the quick start script to set everything up
python quick_start.py
```

**Option 2: Manual Setup**
```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. Create directories
mkdir schema_data
mkdir output
```

---

## Preparing Your Data

### Step 1: Fill Out the Spreadsheet Template

Use the spreadsheet template provided with column definitions:

1. **Organization Variables** (Sheet 1)
   - Fill in your company information
   - This data is used across all category pages
   - Only needs to be set up once

2. **Category Pages** (Sheet 2)
   - Add one row per category page
   - Example: Defensive Driving, Drivers Ed, Real Estate

3. **Courses** (Sheet 4)
   - Add one row per course
   - Link to categories via "Category ID"

4. **Supporting Data** (Sheets 3, 5-8)
   - Add topics, areas served, FAQs, etc.

### Step 2: Export to CSV

**From Google Sheets:**
1. Select a sheet tab
2. File → Download → Comma-separated values (.csv)
3. Save with exact name (e.g., `01_organization_variables.csv`)
4. Repeat for all 8 sheets

**From Excel:**
1. Click on a sheet tab
2. File → Save As → CSV (Comma delimited)
3. Save with exact name
4. Repeat for all 8 sheets

### Step 3: Place CSV Files

```
your-project/
└── schema_data/
    ├── 01_organization_variables.csv  ✓
    ├── 02_category_pages.csv          ✓
    ├── 03_category_about_topics.csv   ✓
    ├── 04_courses_master_list.csv     ✓
    ├── 05_course_topics.csv           ✓
    ├── 06_area_served.csv             ✓
    ├── 07_categories_tags.csv         ✓
    └── 08_faqs.csv                    ✓
```

---

## Running the Generator

### Method 1: Automated Script (Easiest)

**On Windows:**
```bash
generate_schemas.bat
```

**On Mac/Linux:**
```bash
chmod +x generate_schemas.sh
./generate_schemas.sh
```

### Method 2: Python Command
```bash
python schema_generator.py
```

### Method 3: Interactive Python
```python
from schema_generator import SchemaGenerator

# Initialize
generator = SchemaGenerator()
generator.load_data()

# Generate all schemas
generator.generate_all_schemas()
```

### What Happens

The script will:
1. ✓ Load all 8 CSV files
2. ✓ Generate schema for each category
3. ✓ Save JSON files to `output/` directory
4. ✓ Display progress and results

**Example Output:**
```
Loading CSV data...
✓ All CSV files loaded successfully

Generating schemas...
✓ Generated schema for: defensive-driving
✓ Generated schema for: drivers-ed
✓ Generated schema for: real-estate

============================================================
✓ Successfully generated 3 schema files
============================================================
```

---

## Implementing on Your Website

### Step 1: Review Generated Files

Open a generated JSON file:
```bash
# On Mac/Linux
cat output/defensive-driving_schema.json

# On Windows
type output\defensive-driving_schema.json
```

### Step 2: Copy JSON to Your Page

**Static HTML:**
```html
<!DOCTYPE html>
<html>
<head>
    <title>Defensive Driving Courses</title>
    
    <!-- Add schema markup here -->
    <script type="application/ld+json">
    {
      "@context": "https://schema.org",
      "@graph": [
        ... paste your generated JSON here ...
      ]
    }
    </script>
</head>
<body>
    <!-- Your page content -->
</body>
</html>
```

**WordPress (with Yoast or Rank Math):**
1. Edit your category page
2. Scroll to SEO settings
3. Find "Schema" or "Structured Data" section
4. Paste JSON into custom schema field

**React/Next.js:**
```jsx
import Head from 'next/head';

export default function DefensiveDriving() {
  const schema = {
    "@context": "https://schema.org",
    "@graph": [
      // ... paste your generated schema
    ]
  };
  
  return (
    <>
      <Head>
        <script
          type="application/ld+json"
          dangerouslySetInnerHTML={{ __html: JSON.stringify(schema) }}
        />
      </Head>
      {/* Page content */}
    </>
  );
}
```

**Craft CMS:**
```twig
{# In your template #}
{% set schema = craft.app.view.renderTemplate('_schemas/defensive-driving.json') %}

<script type="application/ld+json">
{{ schema | raw }}
</script>
```

### Step 3: Validate Implementation

Test your implementation:

1. **Google Rich Results Test**
   - Visit: https://search.google.com/test/rich-results
   - Enter your page URL
   - Check for errors/warnings

2. **Schema.org Validator**
   - Visit: https://validator.schema.org/
   - Paste your schema JSON
   - Verify structure

3. **Browser DevTools**
   ```javascript
   // In browser console
   JSON.parse(
     document.querySelector('script[type="application/ld+json"]').textContent
   );
   ```

---

## Troubleshooting

### Common Issues

#### "FileNotFoundError: No such file or directory"

**Problem:** CSV files not in correct location

**Solution:**
```bash
# Check your files exist
ls schema_data/

# Should show all 8 CSV files
# If not, export them from your spreadsheet
```

#### "KeyError: 'column_name'"

**Problem:** CSV missing required column

**Solution:**
1. Open the CSV file in a text editor
2. Check first row (headers) matches template
3. Ensure no typos in column names
4. Re-export from spreadsheet if needed

#### "Category ID 'xyz' not found"

**Problem:** Mismatch between category IDs

**Solution:**
1. Open `02_category_pages.csv`
2. Check the "Category ID" column
3. Ensure same IDs used in other CSV files
4. Category IDs are case-sensitive!

#### Generated Schema Invalid

**Problem:** Schema fails validation

**Solution:**
```python
from schema_generator import SchemaGenerator

generator = SchemaGenerator()
generator.load_data()

schema = generator.generate_schema_for_category("defensive-driving")
warnings = generator.validate_schema(schema)

# Review warnings
for w in warnings:
    print(w)
```

Common fixes:
- Ensure URLs are complete (include https://)
- Check date formats (YYYY-MM-DD)
- Verify required fields not empty
- Validate ISO 8601 duration codes

---

## Advanced Workflows

### Workflow 1: Continuous Integration

**Add to your CI/CD pipeline:**

`.github/workflows/generate-schema.yml`:
```yaml
name: Generate Schema

on:
  push:
    paths:
      - 'schema_data/*.csv'

jobs:
  generate:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      
      - name: Set up Python
        uses: actions/setup-python@v2
        with:
          python-version: '3.9'
      
      - name: Install dependencies
        run: pip install -r requirements.txt
      
      - name: Generate schemas
        run: python schema_generator.py
      
      - name: Commit generated files
        run: |
          git config --local user.email "action@github.com"
          git config --local user.name "GitHub Action"
          git add output/*.json
          git commit -m "Update generated schemas" || echo "No changes"
          git push
```

### Workflow 2: Automated Testing

**test_schemas.py:**
```python
import json
import os
from schema_generator import SchemaGenerator

def test_all_categories():
    generator = SchemaGenerator()
    generator.load_data()
    
    for _, row in generator.category_data.iterrows():
        category_id = row['Category ID']
        
        # Generate
        schema = generator.generate_schema_for_category(category_id)
        
        # Validate structure
        assert "@context" in schema
        assert "@graph" in schema
        assert len(schema["@graph"]) >= 4
        
        # Validate required types
        types = [item["@type"] for item in schema["@graph"]]
        assert "WebSite" in types
        assert "EducationalOrganization" in types
        assert "CollectionPage" in types
        assert "OfferCatalog" in types
        
        print(f"✓ {category_id} passed validation")

if __name__ == "__main__":
    test_all_categories()
    print("\n✅ All schemas validated successfully")
```

Run tests:
```bash
python test_schemas.py
```

### Workflow 3: Dynamic Website Integration

**For sites that pull from database:**

```python
from schema_generator import SchemaGenerator
import json

class DynamicSchemaService:
    def __init__(self):
        self.generator = SchemaGenerator()
        self.generator.load_data()
        self._cache = {}
    
    def get_schema_for_page(self, category_id: str) -> dict:
        """Get schema with caching"""
        if category_id not in self._cache:
            self._cache[category_id] = self.generator.generate_schema_for_category(category_id)
        return self._cache[category_id]
    
    def get_schema_json(self, category_id: str) -> str:
        """Get schema as JSON string"""
        schema = self.get_schema_for_page(category_id)
        return json.dumps(schema, ensure_ascii=False)

# Usage in your web framework
service = DynamicSchemaService()

@app.route('/defensive-driving')
def defensive_driving_page():
    schema_json = service.get_schema_json('defensive-driving')
    return render_template('category.html', schema=schema_json)
```

### Workflow 4: Multi-Environment Setup

**Different data per environment:**

```python
import os

# Development
generator_dev = SchemaGenerator(data_directory="./schema_data/dev")
generator_dev.load_data()
generator_dev.generate_all_schemas(output_dir="./output/dev")

# Staging
generator_staging = SchemaGenerator(data_directory="./schema_data/staging")
generator_staging.load_data()
generator_staging.generate_all_schemas(output_dir="./output/staging")

# Production
generator_prod = SchemaGenerator(data_directory="./schema_data/prod")
generator_prod.load_data()
generator_prod.generate_all_schemas(output_dir="./output/prod")
```

### Workflow 5: Schema Versioning

**Track changes to your schemas:**

```bash
# Generate with timestamp
python schema_generator.py
timestamp=$(date +%Y%m%d_%H%M%S)
cp -r output/ "output_archive/${timestamp}/"

# Or use git
git add output/*.json
git commit -m "Update schemas - $(date)"
```

---

## Tips & Best Practices

### Data Management
1. **Keep a master spreadsheet** - Use Google Sheets for team collaboration
2. **Version control CSV files** - Commit them to git
3. **Regular exports** - Schedule weekly/monthly CSV exports
4. **Validate before export** - Check for missing data in spreadsheet

### Schema Quality
1. **Review generated JSON** - Don't blindly implement
2. **Test in staging first** - Verify before production
3. **Monitor search console** - Check for structured data errors
4. **Update regularly** - When courses/content changes

### Performance
1. **Cache generated schemas** - Don't regenerate on every request
2. **Use CDN for JSON files** - If serving via external files
3. **Minify for production** - Remove whitespace (optional)

### Maintenance
1. **Document your Category IDs** - Keep a reference list
2. **Create naming conventions** - Consistent course codes
3. **Regular audits** - Quarterly review of schema accuracy
4. **Team training** - Ensure team knows how to use tool

---

## Need Help?

1. Check error messages carefully
2. Review CSV file format
3. Validate with schema.org validator
4. Test with Google Rich Results
5. Contact SEO team lead

---

**Last Updated:** January 2025  
**Version:** 1.0.0
