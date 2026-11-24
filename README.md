# AI Product Description Generator

Task AI-CM-008 | Data Alcott Systems | Free Online AI & Data Science Internship
Name: Samudrala Neha
Student Code: DAS014399

## About the project
This project takes product details like name, category, features, target audience and
customer reviews, and generates product descriptions for e-commerce platforms.

It makes:
- short description
- long description
- bullet points
- SEO title and meta description
- keywords

Platforms supported: Amazon, Flipkart, Shopify, WooCommerce and Social Media.

## Features
- Product data parsing
- Feature extraction (feature -> customer benefit)
- Short and long description generation
- Bullet point generation
- SEO meta generation
- Multi-platform support
- Tone customization (professional, friendly, premium, casual, youthful)
- Keyword integration
- Review analysis (positive/negative words)
- A/B testing variants

## How to run
1. Install Python 3 (or use Google Colab)
2. Keep simple_generator.py in a folder
3. Run this command in the terminal:

python simple_generator.py

No extra libraries are needed. The output is printed on screen and also saved
in output_descriptions.json.

## Using your own product
Open simple_generator.py, go to the bottom and change the `product` dictionary
(name, category, features, target_audience, main_benefit, reviews). Then run again.

## Files
- simple_generator.py - main code
- output_descriptions.json - sample output
- REPORT.md - project report
- README.md - this file
