#!/usr/bin/env python3
"""
File Processor for SEC Filings Analysis

Extracts structured financial data from PDF, HTML, and Excel SEC filings.
Supports multi-format processing with validation and error handling.
"""

import os
import re
import json
from typing import Dict, List, Any, Optional, Tuple, Union
import logging

# Optional dependencies with fallbacks
try:
    import PyPDF2
    from pdfminer.high_level import extract_text as pdfminer_extract
    PDF_AVAILABLE = True
except ImportError:
    PDF_AVAILABLE = False

try:
    from bs4 import BeautifulSoup
    HTML_AVAILABLE = True
except ImportError:
    HTML_AVAILABLE = False

try:
    import pandas as pd
    EXCEL_AVAILABLE = True
except ImportError:
    EXCEL_AVAILABLE = False

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class FileProcessor:
    """Main class for processing SEC filings in various formats."""

    def __init__(self):
        self.financial_data = {}
        self.metadata = {}

    def extract_pdf_data(self, pdf_path: str) -> Dict[str, Any]:
        """
        Extract financial data from PDF SEC filings.

        Args:
            pdf_path: Path to PDF file

        Returns:
            Dictionary containing extracted financial data

        Raises:
            ValueError: If PDF processing fails
        """
        if not PDF_AVAILABLE:
            raise ImportError("PyPDF2 and pdfminer required for PDF processing")

        if not os.path.exists(pdf_path):
            raise FileNotFoundError(f"PDF file not found: {pdf_path}")

        try:
            # Extract text using pdfminer (better for financial data)
            text = pdfminer_extract(pdf_path)

            # Parse financial statements
            financial_data = self._parse_financial_statements(text)
            metadata = self._extract_metadata(text, pdf_path)

            self.financial_data = financial_data
            self.metadata = metadata

            logger.info(f"Successfully extracted data from PDF: {pdf_path}")
            return {
                'financial_data': financial_data,
                'metadata': metadata,
                'raw_text': text[:1000]  # First 1000 chars for reference
            }

        except Exception as e:
            logger.error(f"Error extracting PDF data: {e}")
            raise ValueError(f"Failed to process PDF file: {e}")

    def extract_html_data(self, html_path: str) -> Dict[str, Any]:
        """
        Extract financial data from HTML SEC filings.

        Args:
            html_path: Path to HTML file

        Returns:
            Dictionary containing extracted financial data
        """
        if not HTML_AVAILABLE:
            raise ImportError("BeautifulSoup4 required for HTML processing")

        if not os.path.exists(html_path):
            raise FileNotFoundError(f"HTML file not found: {html_path}")

        try:
            with open(html_path, 'r', encoding='utf-8') as f:
                content = f.read()

            soup = BeautifulSoup(content, 'html.parser')

            # Extract text content
            text = soup.get_text()

            # Look for structured data in JSON-LD or other formats
            structured_data = self._extract_structured_data(soup)

            # Parse financial statements
            financial_data = self._parse_financial_statements(text)
            metadata = self._extract_metadata(text, html_path)

            self.financial_data = financial_data
            self.metadata = metadata

            logger.info(f"Successfully extracted data from HTML: {html_path}")
            return {
                'financial_data': financial_data,
                'metadata': metadata,
                'structured_data': structured_data,
                'raw_text': text[:1000]
            }

        except Exception as e:
            logger.error(f"Error extracting HTML data: {e}")
            raise ValueError(f"Failed to process HTML file: {e}")

    def extract_excel_data(self, excel_path: str) -> Dict[str, Any]:
        """
        Extract financial data from Excel SEC filings.

        Args:
            excel_path: Path to Excel file

        Returns:
            Dictionary containing extracted financial data
        """
        if not EXCEL_AVAILABLE:
            raise ImportError("pandas required for Excel processing")

        if not os.path.exists(excel_path):
            raise FileNotFoundError(f"Excel file not found: {excel_path}")

        try:
            # Read all sheets
            excel_data = pd.read_excel(excel_path, sheet_name=None)

            financial_data = {}
            metadata = {}

            for sheet_name, df in excel_data.items():
                # Try to identify financial statement type
                statement_type = self._identify_statement_type(df)
                if statement_type:
                    parsed_data = self._parse_excel_financial_data(df, statement_type)
                    financial_data[statement_type] = parsed_data

            # Extract general metadata
            metadata = self._extract_excel_metadata(excel_path)

            self.financial_data = financial_data
            self.metadata = metadata

            logger.info(f"Successfully extracted data from Excel: {excel_path}")
            return {
                'financial_data': financial_data,
                'metadata': metadata,
                'raw_data': {k: v.to_dict() for k, v in excel_data.items()}
            }

        except Exception as e:
            logger.error(f"Error extracting Excel data: {e}")
            raise ValueError(f"Failed to process Excel file: {e}")

    def normalize_financial_data(self, raw_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Normalize extracted financial data to standard format.

        Args:
            raw_data: Raw extracted data

        Returns:
            Normalized financial data
        """
        normalized = {}

        if 'financial_data' in raw_data:
            financial_data = raw_data['financial_data']

            # Normalize income statement
            if 'income_statement' in financial_data:
                normalized['income_statement'] = self._normalize_income_statement(
                    financial_data['income_statement']
                )

            # Normalize balance sheet
            if 'balance_sheet' in financial_data:
                normalized['balance_sheet'] = self._normalize_balance_sheet(
                    financial_data['balance_sheet']
                )

            # Normalize cash flow
            if 'cash_flow' in financial_data:
                normalized['cash_flow'] = self._normalize_cash_flow(
                    financial_data['cash_flow']
                )

        # Add metadata
        if 'metadata' in raw_data:
            normalized['metadata'] = raw_data['metadata']

        return normalized

    def validate_extraction(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Validate extracted financial data for completeness and accuracy.

        Args:
            data: Extracted financial data

        Returns:
            Validation report
        """
        validation_report = {
            'is_valid': True,
            'issues': [],
            'warnings': [],
            'score': 0.0
        }

        # Check for required financial statements
        required_statements = ['income_statement', 'balance_sheet']
        financial_data = data.get('financial_data', {})

        for statement in required_statements:
            if statement not in financial_data:
                validation_report['issues'].append(f"Missing {statement}")
                validation_report['is_valid'] = False

        # Check for financial data completeness
        total_fields = 0
        populated_fields = 0

        for statement_name, statement_data in financial_data.items():
            if isinstance(statement_data, dict):
                for period, values in statement_data.items():
                    if isinstance(values, dict):
                        total_fields += len(values)
                        populated_fields += sum(1 for v in values.values() if v is not None)

        if total_fields > 0:
            completeness_score = populated_fields / total_fields
            validation_report['score'] = completeness_score

            if completeness_score < 0.5:
                validation_report['is_valid'] = False
                validation_report['issues'].append("Data completeness too low")
            elif completeness_score < 0.8:
                validation_report['warnings'].append("Some financial data may be missing")

        # Add metadata validation
        metadata = data.get('metadata', {})
        if 'filing_type' not in metadata:
            validation_report['warnings'].append("Could not determine filing type")
        if 'company_name' not in metadata:
            validation_report['warnings'].append("Could not extract company name")

        return validation_report

    def _parse_financial_statements(self, text: str) -> Dict[str, Any]:
        """Parse financial statements from text content."""
        statements = {}

        # Try to identify and extract income statement
        income_statement = self._extract_income_statement(text)
        if income_statement:
            statements['income_statement'] = income_statement

        # Try to identify and extract balance sheet
        balance_sheet = self._extract_balance_sheet(text)
        if balance_sheet:
            statements['balance_sheet'] = balance_sheet

        # Try to identify and extract cash flow statement
        cash_flow = self._extract_cash_flow(text)
        if cash_flow:
            statements['cash_flow'] = cash_flow

        return statements

    def _extract_income_statement(self, text: str) -> Optional[Dict[str, Any]]:
        """Extract income statement data from text."""
        # Look for common income statement items
        income_items = [
            r'(?i)revenue.*?(\d[\d,\.]*)',
            r'(?i)net income.*?(\d[\d,\.]*)',
            r'(?i)gross profit.*?(\d[\d,\.]*)',
            r'(?i)operating income.*?(\d[\d,\.]*)'
        ]

        data = {}
        for pattern in income_items:
            matches = re.findall(pattern, text)
            if matches:
                # Simple extraction - in practice would need more sophisticated parsing
                key = re.search(r'(?i)(revenue|net income|gross profit|operating income)', pattern).group(1)
                data[key] = self._clean_number(matches[0])

        return data if data else None

    def _extract_balance_sheet(self, text: str) -> Optional[Dict[str, Any]]:
        """Extract balance sheet data from text."""
        balance_items = [
            r'(?i)total assets.*?(\d[\d,\.]*)',
            r'(?i)total liabilities.*?(\d[\d,\.]*)',
            r'(?i)cash and cash equivalents.*?(\d[\d,\.]*)',
            r'(?i)total equity.*?(\d[\d,\.]*)'
        ]

        data = {}
        for pattern in balance_items:
            matches = re.findall(pattern, text)
            if matches:
                key = re.search(r'(?i)(total assets|total liabilities|cash and cash equivalents|total equity)', pattern).group(1)
                data[key] = self._clean_number(matches[0])

        return data if data else None

    def _extract_cash_flow(self, text: str) -> Optional[Dict[str, Any]]:
        """Extract cash flow statement data from text."""
        cash_items = [
            r'(?i)net cash from operating activities.*?(\d[\d,\.]*)',
            r'(?i)capital expenditures.*?(\d[\d,\.]*)',
            r'(?i)free cash flow.*?(\d[\d,\.]*)'
        ]

        data = {}
        for pattern in cash_items:
            matches = re.findall(pattern, text)
            if matches:
                key = re.search(r'(?i)(net cash from operating activities|capital expenditures|free cash flow)', pattern).group(1)
                data[key] = self._clean_number(matches[0])

        return data if data else None

    def _extract_metadata(self, text: str, file_path: str) -> Dict[str, Any]:
        """Extract metadata from document text."""
        metadata = {}

        # Extract company name
        company_match = re.search(r'(?i)company.*?[:\s]+([A-Z][A-Za-z\s&\-\(\)]{2,})', text)
        if company_match:
            metadata['company_name'] = company_match.group(1).strip()

        # Extract filing type
        filing_match = re.search(r'(?i)(10-k|10-q|8-k|form\s+[0-9a-z-]+)', text)
        if filing_match:
            metadata['filing_type'] = filing_match.group(1).upper()

        # Extract filing date
        date_match = re.search(r'(?i)filed.*?(\d{1,2}[-/]\d{1,2}[-/]\d{2,4})', text)
        if date_match:
            metadata['filing_date'] = date_match.group(1)

        # Add file information
        metadata['file_path'] = file_path
        metadata['file_size'] = os.path.getsize(file_path) if os.path.exists(file_path) else 0

        return metadata

    def _extract_structured_data(self, soup) -> Dict[str, Any]:
        """Extract structured data from HTML."""
        structured_data = {}

        # Look for JSON-LD structured data
        json_ld_scripts = soup.find_all('script', type='application/ld+json')
        for script in json_ld_scripts:
            try:
                data = json.loads(script.string)
                structured_data['json_ld'] = data
                break
            except:
                continue

        # Look for table data
        tables = soup.find_all('table')
        if tables:
            structured_data['tables_count'] = len(tables)

        return structured_data

    def _identify_statement_type(self, df) -> Optional[str]:
        """Identify financial statement type from DataFrame."""
        # Check for income statement keywords
        income_keywords = ['revenue', 'income', 'profit', 'expense']
        balance_keywords = ['asset', 'liability', 'equity', 'cash']
        cash_keywords = ['cash flow', 'operating', 'investing', 'financing']

        text_content = ' '.join(df.columns.astype(str)).lower()

        if any(keyword in text_content for keyword in income_keywords):
            return 'income_statement'
        elif any(keyword in text_content for keyword in balance_keywords):
            return 'balance_sheet'
        elif any(keyword in text_content for keyword in cash_keywords):
            return 'cash_flow'

        return None

    def _parse_excel_financial_data(self, df, statement_type: str) -> Dict[str, Any]:
        """Parse financial data from Excel DataFrame."""
        data = {}

        # Convert to dictionary format
        for col in df.columns:
            if col != df.columns[0]:  # Skip first column (usually labels)
                period_data = {}
                for idx, value in df[col].items():
                    if pd.notna(value):
                        label = str(df.iloc[idx, 0]) if idx < len(df) else f"Row_{idx}"
                        period_data[label] = self._clean_number(str(value))
                data[str(col)] = period_data

        return data

    def _extract_excel_metadata(self, excel_path: str) -> Dict[str, Any]:
        """Extract metadata from Excel file."""
        return {
            'file_path': excel_path,
            'file_size': os.path.getsize(excel_path),
            'file_type': 'excel'
        }

    def _normalize_income_statement(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Normalize income statement data."""
        # Standardize field names and ensure numeric values
        normalized = {}
        for period, values in data.items():
            normalized_period = {}
            for key, value in values.items():
                # Standardize field names
                key_lower = key.lower().replace(' ', '_')
                normalized_period[key_lower] = float(value) if self._is_number(value) else None
            normalized[period] = normalized_period
        return normalized

    def _normalize_balance_sheet(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Normalize balance sheet data."""
        normalized = {}
        for period, values in data.items():
            normalized_period = {}
            for key, value in values.items():
                key_lower = key.lower().replace(' ', '_')
                normalized_period[key_lower] = float(value) if self._is_number(value) else None
            normalized[period] = normalized_period
        return normalized

    def _normalize_cash_flow(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Normalize cash flow data."""
        normalized = {}
        for period, values in data.items():
            normalized_period = {}
            for key, value in values.items():
                key_lower = key.lower().replace(' ', '_')
                normalized_period[key_lower] = float(value) if self._is_number(value) else None
            normalized[period] = normalized_period
        return normalized

    def _clean_number(self, value: str) -> Optional[float]:
        """Clean and convert number string to float."""
        if not value:
            return None

        # Remove common formatting
        cleaned = str(value).replace(',', '').replace('$', '').replace('(', '-').replace(')', '')

        try:
            return float(cleaned)
        except (ValueError, TypeError):
            return None

    def _is_number(self, value) -> bool:
        """Check if value can be converted to number."""
        try:
            float(value)
            return True
        except (ValueError, TypeError):
            return False


def main():
    """Example usage of FileProcessor."""
    processor = FileProcessor()

    # Example usage
    file_path = "path/to/sec/filing.pdf"

    try:
        if file_path.endswith('.pdf'):
            result = processor.extract_pdf_data(file_path)
        elif file_path.endswith('.html'):
            result = processor.extract_html_data(file_path)
        elif file_path.endswith(('.xlsx', '.xls')):
            result = processor.extract_excel_data(file_path)
        else:
            raise ValueError("Unsupported file format")

        # Normalize data
        normalized = processor.normalize_financial_data(result)

        # Validate extraction
        validation = processor.validate_extraction(normalized)

        print(f"Extraction successful: {validation['is_valid']}")
        print(f"Data completeness: {validation['score']:.2%}")

    except Exception as e:
        print(f"Error: {e}")


if __name__ == "__main__":
    main()