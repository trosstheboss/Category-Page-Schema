#!/usr/bin/env python3
"""
Quick Start Script for Schema Generator
Sets up directory structure and validates CSV files
"""

import os
import sys
from pathlib import Path


def create_directory_structure():
    """Create necessary directories"""
    dirs = ['schema_data', 'output']
    
    for dir_name in dirs:
        Path(dir_name).mkdir(exist_ok=True)
        print(f"✓ Created directory: {dir_name}/")


def check_csv_files():
    """Check if all required CSV files exist"""
    required_files = [
        '01_organization_variables.csv',
        '02_category_pages.csv',
        '03_category_about_topics.csv',
        '04_courses_master_list.csv',
        '05_course_topics.csv',
        '06_area_served.csv',
        '07_categories_tags.csv',
        '08_faqs.csv'
    ]
    
    missing_files = []
    existing_files = []
    
    for filename in required_files:
        filepath = f'schema_data/{filename}'
        if os.path.exists(filepath):
            existing_files.append(filename)
        else:
            missing_files.append(filename)
    
    print(f"\n📊 CSV File Status:")
    print(f"   Found: {len(existing_files)}/8")
    
    if existing_files:
        print(f"\n   ✓ Existing files:")
        for f in existing_files:
            print(f"     • {f}")
    
    if missing_files:
        print(f"\n   ✗ Missing files:")
        for f in missing_files:
            print(f"     • {f}")
        print(f"\n   → Export these sheets from your spreadsheet as CSV")
        print(f"   → Place them in the schema_data/ directory")
        return False
    
    return True


def check_dependencies():
    """Check if required Python packages are installed"""
    try:
        import pandas
        print("✓ pandas is installed")
        return True
    except ImportError:
        print("✗ pandas is not installed")
        print("  → Run: pip install -r requirements.txt")
        return False


def run_test_generation():
    """Test the schema generator"""
    try:
        from schema_generator import SchemaGenerator
        
        print("\n🧪 Testing schema generator...")
        
        generator = SchemaGenerator(data_directory="./schema_data")
        generator.load_data()
        
        # Get first category
        first_category = generator.category_data.iloc[0]['Category ID']
        print(f"   Generating test schema for: {first_category}")
        
        schema = generator.generate_schema_for_category(first_category)
        
        # Validate
        warnings = generator.validate_schema(schema)
        if warnings:
            print(f"\n   ⚠️  Validation warnings:")
            for w in warnings:
                print(f"      • {w}")
        else:
            print(f"   ✓ Schema validated successfully")
        
        # Save test file
        import json
        test_file = f"output/test_{first_category}_schema.json"
        with open(test_file, 'w') as f:
            json.dump(schema, f, indent=2)
        
        print(f"   ✓ Test schema saved to: {test_file}")
        print(f"\n✅ Schema generator is working correctly!")
        return True
        
    except Exception as e:
        print(f"\n❌ Error during test: {e}")
        return False


def main():
    """Main quick start function"""
    print("\n" + "="*60)
    print("🚀 Category Page Schema Generator - Quick Start")
    print("="*60 + "\n")
    
    # Step 1: Create directories
    print("Step 1: Setting up directory structure...")
    create_directory_structure()
    
    # Step 2: Check dependencies
    print("\nStep 2: Checking Python dependencies...")
    if not check_dependencies():
        print("\n⚠️  Please install dependencies first:")
        print("   pip install -r requirements.txt\n")
        sys.exit(1)
    
    # Step 3: Check CSV files
    print("\nStep 3: Checking for CSV files...")
    if not check_csv_files():
        print("\n⚠️  Please add your CSV files to schema_data/ directory\n")
        print("Next steps:")
        print("1. Export each sheet from your spreadsheet as CSV")
        print("2. Name them exactly as shown above (01-08)")
        print("3. Place them in the schema_data/ directory")
        print("4. Run this script again: python quick_start.py\n")
        sys.exit(1)
    
    # Step 4: Test generation
    print("\nStep 4: Testing schema generation...")
    if run_test_generation():
        print("\n" + "="*60)
        print("✅ Setup Complete! You're ready to generate schemas.")
        print("="*60)
        print("\nNext steps:")
        print("1. Review the test schema in output/ directory")
        print("2. Generate all schemas: python schema_generator.py")
        print("3. Implement generated JSON-LD on your pages\n")
    else:
        print("\n⚠️  Test generation failed. Please check:")
        print("   • CSV files have all required columns")
        print("   • Data format matches the template")
        print("   • No empty required fields\n")
        sys.exit(1)


if __name__ == "__main__":
    main()
