"""
Recipe Scraper Service
Ethical web scraping for recipes with robots.txt compliance and rate limiting
"""

import time
import urllib.robotparser
from typing import Dict, List, Optional, Tuple
from urllib.parse import urlparse
import requests
from bs4 import BeautifulSoup
import logging

from src.core.config import settings
from src.schemas.recipe import RecipeCreate, IngredientInput

logger = logging.getLogger(__name__)


class RateLimiter:
    """Rate limiter for scraping requests"""

    def __init__(self):
        self.last_request_times: Dict[str, float] = {}

    def wait_if_needed(self, domain: str) -> None:
        """
        Wait if necessary to respect rate limits.

        Args:
            domain: Domain to check rate limit for
        """
        if domain in self.last_request_times:
            elapsed = time.time() - self.last_request_times[domain]
            if elapsed < settings.SCRAPER_RATE_LIMIT:
                wait_time = settings.SCRAPER_RATE_LIMIT - elapsed
                logger.info(f"Rate limiting: waiting {wait_time:.2f}s for {domain}")
                time.sleep(wait_time)

        self.last_request_times[domain] = time.time()


class RecipeScraper:
    """
    Recipe scraper with ethical compliance.

    Features:
    - robots.txt compliance
    - Rate limiting (1 req per 5 sec per domain)
    - Descriptive User-Agent
    - Graceful error handling
    """

    def __init__(self):
        self.rate_limiter = RateLimiter()
        self.robot_parsers: Dict[str, urllib.robotparser.RobotFileParser] = {}

    def _get_domain(self, url: str) -> str:
        """Extract domain from URL"""
        parsed = urlparse(url)
        return f"{parsed.scheme}://{parsed.netloc}"

    def _check_robots_txt(self, url: str) -> Tuple[bool, Optional[str]]:
        """
        Check if scraping is allowed by robots.txt.

        Args:
            url: URL to check

        Returns:
            Tuple of (allowed: bool, reason: Optional[str])
        """
        try:
            domain = self._get_domain(url)
            robots_url = f"{domain}/robots.txt"

            # Cache robot parser per domain
            if domain not in self.robot_parsers:
                rp = urllib.robotparser.RobotFileParser()
                rp.set_url(robots_url)
                try:
                    rp.read()
                    self.robot_parsers[domain] = rp
                except Exception as e:
                    logger.warning(f"Could not read robots.txt for {domain}: {e}")
                    # If robots.txt is not accessible, allow scraping (permissive)
                    return True, None

            rp = self.robot_parsers[domain]
            allowed = rp.can_fetch(settings.SCRAPER_USER_AGENT, url)

            if not allowed:
                return False, f"Scraping not allowed by {robots_url}"

            return True, None

        except Exception as e:
            logger.error(f"Error checking robots.txt: {e}")
            # On error, be conservative and disallow
            return False, f"Error checking robots.txt: {str(e)}"

    def _fetch_page(self, url: str) -> Tuple[Optional[str], Optional[str]]:
        """
        Fetch page content with rate limiting.

        Args:
            url: URL to fetch

        Returns:
            Tuple of (content: Optional[str], error: Optional[str])
        """
        try:
            domain = self._get_domain(url)
            self.rate_limiter.wait_if_needed(domain)

            headers = {
                'User-Agent': settings.SCRAPER_USER_AGENT,
                'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
                'Accept-Language': 'en-US,en;q=0.5',
                'Accept-Encoding': 'gzip, deflate',
                'Connection': 'keep-alive',
            }

            response = requests.get(
                url,
                headers=headers,
                timeout=settings.SCRAPER_TIMEOUT,
                allow_redirects=True
            )

            if response.status_code == 200:
                return response.text, None
            else:
                return None, f"HTTP {response.status_code}: {response.reason}"

        except requests.exceptions.Timeout:
            return None, "Request timed out"
        except requests.exceptions.RequestException as e:
            return None, f"Request error: {str(e)}"
        except Exception as e:
            logger.error(f"Error fetching page: {e}")
            return None, f"Unexpected error: {str(e)}"

    def _parse_recipe_json_ld(self, soup: BeautifulSoup) -> Optional[Dict]:
        """
        Parse recipe from JSON-LD structured data (Schema.org Recipe).

        Args:
            soup: BeautifulSoup object

        Returns:
            Optional[Dict]: Parsed recipe data or None
        """
        try:
            import json

            # Find JSON-LD script tags
            scripts = soup.find_all('script', type='application/ld+json')
            for script in scripts:
                try:
                    data = json.loads(script.string)

                    # Handle single recipe or array
                    if isinstance(data, list):
                        data = next((item for item in data if item.get('@type') == 'Recipe'), None)
                    elif data.get('@type') != 'Recipe':
                        continue

                    if not data:
                        continue

                    # Extract recipe data
                    recipe_data = {
                        'title': data.get('name', ''),
                        'description': data.get('description', ''),
                        'prep_time_minutes': self._parse_duration(data.get('prepTime')),
                        'cook_time_minutes': self._parse_duration(data.get('cookTime')),
                        'servings': self._parse_servings(data.get('recipeYield')),
                        'ingredients': self._parse_ingredients(data.get('recipeIngredient', [])),
                        'instructions': self._parse_instructions(data.get('recipeInstructions', [])),
                    }

                    if recipe_data['title'] and recipe_data['ingredients'] and recipe_data['instructions']:
                        return recipe_data

                except json.JSONDecodeError:
                    continue

        except Exception as e:
            logger.error(f"Error parsing JSON-LD: {e}")

        return None

    def _parse_duration(self, duration: Optional[str]) -> Optional[int]:
        """Parse ISO 8601 duration to minutes"""
        if not duration:
            return None

        try:
            import re
            # Simple parser for PT30M or PT1H30M format
            match = re.match(r'PT(?:(\d+)H)?(?:(\d+)M)?', duration)
            if match:
                hours = int(match.group(1) or 0)
                minutes = int(match.group(2) or 0)
                return hours * 60 + minutes
        except Exception:
            pass

        return None

    def _parse_servings(self, servings) -> Optional[int]:
        """Parse servings (can be int, string, or array)"""
        if isinstance(servings, int):
            return servings
        elif isinstance(servings, str):
            import re
            match = re.search(r'\d+', servings)
            if match:
                return int(match.group())
        elif isinstance(servings, list) and servings:
            return self._parse_servings(servings[0])
        return None

    def _parse_ingredients(self, ingredients: List) -> List[IngredientInput]:
        """Parse ingredients list"""
        result = []
        for idx, ing in enumerate(ingredients):
            if isinstance(ing, str):
                result.append(IngredientInput(
                    name=ing.strip(),
                    quantity=None,
                    unit=None
                ))
        return result

    def _parse_instructions(self, instructions) -> str:
        """Parse instructions (can be string, list, or structured)"""
        if isinstance(instructions, str):
            return instructions.strip()
        elif isinstance(instructions, list):
            steps = []
            for idx, inst in enumerate(instructions, 1):
                if isinstance(inst, str):
                    steps.append(f"{idx}. {inst.strip()}")
                elif isinstance(inst, dict):
                    text = inst.get('text', inst.get('itemListElement', ''))
                    if text:
                        steps.append(f"{idx}. {text.strip()}")
            return '\n'.join(steps)
        return ""

    def scrape_recipe(self, url: str) -> Tuple[Optional[RecipeCreate], List[str], Optional[str]]:
        """
        Scrape recipe from URL.

        Args:
            url: Recipe URL to scrape

        Returns:
            Tuple of (recipe_data: Optional[RecipeCreate], warnings: List[str], error: Optional[str])
        """
        warnings = []

        # Check robots.txt
        allowed, reason = self._check_robots_txt(url)
        if not allowed:
            return None, warnings, reason or "Scraping not allowed by robots.txt"

        # Fetch page
        content, error = self._fetch_page(url)
        if error:
            return None, warnings, error

        if not content:
            return None, warnings, "No content received"

        # Parse HTML
        soup = BeautifulSoup(content, 'html.parser')

        # Try JSON-LD first (most reliable)
        recipe_data = self._parse_recipe_json_ld(soup)

        if not recipe_data:
            warnings.append("Could not find structured recipe data (JSON-LD)")
            return None, warnings, "Recipe data not found. The site may not support structured data."

        # Validate required fields
        if not recipe_data.get('title'):
            warnings.append("Recipe title not found")
        if not recipe_data.get('ingredients'):
            warnings.append("No ingredients found")
        if not recipe_data.get('instructions'):
            warnings.append("No instructions found")

        # Create RecipeCreate schema
        try:
            recipe = RecipeCreate(
                title=recipe_data['title'],
                description=recipe_data.get('description', ''),
                prep_time_minutes=recipe_data.get('prep_time_minutes'),
                cook_time_minutes=recipe_data.get('cook_time_minutes'),
                servings=recipe_data.get('servings'),
                difficulty=None,  # Not usually in scraped data
                ingredients=recipe_data['ingredients'],
                instructions=recipe_data['instructions'],
                tags=[],
                source_url=url
            )

            return recipe, warnings, None

        except Exception as e:
            logger.error(f"Error creating recipe schema: {e}")
            return None, warnings, f"Error parsing recipe data: {str(e)}"


# Global scraper instance
recipe_scraper = RecipeScraper()
