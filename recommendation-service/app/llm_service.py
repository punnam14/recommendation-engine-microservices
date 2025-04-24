import openai
import requests
import json
from .config import config
import os
from datetime import datetime

class LLMService:
   """
   Service to handle interactions with the LLM API
   """
  
   def __init__(self):
       """
       Initialize the LLM service with configuration
       """
       openai.api_key = config['OPENAI_API_KEY']
       self.model_name = config['MODEL_NAME']
       self.max_tokens = config['MAX_TOKENS']
       self.temperature = config['TEMPERATURE']
       self.api_key = config['OPENAI_API_KEY']
       self.gemini_url = f"https://generativelanguage.googleapis.com/v1beta/models/{self.model_name}:generateContent?key={self.api_key}"
  
   def generate_recommendations(self, user_preferences, browsing_history, all_products):
       """
       Generate personalized product recommendations based on user preferences and browsing history
      
       Parameters:
       - user_preferences (dict): User's stated preferences
       - browsing_history (list): List of product IDs the user has viewed
       - all_products (list): Full product catalog
      
       Returns:
       - dict: Recommended products with explanations
       """
       # TODO: Implement LLM-based recommendation logic
       # This is where your prompt engineering expertise will be evaluated
      
       # Get browsed products details
       browsed_products = []
       for product_id in browsing_history:
           for product in all_products:
               if product["id"] == product_id:
                   browsed_products.append(product)
                   break
      
       filtered_products = self._filter_products_for_llm(user_preferences, browsed_products, all_products)
       
       # Create a prompt for the LLM
       prompt = self._create_recommendation_prompt(user_preferences, browsed_products, filtered_products)

       # IMPLEMENT YOUR PROMPT ENGINEERING HERE
       # prompt = self._create_recommendation_prompt(user_preferences, browsed_products, all_products)
      
       # Call the LLM API
       try:
           response = requests.post(
               self.gemini_url,
               headers={"Content-Type": "application/json"},
               json={
                   "contents": [{
                       "parts": [{"text": prompt}]
                   }],
                   "generationConfig": {
                       "temperature": self.temperature,
                       "maxOutputTokens": self.max_tokens
                   }
               }
           )

           if response.status_code != 200:
               raise Exception(f"Gemini API error: {response.text}")

           raw_text = response.json()['candidates'][0]['content']['parts'][0]['text']
           print("RAW LLM RESPONSE:", raw_text)

           # Log token usage
           self._log_token_counts(prompt, raw_text)
          
           # Parse the LLM response to extract recommendations
           # IMPLEMENT YOUR RESPONSE PARSING LOGIC HERE
           recommendations = self._parse_recommendation_response(raw_text, all_products)
           return recommendations
          
       except Exception as e:
           # Handle any errors from the LLM API
           print(f"Error calling LLM API: {str(e)}")
           raise Exception(f"Failed to generate recommendations: {str(e)}")
  
   def _create_recommendation_prompt(self, user_preferences, browsed_products, all_products):
       """
       Create a prompt for the LLM to generate recommendations
      
       This is where you should implement your prompt engineering strategy.
      
       Parameters:
       - user_preferences (dict): User's stated preferences
       - browsed_products (list): Products the user has viewed
       - all_products (list): Full product catalog
      
       Returns:
       - str: Prompt for the LLM
       """
       # TODO: Implement your prompt engineering strategy
       # THIS FUNCTION MUST BE IMPLEMENTED BY THE CANDIDATE
      
       # Example basic prompt structure (you should significantly improve this):
       prompt = "Based on the following user preferences and browsing history, recommend 8 products from the catalog with explanations.\n\n"
      
       # Add user preferences to the prompt
       prompt += "User Preferences:\n"
       for key, value in user_preferences.items():
           prompt += f"- {key}: {value}\n"
      
       # Add browsing history to the prompt
       prompt += "\nBrowsing History:\n"
       for product in browsed_products:
           prompt += f"- {product['name']} (Category: {product['category']}, Price: ${product['price']})\n"
      
       # Add instructions for the response format
       prompt += (
           "\nPlease recommend exactly 8 products from the catalog that match the user's preferences and browsing history.\n"
           "Prioritize:\n"
           "- Products similar to what the user browsed before (see history above)\n"
           "- Products that fall into the selected categories: " + ", ".join(user_preferences.get("categories", [])) + "\n"
           "If nothing matches perfectly, use your best judgment to pick the most relevant options.\n"
           "For each recommendation, include:\n"
           "- 'product_id': must match an existing ID from the catalog below\n"
           "- 'explanation': a friendly, persuasive message that tells the user why they'll love this product\n"
           "  — Use a tone like a shopping assistant helping them, not a developer or analyst.\n"
           "  — Speak directly to the user (use phrases like 'you' and 'your').\n"
           "  — Mention things like preferences, categories, or brands in a natural way.\n"
           "- 'score': your confidence in the recommendation, 1 to 10.\n"
       )
       prompt += "\nFormat your response as a JSON array with objects containing 'product_id', 'explanation', and 'score' (1-10 indicating confidence)."
       prompt += ("\nIMPORTANT: Only recommend products that exist in the following catalog. "
                   "Use the exact 'id' values provided below. Do not invent product names or IDs.\n")
      
       prompt += "\nHere are product IDs and names in the catalog:\n"
       for product in all_products[:20]: 
           prompt += f"- {product['id']}: {product['name']}\n"


       # You would likely want to include the product catalog in the prompt
       # But be careful about token limits!
       # For a real implementation, you might need to filter the catalog to relevant products first
      
       return prompt
  
   def _parse_recommendation_response(self, llm_response, all_products):
       """
       Parse the LLM response to extract product recommendations
      
       Parameters:
       - llm_response (str): Raw response from the LLM
       - all_products (list): Full product catalog to match IDs with full product info
      
       Returns:
       - dict: Structured recommendations
       """
       # TODO: Implement response parsing logic
       # THIS FUNCTION MUST BE IMPLEMENTED BY THE CANDIDATE
      
       # Example implementation (very basic, should be improved):
       try:
           import json
           # Attempt to parse JSON from the response
           # Note: This is a simplistic approach and should be made more robust
           # The candidate should implement better parsing logic
          
           # Find JSON content in the response
           start_idx = llm_response.find('[')
           end_idx = llm_response.rfind(']') + 1
          
           if start_idx == -1 or end_idx == 0:
               # Fallback if JSON parsing fails
               return {
                   "recommendations": [],
                   "error": "Could not parse recommendations from LLM response"
               }
          
           json_str = llm_response[start_idx:end_idx]
           rec_data = json.loads(json_str)
           print("PARSED LLM JSON RESPONSE:", rec_data)
          
           # Enrich recommendations with full product details
           recommendations = []
           for rec in rec_data:
               product_id = rec.get('product_id')
               print("Matching LLM product_id:", rec.get("product_id"))
               product_details = None
              
               # Find the full product details
               for product in all_products:
                   if product['id'] == product_id:
                       product_details = product
                       break
              
               if product_details:
                   print("Matched product:", product_details["id"])
                   recommendations.append({
                       "product": product_details,
                       "explanation": rec.get('explanation', ''),
                       "confidence_score": rec.get('score', 5)
                   })
               else:
                   print("Could not find product_id:", product_id)
          
           return {
               "recommendations": recommendations,
               "count": len(recommendations)
           }
          
       except Exception as e:
           print(f"Error parsing LLM response: {str(e)}")
           return {
               "recommendations": [],
               "error": f"Failed to parse recommendations: {str(e)}"
           }


   def _get_related_tags_from_llm(self, browsed_tags, all_tags):
       """
       Uses LLM to identify relevant tags based on browsing history.

       Parameters:
       - browsed_tags (list): List of tags from browsed products
       - all_tags (set): Set of all unique tags in the product catalog

       Returns:
       - list: Tags the LLM considers semantically related
       """
       prompt = (
           "Given the following tags from a user's browsing history, identify other relevant tags "
           "from the catalog that are semantically related or commonly associated. "
           "Respond with a JSON list of relevant tags only (no explanation).\n\n"
           f"Browsing Tags:\n{json.dumps(browsed_tags)}\n\n"
           f"Catalog Tags:\n{json.dumps(list(all_tags))}\n\n"
           "Output a JSON list of tags to include in product matching."
       )
       try:
           response = requests.post(
               self.gemini_url,
               headers={"Content-Type": "application/json"},
               json={
                   "contents": [{"parts": [{"text": prompt}]}]
               }
           )
           if response.status_code != 200:
               raise Exception(f"Tag relevance API error: {response.text}")

           raw_text = response.json()['candidates'][0]['content']['parts'][0]['text']
           print("RAW TAG LLM RESPONSE:", raw_text)

           start_idx = raw_text.find('[')
           end_idx = raw_text.rfind(']') + 1
           if start_idx == -1 or end_idx == 0:
               return []

           return json.loads(raw_text[start_idx:end_idx])

       except Exception as e:
           print(f"Error while getting relevant tags from LLM: {str(e)}")
           return []

   def _get_products_by_tags(self, tag_list, all_products, price_cap=float('inf'), exclude_ids=set()):
       """
       Returns products that contain any of the tags in `tag_list`.
       """
       tag_set = set(tag_list)
       matched = [
           p for p in all_products
           if p["price"] <= price_cap and
           p["id"] not in exclude_ids and
           tag_set.intersection(set(p.get("tags", [])))
       ]
       return matched

   def _filter_products_for_llm(self, user_preferences, browsed_products, all_products):
       """
       Filters products by:
       - Max price cap based on user's price range
       - Categories from user selection and browsing history
       - Brands from browsing history
       - Tags related to browsing history (via LLM)
       - Excludes already browsed products
       - Ensures at least 20 products, topped up with fallbacks
       - Returns top 50 results sorted by rating and inventory
       """
       MAX_PRODUCTS = 50
       MIN_PRODUCTS = 20

       # Determine price cap
       price_range = user_preferences.get("priceRange")
       if price_range == "under50":
           price_cap = 50
       elif price_range == "50to100":
           price_cap = 100
       elif price_range == "over100":
           price_cap = float('inf')
       else:
           price_cap = float('inf')

       # Gather categories & brands
       selected_categories = set(user_preferences.get("categories", []))
       browsed_categories = {p["category"] for p in browsed_products}
       valid_categories = selected_categories.union(browsed_categories)
       selected_brands = set(user_preferences.get("brands", []))
       browsed_brands = {p["brand"] for p in browsed_products}
       valid_brands = selected_brands.union(browsed_brands)

       # Category-based match
       category_matches = [
           p for p in all_products
           if p["price"] <= price_cap and p["category"] in valid_categories
       ]

       # Brand-based match
       brand_matches = [
           p for p in all_products
           if p["price"] <= price_cap and p["brand"] in valid_brands
       ]

       # Tag-based match 
       browsed_tags = set()
       catalog_tags = set()
       for p in browsed_products:
           browsed_tags.update(p.get("tags", []))
       for p in all_products:
           catalog_tags.update(p.get("tags", []))

       related_tags = self._get_related_tags_from_llm(list(browsed_tags), catalog_tags)
       browsed_ids = {p["id"] for p in browsed_products}
       exclude_ids = browsed_ids.union({p["id"] for p in category_matches + brand_matches})

       tag_matches = self._get_products_by_tags(
           tag_list=related_tags,
           all_products=all_products,
           price_cap=price_cap,
           exclude_ids=exclude_ids
       )

       # Merge & deduplicate
       combined = {p["id"]: p for p in category_matches + brand_matches + tag_matches}
       merged_products = [p for pid, p in combined.items() if pid not in browsed_ids]

       # If still < MIN_PRODUCTS backfill from browsed categories
       if len(merged_products) < MIN_PRODUCTS:
           missing = MIN_PRODUCTS - len(merged_products)
           fallback_candidates = [
               p for p in all_products
               if p["price"] <= price_cap
               and p["category"] in browsed_categories
               and p["id"] not in combined
               and p["id"] not in browsed_ids
           ]
           fallback_sorted = sorted(fallback_candidates, key=lambda x: (x["rating"], x["inventory"]), reverse=True)
           merged_products.extend(fallback_sorted[:missing])

       # Final fallback — top-rated from catalog
       if len(merged_products) < MIN_PRODUCTS:
           missing = MIN_PRODUCTS - len(merged_products)
           used_ids = {p["id"] for p in merged_products}.union(browsed_ids)
           top_fallbacks = [
               p for p in all_products
               if p["price"] <= price_cap and p["id"] not in used_ids
           ]
           top_sorted = sorted(top_fallbacks, key=lambda x: (x["rating"], x["inventory"]), reverse=True)
           merged_products.extend(top_sorted[:missing])

       # Final sort and cap
       final_sorted = sorted(merged_products, key=lambda x: (x["rating"], x["inventory"]), reverse=True)
       top_filtered = final_sorted[:MAX_PRODUCTS]

       # Logging
       print("\n=== Filtered Products Sent to LLM (Category + Brand + LLM Tags) ===")
       for p in top_filtered:
           print(f"- {p['id']}: {p['name']} | ${p['price']} | {p['category']} | {p['brand']} | Rating: {p['rating']}")
       print("=====================================================================\n")
       return top_filtered

   def _log_token_counts(self, prompt, response_text):
       """
       Logs the estimated number of input and output tokens for each LLM call.
       Gemini ≈ 1 token per 4 characters.
       """
       try:
           input_token_count = int(len(prompt) / 4)
           output_token_count = int(len(response_text) / 4)
           log_entry = (
               f"{datetime.now()} - Token Usage Log\n"
               f"Input Tokens : {input_token_count}\n"
               f"Output Tokens: {output_token_count}\n"
               f"{'-' * 60}\n"
           )

           log_file = "logs/output_token_log.txt"
           os.makedirs(os.path.dirname(log_file), exist_ok=True)

           with open(log_file, "a") as f:
               f.write(log_entry)

       except Exception as e:
           print(f"Failed to log token counts: {str(e)}")
