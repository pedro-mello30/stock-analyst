# Chart Templates and Specifications

This reference provides specifications for creating professional financial charts with consistent formatting and best practices.

## Chart Type Specifications

### 1. Ratio Analysis Charts

#### Multi-Line Ratio Trend Chart
**Purpose**: Display multiple financial ratios over time for trend analysis
**Dimensions**: 1200x800 pixels (16:10 ratio)
**Colors**: Use consistent color scheme across all ratios
**Data Points**: Minimum 4 time periods for meaningful trends

**Specifications**:
- **Title**: "Company Name - Ratio Analysis" (14pt, bold)
- **X-Axis**: Time periods (quarters or years)
- **Y-Axis**: Ratio values with appropriate scaling
- **Legend**: Clear identification of each ratio line
- **Gridlines**: Light gray, horizontal only
- **Data Labels**: Optional for key inflection points

**Color Scheme**:
- Liquidity Ratios: Blue family (Current: #2E86AB, Quick: #5AA9E6)
- Profitability Ratios: Green family (Gross: #2CA453, Net: #66BB6A)
- Leverage Ratios: Red/Orange family (Debt/Equity: #D32F2F, Debt/Assets: #FF7043)
- Efficiency Ratios: Purple family (Asset Turnover: #7E57C2, Inventory: #AB47BC)

**Best Practices**:
- Use line charts with markers for discrete data points
- Maintain consistent axis scales for comparison
- Highlight industry benchmarks with dashed reference lines
- Include data source and date in chart footer

#### Single Ratio Comparison Chart
**Purpose**: Compare single ratio across multiple companies or periods
**Chart Type**: Bar chart or grouped bar chart
**Dimensions**: 1000x600 pixels

**Specifications**:
- **X-Axis**: Companies or time periods
- **Y-Axis**: Ratio values
- **Bars**: Solid colors with subtle gradients
- **Annotations**: Industry average as reference line

### 2. Trend Analysis Charts

#### Revenue and Earnings Trend Chart
**Purpose**: Show top-line and bottom-line performance over time
**Chart Type**: Dual-axis line chart
**Dimensions**: 1200x800 pixels

**Specifications**:
- **Primary Y-Axis**: Revenue (left, currency format)
- **Secondary Y-Axis**: Earnings (right, currency format)
- **X-Axis**: Time periods
- **Lines**: Solid for revenue, dashed for earnings
- **Colors**: Revenue: #2E86AB, Earnings: #D32F2F

**Data Requirements**:
- Minimum 8 data points for trend identification
- Consistent time intervals
- YoY and QoQ growth rate annotations

#### Margin Trend Chart
**Purpose**: Display profitability margin trends over time
**Chart Type**: Area chart or line chart
**Dimensions**: 1000x600 pixels

**Specifications**:
- **Y-Axis**: Margin percentages (0-100%)
- **Colors**: Gradient from red (low) to green (high)
- **Reference Lines**: Industry average margins
- **Annotations**: Key events affecting margins

**Color Coding**:
- Gross Margin: #4CAF50
- Operating Margin: #2196F3
- Net Margin: #9C27B0

### 3. Waterfall Charts

#### Cash Flow Waterfall Chart
**Purpose**: Show sources and uses of cash flow
**Chart Type**: Waterfall chart
**Dimensions**: 1000x700 pixels

**Specifications**:
- **Starting Point**: Net income or operating cash flow
- **Positive Values**: Cash inflows (green bars)
- **Negative Values**: Cash outflows (red bars)
- **Ending Point**: Free cash flow or ending cash balance

**Bar Formatting**:
- **Net Income**: Dark blue (#1976D2)
- **Non-Cash Adjustments**: Light blue (#90CAF9)
- **Working Capital Changes**: Gray (#757575)
- **Capital Expenditures**: Orange (#FF9800)
- **Free Cash Flow**: Dark green (#2E7D32)

**Best Practices**:
- Use connector lines between bars
- Add value labels on each bar
- Include cumulative total line
- Highlight significant drivers

#### Revenue Waterfall Chart
**Purpose**: Break down revenue changes from period to period
**Chart Type**: Waterfall chart
**Dimensions**: 1200x800 pixels

**Components**:
- **Base Period Revenue**: Starting bar
- **Price Changes**: Volume vs. price decomposition
- **Volume Changes**: Quantity impact
- **Currency Impact**: FX effects
- **Acquisitions/Disposals**: M&A impact
- **Current Period Revenue**: Ending bar

### 4. Executive Summary Dashboards

#### Key Metrics Dashboard
**Purpose**: High-level overview of critical financial metrics
**Chart Type**: Multi-panel dashboard
**Dimensions**: 1600x1200 pixels

**Layout**:
- **Top Row**: Revenue and earnings charts (2 panels)
- **Middle Row**: Margin and ratio charts (2 panels)
- **Bottom Row**: Cash flow and valuation metrics (2 panels)

**Panel Specifications**:
- **Individual Panel Size**: 500x350 pixels
- **Consistent Color Scheme**: Across all panels
- **Metric Cards**: Key numbers with trend indicators
- **Sparklines**: Mini trend charts for each metric

#### Risk Assessment Dashboard
**Purpose**: Visual summary of risk factors and mitigation
**Chart Type**: Mixed chart types
**Dimensions**: 1400x1000 pixels

**Components**:
- **Risk Heat Map**: Matrix of likelihood vs. impact
- **Risk Category Distribution**: Pie chart of risk categories
- **Mitigation Progress**: Progress bars for key risks
- **Risk Trend**: Line chart of overall risk score over time

## Chart Formatting Standards

### Typography
- **Font Family**: Sans-serif (Arial, Helvetica, or system fonts)
- **Title Font Size**: 14-16pt, bold
- **Axis Labels**: 11-12pt
- **Data Labels**: 9-10pt
- **Legend**: 10-11pt

### Color Standards
- **Primary Colors**: Use company brand colors when available
- **Accessibility**: Ensure color contrast for readability
- **Color Blind Friendly**: Avoid red-green combinations alone
- **Consistency**: Use same colors for same metrics across charts

### Grid and Layout
- **Gridlines**: Light gray (#E0E0E0), horizontal only for line charts
- **Margins**: Minimum 20px around chart area
- **Spacing**: Consistent spacing between chart elements
- **Alignment**: Proper alignment of chart components

### Data Presentation
- **Precision**: Round numbers appropriately (no more than 2 decimal places for most metrics)
- **Currency**: Use appropriate currency symbols and formatting
- **Percentages**: Display with % symbol, proper rounding
- **Date Format**: Consistent date formatting (MMM YYYY or YYYY format)

## Chart Generation Guidelines

### Data Preparation
1. **Data Quality**: Ensure data accuracy and completeness
2. **Time Periods**: Use consistent time intervals
3. **Outliers**: Identify and handle outliers appropriately
4. **Scaling**: Choose appropriate scales for data range

### Chart Creation Process
1. **Select Chart Type**: Based on data and message
2. **Set Dimensions**: Appropriate size for intended use
3. **Apply Formatting**: Consistent styles and colors
4. **Add Annotations**: Context and explanations
5. **Review**: Check for accuracy and readability

### Quality Control
- **Data Accuracy**: Verify all calculations and data sources
- **Visual Clarity**: Ensure charts are readable at intended size
- **Message Clarity**: Chart should clearly convey intended insight
- **Professional Appearance**: Consistent with company standards

## Chart Integration Guidelines

### PowerPoint Integration
- **Chart Size**: Optimize for slide dimensions
- **Resolution**: 300 DPI for professional presentation
- **File Format**: PNG or embedded chart objects
- **Animation**: Use sparingly, only when it adds value

### Word Document Integration
- **Chart Size**: Fit within document margins
- **Resolution**: 150-300 DPI for print quality
- **Captions**: Include descriptive captions
- **Referencing**: Reference charts in text

### Excel Integration
- **Chart Objects**: Use Excel chart objects for interactivity
- **Data Links**: Maintain live data connections
- **Formatting**: Apply consistent Excel chart styles
- **Export**: Export as high-resolution images when needed

## Chart Templates

### Template Structure
Each chart template should include:
1. **Data Input Range**: Clearly defined data source
2. **Chart Formatting**: Pre-applied styles and colors
3. **Axis Configuration**: Proper scaling and labels
4. **Legend Setup**: Consistent legend formatting
5. **Title and Labels**: Pre-formatted text elements

### Template Maintenance
- **Version Control**: Track changes to chart templates
- **Brand Updates**: Update templates when brand guidelines change
- **Technology Updates**: Update templates for new software versions
- **User Feedback**: Incorporate feedback for template improvements

This reference ensures consistent, professional chart creation that effectively communicates financial analysis results.