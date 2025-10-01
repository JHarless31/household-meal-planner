# User Guide

## Table of Contents

1. [Introduction](#introduction)
2. [Getting Started](#getting-started)
3. [User Account Management](#user-account-management)
4. [Recipe Management](#recipe-management)
5. [Recipe Suggestions](#recipe-suggestions)
6. [Inventory Management](#inventory-management)
7. [Menu Planning](#menu-planning)
8. [Shopping Lists](#shopping-lists)
9. [Notifications](#notifications)
10. [Admin Features](#admin-features)
11. [Tips and Best Practices](#tips-and-best-practices)
12. [Troubleshooting](#troubleshooting)

---

## Introduction

### Welcome

Welcome to the Household Meal Planning System! This guide will help you make the most of your meal planning application.

### What is the Household Meal Planning System?

The Household Meal Planning System is a comprehensive web application designed to help families organize meals, manage kitchen inventory, track recipes, and streamline grocery shopping. Built for local deployment, it provides a secure, private solution for household meal management.

### Key Features and Benefits

- **Recipe Management**: Store unlimited recipes with version history
- **Web Scraping**: Import recipes automatically from popular recipe websites
- **Intelligent Suggestions**: Get recipe recommendations based on rotation, favorites, and available ingredients
- **Inventory Tracking**: Monitor kitchen stock with low stock alerts and expiration warnings
- **Menu Planning**: Plan weekly menus with drag-and-drop simplicity
- **Shopping Lists**: Auto-generate shopping lists from your menu plans
- **Recipe Ratings**: Rate recipes and track household favorites
- **Notifications**: Stay informed with alerts for low stock, expiring items, and meal reminders
- **Multi-User Support**: Separate accounts for family members with role-based access

### Who Should Use This Guide

This guide is for all users of the application, including:
- **Home cooks** planning family meals
- **Household managers** tracking inventory and shopping
- **Family members** viewing menus and rating recipes
- **Administrators** managing users and system settings

For technical documentation, see the [Developer Guide](DEVELOPER_GUIDE.md).
For system administration, see the [Administrator Guide](ADMIN_GUIDE.md).

---

## Getting Started

### How to Access the Application

The application runs on your local network. To access it:

1. **Open your web browser** (Chrome, Firefox, Safari, or Edge)
2. **Enter the URL** provided by your administrator:
   - Typically: `http://[server-ip]:3000` or `https://meal-planner.local`
3. **Bookmark the page** for easy access

**System Requirements:**
- Modern web browser (latest version recommended)
- Internet connection for recipe scraping (optional)
- JavaScript enabled

### First-Time Login and Registration

#### Creating Your First Account

If no accounts exist yet:

1. Click **"Register"** on the login page
2. Fill in the registration form:
   - **Username**: 3-50 characters, letters/numbers/underscores
   - **Email**: Valid email address
   - **Password**: Minimum 8 characters, mix of letters and numbers
   - **Confirm Password**: Must match
3. Click **"Create Account"**
4. You'll be logged in automatically

**Note:** The first user created is automatically assigned the **admin** role.

#### Logging In

1. Go to the application URL
2. Enter your **username** and **password**
3. Click **"Log In"**
4. You'll be redirected to the dashboard

### Understanding the Dashboard

The dashboard is your command center. It shows:

**Top Section:**
- **Active Menu Plan**: Current week's meal plan summary
- **Quick Actions**: Buttons to create recipes, add inventory, plan menus

**Notifications Panel:**
- **Recent Alerts**: Low stock, expiring items, meal reminders
- **Unread Count**: Badge showing number of unread notifications

**Statistics (if available):**
- **Recipe Count**: Total recipes in your collection
- **Inventory Items**: Number of items in stock
- **This Week's Meals**: Number of planned meals

**Quick Links:**
- **Browse Recipes**: View all recipes
- **Manage Inventory**: Check stock levels
- **Plan Menu**: Create or edit menu plans
- **Shopping List**: Generate shopping list

### Navigation Overview

The application has a persistent navigation menu at the top:

| Menu Item | Description |
|-----------|-------------|
| **Dashboard** | Home page with overview |
| **Recipes** | Browse, search, and manage recipes |
| **Inventory** | View and manage kitchen stock |
| **Menu Plans** | Create and manage weekly meal plans |
| **Shopping List** | Generate lists from menu plans |
| **Notifications** | Bell icon with unread count |
| **Profile** | Account settings and logout |
| **Admin** | User management and settings (admin only) |

---

## User Account Management

### Creating an Account

See [First-Time Login and Registration](#first-time-login-and-registration) above.

### Logging In and Out

**To Log In:**
1. Navigate to the application URL
2. Enter username and password
3. Click "Log In"

**To Log Out:**
1. Click your username in the top-right corner
2. Select "Logout" from the dropdown
3. You'll be redirected to the login page

**Session Duration:** Sessions last 24 hours by default. You'll be automatically logged out after this time for security.

### Profile Settings

To update your profile:

1. Click your **username** in the top-right
2. Select **"Profile"**
3. Update fields as needed:
   - Email address
   - Display preferences (if available)
4. Click **"Save Changes"**

### Password Management

**To Change Your Password:**

1. Go to **Profile** settings
2. Click **"Change Password"**
3. Enter:
   - Current password
   - New password (min 8 characters)
   - Confirm new password
4. Click **"Update Password"**

**Password Requirements:**
- Minimum 8 characters
- Mix of uppercase and lowercase letters recommended
- Include numbers or special characters for security

**If You Forget Your Password:**
- Contact your system administrator to reset your password
- They can create a temporary password for you

### Account Roles

The system has three user roles:

| Role | Permissions | Typical Use |
|------|-------------|-------------|
| **Admin** | Full access to all features, user management, system settings | Household manager |
| **User** | Create/edit recipes, manage inventory, plan menus, rate recipes | Family members |
| **Child** | View recipes and menus, limited editing (future feature) | Children |

Your role is displayed in your profile. Contact an admin to request role changes.

---

## Recipe Management

### Browsing Recipes

To view all recipes:

1. Click **"Recipes"** in the navigation menu
2. You'll see a grid of recipe cards showing:
   - Recipe title
   - Description
   - Preparation and cook time
   - Difficulty level
   - Tags
   - Average rating (thumbs up/down count)

**Recipe Card Actions:**
- Click the recipe card to view full details
- Click the star icon to favorite
- Click the thumbs up/down to rate

### Searching and Filtering Recipes

#### Search by Title or Ingredients

1. Use the **search bar** at the top of the Recipes page
2. Type keywords (recipe title or ingredient names)
3. Results update automatically as you type
4. Search is case-insensitive

**Example Searches:**
- "chicken" - finds all recipes with chicken in title or ingredients
- "pasta alfredo" - finds pasta recipes
- "basil tomato" - finds recipes with both ingredients

#### Filter by Tags

1. Click the **"Tags"** dropdown
2. Select one or more tags:
   - Cuisine types: Italian, Mexican, Asian, etc.
   - Meal types: Breakfast, Lunch, Dinner, Dessert
   - Dietary: Vegetarian, Vegan, Gluten-Free, Dairy-Free
   - Seasons: Spring, Summer, Fall, Winter
   - Occasions: Holiday, Quick Meal, Comfort Food
3. Recipes matching ANY selected tag are shown

#### Filter by Difficulty Level

1. Use the **"Difficulty"** dropdown
2. Select: Easy, Medium, or Hard
3. Only recipes at that difficulty level are shown

#### Filter by Preparation Time

1. Use the **"Max Prep Time"** slider (if available)
2. Set maximum total time (prep + cook)
3. Only recipes under that time are shown

#### Favorites Filter

1. Click the **"Favorites Only"** checkbox
2. Shows only recipes marked as household favorites
3. A recipe becomes a favorite based on:
   - Average rating threshold (configured by admin)
   - Minimum number of raters (configured by admin)
   - Default: 75% positive ratings with at least 2 raters

#### Available Inventory Filter

1. Click **"Available Ingredients"** checkbox
2. Shows recipes where you have most/all ingredients in stock
3. Great for deciding what to cook right now

**Combining Filters:**
You can combine multiple filters. For example:
- Search "chicken" + Tag "Italian" + Difficulty "Easy"
- Shows easy Italian chicken recipes

### Viewing Recipe Details

To see full recipe information:

1. Click on any recipe card
2. The recipe detail page shows:

**Header Section:**
- Recipe title
- Description
- Current version number
- Created by and date
- Last updated date

**Metadata:**
- **Prep Time**: Time to prepare ingredients
- **Cook Time**: Time to cook
- **Total Time**: Prep + Cook time
- **Servings**: Number of servings
- **Difficulty**: Easy, Medium, or Hard
- **Source URL**: Link to original recipe (if scraped)

**Ingredients List:**
- Quantity (e.g., "2 cups")
- Unit (cups, tablespoons, pounds, etc.)
- Item name
- Notes (optional, e.g., "diced", "fresh")

**Instructions:**
- Step-by-step numbered instructions
- Clear, detailed directions

**Tags:**
- All tags associated with the recipe
- Click a tag to see other recipes with that tag

**Rating Section:**
- Your rating (if you've rated it)
- Overall rating: X thumbs up, Y thumbs down
- Favorite badge if it's a household favorite

**Actions:**
- **Rate Recipe**: Thumbs up or down
- **Edit Recipe**: Update recipe (creates new version)
- **Delete Recipe**: Remove recipe (soft delete)
- **Add to Menu**: Add to a menu plan
- **View Version History**: See all versions

### Creating New Recipes

There are two ways to add recipes:

#### Method 1: Manual Entry

1. Click **"Recipes"** → **"New Recipe"**
2. Fill in the recipe form:

**Basic Information:**
- **Title**: Recipe name (required, max 200 characters)
- **Description**: Brief description (optional, max 500 characters)
- **Servings**: Number of servings (required, default 4)
- **Prep Time**: Minutes to prep (required)
- **Cook Time**: Minutes to cook (required)
- **Difficulty**: Easy, Medium, or Hard (required)

**Ingredients:**
- Click **"Add Ingredient"**
- For each ingredient:
  - **Quantity**: Amount (e.g., 2, 1.5)
  - **Unit**: Select from dropdown (cup, tablespoon, pound, etc.)
  - **Name**: Ingredient name (e.g., "flour", "chicken breast")
  - **Notes**: Optional details (e.g., "diced", "room temperature")
- Click **"Remove"** to delete an ingredient
- Add as many ingredients as needed

**Instructions:**
- Click **"Add Step"**
- Enter detailed instructions for each step
- Steps are automatically numbered
- Reorder steps by dragging (if available)
- Click **"Remove"** to delete a step

**Tags:**
- Click **"Add Tag"**
- Type tag name or select from suggestions
- Tags help with filtering and searching
- Suggested tags: meal type, cuisine, dietary restrictions, season

**Image (Optional):**
- Upload a photo of the dish
- Supported formats: JPG, PNG
- Maximum size: 5MB

**Source URL (Optional):**
- If adapted from another recipe, include the URL

3. Click **"Create Recipe"**
4. Recipe is saved and you're redirected to its detail page

**Tips:**
- Be specific in measurements
- Break instructions into clear steps
- Use descriptive tags
- Include all ingredients, even salt and pepper

#### Method 2: Web Scraping

Import recipes automatically from supported recipe websites:

1. Click **"Recipes"** → **"Import from Web"**
2. Enter the **recipe URL** (e.g., allrecipes.com, foodnetwork.com)
3. Click **"Scrape Recipe"**
4. The system attempts to extract:
   - Title and description
   - Ingredients with quantities
   - Instructions
   - Prep/cook time
   - Servings
5. Review the imported data
6. Make any necessary edits
7. Click **"Save Recipe"**

**Supported Websites:**
The scraper works with most popular recipe sites that follow standard recipe schema markup, including:
- AllRecipes
- Food Network
- Bon Appetit
- Serious Eats
- Tasty
- Many others

**Scraping Notes:**
- Check `robots.txt` compliance warning if shown
- Not all sites are supported
- You may need to manually adjust scraped data
- Images are not imported (add manually if desired)
- Rate limit: 1 scrape per 5 seconds per domain

**If Scraping Fails:**
- Verify the URL is correct
- Check if the site is supported
- Try manual entry instead
- Contact admin if consistent failures occur

### Editing Recipes

The system uses **version control** for recipes, meaning every edit creates a new version while preserving the old one.

**To Edit a Recipe:**

1. Open the recipe detail page
2. Click **"Edit Recipe"**
3. Make your changes in the form:
   - Update title, description, or metadata
   - Add, remove, or modify ingredients
   - Edit or reorder instructions
   - Add or remove tags
4. Click **"Save Changes"**
5. A new version is created automatically

**What Happens:**
- Old version is preserved
- Current_version increments (e.g., v1 → v2)
- Recipe page shows new version by default
- All menu plans using this recipe reference the latest version
- Version history is maintained

**When to Edit vs. Create New:**
- **Edit** when improving/correcting an existing recipe
- **Create New** when making a significantly different recipe

### Understanding Recipe Versioning

Version control helps you:
- Track changes over time
- Revert to previous versions if needed
- See who made changes and when
- Compare different versions

#### Viewing Version History

1. Open recipe detail page
2. Click **"Version History"**
3. You'll see a list of all versions:
   - Version number (v1, v2, v3...)
   - Date created
   - Created by user
   - Change summary (if available)

#### Viewing a Specific Version

1. In version history, click on any version
2. The recipe page shows that version's content
3. A banner indicates you're viewing an old version
4. Click **"Back to Latest"** to return

#### Comparing Versions

1. Go to version history
2. Select two versions to compare
3. Side-by-side comparison shows:
   - Changed ingredients (highlighted)
   - Modified instructions (highlighted)
   - Updated metadata (shown in diff view)

#### Reverting to a Previous Version

If you made a mistake or want to go back:

1. View the version you want to restore
2. Click **"Revert to This Version"**
3. Confirm the action
4. A new version is created with the old content
5. Version history is preserved (no data is lost)

**Example:**
- v1: Original recipe
- v2: Added more garlic (mistake)
- v3: Revert to v1 (restores original, but creates v3)

### Deleting Recipes

The system uses **soft delete**, meaning recipes are marked as deleted but not permanently removed.

**To Delete a Recipe:**

1. Open recipe detail page
2. Click **"Delete Recipe"**
3. Confirm the deletion
4. Recipe is marked as deleted

**What Happens:**
- Recipe disappears from recipe lists
- Recipe detail page shows "deleted" status
- Old menu plans still reference it (for history)
- Data remains in database (for recovery)

**To Undelete a Recipe (Admin Only):**
- Admins can restore deleted recipes via database
- Contact your administrator if you deleted a recipe by mistake

**Permanent Deletion:**
- Not available through UI
- Requires database access
- Consult with administrator

### Rating Recipes

Rate recipes to help identify household favorites:

**To Rate a Recipe:**

1. Open recipe detail page
2. Find the rating section
3. Click **thumbs up** (liked it) or **thumbs down** (didn't like it)
4. Your rating is saved immediately

**Changing Your Rating:**

1. Open the recipe again
2. Click a different rating (or the same to remove it)
3. You can only have one rating per recipe

**To Remove Your Rating:**

1. Open recipe detail page
2. Click the rating you already selected (toggles off)

### Understanding Favorites

Recipes can be marked as **household favorites** based on ratings.

**How Favorites are Calculated:**

A recipe becomes a favorite when:
1. **Minimum Raters**: At least X users have rated it (default: 2)
2. **Rating Threshold**: At least Y% of ratings are positive (default: 75%)

**Example:**
- 4 users rate a recipe
- 3 thumbs up, 1 thumbs down
- 75% positive (3/4 = 75%)
- Recipe becomes a favorite

**Favorite Badge:**
- Displayed on recipe cards
- Shown on recipe detail page
- Used in suggestion algorithms

**Admin Configuration:**
- Admins can adjust the threshold percentage
- Admins can change minimum rater requirement
- See [Admin Features](#admin-features)

---

## Recipe Suggestions

Recipe suggestions help you decide what to cook using intelligent algorithms.

### How Suggestions Work

The system analyzes your recipes, inventory, and cooking history to provide personalized recommendations. There are 6 different strategies, each designed for a specific need.

### The 6 Suggestion Strategies

#### 1. Rotation Strategy

**What it does:** Suggests recipes you haven't cooked recently or never tried.

**Best for:** Ensuring variety and preventing meal repetition

**How it works:**
- Prioritizes recipes never cooked (times_cooked = 0)
- Then recipes not cooked in longest time (oldest last_cooked_date)
- Then recipes cooked least frequently (lowest times_cooked)

**Example suggestions:**
- "Lemon Herb Chicken - Never tried before"
- "Beef Stew - Not cooked in 45 days"
- "Vegetable Stir Fry - Only cooked 2 times"

**Use this when:** Planning weekly menus to avoid repeating the same meals.

#### 2. Favorites Strategy

**What it does:** Suggests household favorite recipes based on ratings.

**Best for:** Quick wins, crowd-pleasers, family favorites

**How it works:**
- Ranks recipes by average rating
- Requires minimum number of raters
- Filters to only favorites (>= threshold %)
- Orders by most popular first

**Example suggestions:**
- "Mom's Spaghetti - 5 thumbs up, 0 thumbs down"
- "Taco Tuesday - 4 thumbs up, 1 thumbs down"

**Use this when:** You want to cook something you know everyone will love.

#### 3. Never Tried Strategy

**What it does:** Suggests recipes you've never cooked before.

**Best for:** Trying new recipes, expanding your repertoire

**How it works:**
- Filters recipes with times_cooked = 0
- Orders by recently added (newest first)
- Shows brand new recipes

**Example suggestions:**
- "Thai Coconut Curry - Added 2 days ago"
- "Baked Salmon - Added last week"

**Use this when:** You're in the mood to experiment with something new.

#### 4. Available Inventory Strategy

**What it does:** Suggests recipes you can make with current inventory.

**Best for:** Using up ingredients, reducing food waste, avoiding shopping

**How it works:**
- Compares recipe ingredients to current inventory
- Calculates match percentage
- Ranks by highest availability
- Shows what you have vs. what you need

**Example suggestions:**
- "Chicken Alfredo - 90% available (9/10 ingredients)"
- "Vegetable Soup - 75% available (6/8 ingredients)"

**Use this when:**
- You want to cook without shopping
- You need to use up ingredients before they expire
- You're trying to minimize grocery trips

#### 5. Seasonal Strategy

**What it does:** Suggests recipes tagged for the current season.

**Best for:** Seasonal eating, using fresh seasonal produce

**How it works:**
- Detects current season (Spring, Summer, Fall, Winter)
- Filters recipes tagged with that season
- Orders by rating or rotation

**Example suggestions:**
- "Pumpkin Soup - Fall seasonal favorite"
- "Grilled Vegetables - Summer recipe"

**Use this when:**
- You have seasonal produce
- You want comfort food appropriate for the weather
- You're planning seasonal menus

**Seasons:**
- Spring: March, April, May
- Summer: June, July, August
- Fall: September, October, November
- Winter: December, January, February

#### 6. Quick Meals Strategy

**What it does:** Suggests fast recipes (under 30 minutes total time).

**Best for:** Busy weeknights, quick lunches, time-constrained cooking

**How it works:**
- Filters recipes where (prep_time_minutes + cook_time_minutes) <= 30
- Orders by total time (fastest first)
- Shows prep and cook time

**Example suggestions:**
- "15-Minute Pasta - 5 min prep, 10 min cook"
- "Quick Stir Fry - 10 min prep, 12 min cook"

**Use this when:**
- You have limited time to cook
- You need a quick weeknight dinner
- You're planning lunch meals

### Using Suggestions for Menu Planning

**To Get Suggestions:**

1. Go to **Recipes** → **"Get Suggestions"**
2. Select a **strategy** from the dropdown
3. Adjust the **number of suggestions** (default: 10)
4. Click **"Get Suggestions"**
5. View the suggestions with reasoning

**Suggestion Display:**

Each suggestion shows:
- Recipe title
- Description
- Prep and cook time
- Difficulty level
- **Reason for suggestion** (e.g., "Not cooked in 30 days")
- **Match percentage** (for inventory strategy)
- **Quick actions**: View recipe, Add to menu

**Adding Suggestions to Menu:**

1. Click **"Add to Menu"** on a suggestion
2. Select the menu plan
3. Choose the day and meal type
4. Click **"Add"**
5. Suggestion is added to your menu

**Refreshing Suggestions:**

- Suggestions are regenerated each time you click "Get Suggestions"
- Different strategies provide different results
- Try multiple strategies to find the best fit

**Best Practices:**

- Use **Rotation** for weekly planning to ensure variety
- Use **Favorites** when you need crowd-pleasers
- Use **Available Inventory** on shopping day to use up ingredients
- Use **Quick Meals** for weeknight planning
- Use **Seasonal** to take advantage of seasonal produce
- Combine suggestions from multiple strategies for a balanced week

---

## Inventory Management

Track what's in your kitchen to reduce waste, avoid over-purchasing, and plan better.

### Viewing Your Inventory

To see all inventory items:

1. Click **"Inventory"** in the navigation
2. View your items in a table or grid
3. Each item shows:
   - Item name
   - Quantity and unit
   - Category (produce, dairy, meat, pantry, etc.)
   - Location (fridge, freezer, pantry, etc.)
   - Expiration date (if applicable)
   - Last updated date

**Inventory Statistics:**
- Total items in stock
- Low stock items count
- Expiring soon count

### Adding New Items

**To Add an Item:**

1. Click **"Inventory"** → **"Add Item"**
2. Fill in the form:

**Required Fields:**
- **Item Name**: Name of the ingredient (e.g., "Milk", "Chicken Breast")
- **Quantity**: Amount in stock (numeric, e.g., 2.5)
- **Unit**: Select from dropdown:
  - Weight: pound, ounce, gram, kilogram
  - Volume: cup, tablespoon, teaspoon, liter, milliliter, gallon, quart, pint
  - Count: piece, whole, can, package, bag

**Optional Fields:**
- **Category**: Classify for organization
  - Produce, Dairy, Meat, Seafood, Grains, Pantry, Condiments, Spices, Frozen, Other
- **Location**: Where it's stored
  - Fridge, Freezer, Pantry, Counter, Cabinet, Other
- **Expiration Date**: When it expires (date picker)
- **Minimum Quantity Threshold**: Low stock alert threshold
- **Notes**: Additional information

3. Click **"Add Item"**
4. Item is added to inventory

**Tips:**
- Be consistent with naming (e.g., always "Tomato" not "Tomatoes")
- Set expiration dates for perishables
- Set minimum thresholds for items you always want in stock
- Use categories and locations to organize

### Editing Inventory Items

**To Update an Item:**

1. Find the item in the inventory list
2. Click **"Edit"** or click on the item row
3. Update fields:
   - Change quantity (increase or decrease)
   - Update expiration date
   - Modify location or category
4. Click **"Save Changes"**

**What Happens:**
- Item is updated immediately
- Change is recorded in item history
- If quantity goes below minimum threshold, low stock notification is generated

**Quantity Changes:**
- You can increase quantity (e.g., after shopping)
- You can decrease quantity (e.g., after using some)
- Quantity cannot go below 0

### Deleting Items

**To Remove an Item:**

1. Find the item in the inventory list
2. Click **"Delete"**
3. Confirm the deletion
4. Item is removed from inventory

**When to Delete:**
- Item is completely used up (though 0 quantity is also fine)
- Item is no longer kept in stock
- Item was added by mistake

**Note:** Deletion is permanent. Consider setting quantity to 0 instead if you might restock it later.

### Understanding Low Stock Alerts

The system can alert you when items run low:

**How It Works:**
- Each item can have a **minimum quantity threshold**
- When quantity drops below this threshold, a notification is generated
- Notification appears in your notifications panel
- Low stock items are highlighted in the inventory list

**Setting Thresholds:**
1. Edit the inventory item
2. Set **"Minimum Quantity"** field
3. Save the item

**Example:**
- Milk: Minimum 1 gallon
- Current: 0.5 gallon
- Alert: "Milk is running low (0.5 gallon remaining, minimum 1 gallon)"

**Viewing Low Stock Items:**
1. Go to **Inventory**
2. Click **"Low Stock"** filter
3. See only items below their threshold

**Disabling Alerts:**
- Leave minimum quantity blank or 0
- No alerts will be generated for that item

### Viewing Expiring Items

Track items nearing expiration to reduce food waste:

**How It Works:**
- System checks expiration dates daily
- Items expiring within X days trigger a notification
- Default: 7 days warning (configurable by admin)

**Viewing Expiring Items:**
1. Go to **Inventory**
2. Click **"Expiring Soon"** filter
3. See items expiring within the warning period
4. Items are sorted by expiration date (soonest first)

**Expiration Display:**
- Red: Expires in 1-3 days
- Yellow: Expires in 4-7 days
- Green: Expires in 8+ days

**Tips:**
- Check expiring items regularly
- Plan meals around ingredients that need to be used
- Use the "Available Inventory" recipe suggestion strategy
- Update or remove items after they expire

### Checking Inventory History

Track how your inventory changes over time:

**To View History:**
1. Find the item in inventory
2. Click **"View History"** or click on the item
3. See a log of all changes:
   - Date and time of change
   - Previous quantity
   - New quantity
   - Change amount (+/-)
   - User who made the change
   - Reason for change (if recorded)

**History Events:**
- Manual updates (user edit)
- Auto-deduction (meal cooked)
- Initial creation
- Restocking

**Uses for History:**
- Verify auto-deductions
- Track consumption patterns
- Identify discrepancies
- Audit inventory changes

### Auto-Deduction When Cooking

When you mark a meal as cooked, inventory is automatically reduced:

**How It Works:**
1. You mark a planned meal as "Cooked"
2. System retrieves recipe ingredients
3. For each ingredient:
   - System searches inventory for matching item (case-insensitive)
   - If found, quantity is reduced by recipe amount
   - If not found, no action (you're assumed to have purchased it or it's a pantry staple)
4. Inventory history records the deduction with link to recipe

**Example:**
- Recipe calls for 2 cups of milk
- Inventory has 4 cups of milk
- After marking meal cooked: 2 cups remaining
- History shows: "-2 cups (used in Recipe: Pancakes)"

**Notes:**
- Only exact or close name matches are deducted
- System won't reduce below 0 (stops at 0)
- You can manually adjust if auto-deduction is incorrect
- Pantry staples (salt, pepper) may not be in inventory but recipes can still include them

**Disabling Auto-Deduction:**
- Not currently configurable (always enabled)
- You can manually adjust inventory after if needed

---

## Menu Planning

Plan your weekly meals in advance for organized, stress-free cooking.

### Understanding Menu Plans

A **menu plan** is a weekly schedule of meals:

**Structure:**
- **Week Start Date**: The Monday of the week
- **Plan Name**: Optional name (e.g., "Week of Oct 15", "Thanksgiving Week")
- **Active Status**: Only one plan can be active at a time
- **Meals**: Collection of planned meals

**Meal Structure:**
- **Day**: Monday through Sunday
- **Meal Type**: Breakfast, Lunch, Dinner, Snack
- **Recipe**: Linked to a recipe
- **Servings**: Number of servings to make
- **Cooked Status**: Whether the meal has been prepared
- **Notes**: Optional notes

### Creating a New Menu Plan

**To Create a Plan:**

1. Click **"Menu Plans"** → **"New Menu Plan"**
2. Fill in the form:
   - **Week Start Date**: Select the Monday of the week
   - **Plan Name**: Optional descriptive name
   - **Make Active**: Check to make this the active plan
3. Click **"Create Plan"**
4. Empty plan is created
5. Now add meals to the plan

**Tips:**
- Create plans a week or two in advance
- Use descriptive names for special weeks
- Only one plan should be active at a time

### Adding Meals to Your Plan

There are three ways to add meals:

#### Method 1: Manual Selection

1. Open the menu plan
2. Find the day and meal slot (e.g., Monday Dinner)
3. Click **"Add Meal"**
4. Select a recipe from the dropdown or search
5. Set number of servings
6. Add optional notes
7. Click **"Add"**

#### Method 2: Using Recipe Suggestions

1. Open the menu plan
2. Click **"Get Suggestions"**
3. Select a suggestion strategy
4. View suggested recipes
5. Click **"Add to Menu"** on a suggestion
6. Choose day and meal type
7. Click **"Add"**

#### Method 3: Drag and Drop (if available)

1. Open the menu plan
2. Browse recipes in the sidebar
3. Drag a recipe card
4. Drop it on a day/meal slot
5. Confirm servings
6. Recipe is added

### Viewing Your Weekly Menu

**Calendar View:**
- 7 columns (Monday-Sunday)
- 4 rows (Breakfast, Lunch, Dinner, Snack)
- Each cell shows:
  - Recipe name
  - Servings
  - Cooked checkmark (if cooked)
  - Quick actions (view recipe, mark cooked, remove)

**List View:**
- Meals listed chronologically
- Grouped by day
- Shows full details

**Filtering:**
- Show only uncooked meals
- Show only specific days
- Show only specific meal types

### Editing Meal Assignments

**To Edit a Meal:**

1. Click on the meal in the plan
2. Edit:
   - Recipe (change to different recipe)
   - Servings (adjust quantity)
   - Notes
3. Click **"Save"**

**To Move a Meal:**
1. Edit the meal
2. Change the day or meal type
3. Save

**To Remove a Meal:**
1. Click on the meal
2. Click **"Remove from Plan"**
3. Confirm removal
4. Meal is deleted from plan

### Marking Meals as Cooked

When you prepare a meal, mark it cooked:

**To Mark as Cooked:**

1. Find the meal in the plan
2. Click the **"Mark as Cooked"** button (or checkbox)
3. Meal is marked cooked immediately

**What Happens:**
- Meal shows a checkmark or "Cooked" badge
- Recipe's `last_cooked_date` is updated to today
- Recipe's `times_cooked` is incremented by 1
- Inventory is auto-deducted (see [Auto-Deduction](#auto-deduction-when-cooking))
- You may receive a notification prompt to rate the recipe

**To Unmark as Cooked:**
1. Click the meal again
2. Click **"Mark as Not Cooked"**
3. Meal is reverted (inventory is NOT restored automatically)

### Copying a Previous Week's Plan

Easily recreate a successful week:

**To Copy a Plan:**

1. Open the plan you want to copy
2. Click **"Copy Plan"**
3. Select a new week start date
4. Optionally rename the plan
5. Click **"Copy"**
6. New plan is created with all meals
7. All meals are marked as "not cooked"
8. Dates are adjusted to the new week

**Use Cases:**
- Repeat a favorite week
- Rotate between a few standard weeks
- Start from a template and make small changes

**Notes:**
- Copying preserves recipes, servings, and meal types
- Cooked status is reset (all marked uncooked)
- Inventory is not affected until you cook the meals

### Auto-Generating a Week Plan

Let the system create a balanced week for you:

**To Auto-Generate:**

1. Click **"Menu Plans"** → **"Auto-Generate Week"**
2. Select:
   - **Week Start Date**
   - **Suggestion Strategy** (Rotation, Favorites, etc.)
   - **Meal Types** to include (Breakfast, Lunch, Dinner, Snack)
   - **Servings** per meal
3. Click **"Generate"**
4. System creates a full week plan:
   - 7 days of meals
   - Uses selected strategy
   - Ensures variety (no duplicate recipes)
   - Balances across days

**What Gets Created:**
- Default: 14 meals (Lunch + Dinner × 7 days)
- You can customize meal types
- All meals are marked as "not cooked"

**After Generation:**
- Review the generated plan
- Make any desired changes
- Recipes can be swapped or removed
- Mark as active when ready

**Tips:**
- Use **Rotation** strategy for variety
- Use **Favorites** for a crowd-pleasing week
- Use **Available Inventory** to minimize shopping
- Combine strategies: Generate with one, then manually swap a few meals

### Deleting Menu Plans

**To Delete a Plan:**

1. Open the menu plan
2. Click **"Delete Plan"**
3. Confirm deletion
4. Plan and all its meals are deleted

**When to Delete:**
- Plan is no longer needed (week has passed)
- Plan was created by mistake
- Starting over with a new plan

**Note:** Deletion is permanent. Recipes and inventory are not affected, only the plan.

---

## Shopping Lists

Generate shopping lists automatically from your menu plans.

### Generating Shopping Lists

**To Create a Shopping List:**

1. Go to **"Menu Plans"**
2. Open the menu plan you want to shop for
3. Click **"Generate Shopping List"**
4. Shopping list is created automatically

**What's Included:**
- All ingredients from all meals in the plan
- Quantities are aggregated (if same ingredient used multiple times)
- Current inventory is factored in
- Only items you actually need to purchase are listed

### Understanding Grouped vs. Ungrouped View

Shopping lists can be viewed in two ways:

#### Grouped by Category

**Default view:**
- Items organized by category:
  - Produce
  - Dairy
  - Meat/Seafood
  - Grains/Bread
  - Pantry
  - Condiments/Sauces
  - Frozen
  - Other
- Easier for shopping (matches store layout)
- Click category headers to expand/collapse

**Example:**
```
Produce:
  - 5 lbs Tomatoes
  - 2 heads Lettuce
  - 3 cups Onions, diced

Dairy:
  - 2 gallons Milk
  - 1 lb Butter
```

#### Ungrouped (Flat List)

**Alternative view:**
- All items in a single list
- Sorted alphabetically
- Simpler, more compact

**To Switch Views:**
- Toggle **"Group by Category"** button
- View preference is saved

### Smart Quantity Calculations

The shopping list is intelligent about quantities:

**How It Works:**

1. **Aggregation**: If multiple recipes use the same ingredient, quantities are summed
   - Recipe 1: 2 cups milk
   - Recipe 2: 3 cups milk
   - Shopping list: 5 cups milk

2. **Inventory Check**: Current inventory is subtracted
   - Total needed: 5 cups milk
   - Current stock: 1 cup milk
   - Shopping list: 4 cups milk

3. **Net Deficit Calculation**: Only what you need to buy is shown
   - If current stock >= needed: Item not on list
   - If current stock < needed: Net amount shown

**Display Format:**

Each item shows:
- **Item name**
- **Total quantity needed** (for all recipes)
- **Current stock** (what you have)
- **Net quantity to buy** (highlighted)

**Example:**
```
Milk
  Need: 5 cups
  Have: 1 cup
  Buy: 4 cups

Eggs
  Need: 12 eggs
  Have: 6 eggs
  Buy: 6 eggs

Flour
  Need: 2 cups
  Have: 5 cups
  Buy: 0 cups (sufficient stock)
```

**Stock Status Messages:**
- **"Sufficient stock"**: You have enough, no need to buy
- **"Not in inventory"**: Item not tracked, buy full amount
- **"Low stock, buy X"**: Item is low, buy net amount

### Checking Off Items

As you shop, mark items as purchased:

**To Check Off Items:**

1. Open the shopping list (on mobile or print it)
2. Click the checkbox next to each item as you add it to cart
3. Checked items are crossed out or moved to "purchased" section

**Notes:**
- Checking items does NOT update inventory
- This is just a shopping aid
- You'll update inventory manually after shopping

### Printing Shopping Lists

**To Print:**

1. Open the shopping list
2. Click **"Print"** button
3. Print dialog opens
4. Select printer and click **"Print"**

**Print Format:**
- Clean, printer-friendly layout
- Grouped by category (or flat, depending on view)
- Checkboxes for manual marking
- Quantities clearly displayed

**Tips:**
- Print in portrait orientation
- Use grouped view for easier shopping
- Print before heading to the store

### Exporting to PDF (if implemented)

**To Export:**

1. Open the shopping list
2. Click **"Export PDF"**
3. PDF is generated and downloaded
4. Open PDF to view or share

**Uses:**
- Email to family members
- Save for records
- View on mobile device without internet

---

## Notifications

Stay informed with alerts and reminders.

### Understanding Notification Types

The system generates several types of notifications:

| Type | Description | Triggered By |
|------|-------------|--------------|
| **Low Stock** | Item below minimum threshold | Inventory update |
| **Expiring** | Item expiring soon | Daily check (auto) |
| **Meal Reminder** | Upcoming meal alert | Admin generation or schedule |
| **Recipe Update** | Recipe version changed | Recipe edit |
| **System** | System announcements | Admin message |

**Notification Frequency:**
- Low Stock: Immediate (when quantity drops below threshold)
- Expiring: Daily (generated at midnight)
- Meal Reminder: Configurable (e.g., morning of meal day)
- Recipe Update: Immediate (when recipe is edited)
- System: Ad-hoc (admin-initiated)

### Viewing Notifications

**Notification Bell:**
- Located in top navigation bar
- Badge shows unread count
- Click to open notifications dropdown

**Dropdown:**
- Shows recent notifications (last 10)
- Newest first
- Unread notifications highlighted
- Click notification to view details or navigate

**Notification Page:**
1. Click **"View All"** in dropdown, or
2. Click your profile → **"Notifications"**
3. See all notifications in a list
4. Filter by type, read/unread status, date

**Notification Details:**

Each notification shows:
- **Icon**: Type-specific icon (warning, info, bell, etc.)
- **Title**: Brief headline
- **Message**: Detailed message
- **Link**: Click to navigate to related page (e.g., inventory item, recipe)
- **Timestamp**: When notification was created
- **Read status**: Read or unread

**Color Coding:**
- Red: Urgent (low stock, expiring soon)
- Yellow: Warning (approaching expiration)
- Blue: Informational (recipe update, system message)
- Green: Positive (meal reminder, achievements)

### Marking as Read

**To Mark a Single Notification as Read:**

1. Click on the notification
2. It's automatically marked as read
3. Badge count decreases

**To Mark All as Read:**

1. Open notifications dropdown or page
2. Click **"Mark All as Read"**
3. All unread notifications are marked read
4. Badge count resets to 0

**Auto-Read:**
- Notifications are auto-marked read when you click them
- Navigating to the linked page marks it read
- You can manually mark as unread (if feature available)

### Notification Settings (if applicable)

**To Configure Notifications:**

1. Go to **Profile** → **"Notification Settings"**
2. Toggle notification types on/off:
   - Low stock alerts
   - Expiring item alerts
   - Meal reminders
   - Recipe updates
   - System announcements
3. Set notification frequency:
   - Immediate
   - Daily digest
   - Weekly digest
4. Choose delivery method:
   - In-app only
   - Email (if configured)
5. Click **"Save Settings"**

**Notes:**
- Admins cannot override your notification preferences
- Some critical system notifications cannot be disabled
- Email notifications require email configuration by admin

---

## Admin Features

*This section is for users with **admin** role only.*

If you're a standard user, you won't see these menu options.

### Accessing Admin Dashboard

**To Access:**

1. Click **"Admin"** in the navigation menu
2. You'll see the admin dashboard

**Dashboard Sections:**
- **User Management**: Create, edit, activate/deactivate users
- **System Settings**: Configure application settings
- **Statistics**: View system usage and analytics
- **Notification Management**: Generate notifications manually

### User Management

#### Viewing All Users

1. Go to **Admin** → **"Users"**
2. See a table of all users:
   - Username
   - Email
   - Role (admin, user, child)
   - Active status
   - Last login
   - Created date
3. Search and filter users
4. Sort by column

#### Creating Users

**To Create a New User:**

1. Click **"Admin"** → **"Users"** → **"Create User"**
2. Fill in the form:
   - **Username**: 3-50 characters, unique
   - **Email**: Valid email, unique
   - **Password**: Minimum 8 characters
   - **Role**: admin, user, or child
   - **Active**: Check to activate immediately
3. Click **"Create User"**
4. User account is created
5. Provide credentials to the user

**Tips:**
- Use strong passwords for admin accounts
- Activate users immediately unless creating for future use
- Choose roles carefully (admins have full access)

#### Editing Users

**To Edit a User:**

1. Find the user in the users list
2. Click **"Edit"**
3. Update:
   - Email address
   - Role
   - Active status
4. Click **"Save"**

**What You Can Change:**
- Email
- Role (promote to admin, demote to user)
- Active status (activate/deactivate)

**What You Cannot Change:**
- Username (permanent)
- User ID

**Changing Passwords:**
- Click **"Reset Password"**
- Enter new password
- User must be notified of the new password

#### Activating/Deactivating Users

**To Deactivate a User:**

1. Find the user
2. Click **"Edit"**
3. Uncheck **"Active"**
4. Click **"Save"**
5. User cannot log in anymore

**To Reactivate:**
1. Follow same steps but check **"Active"**

**Uses:**
- Temporarily disable accounts
- Offboard family members
- Suspend access for any reason

**Note:** Deactivating does NOT delete user data. Recipes, ratings, and activity history are preserved.

### System Settings

**To Access Settings:**

1. Go to **Admin** → **"Settings"**
2. View and edit system configuration

**Available Settings:**

#### Favorites Configuration

- **Favorites Threshold Percentage** (default: 75%)
  - Minimum percentage of positive ratings to be a favorite
  - Range: 50-100%
  - Example: 75% means at least 3/4 ratings must be positive

- **Favorites Minimum Raters** (default: 2)
  - Minimum number of users who must rate a recipe
  - Range: 1-10
  - Prevents single ratings from marking favorites

#### Inventory Configuration

- **Low Stock Threshold Days** (default: 3 days)
  - How many days of stock triggers low stock alert
  - Range: 1-30 days
  - Applies to items with minimum quantity set

- **Expiration Warning Days** (default: 7 days)
  - How many days before expiration to generate warning
  - Range: 1-30 days
  - Example: 7 days means you're notified a week before expiration

#### Recipe Scraper Configuration

- **Scraper Rate Limit** (default: 5 seconds)
  - Minimum seconds between scrape requests to same domain
  - Range: 1-60 seconds
  - Prevents overloading recipe websites

**To Update Settings:**

1. Edit the values
2. Click **"Save Settings"**
3. Settings are applied immediately
4. Existing data may be recalculated (e.g., favorites)

**Tips:**
- Start with defaults and adjust based on usage
- Lower favorites threshold for small households
- Increase expiration warning for less frequent shopping
- Respect scraper rate limits to be a good web citizen

### Viewing Statistics

**To Access Statistics:**

1. Go to **Admin** → **"Dashboard"** or **"Statistics"**
2. View system analytics

**Available Statistics:**

#### Overview Metrics

- **Total Users**: Number of registered users
- **Active Users**: Users logged in recently
- **Total Recipes**: Recipe count
- **Total Inventory Items**: Items in stock
- **Menu Plans Created**: Number of plans

#### Recipe Analytics

**Most Cooked Recipes** (Chart)
- Bar chart showing top 10 most cooked recipes
- X-axis: Recipe title
- Y-axis: Times cooked
- Data: From `times_cooked` field

**Most Favorited Recipes** (Chart)
- Bar chart showing recipes with highest positive rating percentage
- Filtered to favorites only
- Shows rating statistics

**Recipe Distribution by Difficulty** (Pie Chart)
- Breakdown: Easy, Medium, Hard
- Shows percentage of each

#### Inventory Analytics

**Low Stock Items**: Count and list
**Expiring Soon**: Count and list
**Items by Category**: Breakdown of inventory by category

#### User Activity

**Recent Activity Log**:
- Last 50 actions
- User, action type, timestamp
- Filterable by user and date

**Usage Trends** (Line Chart):
- Daily active users over last 30 days
- Recipe creations over time
- Menu plans created over time

#### System Health

- **Database Size**: Total database size in MB
- **Total Recipes**: Count
- **Total Ingredients**: Count across all recipe versions
- **Total Ratings**: Count

**Exporting Statistics:**
- Click **"Export CSV"** to download data
- Use for reporting, analysis, or record-keeping

---

## Tips and Best Practices

### Weekly Planning Workflow

A suggested weekly workflow:

**Sunday:**
1. Review current inventory
2. Mark meals cooked during the week
3. Check expiring items
4. Plan next week's menu:
   - Use Rotation strategy for variety
   - Include favorites for crowd-pleasers
   - Plan quick meals for busy nights
   - Consider seasonal recipes
5. Generate shopping list
6. Check shopping list against inventory

**Monday:**
- Go grocery shopping with list
- Update inventory with new items
- Check off items as purchased

**Throughout the Week:**
- Mark meals as cooked when you prepare them
- Rate recipes after eating
- Check notifications for low stock alerts
- Update inventory if you use items for other meals

### Keeping Inventory Updated

Best practices for accurate inventory:

- **Regular Updates**: Update inventory at least once a week
- **After Shopping**: Add all new items immediately
- **After Cooking**: Let auto-deduction handle it, but verify
- **Set Expirations**: Always set expiration dates for perishables
- **Consistent Naming**: Use the same names (e.g., "Milk" not "Whole Milk" or "2% Milk")
- **Use Categories**: Categorize items for better organization
- **Set Thresholds**: Set minimum quantities for staples

### Using Tags Effectively

Maximize recipe discoverability with good tagging:

**Tag Categories:**
- **Cuisine**: Italian, Mexican, Asian, French, etc.
- **Meal Type**: Breakfast, Lunch, Dinner, Dessert, Snack
- **Dietary**: Vegetarian, Vegan, Gluten-Free, Dairy-Free, Keto, Paleo
- **Season**: Spring, Summer, Fall, Winter
- **Occasion**: Holiday, Birthday, Quick Meal, Comfort Food, Healthy
- **Cooking Method**: Grilled, Baked, Slow Cooker, Instant Pot, Stovetop
- **Main Ingredient**: Chicken, Beef, Pasta, Rice, Seafood

**Tagging Tips:**
- Use 3-7 tags per recipe
- Be specific and consistent
- Create tag naming conventions (e.g., "Gluten-Free" not "No Gluten")
- Tag both cuisine and dietary restrictions
- Include season tags for produce-heavy recipes
- Add occasion tags for special meals

### Managing Recipe Versions

Version control best practices:

**When to Create a New Version:**
- Adjusting ingredient quantities
- Modifying cooking instructions
- Changing cooking method
- Fixing mistakes or typos
- Improving based on feedback

**When to Create a New Recipe:**
- Significantly different dish
- Different cuisine style
- Different main ingredients
- Variations that would confuse the original

**Version Management:**
- Add notes explaining major changes
- Test new versions before replacing originals
- Keep version history for reference
- Revert if new version doesn't work out

### Meal Prep Strategies

Use the app to support meal prep:

**Batch Cooking:**
1. Find recipes suitable for batch cooking (tag: "Batch Friendly")
2. Plan same recipe multiple times in a week
3. Adjust servings to cook once, eat multiple times
4. Mark first meal as cooked, subsequent meals as "pre-cooked"

**Theme Nights:**
- Use tags to create themes: Taco Tuesday, Pasta Friday
- Search by tag when planning
- Rotate within theme each week

**Ingredient Grouping:**
- Plan meals with overlapping ingredients
- Use "Available Inventory" suggestions
- Reduces shopping and waste

**Prep Day Planning:**
- Use notes field to track what can be prepped ahead
- Plan complex recipes for days with more time
- Schedule quick meals for busy nights

---

## Troubleshooting

### Common Issues and Solutions

#### Cannot Log In

**Problem:** Username or password not working

**Solutions:**
- Verify username and password (case-sensitive)
- Check Caps Lock is off
- Ensure your account is active (contact admin)
- Clear browser cache and cookies
- Try a different browser
- Contact admin to reset password

#### Recipe Scraping Not Working

**Problem:** Cannot import recipe from website

**Solutions:**
- Verify the URL is correct
- Check if site is supported (not all sites work)
- Look for `robots.txt` warning - site may block scraping
- Wait 5 seconds between scrape attempts (rate limit)
- Try copying data manually instead
- Contact admin if issue persists

#### Inventory Not Auto-Deducting

**Problem:** Marking meal as cooked doesn't reduce inventory

**Solutions:**
- Verify ingredient names match exactly (case doesn't matter)
- Check inventory item exists
- Ensure quantity is >0 before cooking
- Check inventory history to confirm deduction occurred
- Manually adjust if needed
- Report issue to admin if happening consistently

#### Notifications Not Appearing

**Problem:** Not receiving expected notifications

**Solutions:**
- Check notification settings (if available)
- Verify notifications are enabled for that type
- Check notification page (may not show in bell icon)
- Ensure items have expiration dates / thresholds set
- Ask admin to manually generate notifications
- Try logging out and back in
- Check browser permissions (if using push notifications)

#### Shopping List Incorrect Quantities

**Problem:** Shopping list shows wrong amounts

**Solutions:**
- Verify inventory is up-to-date
- Check recipe ingredient quantities
- Ensure units match between recipe and inventory
- Regenerate shopping list
- Manually adjust as needed
- Report issue to admin with specific example

#### Menu Plan Not Saving

**Problem:** Changes to menu plan don't persist

**Solutions:**
- Check internet connection
- Verify you clicked "Save"
- Look for error messages
- Try refreshing the page
- Clear browser cache
- Try a different browser
- Contact admin if issue continues

### Browser Compatibility

**Supported Browsers:**
- Google Chrome (latest version)
- Mozilla Firefox (latest version)
- Safari (latest version, macOS/iOS)
- Microsoft Edge (latest version)

**Recommended:**
- Google Chrome for best experience
- Keep browser updated to latest version

**Not Supported:**
- Internet Explorer (any version)
- Older browser versions (>2 years old)

**If Using an Unsupported Browser:**
- Some features may not work
- Layout may appear broken
- Update to a supported browser

### Getting Help

**If you need assistance:**

1. **Check this guide**: Search for your issue
2. **Check FAQ**: See [FAQ.md](FAQ.md)
3. **Contact your admin**: They can help with user-specific issues
4. **Report a bug**: Provide:
   - What you were trying to do
   - What happened vs. what you expected
   - Steps to reproduce
   - Browser and version
   - Screenshots if applicable

**For Administrators:**
- See [Administrator Guide](ADMIN_GUIDE.md)
- See [Developer Guide](DEVELOPER_GUIDE.md) for technical issues

---

## Conclusion

This user guide covers all features of the Household Meal Planning System. For additional information:

- **Developer Guide**: [DEVELOPER_GUIDE.md](DEVELOPER_GUIDE.md) - For technical implementation details
- **Admin Guide**: [ADMIN_GUIDE.md](ADMIN_GUIDE.md) - For system administration
- **API Documentation**: [API_DOCUMENTATION.md](API_DOCUMENTATION.md) - For API integration
- **FAQ**: [FAQ.md](FAQ.md) - Frequently asked questions

Happy meal planning!

---

**Document Version:** 1.0
**Last Updated:** October 1, 2025
**Application Version:** 1.0.0
