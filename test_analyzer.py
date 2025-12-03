"""
Test script to verify the document analyzer works correctly
"""
from analyzer import DocumentAnalyzer
import json

# Initialize analyzer
analyzer = DocumentAnalyzer()

# Test with sample document
print("Testing document analysis...")
print("=" * 50)

file_path = "sample_documents/research_paper.txt"
print(f"Analyzing: {file_path}")

try:
    result = analyzer.analyze_document(file_path)
    
    print("\n✓ Analysis completed successfully!")
    print(f"\nTitle: {result['title']}")
    print(f"Number of sections: {len(result['sections'])}")
    print(f"Layout: {result['ui_theme']['layout']}")
    print(f"Share ready: {result['share_ready']}")
    
    print("\nSections found:")
    for i, section in enumerate(result['sections'], 1):
        has_chart = "✓" if section.get('chart') else "✗"
        print(f"  {i}. {section['title']} [Chart: {has_chart}]")
    
    # Save result for inspection
    with open('test_output.json', 'w', encoding='utf-8') as f:
        json.dump(result, f, indent=2)
    
    print("\n✓ Full output saved to test_output.json")
    
except Exception as e:
    print(f"\n✗ Error: {e}")
    import traceback
    traceback.print_exc()
