# Stack Overflow Developer Survey Dashboard

A comprehensive modular dashboard project analyzing developer trends from Stack Overflow Developer Surveys (2017-2025). This project explores work mode transformations, compensation patterns, technology adoption, and framework evolution in the software development ecosystem.

## 📊 Project Overview

**8 Interactive Dashboards** covering:
- Work mode evolution and COVID-19 impact
- Company size and flexibility patterns
- Developer compensation analysis
- Programming language trends
- Framework ecosystem evolution

## 📁 Project Structure

```
stack_overflow_dashboard/
├── config/                    # Configuration settings
│   ├── __init__.py
│   └── config.py             # Central config (CSV path, colors, ports)
│
├── utils/                     # Shared utilities
│   ├── __init__.py
│   ├── data_loader.py        # Data loading functions
│   ├── data_processing.py    # Data canonicalization & cleaning
│   └── browser_utils.py      # Browser automation utilities
│
├── h1a/                       # Hypothesis 1A: Global Work Mode Shift
│   ├── __init__.py
│   ├── layout.py             # Dashboard layout components
│   ├── callbacks.py          # Interactive callbacks
│   └── run_h1a.py           # Entry point (Port 8051)
│
├── h1b/                       # Hypothesis 1B: Flexibility by Organization Size
│   ├── __init__.py
│   ├── layout.py
│   ├── callbacks.py
│   └── run_h1b.py           # Entry point (Port 8052)
│
├── h2/                        # Hypothesis 2: Flexibility Gap Evolution
│   ├── __init__.py
│   ├── layout.py
│   ├── callbacks.py
│   ├── data_processing.py    # H2-specific data processing
│   └── run_h2.py            # Entry point (Port 8053)
│
├── h3/                        # Hypothesis 3: The Flexibility Dividend
│   ├── __init__.py
│   ├── layout.py
│   ├── callbacks.py
│   ├── data_processing.py    # H3-specific data processing
│   └── run_h3.py            # Entry point (Port 8054)
│
├── h4/                        # Hypothesis 4: Experience vs Compensation
│   ├── __init__.py
│   ├── layout.py
│   ├── callbacks.py
│   ├── data_processing.py    # H4-specific data processing
│   └── run_h4.py            # Entry point (Port 8055)
│
├── h5/                        # Hypothesis 5: Programming Language Evolution
│   ├── __init__.py
│   ├── layout.py
│   ├── callbacks.py
│   ├── data_processing.py    # H5-specific data processing
│   └── run_h5.py            # Entry point (Port 8056)
│
├── h6a/                       # Hypothesis 6A: Framework Cohorts
│   ├── __init__.py
│   ├── layout.py
│   ├── callbacks.py
│   ├── data_processing.py    # H6a-specific data processing
│   └── run_h6a.py           # Entry point (Port 8057)
│
├── h6b/                       # Hypothesis 6B: Framework Lifecycles
│   ├── __init__.py
│   ├── layout.py
│   ├── callbacks.py
│   ├── data_processing.py    # H6b-specific data processing
│   └── run_h6b.py           # Entry point (Port 8058)
│
├── requirements.txt           # Python dependencies
├── README.md                 # This file
├── QUICKSTART.md             # Quick setup guide
└── COMPLETE_PROJECT_STRUCTURE.txt  # Detailed architecture
```

## 🎯 Hypotheses

### H1A: Global Shift in Work Mode (2017-2025)
**Port: 8050** | **Focus: COVID-19 Impact**

Analyzes how the COVID-19 pandemic transformed developer work arrangements globally.

**Features:**
- Pre/Post COVID comparison metrics
- Interactive timeline visualizations (line, area, bar charts)
- Story mode highlighting the critical 2018-2022 transition period
- Year-over-year growth rate analysis
- COVID-19 pandemic marker for temporal context

**Key Insights:**
- Remote work adoption surge in 2020
- Dramatic shift from on-site to remote/hybrid
- Persistence of flexible arrangements post-pandemic

---

### H1B: Who Gets Hybrid? Flexibility by Organization Size (2025)
**Port: 8051** | **Focus: Company Size Patterns**

Explores how company size determines access to flexible work arrangements.

**Features:**
- Work mode distribution across company sizes
- Multiple visualization types (grouped bar, stacked bar, heatmap, pie charts)
- Evolution trends (2020-2025) by company size
- Deep dive filtering by company size and experience level
- Flexibility adoption comparison

**Key Insights:**
- Larger companies offer more flexibility
- SMBs lag in hybrid adoption
- Experience level influences work mode access

---

### H2: The Flexibility Gap Evolution (2017-2025)
**Port: 8052** | **Focus: 8-Year Gap Analysis**

Tracks how differences in work flexibility between company sizes evolved over time.

**Features:**
- Flexibility gap tracking (max - min)
- Company size trajectory analysis (4 visualization types)
- Interactive year-to-year comparisons
- Comprehensive heatmaps
- Individual company size deep dives

**Key Insights:**
- Gap widened during COVID-19
- Enterprise vs SMB divide
- Convergence trends in recent years

---

### H3: The Flexibility Dividend (2017-2025)
**Port: 8053** | **Focus: Job Satisfaction Analysis**

Analyzes whether work mode flexibility impacts job satisfaction.

**Features:**
- Pre/Post COVID satisfaction comparison across work modes
- Multiple visualization types (box plot, violin plot, bar chart, line chart)
- Satisfaction change analysis and rankings
- Timeline evolution showing trends
- Interactive deep dive by work mode, period, and dimensions

**Key Insights:**
- Remote work correlates with higher satisfaction
- Hybrid offers balanced benefits
- On-site satisfaction declined post-COVID

---

### H4: Experience vs Compensation (2017-2025)
**Port: 8054** | **Focus: Salary Analysis**

Explores the relationship between coding experience and annual compensation.

**Features:**
- Scatter plot with OLS trendlines
- Compensation outlier clipping (1-99 percentiles)
- Multi-filter system (year, work mode, company size)
- Hover data includes company size and job satisfaction
- Experience-salary correlation visualization

**Key Insights:**
- Strong positive correlation between experience and compensation
- Work mode affects compensation patterns
- Company size influences salary ranges

---

### H5: Programming Language Evolution (2017-2025)
**Port: 8055** | **Focus: Language Popularity Trends**

Tracks the rise and fall of programming languages over time.

**Features:**
- Multi-line time series for language evolution
- Multi-delimiter parsing for survey data
- Top 12 language tracking by total mentions
- Share calculation with year aggregation
- Dynamic language selection

**Key Insights:**
- JavaScript maintains dominance
- Python's steady growth
- Legacy language decline
- Emerging language adoption patterns

---

### H6a: Framework Cohorts - Rise & Fall (2017-2025)
**Port: 8056** | **Focus: Front-End vs Back-End Evolution**

Analyzes framework popularity within cohorts (Front-End, Back-End, Other).

**Features:**
- Intelligent cohort classification
- Cohort-specific color palettes for visual distinction
- Dynamic top N selection (3-15 frameworks)
- Framework competition tracking within cohorts
- Configurable framework definitions

**Cohort Classifications:**
- **Front-End:** React, Angular, Vue.js, Svelte, Ember.js, Next.js, Nuxt.js
- **Back-End:** Django, Flask, Spring, Express, Laravel, FastAPI, Ruby on Rails, ASP.NET, ASP.NET Core
- **Other:** All other frameworks

**Key Insights:**
- React dominance in front-end
- Express growth in back-end
- Framework consolidation trends

---

### H6b: Framework Lifecycles - Entry & Peak (2017-2025)
**Port: 8057** | **Focus: Framework Lifecycle Analysis**

Tracks when frameworks first appeared and when they reached peak popularity.

**Features:**
- Lifecycle statistics calculation (first year, peak year, peak share)
- Peak marker annotations on chart
- Professional styled DataTable with lifecycle metrics
- Dual output callback (chart + table synchronized)
- Sortable table by any column

**Lifecycle Metrics:**
- **First Year:** Framework entry into ecosystem
- **Peak Year:** Year of maximum usage
- **Peak Share:** Maximum adoption percentage

**Key Insights:**
- Fast-growing frameworks reach peak in 1-2 years
- Mature frameworks show stability
- Declining frameworks past their peak

---

## Features

### Modular Architecture
- **Separation of concerns**: Layout, callbacks, and data processing are separated
- **Reusable utilities**: Common functions are centralized in the `utils` module
- **Easy maintenance**: Each hypothesis is self-contained and easy to modify
- **Consistent configuration**: All settings in one place (`config/config.py`)
- **37 module files**: Professional organization across 8 dashboards

### Interactive Visualizations
- Multiple chart types (line, area, bar, scatter, heatmap, pie, box, violin)
- COVID-19 pandemic markers for temporal context
- Hover tooltips with detailed information
- Dynamic filtering and comparison tools
- Peak annotations and trendlines
- Cohort-specific color palettes

### Advanced Data Processing
- Automatic work mode canonicalization
- Company size cleaning and sorting
- Compensation outlier clipping
- Multi-delimiter parsing for list columns
- Framework cohort classification
- Lifecycle statistics calculation
- Efficient data aggregation

### Professional UI/UX
- Bootstrap styling for professional appearance
- Responsive design
- Informative tooltips and descriptions
- Automatic browser opening
- Progress messages and logging
- Graceful error handling

---

## 📊 Technical Stack

- **Dash**: Web application framework for interactive dashboards
- **Plotly**: Interactive visualization library with rich chart types
- **Pandas**: Data manipulation and analysis
- **Bootstrap**: Responsive UI components via dash-bootstrap-components
- **Python**: 3.8+ recommended

---

## 🎓 Use Cases

### Academic Research
- Work mode transformation studies
- Technology adoption analysis
- Developer satisfaction research
- Compensation trend analysis

### Industry Insights
- Recruitment strategy planning
- Competitive compensation analysis
- Technology stack decisions
- Framework adoption trends

### Data Visualization
- Interactive dashboard design patterns
- Modular architecture examples
- Professional data presentation
- Multi-hypothesis analysis

---
