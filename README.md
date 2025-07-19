# Smart Grocery & Budget Assistant 🛒

A comprehensive web application built with Streamlit that helps you manage your grocery shopping and budget effectively. Track your purchases, set budgets, analyze spending patterns, and get smart recommendations for better financial management.

## ✨ Features

### 📊 Dashboard
- **Real-time Overview**: Get instant insights into your grocery spending
- **Key Metrics**: Total items, spending, categories, and average item cost
- **Recent Purchases**: Quick view of your latest grocery additions
- **Budget Status**: Visual progress bars showing budget vs actual spending

### 🛍️ Grocery Management
- **Easy Item Addition**: Add items with details like price, quantity, category, brand, and expiry date
- **Smart Categorization**: Pre-defined categories for better organization
- **Advanced Search & Filter**: Find items by name, category, or other criteria
- **Expiry Tracking**: Never let food go to waste with expiry date alerts

### 💰 Budget Management
- **Monthly Budget Setting**: Set category-wise monthly budgets
- **Budget vs Actual Tracking**: Visual comparison of planned vs actual spending
- **Overspending Alerts**: Get notified when you exceed category budgets
- **Historical Budget Data**: Track budget performance over time

### 📈 Advanced Analytics
- **Spending Distribution**: Pie charts showing spending by category
- **Trend Analysis**: Line graphs of daily spending patterns
- **Top Expensive Items**: Identify your costliest purchases
- **Shopping Frequency**: Understand your shopping habits by category

### 🎯 Smart Recommendations
- **Budget Optimization**: Get suggestions to stay within budget
- **Price Alerts**: Recommendations for expensive items
- **Expiry Warnings**: 7-day expiry alerts to reduce food waste
- **Seasonal Tips**: Monthly suggestions for seasonal produce
- **Shopping Pattern Insights**: Personalized recommendations based on your habits

## 🚀 Quick Start

### Prerequisites
- Python 3.7 or higher
- pip package manager

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/yourusername/smart-grocery-budget-assistant.git
   cd smart-grocery-budget-assistant
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the application**
   ```bash
   streamlit run app.py
   ```

4. **Open your browser**
   Navigate to `http://localhost:8501` to start using the app!

## 📱 Usage Guide

### Adding Your First Grocery Item
1. Navigate to "Add Grocery Item" in the sidebar
2. Fill in the item details (name, category, price, quantity)
3. Optionally add brand and expiry date
4. Click "Add Item" to save

### Setting Up Your Budget
1. Go to "Budget Manager"
2. Select a category and set your monthly budget
3. The app will automatically track your spending against this budget
4. View your budget status on the Dashboard

### Analyzing Your Spending
1. Visit the "Analytics" page for detailed insights
2. View spending distribution, trends, and top expensive items
3. Use these insights to make informed decisions about your grocery spending

### Getting Smart Recommendations
1. Check the "Smart Recommendations" page
2. Get personalized tips based on your shopping patterns
3. Receive alerts for expiring items and budget overruns
4. Learn about seasonal produce for cost savings

## 🛠️ Technical Details

### Built With
- **Streamlit**: Modern web framework for Python
- **Pandas**: Data manipulation and analysis
- **Plotly**: Interactive visualizations
- **JSON**: Data persistence (files stored locally)

### Data Storage
- Grocery items and budget data are stored in local JSON files
- `grocery_data.json`: Stores all grocery items with their details
- `budget_data.json`: Stores budget allocations and spending data

### Project Structure
```
smart-grocery-budget-assistant/
│
├── app.py                 # Main Streamlit application
├── requirements.txt       # Python dependencies
├── README.md             # Project documentation
├── grocery_data.json     # Grocery items data (created automatically)
└── budget_data.json      # Budget data (created automatically)
```

## 🎨 Features Showcase

### Dashboard Preview
- Clean, intuitive interface with key metrics at a glance
- Recent purchases with expandable details
- Budget progress bars with color-coded status

### Smart Analytics
- Interactive pie charts for spending distribution
- Time-series analysis of spending patterns
- Detailed breakdowns of expensive purchases

### Budget Intelligence
- Visual budget vs actual comparisons
- Proactive overspending alerts
- Category-wise budget management

### Personalized Recommendations
- AI-powered spending insights
- Seasonal shopping tips
- Food waste reduction through expiry tracking

## 🔧 Customization

### Adding New Categories
Modify the `get_category_suggestions()` function in `app.py` to add or remove categories:

```python
def get_category_suggestions():
    return [
        "Your Custom Category",
        "Fruits & Vegetables",
        # ... other categories
    ]
```

### Modifying Data Storage
Currently uses JSON files for simplicity. Can be easily extended to use:
- SQLite database
- PostgreSQL
- MongoDB
- Cloud storage solutions

## 🚀 Future Enhancements

- [ ] **Multi-user Support**: User authentication and personal data separation
- [ ] **Receipt Scanning**: OCR integration for automatic item entry
- [ ] **Price Comparison**: Integration with grocery store APIs
- [ ] **Meal Planning**: Recipe suggestions based on available items
- [ ] **Shopping List Sharing**: Collaborative grocery lists
- [ ] **Mobile App**: React Native or Flutter mobile application
- [ ] **Barcode Scanning**: Quick item addition via barcode
- [ ] **Nutritional Tracking**: Health and nutrition insights
- [ ] **Store Locator**: Find best prices at nearby stores
- [ ] **Coupons Integration**: Automatic coupon recommendations

## 🤝 Contributing

We welcome contributions! Here's how you can help:

1. **Fork the repository**
2. **Create a feature branch** (`git checkout -b feature/AmazingFeature`)
3. **Commit your changes** (`git commit -m 'Add some AmazingFeature'`)
4. **Push to the branch** (`git push origin feature/AmazingFeature`)
5. **Open a Pull Request**

### Contribution Guidelines
- Follow PEP 8 style guidelines
- Add comments for complex logic
- Update documentation for new features
- Test your changes thoroughly

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- **Streamlit Team** for the amazing framework
- **Plotly** for beautiful interactive visualizations
- **Pandas** for powerful data manipulation capabilities
- **Open Source Community** for inspiration and tools

## 📞 Support

If you have any questions, suggestions, or issues:

- **Create an Issue**: Use GitHub Issues for bug reports and feature requests
- **Discussions**: Join our GitHub Discussions for general questions
- **Email**: [your-email@example.com](mailto:your-email@example.com)

## 🌟 Show Your Support

If you find this project helpful:
- ⭐ Star the repository
- 🐛 Report bugs
- 💡 Suggest new features
- 🤝 Contribute to the code
- 📢 Share with friends and colleagues

---

**Made with ❤️ and Python**

*Transform your grocery shopping experience with smart budgeting and analytics!*
