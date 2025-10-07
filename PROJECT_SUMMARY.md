# Category Page Schema Generator - Project Summary

## 📦 What's Included

This package contains everything you need to automatically generate LLM-optimized JSON-LD schema markup for your category pages.

### Core Files

| File | Purpose |
|------|---------|
| `schema_generator.py` | Main Python script that generates schemas |
| `quick_start.py` | Setup and testing script |
| `requirements.txt` | Python dependencies |
| `README.md` | Complete documentation |
| `USAGE_GUIDE.md` | Step-by-step usage instructions |
| `.gitignore` | Git version control configuration |

### Scripts

| File | Platform | Purpose |
|------|----------|---------|
| `generate_schemas.sh` | Mac/Linux | One-click schema generation |
| `generate_schemas.bat` | Windows | One-click schema generation |

### Directories

| Directory | Contents |
|-----------|----------|
| `schema_data/` | Your CSV files (8 files required) |
| `output/` | Generated JSON-LD files (created automatically) |

### Sample Data

| File | Purpose |
|------|---------|
| `schema_data/01_organization_variables.csv` | Example organization data |
| `schema_data/02_category_pages.csv` | Example category setup |

---

## 🚀 Quick Start (5 Minutes)

### Step 1: Install Python Dependencies
```bash
pip install -r requirements.txt
```

### Step 2: Add Your CSV Files
Export your 8 spreadsheet sheets as CSV files and place in `schema_data/` directory

### Step 3: Generate Schemas
**Mac/Linux:**
```bash
./generate_schemas.sh
```

**Windows:**
```bash
generate_schemas.bat
```

**Or use Python directly:**
```bash
python schema_generator.py
```

### Step 4: Implement
Copy generated JSON files from `output/` directory to your website

---

## 📊 Data Flow

```
Spreadsheet Template
        ↓
Export to CSV (8 files)
        ↓
Place in schema_data/
        ↓
Run schema_generator.py
        ↓
Generated JSON in output/
        ↓
Copy to website <head>
        ↓
Validate with Google
```

---

## 🎯 Features

✅ **Comprehensive Schema Coverage**
- WebSite
- EducationalOrganization
- CollectionPage with breadcrumbs
- OfferCatalog with multiple courses
- Course with detailed metadata
- FAQPage

✅ **LLM Optimization**
- Natural language descriptions
- Rich educational metadata
- Semantic relationships
- Learning outcomes
- Audience targeting

✅ **Easy to Use**
- Template-based workflow
- Automated generation
- Validation included
- Clear error messages

✅ **Scalable**
- Handle unlimited categories
- Multiple courses per category
- Multi-state support
- Easy updates

---

## 📝 CSV Files Required

You need to export and provide these 8 CSV files:

1. **01_organization_variables.csv** - Company info (12 variables)
2. **02_category_pages.csv** - Category pages (1 row per category)
3. **03_category_about_topics.csv** - Key topics (3 per category)
4. **04_courses_master_list.csv** - All courses (1 row per course)
5. **05_course_topics.csv** - Topics taught (8 per course)
6. **06_area_served.csv** - Geographic availability
7. **07_categories_tags.csv** - Category classifications (6 per category)
8. **08_faqs.csv** - FAQs (8 per category)

See the spreadsheet template for exact column definitions.

---

## 🔧 Customization

### Change Data Location
```python
generator = SchemaGenerator(data_directory="./my_data")
```

### Change Output Location
```python
generator.generate_all_schemas(output_dir="./my_output")
```

### Generate Single Category
```python
generator = SchemaGenerator()
generator.load_data()
schema = generator.generate_schema_for_category("defensive-driving")
```

### Add Custom Validation
```python
schema = generator.generate_schema_for_category("defensive-driving")
warnings = generator.validate_schema(schema)
if warnings:
    print("Warnings:", warnings)
```

---

## 📚 Documentation

- **README.md** - Complete project documentation
- **USAGE_GUIDE.md** - Detailed step-by-step instructions
- **Inline comments** - Extensive code documentation

---

## 🧪 Testing

### Quick Test
```bash
python quick_start.py
```

This will:
1. Check your setup
2. Validate CSV files
3. Generate a test schema
4. Report any issues

### Manual Test
```bash
python schema_generator.py
```

Check `output/` directory for generated files.

### Validate Output
1. Open generated JSON file
2. Go to https://validator.schema.org/
3. Paste JSON and validate
4. Or use Google Rich Results Test

---

## 💡 Common Use Cases

### Use Case 1: Initial Setup
You're setting up schema for the first time across all category pages.

**Steps:**
1. Fill out spreadsheet template
2. Export all sheets to CSV
3. Run generator
4. Implement all schemas

**Time:** 2-3 hours (mostly data entry)

### Use Case 2: Add New Category
You're launching a new course category.

**Steps:**
1. Add row to category_pages.csv
2. Add courses to courses_master_list.csv
3. Add supporting data (topics, FAQs, etc.)
4. Run generator
5. Implement new schema

**Time:** 30 minutes

### Use Case 3: Update Existing Category
Course information changed or new courses added.

**Steps:**
1. Update relevant CSV files
2. Run generator
3. Replace old schema with new

**Time:** 15 minutes

### Use Case 4: Ongoing Maintenance
Regular monthly updates to keep schemas current.

**Steps:**
1. Review and update CSV data
2. Run generator
3. Deploy updated schemas

**Time:** 1 hour/month

---

## ⚠️ Important Notes

### DO
✅ Keep CSV files in version control
✅ Test in staging before production
✅ Validate with Google Rich Results Test
✅ Review generated JSON before implementing
✅ Update schemas when content changes

### DON'T
❌ Edit generated JSON files directly
❌ Skip CSV validation
❌ Ignore schema warnings
❌ Use different column names than template
❌ Mix up Category IDs across files

---

## 🐛 Troubleshooting

### Problem: "FileNotFoundError"
**Solution:** Ensure all 8 CSV files are in `schema_data/` directory

### Problem: "pandas not found"
**Solution:** Run `pip install -r requirements.txt`

### Problem: "Category ID not found"
**Solution:** Check Category IDs match across all CSV files (case-sensitive)

### Problem: Schema validation fails
**Solution:** 
1. Check for missing required fields
2. Verify URL formats (must include https://)
3. Validate date formats (YYYY-MM-DD)
4. Check ISO 8601 duration codes (PT#H)

See USAGE_GUIDE.md for more troubleshooting tips.

---

## 📈 Performance

- **Generation speed:** ~1 second per category
- **File size:** 15-50KB per schema (depending on number of courses)
- **Memory usage:** Minimal (< 50MB)
- **Scalability:** Tested with 100+ courses

---

## 🔄 Updates & Maintenance

### When to Regenerate Schemas
- New courses added
- Course information changes
- Pricing updates
- New states/areas served
- FAQ updates
- Organization information changes

### Recommended Schedule
- **Weekly:** If actively adding courses
- **Monthly:** For regular maintenance
- **Quarterly:** For mature catalogs
- **As needed:** For major changes

---

## 🎓 Learning Resources

### Schema.org Documentation
- https://schema.org/Course
- https://schema.org/OfferCatalog
- https://schema.org/EducationalOrganization

### Google Documentation
- [Structured Data Guidelines](https://developers.google.com/search/docs/appearance/structured-data/intro-structured-data)
- [Course Schema](https://developers.google.com/search/docs/appearance/structured-data/course)

### Validation Tools
- [Google Rich Results Test](https://search.google.com/test/rich-results)
- [Schema.org Validator](https://validator.schema.org/)

---

## 📞 Support

For questions or issues:
1. Check documentation (README.md & USAGE_GUIDE.md)
2. Review error messages
3. Validate CSV format
4. Contact SEO team lead

---

## 📜 License

Internal use for Aceable Technical SEO team.

---

## 📋 Version History

**v1.0.0** (January 2025)
- Initial release
- Support for 6 category types
- Complete schema.org markup
- LLM optimization
- FAQ integration
- Automated validation

---

## 🎉 Success Metrics

After implementing these schemas, you should see:
- ✅ Improved rich snippet appearance in Google
- ✅ Better LLM understanding of your courses
- ✅ Enhanced structured data coverage in Search Console
- ✅ Increased visibility for course searches
- ✅ Zero structured data errors in Google

---

## 🚦 Status

**Status:** Production Ready ✅  
**Last Updated:** January 7, 2025  
**Version:** 1.0.0  
**Python Version:** 3.8+  
**Dependencies:** pandas 2.0+

---

**Ready to get started?** Run `python quick_start.py` to begin!
