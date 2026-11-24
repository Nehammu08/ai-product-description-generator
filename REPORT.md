# Project Report - AI Product Description Generator

Name: Samudrala Neha | Student Code: DAS014399 | Task: AI-CM-008

## 1. Aim
To build a system that creates product descriptions for e-commerce platforms from product details,
using Python, basic NLP and templates.

## 2. How I built it
1. **Parsing** - `parse_product()` checks the input, converts the feature string into a list and fills missing values.
2. **Feature extraction** - `get_benefit()` looks for a keyword (battery, gps, display...) in the feature and
   gives the benefit for the customer, because customers care about benefits more than specifications.
3. **Review analysis** - `analyse_reviews()` counts positive and negative words and gives the sentiment,
   praised words and complaints. Praised words are used in a bullet point.
4. **Keywords** - `get_keywords()` uses category, features, modifier words like "best"/"buy" and the most
   common review words (after removing stop words).
5. **Generation** - short description, bullets, long description and SEO meta are made using templates.
   Each platform has its own length limit, bullet count and default tone.
6. **Tone and A/B testing** - 4 tones (professional, friendly, premium, casual). `ab_variants()` makes the same
   description in different tones so they can be compared.

## 3. Output
For the sample product "SmartWatch Pro X", descriptions were generated for all 5 platforms.
Every output stayed within the platform length limit. Review analysis gave positive sentiment
(praised: great, bright, accurate; complaints: slow, cheap).

## 4. Problems I faced
- **Words getting cut in the middle:** when a description crossed the platform limit, normal slicing cut
  a word in half. I solved it with `cut_text()`, which cuts at the last space.
- **Grammar mistake:** the text sometimes said "a exceptional smartwatch". I added a small a/an check
  based on the first letter of the adjective.
- **Running the code:** I ran the code in Google Colab by pasting the whole file in one cell and
  checked that the JSON output, A/B variants and all 5 platforms were printed correctly.
- **Making it my own:** I added new features to the `BENEFITS` dictionary (camera, fast charging,
  lightweight) and a new tone called "youthful", then ran it again to check it worked.

## 5. Limitations and future work
- It is template based, so the variety is limited.
- Sentiment uses a small word list only.
- Future: use an LLM / Transformers for better text, spaCy for keywords, and a Flask web interface.

## 6. Tools used
I used an AI assistant for guidance and help while building and debugging, as allowed in the task FAQ.
I ran, tested and modified the code myself and I can explain how each function works.

## 7. Conclusion
The project covers all the core features and the bonus features (multi-platform, tone, keywords,
review analysis, A/B variants) using only Python.
