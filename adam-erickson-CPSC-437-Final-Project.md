# Stuffd: CPSC 437 Final Project (Database Systems)

> Adam Erickson
>
> netid: age3
>
> Github Link: 

## General Idea

After watching Michael Pollan's netflix documentary series, "Cooked", I came away with one big understanding about healthy food.  It doesn't matter what the ingredients are, what the fat/protein/carbohydrate content is, or how much you eat: the number one rule of thumb that leads to healthier food is "food is healthiest when you cook it yourself".  This is because corporations cook very differently than people do, and use all kind of cheap additives and fillers in order to cut cost.

It's very easy to order take out food.  Think of apps like GrubHub.  I wanted to create an experience similar to that, where you scroll through a menu and choose the items you'd like to eat, but instead of charging you to cook the food and deliver it to you, instead we provide you all theinformation to get the ingredients and cook it yourself.  Like generating an automatic shopping list.

Ultimately, if this app went beyond prototype, the goal would be to have an app like a delivery app, except instead of the cooked meal being delivered to you someone would deliver to you fresh ingredients.

This is sort of what "hello fresh" is like, except they choose the menu items for you and they are the sole supplier of ingredients.  I was thinking something similar, except we tell you what ingredients to buy so you can locate them as cheaply as possible somewhere, be it your local grocery store or farmer's market.

### My Goal

So, my goal was simple.  Make some kind of app that makes it easier to cook food at home, instead of buying pre-cooked food at the grocery store, ordering fast food, or going to a restaurant.

## Process

#### 1. Get Data

First I had to get data for the nutritional information.  I got data from the USA government on scientific contents of different food "ingredients", the sort of thing that you might find in a recipe.  This data can be gotten from: https://ndb.nal.usda.gov/ndb/.   It is provided in raw ASCII files, and has all of the nutritional and scientific information you could want.

Then I also had to get recipe data.  At first I tried scraping the web for recipes with Python, beautiful soup, and using some NLP techniques described by the New York Times here: https://open.blogs.nytimes.com/2015/04/09/extracting-structured-data-from-recipes-using-conditional-random-fields/.  This proved difficult because of many reasons, like converting Unicode, properly handling strings, syncing up different ways of describing the same ingredient, etc.  This was only done for a small number of recipes.

When these efforts proved hard to scale, I also turned to API's for recipe data.  For example, you can see one example api here: https://spoonacular.com/food-api, and another one here: https://www.edamam.com/.  These returned JSON objects that did not neccesarily have all of the attributes I wanted, and had to be parsed in certain ways to fit into the database.

#### 2. Build Database

In order to get the data into a normalized table format there were several challenged:

**First**: Matching the names of the ingredients with the names of the items in the **nutritional data** table.  This was challenging, and at times I had to approximate with fuzzy string matching.  There were some ingredients that were not included in the nutritional database of course.  These were often branded ingredients, like a particular sauce, and since they were always relatively small by mass they were left out of the nutritional calculations.

**Second**: The same problem as above, matching strings, except this time with the **units** or amount of each ingredient.  This was especially challenging since sometimes the amounts would contain **qualitative information about the ingredient**.   For example, consider the following:

```javascript
amount: "3 cups, fresh, finely chopped"
```

Obviously the **fresh, finely chopped** part is **NOT ACTUALLY AN AMOUNT**, but is telling you more about the **type of ingredient** you want to use.  This was very difficult and confusing at first, since the only data I really want from this is **`3 cups`**.  The extra information was stripped away, and an attempt was made to use it in the **first** problem above, matching ingredients between the **recipes data** and the **nutrition data**. 

**Third**: There were several many to many relationships, where I had to implement Association entities, that contained attributes on that relationship.  For example, the many to many between recipes and ingredients, which has the attribute on the relationship "amount", because each recipe calls for a certain amount of something, but that ingredient can be used in many recipes.  Figuring out exactly how to do this of course is the **challenge of the normalized table schema**, but it was particularly difficult to figure out how to do properly while handling the above challenges.

**In summary**: there were many **NLP** type of challenges with the recipes that were difficult to deal with, and simpler methods were favored over more complex ones for expediency.

In the end, here is a picture of the database schema:
![](/home/agerick/stuffd/stuffd-schema.png)

## What NF our table design meets

So the schema is above, with foreign key relationships.  It can also be written:

1. **Association:** (id, recipe_id, ingredient_id, amount, unit)
2. **Weight:** (ingredient_id, seq, amount,msre_unit, grams, num_Data_Pts, std_Dev)
3. **Nutrient:** (id, name, units)
4. **SourceCode:** (id, description)
5. **NutrientData**: (ingredient_id, nutrient_id, amount, number_of_data_points, std_Error ,source_code ,number_of_studies, minVal, maxVal)
6. **DataSource:** (id, publication)
7. **DataSourceLink:** (ingredient_id,nutrient_id,data_source_id)
8. **Recipe: **(id,title,instructions,vegetarian,glutenFree,dairyFree,sourceUrl,pricePerServing,readyInMinutes,servings,image)
9. **Ingredient:** (id,name,aisle,consistency,image)
10. **User:** (id,username,password_hash)
11. **ShoppingCart:** (quantity, recipe_id, user_id)

and thats it.

>  As you can see, our schema is **large** and **fairly complicated**. Indeed, **a majority of the time went into building the database**

Looking at the associations, we see:

1. id **--->** recipe_id, ingredient_id, amount, unit
2. (ingredient_id, seq) **--->** amount, msre_unit, grams, num_Data_Pts, std_Dev
3. id **--->** name, units
4. id **--->** description
5. (ingredient_id, nutrient_id) **--->** amount, number_of_data_points, std_Error ,source_code ,number_of_studies, minVal, maxVal
6. id **--->** publication
7. (ingredient_id,nutrient_id) **--->** data_source_id
8. id **--->** title, instructions, vegetarian, glutenFree, dairyFree, sourceUrl, pricePerServing, readyInMinutes, servings, image
9. id **--->** name,aisle,consistency,image
10. id **--->** username, password_hash
11. (recipe_id, user_id) **--->** quantity

Above, we are in 1st normal form (trivially).  Then, for any non-prime attribute, it is dependent on only the entire candidate key and no proper subset, so we are in 2nd normal form.

We achieve 3rd normal form because **every non-prime attribute** is **non-transitively dependent** on **every candidate key**, for all of the relations above.

**BUT WAIT!**: Maybe you are looking at the **association** table.  Doesn't the recipie_id and ingredient_id determine all the non-prime attributes, since surely there is only one association per recipe-ingredient?

**NO!**: I learned this the hard way!  A recipe could call for `2 sticks of butter`, and then later also for `2 grams of butter`.  They do this because maybe you are using this butter in different ways.  I had to add the **id** column in order for this to **be able to be index** on anything other than the full, entire row.  This introduces some multiple, overlapping candidate keys though.

And this is why we are **3NF** not **BCNF**.  To see this explanation with cantidate keys see(https://stackoverflow.com/a/8438829).


#### 3. Perform more computation and cleaning on data

Once the data were **in the database**, there was still cleaning and computation to be performed.  For example, the **nutrition data** is all in terms of 100 gram samples of a given ingredient, but the amounts given for ingredients in the recipes was given in a wide variety of ways.  

**Volume units**: When the ingredient amount was given in volume units, we could use the **weights** table to convert it into a mass unit, and thus use the 100 gram sample measurement in the nutritional data table.

**Slang Units**: It does not help that most ingredients have their own slang units, like **sprig of parsley**, and this has no easy conversion to mass units.  If there was a comparable ingredient an approximation of the mass was attained, otherwise these units were assumed small and left out of the computation of nutrition, for lack of a better solution.

**Nutrient**: Similarly, each nutrient had its own units (`grams`, `micrograms`, etc.), but these were usually mass and easier to convert.

#### 4. Build backend and API

Now the backend was built in **Python Flask**, to create various **API Endpoints**.  Note that much more computation is possible with the backend than is exposed in **endpoints**, as is typical.  Many future queries could be added to specific endpoints, and so the backend **is extendable**.  With more group members, perhaps they would have added additional ways for the browser to query the database.

**Composing Recipes**: When the user of the application wants something from the database, they usually want just a **recipe** like how you or I imagine it.  However, due to database normalization, the recipes are spread across many tables.  The recipe table in fact only includes things like the name and image, with **links to the ingredients**, which then **links to nutrition association**, which then **links to nutrients**, which **links to data sources**, and so on.  In order to present something sensible to the user as an **object** how they might imagine it, some clever **joins** and **object oriented programming** went into creating a nice **`Recipe` resource**.  This is the object most commonly dealt with in the API endpoints.

The queries, in the form of **GET** and **POST** requests that can be executed from the web onto the database, include:

1. **Retrieving** list / random recipes to display to the user for _discovery_
2. **Searching** the database for a particular recipe when none is presented on the front end
3. **Adding** a certain recipe to the **shopping cart** of a particular user, so they may come back later, and so that computation can be done on their cart to reveal nutrition information, time to cook, shopping list, etc.

Note that the API is **also**  built more thoroughly than the front-end, as I imagine is usually the case.  For example, linking the exact scientific paper (**"data source"**) of the nutrition information is possible with the database and the backend, but I did not see a sensible way to present this to the end user on the frontend, without considerably bloating the interface.

#### 5. Build Frontend and Interface

Now, I didn't know much of any javascript, so I spent several days learning.  Then, to avoid learning HTML and CSS and everything at once, I built the frontend in **`React.js`**, which allows you to build a full **view** layer in basically pure javascript.

As built in react.js, the frontend allows users to:

- **View** and **load more** recipes from example recipes
- **Filter** the recipes by dietary restrictions
- **Search** the database via text string if a recipe is not loaded of a particular kind
- **Add** recipes to cart
  - Cart computes time to make, total price, and nutritional aspects of all recipes
  - Can also produce a shopping list of ingredients
    - (not necessarily of amounts, because one recipe might say **2 springs of parsley** and another might say, **2 grams of parsley**, and reconciling this without a mapping is an advanced challenge at scale
- **Select quantity** of the recipes to add to cart
- **Click to learn more** as a modal dialog pops up for every ingredient
  - Includes more information about the recipe object generated from database
- **Find source url** so you can view the original recipe where it appears on the web
- **View instructions** so you could prepare the recipe yourself at home
- **.....and more!**

Here are some quick screenshots of the front end:

![](/home/agerick/stuffd/app-screenshot.png)


![](/home/agerick/stuffd/modal-screenshot.png)

![](/home/agerick/stuffd/cart-screenshot.png)





#### 6. Make a logo

My girlfriend made the orange mushroom logo you see in the site :)

![](/home/agerick/stuffd/logo.png)

#### 7. Future Steps (and things that other group members would have done)

The biggest future step I would like to take is...:

**Integrate into an online grocer:** Ideally, you could choose a recipe and it would connect via some **private api** to a grocery store, say **amazon fresh**, and then it would automatically populate the shopping list in your amazon account with the ingredients of the recipes you chose.

This is difficult because again, we have to **map from ingredients in recipes to actual items in stores**.  This means a couple things, like:

- Choosing amoungst different brands of items
  - Say the recipe says **milk**.  There are multiple brands, which does app choose?
- Mapping different names
  - **Corriander** is a nickname for **cilatro** for example
- Finding substitutes
  - If there are no **red peppers**, can the store instead give you **green peppers**?

And then there are the obvious app-upgrades to the prototype, like:

- More robust user management
- Log in with google
- Plots and charts of nutrition information in your cart
- History tracking of your food eating habits over time
- **Recommender systems** for different recipes you might like

## Biggest Challenges

First, it would have been much easier with more group members.  Since I had to deal with the frontend, database, and backend, it  was not enough time to learn one thing well, like **learn javascript well** and forget about the database and python, for example.

Second, the matching up of text, especially the ingredients with different names and the unit conversion, gave me a special appreciation for the difficulty of NLP for even simple tasks, like structuring the data of a recipe.

**Other challenges** are included in the specific sections of the document above.

## Most interesting Factor of project

The ability to search for, filter, and add different recipes in a structure fashion, without all the sidebars and pop-ups on "allrecipes.com", is something I've been wanting for a while.







