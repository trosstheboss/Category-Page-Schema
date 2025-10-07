#!/usr/bin/env python3
"""
Category Page Schema Generator for SEO
Reads CSV data and generates JSON-LD structured data for category pages
Author: Technical SEO Team
"""

import pandas as pd
import json
from typing import Dict, List, Any
from datetime import datetime
import os


class SchemaGenerator:
    """Generate JSON-LD schema markup from CSV data"""
    
    def __init__(self, data_directory: str = "./schema_data"):
        """
        Initialize the schema generator
        
        Args:
            data_directory: Path to directory containing CSV files
        """
        self.data_dir = data_directory
        self.org_data = None
        self.category_data = None
        self.courses_data = None
        self.topics_data = None
        self.areas_data = None
        self.categories_data = None
        self.faqs_data = None
        self.about_topics_data = None
        
    def load_data(self):
        """Load all CSV files into pandas DataFrames"""
        try:
            self.org_data = pd.read_csv(f"{self.data_dir}/01_organization_variables.csv")
            self.category_data = pd.read_csv(f"{self.data_dir}/02_category_pages.csv")
            self.about_topics_data = pd.read_csv(f"{self.data_dir}/03_category_about_topics.csv")
            self.courses_data = pd.read_csv(f"{self.data_dir}/04_courses_master_list.csv")
            self.topics_data = pd.read_csv(f"{self.data_dir}/05_course_topics.csv")
            self.areas_data = pd.read_csv(f"{self.data_dir}/06_area_served.csv")
            self.categories_data = pd.read_csv(f"{self.data_dir}/07_categories_tags.csv")
            self.faqs_data = pd.read_csv(f"{self.data_dir}/08_faqs.csv")
            print("✓ All CSV files loaded successfully")
        except FileNotFoundError as e:
            print(f"✗ Error loading CSV files: {e}")
            print(f"  Make sure all CSV files are in the '{self.data_dir}' directory")
            raise
    
    def get_org_value(self, variable_name: str) -> str:
        """Get organization variable value by name"""
        row = self.org_data[self.org_data['Variable Name'] == variable_name]
        if not row.empty:
            return str(row.iloc[0]['Value'])
        return ""
    
    def generate_website_schema(self) -> Dict[str, Any]:
        """Generate WebSite schema"""
        return {
            "@type": "WebSite",
            "name": self.get_org_value('organization_name'),
            "@id": f"{self.get_org_value('base_url')}/#website",
            "url": self.get_org_value('base_url'),
            "description": self.get_org_value('organization_description'),
            "publisher": {
                "@id": f"{self.get_org_value('base_url')}/#organization"
            }
        }
    
    def generate_organization_schema(self) -> Dict[str, Any]:
        """Generate EducationalOrganization schema"""
        return {
            "@type": "EducationalOrganization",
            "@id": f"{self.get_org_value('base_url')}/#organization",
            "name": self.get_org_value('organization_name'),
            "description": self.get_org_value('organization_long_description'),
            "url": self.get_org_value('base_url'),
            "logo": self.get_org_value('organization_logo_url'),
            "sameAs": [
                self.get_org_value('social_facebook'),
                self.get_org_value('social_instagram'),
                self.get_org_value('social_twitter'),
                self.get_org_value('social_linkedin'),
                self.get_org_value('social_youtube'),
                self.get_org_value('social_tiktok')
            ],
            "award": self.get_org_value('organization_award')
        }
    
    def generate_breadcrumb_schema(self, category_row: pd.Series) -> Dict[str, Any]:
        """Generate BreadcrumbList schema"""
        breadcrumb_items = []
        
        # Add first breadcrumb
        if pd.notna(category_row['breadcrumb_1_name']):
            breadcrumb_items.append({
                "@type": "ListItem",
                "position": 1,
                "name": category_row['breadcrumb_1_name'],
                "item": category_row['breadcrumb_1_url']
            })
        
        # Add second breadcrumb (current page)
        if pd.notna(category_row['breadcrumb_2_name']):
            breadcrumb_items.append({
                "@type": "ListItem",
                "position": 2,
                "name": category_row['breadcrumb_2_name']
            })
        
        return {
            "@type": "BreadcrumbList",
            "itemListElement": breadcrumb_items
        }
    
    def generate_about_topics(self, category_id: str) -> List[Dict[str, Any]]:
        """Generate about topics for category"""
        topics = []
        about_row = self.about_topics_data[
            self.about_topics_data['Category ID'] == category_id
        ]
        
        if not about_row.empty:
            row = about_row.iloc[0]
            for i in range(1, 4):  # 3 topics
                topic_name = f'about_topic_{i}_name'
                topic_desc = f'about_topic_{i}_description'
                if pd.notna(row[topic_name]):
                    topics.append({
                        "@type": "Thing",
                        "name": row[topic_name],
                        "description": row[topic_desc]
                    })
        
        return topics
    
    def generate_collection_page_schema(self, category_row: pd.Series) -> Dict[str, Any]:
        """Generate CollectionPage schema"""
        category_id = category_row['Category ID']
        
        return {
            "@type": "CollectionPage",
            "@id": f"{category_row['category_page_url']}#catalog",
            "url": category_row['category_page_url'],
            "name": category_row['category_page_name'],
            "headline": category_row['category_page_headline'],
            "description": category_row['category_page_description'],
            "alternativeHeadline": category_row['category_page_alternative_headline'],
            "about": self.generate_about_topics(category_id),
            "keywords": category_row['category_keywords'],
            "isPartOf": {
                "@id": f"{self.get_org_value('base_url')}/#website"
            },
            "breadcrumb": self.generate_breadcrumb_schema(category_row),
            "mainEntity": {
                "@id": f"#{category_row['catalog_id']}"
            }
        }
    
    def generate_course_schema(self, course_row: pd.Series, category_row: pd.Series) -> Dict[str, Any]:
        """Generate Course schema for a single course"""
        category_id = course_row['Category ID']
        course_position = int(course_row['course_position'])
        
        # Get course topics
        topics_row = self.topics_data[
            (self.topics_data['Category ID'] == category_id) &
            (self.topics_data['course_position'] == course_position)
        ]
        
        teaches = []
        if not topics_row.empty:
            topic_row = topics_row.iloc[0]
            for i in range(1, 9):  # 8 topics
                topic_col = f'course_topic_{i}'
                if pd.notna(topic_row[topic_col]):
                    teaches.append(topic_row[topic_col])
        
        # Build course schema
        course_schema = {
            "@type": "Course",
            "position": course_position,
            "name": course_row['course_name'],
            "alternateName": course_row['course_alternate_name'],
            "description": course_row['course_description'],
            "url": course_row['course_url'],
            "educationalCredentialAwarded": course_row['course_credential'],
            "educationalLevel": course_row['course_level'],
            "timeRequired": course_row['course_duration_iso8601'],
            "abstract": course_row['course_abstract'],
            "coursePrerequisites": course_row['course_prerequisites'],
            "occupationalCredentialAwarded": course_row['course_benefits'],
            "teaches": teaches,
            "audience": {
                "@type": "Audience",
                "audienceType": course_row['course_audience_type']
            },
            "availableLanguage": course_row['course_language'],
            "hasCourseInstance": {
                "@type": "CourseInstance",
                "courseMode": [course_row['course_mode_1']],
                "courseWorkload": course_row['course_workload_iso8601'],
                "courseSchedule": {
                    "@type": "Schedule",
                    "scheduleTimezone": course_row['course_timezone'],
                    "repeatFrequency": "P1D",
                    "byDay": ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
                },
                "instructor": {
                    "@type": "Organization",
                    "name": course_row['course_instructor_org']
                }
            },
            "offers": {
                "@type": "Offer",
                "category": course_row['offer_category'],
                "priceCurrency": "USD",
                "availability": "https://schema.org/InStock",
                "availabilityStarts": course_row['offer_availability_starts'],
                "validFrom": course_row['offer_valid_from'],
                "url": course_row['course_url'],
                "eligibleRegion": {
                    "@type": course_row['eligible_region_type'],
                    "name": course_row['eligible_region_name'],
                    "address": {
                        "@type": "PostalAddress",
                        "addressRegion": course_row['eligible_region_code'],
                        "addressCountry": "US"
                    }
                },
                "deliveryMethod": "OnlineOnly"
            },
            "provider": {
                "@id": f"{self.get_org_value('base_url')}/#organization"
            },
            "isPartOf": {
                "@id": f"{category_row['category_page_url']}#catalog"
            },
            "inLanguage": course_row['course_in_language'],
            "locationCreated": {
                "@type": course_row['location_created_type'],
                "name": course_row['location_created_name'],
                "address": {
                    "@type": "PostalAddress",
                    "addressRegion": course_row['location_created_region'],
                    "addressCountry": "US"
                }
            },
            "educationalUse": course_row['course_educational_use'],
            "learningResourceType": course_row['course_learning_resource_type'],
            "interactivityType": "mixed",
            "typicalAgeRange": course_row['course_age_range']
        }
        
        # Add course code if present
        if pd.notna(course_row['course_code']) and course_row['course_code'] != 'N/A':
            course_schema['courseCode'] = course_row['course_code']
        
        # Add second course mode if present
        if pd.notna(course_row['course_mode_2']):
            course_schema['hasCourseInstance']['courseMode'].append(course_row['course_mode_2'])
        
        # Add geographic area to audience if present
        if pd.notna(course_row['geographic_type']):
            course_schema['audience']['geographicArea'] = {
                "@type": course_row['geographic_type'],
                "name": course_row['geographic_name']
            }
        
        return course_schema
    
    def generate_area_served(self, category_id: str) -> List[Dict[str, Any]]:
        """Generate areaServed array for catalog"""
        areas = []
        area_rows = self.areas_data[self.areas_data['Category ID'] == category_id]
        
        for _, row in area_rows.iterrows():
            areas.append({
                "@type": "State",
                "name": row['area_served_name'],
                "alternateName": row['area_served_code'],
                "address": {
                    "@type": "PostalAddress",
                    "addressRegion": row['area_served_code'],
                    "addressCountry": "US"
                },
                "description": row['area_served_description']
            })
        
        return areas
    
    def generate_categories(self, category_id: str) -> List[str]:
        """Generate category tags array"""
        categories = []
        cat_row = self.categories_data[self.categories_data['Category ID'] == category_id]
        
        if not cat_row.empty:
            row = cat_row.iloc[0]
            for i in range(1, 7):  # 6 categories
                cat_col = f'category_{i}'
                if pd.notna(row[cat_col]):
                    categories.append(row[cat_col])
        
        return categories
    
    def generate_offer_catalog_schema(self, category_row: pd.Series) -> Dict[str, Any]:
        """Generate OfferCatalog schema with all courses"""
        category_id = category_row['Category ID']
        
        # Get all courses for this category
        category_courses = self.courses_data[
            self.courses_data['Category ID'] == category_id
        ].sort_values('course_position')
        
        # Generate course schemas
        course_list = []
        for _, course_row in category_courses.iterrows():
            course_schema = self.generate_course_schema(course_row, category_row)
            course_list.append(course_schema)
        
        return {
            "@type": "OfferCatalog",
            "@id": f"#{category_row['catalog_id']}",
            "name": category_row['catalog_name'],
            "description": category_row['catalog_description'],
            "numberOfItems": int(category_row['total_courses']),
            "provider": {
                "@id": f"{self.get_org_value('base_url')}/#organization"
            },
            "itemListElement": course_list,
            "areaServed": self.generate_area_served(category_id),
            "category": self.generate_categories(category_id)
        }
    
    def generate_faq_schema(self, category_id: str, category_url: str) -> Dict[str, Any]:
        """Generate FAQPage schema"""
        faq_rows = self.faqs_data[
            self.faqs_data['Category ID'] == category_id
        ].sort_values('faq_position')
        
        faq_items = []
        for _, row in faq_rows.iterrows():
            if pd.notna(row['faq_question']):
                faq_items.append({
                    "@type": "Question",
                    "name": row['faq_question'],
                    "acceptedAnswer": {
                        "@type": "Answer",
                        "text": row['faq_answer']
                    }
                })
        
        return {
            "@type": "FAQPage",
            "@id": f"{category_url}#faq",
            "mainEntity": faq_items
        }
    
    def generate_schema_for_category(self, category_id: str) -> Dict[str, Any]:
        """Generate complete schema for a category page"""
        # Get category data
        category_row = self.category_data[
            self.category_data['Category ID'] == category_id
        ]
        
        if category_row.empty:
            raise ValueError(f"Category ID '{category_id}' not found in category_pages.csv")
        
        category_row = category_row.iloc[0]
        
        # Build complete schema
        schema = {
            "@context": "https://schema.org",
            "@graph": [
                self.generate_website_schema(),
                self.generate_organization_schema(),
                self.generate_collection_page_schema(category_row),
                self.generate_offer_catalog_schema(category_row),
                self.generate_faq_schema(category_id, category_row['category_page_url'])
            ]
        }
        
        return schema
    
    def generate_all_schemas(self, output_dir: str = "./output"):
        """Generate schemas for all categories and save to files"""
        # Create output directory if it doesn't exist
        os.makedirs(output_dir, exist_ok=True)
        
        generated_files = []
        
        # Generate schema for each category
        for _, row in self.category_data.iterrows():
            category_id = row['Category ID']
            
            try:
                schema = self.generate_schema_for_category(category_id)
                
                # Save to file
                filename = f"{output_dir}/{category_id}_schema.json"
                with open(filename, 'w', encoding='utf-8') as f:
                    json.dump(schema, f, indent=2, ensure_ascii=False)
                
                generated_files.append(filename)
                print(f"✓ Generated schema for: {category_id}")
                
            except Exception as e:
                print(f"✗ Error generating schema for {category_id}: {e}")
        
        return generated_files
    
    def validate_schema(self, schema: Dict[str, Any]) -> List[str]:
        """Basic validation of schema structure"""
        warnings = []
        
        if "@context" not in schema:
            warnings.append("Missing @context")
        
        if "@graph" not in schema:
            warnings.append("Missing @graph")
        
        # Check for required schema types
        schema_types = [item.get("@type") for item in schema.get("@graph", [])]
        required_types = ["WebSite", "EducationalOrganization", "CollectionPage", "OfferCatalog"]
        
        for req_type in required_types:
            if req_type not in schema_types:
                warnings.append(f"Missing required schema type: {req_type}")
        
        return warnings


def main():
    """Main execution function"""
    print("\n" + "="*60)
    print("Category Page Schema Generator")
    print("="*60 + "\n")
    
    # Initialize generator
    generator = SchemaGenerator(data_directory="./schema_data")
    
    # Load data
    print("Loading CSV data...")
    try:
        generator.load_data()
    except Exception as e:
        print(f"\n✗ Failed to load data: {e}")
        return
    
    print("\nGenerating schemas...")
    generated_files = generator.generate_all_schemas(output_dir="./output")
    
    print("\n" + "="*60)
    print(f"✓ Successfully generated {len(generated_files)} schema files")
    print("="*60)
    print("\nGenerated files:")
    for file in generated_files:
        print(f"  • {file}")
    
    print("\nSchema files are ready to use!")
    print("Copy the JSON content into your page's <script type='application/ld+json'> tag\n")


if __name__ == "__main__":
    main()
