from flask import Flask, request, jsonify, send_from_directory, render_template
from flask_cors import CORS
import random
import json
import os

app = Flask(__name__)
CORS(app)

# Enhanced Nutrition and Fitness Database
NUTRITION_RESPONSES = {
    'breakfast': [
        "Power Breakfast Bowl:\n- 1 cup quinoa\n- 1 banana\n- 1/4 cup almonds\n- 1 tbsp chia seeds\n- 1 cup almond milk\n- 1 tbsp honey\nCook quinoa in almond milk, top with sliced banana, almonds, and chia seeds. Drizzle with honey.",
        "Protein-Packed Breakfast:\n- 3 eggs\n- 1 cup spinach\n- 1/2 avocado\n- 1 slice whole grain toast\n- 1 tbsp olive oil\nSauté spinach in olive oil, scramble eggs, serve with avocado and toast.",
        "Overnight Oats:\n- 1 cup rolled oats\n- 1 cup almond milk\n- 1 tbsp chia seeds\n- 1 tbsp honey\n- 1/4 cup mixed berries\nMix ingredients, refrigerate overnight, top with berries before serving."
    ],
    'lunch_dinner': [
        "Mediterranean Bowl:\n- 1 cup quinoa\n- 1 cup chickpeas\n- 2 cups mixed vegetables\n- 2 tbsp olive oil\n- 1 lemon\n- Fresh herbs\n- 4 oz grilled chicken\nCook quinoa, roast vegetables, combine with chickpeas and chicken, dress with olive oil and lemon juice.",
        "Healthy Buddha Bowl:\n- 1 cup brown rice\n- 1 cup black beans\n- 1 cup roasted vegetables\n- 1 avocado\n- 2 tbsp tahini dressing\n- 1/4 cup pumpkin seeds\nCook rice, combine with beans and vegetables, top with avocado and seeds.",
        "Salmon Power Bowl:\n- 6 oz salmon fillet\n- 1 cup quinoa\n- 2 cups mixed vegetables\n- 1 tbsp olive oil\n- 1/4 cup almonds\n- Lemon herb dressing\nBake salmon, serve with quinoa and roasted vegetables."
    ],
    'snacks': [
        "Energy Bites:\n- 1 cup dates\n- 1/2 cup nuts\n- 1/4 cup chia seeds\n- 1/4 cup coconut\n- 1 tbsp honey\nBlend ingredients, form into balls, refrigerate.",
        "Protein Smoothie:\n- 1 banana\n- 1 cup spinach\n- 1 scoop protein powder\n- 1 cup almond milk\n- 1 tbsp chia seeds\n- 1/4 cup berries\nBlend all ingredients until smooth.",
        "Veggie Platter:\n- Carrot sticks\n- Celery\n- Cherry tomatoes\n- Cucumber\n- 1/4 cup hummus\n- 1/4 cup guacamole\nArrange vegetables with dips."
    ],
    'protein': [
        "Complete Protein Guide:\n- Lean meats: chicken (25g/3oz), fish (22g/3oz)\n- Plant-based: lentils (9g/1/2 cup), tofu (10g/1/2 cup)\n- Eggs: 6g per egg\n- Dairy: Greek yogurt (17g/cup)\nAim for 0.8-1g protein per kg body weight daily.",
        "Vegetarian Protein Sources:\n- Legumes: beans, lentils, chickpeas\n- Tofu and tempeh\n- Seitan\n- Quinoa\n- Nuts and seeds\nCombine with whole grains for complete proteins.",
        "Protein Timing:\n- Pre-workout: 20-30g protein\n- Post-workout: 20-40g protein\n- Space protein intake throughout the day\n- Include protein in every meal."
    ],
    'vegetables': [
        "Colorful Vegetable Guide:\n- Green: spinach, kale, broccoli\n- Orange: carrots, sweet potatoes\n- Red: tomatoes, bell peppers\n- Purple: eggplant, purple cabbage\n- White: cauliflower, mushrooms\nAim for 5-7 servings daily.",
        "Cooking Methods:\n- Steaming: preserves nutrients\n- Roasting: enhances flavor\n- Sautéing: quick and healthy\n- Raw: maximum nutrients\n- Fermenting: adds probiotics",
        "Seasonal Vegetables:\nSpring: asparagus, artichokes\nSummer: tomatoes, zucchini\nFall: squash, Brussels sprouts\nWinter: root vegetables, leafy greens"
    ],
    'fruits': [
        "Fruit Nutrition Guide:\n- Berries: high in antioxidants\n- Citrus: rich in vitamin C\n- Apples: good source of fiber\n- Bananas: potassium-rich\n- Avocados: healthy fats\nAim for 2-3 servings daily.",
        "Fruit Pairings:\n- Apple + peanut butter\n- Banana + yogurt\n- Berries + oatmeal\n- Citrus + nuts\n- Avocado + whole grain toast",
        "Fruit Timing:\n- Morning: citrus fruits\n- Pre-workout: bananas\n- Post-workout: berries\n- Evening: apples\n- Snacks: mixed fruits"
    ],
    'weight_management': [
        "Sustainable Weight Management:\n- Track portions using hand measurements\n- Eat mindfully and slowly\n- Stay hydrated (8-10 glasses daily)\n- Get 7-9 hours of sleep\n- Manage stress levels",
        "Meal Planning Tips:\n- Prepare meals in advance\n- Use smaller plates\n- Include protein in every meal\n- Eat fiber-rich foods\n- Limit processed foods",
        "Exercise Integration:\n- 150 minutes cardio weekly\n- 2-3 strength training sessions\n- Daily walking (10,000 steps)\n- HIIT workouts 2-3 times/week\n- Regular activity breaks"
    ],
    'exercises': [
        "Full Body Workout:\n- Push-ups: 3 sets of 10-12 reps\n- Squats: 3 sets of 15 reps\n- Plank: 3 sets of 30 seconds\n- Pull-ups: 3 sets of 8-10 reps\n- Deadlifts: 3 sets of 12 reps\nRest 60 seconds between sets.",
        "Cardio HIIT:\n- 5-minute warm-up\n- 30 seconds sprint\n- 90 seconds walk\n- Repeat 10 times\n- 5-minute cool-down\nTotal time: 25 minutes",
        "Flexibility Routine:\n- Neck rolls: 10 each direction\n- Shoulder stretches: 30 seconds each\n- Hamstring stretches: 30 seconds each\n- Hip flexor stretches: 30 seconds each\n- Cat-cow stretches: 10 reps"
    ],
    'recipes': [
        "Healthy Mediterranean Bowl:\n- 1 cup quinoa\n- 1 cup chickpeas\n- 2 cups mixed vegetables\n- 2 tbsp olive oil\n- 1 lemon\n- Fresh herbs\nCook quinoa, roast vegetables, combine with chickpeas, dress with olive oil and lemon juice.",
        "Protein-Packed Smoothie:\n- 1 banana\n- 1 cup spinach\n- 1 scoop protein powder\n- 1 cup almond milk\n- 1 tbsp chia seeds\nBlend all ingredients until smooth.",
        "Baked Salmon with Vegetables:\n- 6 oz salmon fillet\n- 2 cups mixed vegetables\n- 1 tbsp olive oil\n- Herbs and lemon\nPreheat oven to 400°F, bake for 20-25 minutes."
    ],
    'meal_planning': [
        "Weekly Meal Planning:\n- Plan meals on Sunday\n- Prep ingredients in advance\n- Cook in batches\n- Store in portion containers\n- Keep healthy snacks ready",
        "Grocery Shopping Guide:\n- Shop the perimeter\n- Buy seasonal produce\n- Choose whole grains\n- Include lean proteins\n- Stock healthy fats",
        "Portion Control Tips:\n- Use smaller plates\n- Measure portions\n- Eat slowly\n- Stop at 80% full\n- Stay hydrated"
    ],
    'supplements': [
        "Essential Supplements:\n- Multivitamin\n- Omega-3 fatty acids\n- Vitamin D\n- Probiotics\n- Magnesium\nConsult healthcare provider before starting.",
        "Pre-Workout:\n- Caffeine\n- Beta-alanine\n- Creatine\n- BCAAs\n- Electrolytes\nTake 30 minutes before exercise.",
        "Post-Workout:\n- Protein powder\n- Electrolytes\n- BCAAs\n- Glutamine\n- Antioxidants\nTake within 30 minutes after exercise."
    ],
    'general_health': [
        "Daily Health Checklist:\n- 7-9 hours of sleep\n- 8-10 glasses of water\n- 30 minutes exercise\n- 5 servings of vegetables\n- 2 servings of fruit\n- Stress management\n- Regular check-ups",
        "Healthy Lifestyle Tips:\n- Practice mindfulness\n- Stay socially connected\n- Regular physical activity\n- Balanced diet\n- Adequate sleep\n- Stress reduction\n- Regular health screenings",
        "Wellness Routine:\n- Morning: Stretching and water\n- Midday: Healthy snack and walk\n- Evening: Relaxation and sleep prep\n- Weekly: Exercise and meal planning\n- Monthly: Health check and goals review"
    ],
    'mental_health': [
        "Mental Wellness Tips:\n- Regular exercise\n- Balanced diet\n- Adequate sleep\n- Stress management\n- Social connections\n- Mindfulness practice\n- Professional support when needed",
        "Stress Management:\n- Deep breathing exercises\n- Regular physical activity\n- Meditation or yoga\n- Time management\n- Healthy boundaries\n- Adequate rest\n- Professional counseling if needed",
        "Mood-Boosting Foods:\n- Fatty fish (omega-3)\n- Dark chocolate\n- Berries\n- Green tea\n- Nuts and seeds\n- Leafy greens\n- Fermented foods"
    ],
    'sleep_health': [
        "Sleep Hygiene Tips:\n- Consistent sleep schedule\n- Dark, cool bedroom\n- No screens before bed\n- Regular exercise\n- Caffeine management\n- Relaxation routine\n- Comfortable bedding",
        "Better Sleep Habits:\n- Avoid large meals before bed\n- Limit alcohol intake\n- Create bedtime routine\n- Exercise during day\n- Manage stress\n- Limit naps\n- Regular wake time",
        "Sleep-Boosting Foods:\n- Warm milk\n- Chamomile tea\n- Bananas\n- Almonds\n- Turkey\n- Kiwi\n- Tart cherries"
    ],
    'stress_management': [
        "Stress Reduction Techniques:\n- Deep breathing\n- Meditation\n- Exercise\n- Time management\n- Social support\n- Hobbies\n- Professional help",
        "Work-Life Balance:\n- Set boundaries\n- Regular breaks\n- Time management\n- Delegate tasks\n- Self-care routine\n- Regular exercise\n- Adequate rest",
        "Quick Stress Relief:\n- 5-minute meditation\n- Deep breathing\n- Short walk\n- Stretching\n- Music therapy\n- Journaling\n- Nature exposure"
    ],
    'immune_health': [
        "Immune System Support:\n- Vitamin C rich foods\n- Adequate sleep\n- Regular exercise\n- Stress management\n- Hydration\n- Probiotic foods\n- Zinc-rich foods",
        "Immune-Boosting Foods:\n- Citrus fruits\n- Garlic\n- Ginger\n- Turmeric\n- Green tea\n- Yogurt\n- Leafy greens",
        "Lifestyle for Immunity:\n- Regular exercise\n- Adequate sleep\n- Stress management\n- Balanced diet\n- Hydration\n- Regular check-ups\n- Good hygiene"
    ],
    'heart_health': [
        "Heart-Healthy Tips:\n- Regular exercise\n- Balanced diet\n- Stress management\n- Adequate sleep\n- Regular check-ups\n- No smoking\n- Limited alcohol",
        "Heart-Healthy Foods:\n- Fatty fish\n- Leafy greens\n- Berries\n- Nuts\n- Olive oil\n- Whole grains\n- Dark chocolate",
        "Cardiovascular Care:\n- 150 minutes weekly exercise\n- Blood pressure monitoring\n- Cholesterol management\n- Stress reduction\n- Healthy diet\n- Regular check-ups\n- Weight management"
    ],
    'digestive_health': [
        "Digestive Wellness:\n- Fiber-rich diet\n- Probiotic foods\n- Regular exercise\n- Adequate water\n- Stress management\n- Regular meals\n- Good hygiene",
        "Gut-Healthy Foods:\n- Yogurt\n- Fermented foods\n- Fiber-rich foods\n- Ginger\n- Peppermint\n- Bone broth\n- Leafy greens",
        "Digestive Tips:\n- Regular meal times\n- Chew food well\n- Stay hydrated\n- Manage stress\n- Regular exercise\n- Fiber intake\n- Probiotic support"
    ],
    'bone_health': [
        "Bone Health Tips:\n- Calcium-rich foods\n- Vitamin D\n- Regular exercise\n- Weight-bearing activities\n- Limited alcohol\n- No smoking\n- Regular check-ups",
        "Bone-Healthy Foods:\n- Dairy products\n- Leafy greens\n- Fatty fish\n- Nuts and seeds\n- Fortified foods\n- Eggs\n- Tofu",
        "Bone Care Routine:\n- Weight-bearing exercise\n- Calcium supplementation\n- Vitamin D intake\n- Regular check-ups\n- Fall prevention\n- Good posture\n- Healthy lifestyle"
    ],
    'eye_health': [
        "Eye Health Tips:\n- Regular check-ups\n- UV protection\n- Screen breaks\n- Healthy diet\n- Adequate sleep\n- Regular exercise\n- Eye hygiene",
        "Eye-Healthy Foods:\n- Leafy greens\n- Carrots\n- Fatty fish\n- Eggs\n- Citrus fruits\n- Nuts\n- Berries",
        "Digital Eye Care:\n- 20-20-20 rule\n- Proper lighting\n- Screen distance\n- Regular breaks\n- Blue light protection\n- Eye exercises\n- Adequate rest"
    ],
    'skin_health': [
        "Skin Care Tips:\n- Sun protection\n- Regular cleansing\n- Moisturizing\n- Healthy diet\n- Adequate sleep\n- Stress management\n- Regular check-ups",
        "Skin-Healthy Foods:\n- Fatty fish\n- Avocados\n- Nuts\n- Berries\n- Green tea\n- Tomatoes\n- Sweet potatoes",
        "Skin Care Routine:\n- Daily cleansing\n- Moisturizing\n- Sun protection\n- Regular exfoliation\n- Healthy diet\n- Adequate sleep\n- Stress management"
    ],
    'dental_health': [
        "Dental Care Tips:\n- Regular brushing\n- Daily flossing\n- Regular check-ups\n- Healthy diet\n- Limited sugar\n- No smoking\n- Proper technique",
        "Dental-Healthy Foods:\n- Dairy products\n- Leafy greens\n- Nuts\n- Apples\n- Carrots\n- Celery\n- Green tea",
        "Oral Hygiene Routine:\n- Brush twice daily\n- Daily flossing\n- Regular check-ups\n- Healthy diet\n- Limited sugar\n- Good technique\n- Regular cleaning"
    ],
    'hair_health': [
        "Hair Care Tips:\n- Regular washing\n- Proper conditioning\n- Healthy diet\n- Stress management\n- Regular trims\n- Protection from damage\n- Scalp care",
        "Hair-Healthy Foods:\n- Eggs\n- Fatty fish\n- Nuts\n- Leafy greens\n- Sweet potatoes\n- Berries\n- Avocados",
        "Hair Care Routine:\n- Regular washing\n- Conditioning\n- Protection\n- Regular trims\n- Scalp massage\n- Healthy diet\n- Stress management"
    ],
    'joint_health': [
        "Joint Health Tips:\n- Regular exercise\n- Weight management\n- Healthy diet\n- Proper posture\n- Regular movement\n- Stress management\n- Regular check-ups",
        "Joint-Healthy Foods:\n- Fatty fish\n- Leafy greens\n- Nuts\n- Berries\n- Olive oil\n- Turmeric\n- Ginger",
        "Joint Care Routine:\n- Regular exercise\n- Stretching\n- Weight management\n- Healthy diet\n- Proper posture\n- Regular movement\n- Stress management"
    ],
    'energy_levels': [
        "Energy Boost Tips:\n- Regular exercise\n- Balanced diet\n- Adequate sleep\n- Stress management\n- Regular breaks\n- Hydration\n- Regular check-ups",
        "Energy-Boosting Foods:\n- Complex carbs\n- Lean protein\n- Nuts\n- Fruits\n- Leafy greens\n- Whole grains\n- Green tea",
        "Energy Management:\n- Regular exercise\n- Balanced diet\n- Adequate sleep\n- Stress management\n- Regular breaks\n- Hydration\n- Regular check-ups"
    ],
    'hormonal_health': [
        "Hormonal Balance Tips:\n- Regular exercise\n- Balanced diet\n- Stress management\n- Adequate sleep\n- Regular check-ups\n- Healthy lifestyle\n- Professional support",
        "Hormone-Healthy Foods:\n- Fatty fish\n- Leafy greens\n- Nuts\n- Seeds\n- Avocados\n- Berries\n- Whole grains",
        "Hormonal Care:\n- Regular exercise\n- Balanced diet\n- Stress management\n- Adequate sleep\n- Regular check-ups\n- Healthy lifestyle\n- Professional support"
    ],
    'respiratory_health': [
        "Respiratory Health Tips:\n- Regular exercise\n- Clean air\n- No smoking\n- Stress management\n- Regular check-ups\n- Good hygiene\n- Healthy lifestyle",
        "Lung-Healthy Foods:\n- Apples\n- Berries\n- Leafy greens\n- Fatty fish\n- Nuts\n- Green tea\n- Garlic",
        "Breathing Care:\n- Regular exercise\n- Clean air\n- No smoking\n- Stress management\n- Regular check-ups\n- Good hygiene\n- Healthy lifestyle"
    ],
    'metabolic_health': [
        "Metabolic Health Tips:\n- Regular exercise\n- Balanced diet\n- Weight management\n- Stress management\n- Regular check-ups\n- Healthy lifestyle\n- Professional support",
        "Metabolism-Boosting Foods:\n- Lean protein\n- Whole grains\n- Leafy greens\n- Spicy foods\n- Green tea\n- Nuts\n- Berries",
        "Metabolic Care:\n- Regular exercise\n- Balanced diet\n- Weight management\n- Stress management\n- Regular check-ups\n- Healthy lifestyle\n- Professional support"
    ],
    'default': [
        "A balanced diet should include a variety of whole foods, lean proteins, healthy fats, and complex carbohydrates.",
        "Remember to stay hydrated by drinking 8-10 glasses of water daily. This supports all bodily functions.",
        "Consider consulting with a registered dietitian for personalized nutrition advice based on your specific needs."
    ]
}

def get_response_category(text):
    text_lower = text.lower()
    
    if any(word in text_lower for word in ['breakfast', 'morning meal', 'early meal']):
        return 'breakfast'
    elif any(word in text_lower for word in ['lunch', 'dinner', 'supper', 'meal plan']):
        return 'lunch_dinner'
    elif any(word in text_lower for word in ['snack', 'small meal', 'quick eat']):
        return 'snacks'
    elif any(word in text_lower for word in ['protein', 'meat', 'fish', 'eggs', 'tofu']):
        return 'protein'
    elif any(word in text_lower for word in ['vegetable', 'veggies', 'greens']):
        return 'vegetables'
    elif any(word in text_lower for word in ['fruit', 'berry', 'berries']):
        return 'fruits'
    elif any(word in text_lower for word in ['weight', 'diet', 'fat', 'slim', 'loss']):
        return 'weight_management'
    elif any(word in text_lower for word in ['recipe', 'cook', 'bake', 'dish', 'meal']):
        return 'recipes'
    elif any(word in text_lower for word in ['exercise', 'workout', 'gym', 'train', 'fitness']):
        return 'exercises'
    elif any(word in text_lower for word in ['plan', 'prep', 'shopping', 'grocery']):
        return 'meal_planning'
    elif any(word in text_lower for word in ['supplement', 'vitamin', 'mineral', 'pill']):
        return 'supplements'
    elif any(word in text_lower for word in ['general health', 'wellness', 'lifestyle']):
        return 'general_health'
    elif any(word in text_lower for word in ['mental', 'mind', 'brain', 'anxiety', 'depression']):
        return 'mental_health'
    elif any(word in text_lower for word in ['sleep', 'insomnia', 'rest']):
        return 'sleep_health'
    elif any(word in text_lower for word in ['stress', 'anxiety', 'pressure']):
        return 'stress_management'
    elif any(word in text_lower for word in ['immune', 'immunity', 'sick', 'cold']):
        return 'immune_health'
    elif any(word in text_lower for word in ['heart', 'cardio', 'blood pressure']):
        return 'heart_health'
    elif any(word in text_lower for word in ['digest', 'gut', 'stomach']):
        return 'digestive_health'
    elif any(word in text_lower for word in ['bone', 'skeleton', 'calcium']):
        return 'bone_health'
    elif any(word in text_lower for word in ['eye', 'vision', 'sight']):
        return 'eye_health'
    elif any(word in text_lower for word in ['skin', 'face', 'complexion']):
        return 'skin_health'
    elif any(word in text_lower for word in ['dental', 'teeth', 'mouth']):
        return 'dental_health'
    elif any(word in text_lower for word in ['hair', 'scalp']):
        return 'hair_health'
    elif any(word in text_lower for word in ['joint', 'arthritis', 'pain']):
        return 'joint_health'
    elif any(word in text_lower for word in ['energy', 'tired', 'fatigue']):
        return 'energy_levels'
    elif any(word in text_lower for word in ['hormone', 'hormonal', 'endocrine']):
        return 'hormonal_health'
    elif any(word in text_lower for word in ['respiratory', 'breathing', 'lung']):
        return 'respiratory_health'
    elif any(word in text_lower for word in ['metabolic', 'metabolism']):
        return 'metabolic_health'
    
    return 'default'

def is_nutrition_related(text):
    nutrition_keywords = {
        'food', 'diet', 'nutrition', 'eat', 'meal', 'protein', 'carbs', 'fat',
        'vitamin', 'mineral', 'calorie', 'weight', 'healthy', 'recipe', 'vegetable',
        'fruit', 'meat', 'fish', 'dairy', 'grain', 'portion', 'breakfast', 'lunch',
        'dinner', 'snack', 'nutrient', 'supplement', 'exercise', 'workout', 'fitness',
        'plan', 'prep', 'shopping', 'grocery', 'cook', 'bake', 'dish', 'health',
        'wellness', 'lifestyle', 'mental', 'mind', 'brain', 'sleep', 'stress',
        'immune', 'heart', 'digest', 'bone', 'eye', 'skin', 'dental', 'hair',
        'joint', 'energy', 'hormone', 'respiratory', 'metabolic', 'anxiety',
        'depression', 'insomnia', 'pressure', 'sick', 'cold', 'cardio',
        'blood pressure', 'gut', 'stomach', 'skeleton', 'calcium', 'vision',
        'sight', 'face', 'complexion', 'teeth', 'mouth', 'scalp', 'arthritis',
        'pain', 'tired', 'fatigue', 'endocrine', 'breathing', 'lung'
    }
    text_lower = text.lower()
    return any(keyword in text_lower for keyword in nutrition_keywords)

def get_nutrition_response(user_message):
    try:
        if not is_nutrition_related(user_message):
            return "I am a nutrition and fitness specialist. Please ask me about diet, nutrition, healthy eating, meal planning, recipes, exercises, or specific foods."
        
        category = get_response_category(user_message)
        if category not in NUTRITION_RESPONSES:
            return random.choice(NUTRITION_RESPONSES['default'])
            
        return random.choice(NUTRITION_RESPONSES[category])
    except Exception as e:
        print(f"Error in get_nutrition_response: {str(e)}")
        return random.choice(NUTRITION_RESPONSES['default'])

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/static/<path:path>')
def serve_static(path):
    return send_from_directory('static', path)

@app.route('/chat', methods=['POST'])
def chat():
    try:
        data = request.get_json()
        if not data or 'message' not in data:
            return jsonify({'error': 'No message provided'}), 400
        
        user_message = data['message']
        if not user_message.strip():
            return jsonify({'error': 'Empty message'}), 400
            
        response = get_nutrition_response(user_message)
        return jsonify({'response': response})
    except Exception as e:
        print(f"Error in chat route: {str(e)}")
        return jsonify({'error': 'Internal server error'}), 500

def load_recipes():
    try:
        default_recipes = [
            {
                'id': '1',
                'title': 'Healthy Breakfast Bowl',
                'image': 'https://images.unsplash.com/photo-1490645935967-10de6ba17061',
                'time': 15,
                'calories': 350,
                'tags': ['breakfast', 'vegetarian', 'quick'],
                'ingredients': [
                    '1 cup rolled oats',
                    '1 banana, sliced',
                    '1 tbsp chia seeds',
                    '1 tbsp honey',
                    '1 cup almond milk',
                    '1/4 cup mixed berries',
                    '1 tbsp almond butter'
                ],
                'instructions': [
                    'In a saucepan, combine oats and almond milk',
                    'Bring to a boil, then simmer for 5 minutes',
                    'Stir in chia seeds and honey',
                    'Pour into a bowl',
                    'Top with banana slices, berries, and almond butter',
                    'Serve warm'
                ],
                'nutrition': {
                    'Calories': '350',
                    'Protein': '12g',
                    'Carbs': '45g',
                    'Fat': '15g',
                    'Fiber': '8g'
                }
            },
            {
                'id': '2',
                'title': 'Mediterranean Quinoa Salad',
                'image': 'https://images.unsplash.com/photo-1512621776951-a57141f2eefd',
                'time': 25,
                'calories': 420,
                'tags': ['lunch', 'vegetarian', 'healthy'],
                'ingredients': [
                    '1 cup quinoa',
                    '1 cucumber, diced',
                    '1 cup cherry tomatoes',
                    '1/2 cup olives',
                    '1/4 cup feta cheese',
                    '2 tbsp olive oil',
                    '1 lemon, juiced',
                    'Fresh herbs (parsley, mint)'
                ],
                'instructions': [
                    'Cook quinoa according to package instructions',
                    'Let quinoa cool to room temperature',
                    'Mix in diced cucumber and cherry tomatoes',
                    'Add olives and crumbled feta cheese',
                    'Dress with olive oil and lemon juice',
                    'Garnish with fresh herbs',
                    'Season with salt and pepper'
                ],
                'nutrition': {
                    'Calories': '420',
                    'Protein': '15g',
                    'Carbs': '52g',
                    'Fat': '18g',
                    'Fiber': '10g'
                }
            },
            {
                'id': '3',
                'title': 'Grilled Chicken Stir-Fry',
                'image': 'https://images.unsplash.com/photo-1512058564366-18510be2db19',
                'time': 30,
                'calories': 450,
                'tags': ['dinner', 'protein', 'healthy'],
                'ingredients': [
                    '2 chicken breasts, sliced',
                    '2 cups mixed vegetables',
                    '2 tbsp soy sauce',
                    '1 tbsp ginger, minced',
                    '2 cloves garlic, minced',
                    '1 tbsp sesame oil',
                    '1/4 cup cashews'
                ],
                'instructions': [
                    'Slice chicken into thin strips',
                    'Heat sesame oil in a wok or large pan',
                    'Add chicken and cook until golden',
                    'Add ginger and garlic, stir-fry for 1 minute',
                    'Add vegetables and stir-fry for 3-4 minutes',
                    'Add soy sauce and cashews',
                    'Cook until vegetables are tender-crisp'
                ],
                'nutrition': {
                    'Calories': '450',
                    'Protein': '35g',
                    'Carbs': '25g',
                    'Fat': '22g',
                    'Fiber': '8g'
                }
            },
            {
                'id': '4',
                'title': 'Veggie Buddha Bowl',
                'image': 'https://images.unsplash.com/photo-1512621776951-a57141f2eefd',
                'time': 35,
                'calories': 480,
                'tags': ['lunch', 'vegetarian', 'healthy'],
                'ingredients': [
                    '1 cup quinoa',
                    '1 sweet potato, cubed',
                    '1 cup chickpeas',
                    '2 cups mixed greens',
                    '1 avocado',
                    '2 tbsp tahini dressing',
                    'Mixed seeds'
                ],
                'instructions': [
                    'Cook quinoa according to package instructions',
                    'Roast sweet potato cubes at 400°F for 20 minutes',
                    'Drain and rinse chickpeas',
                    'Assemble bowl with quinoa base',
                    'Add roasted sweet potato and chickpeas',
                    'Top with mixed greens and sliced avocado',
                    'Drizzle with tahini dressing and sprinkle seeds'
                ],
                'nutrition': {
                    'Calories': '480',
                    'Protein': '18g',
                    'Carbs': '65g',
                    'Fat': '22g',
                    'Fiber': '15g'
                }
            },
            {
                'id': '5',
                'title': 'Protein Power Smoothie Bowl',
                'image': 'https://images.unsplash.com/photo-1490474418585-ba9bad8fd0ea',
                'time': 10,
                'calories': 380,
                'tags': ['breakfast', 'protein', 'quick'],
                'ingredients': [
                    '1 banana',
                    '1 cup spinach',
                    '1 scoop protein powder',
                    '1 cup almond milk',
                    '1 tbsp chia seeds',
                    '1/4 cup granola',
                    '1/4 cup mixed berries'
                ],
                'instructions': [
                    'Blend banana, spinach, protein powder, and almond milk',
                    'Pour into a bowl',
                    'Top with chia seeds, granola, and berries',
                    'Serve immediately'
                ],
                'nutrition': {
                    'Calories': '380',
                    'Protein': '28g',
                    'Carbs': '42g',
                    'Fat': '12g',
                    'Fiber': '8g'
                }
            },
            {
                'id': '6',
                'title': 'Spicy Thai Curry',
                'image': 'https://images.unsplash.com/photo-1559314809-0d155014e29e',
                'time': 40,
                'calories': 450,
                'tags': ['dinner', 'thai', 'spicy'],
                'ingredients': [
                    '1 can coconut milk',
                    '2 tbsp red curry paste',
                    '1 cup vegetables',
                    '1 cup tofu',
                    '1 cup rice',
                    'Thai basil',
                    'Lime juice'
                ],
                'instructions': [
                    'Cook rice according to package instructions',
                    'Sauté curry paste in oil',
                    'Add coconut milk and vegetables',
                    'Simmer until vegetables are tender',
                    'Add tofu and Thai basil',
                    'Serve with rice and lime juice'
                ],
                'nutrition': {
                    'Calories': '450',
                    'Protein': '18g',
                    'Carbs': '52g',
                    'Fat': '22g',
                    'Fiber': '8g'
                }
            },
            {
                'id': '7',
                'title': 'Mediterranean Pasta',
                'image': 'https://images.unsplash.com/photo-1473093226795-af9932fe5856',
                'time': 25,
                'calories': 420,
                'tags': ['dinner', 'pasta', 'mediterranean'],
                'ingredients': [
                    '8 oz whole grain pasta',
                    '1 cup cherry tomatoes',
                    '2 cups spinach',
                    '2 cloves garlic',
                    '2 tbsp olive oil',
                    '1/4 cup parmesan',
                    'Fresh basil'
                ],
                'instructions': [
                    'Cook pasta according to package instructions',
                    'Sauté garlic in olive oil',
                    'Add cherry tomatoes and cook until soft',
                    'Add spinach and cook until wilted',
                    'Toss with pasta',
                    'Top with parmesan and basil'
                ],
                'nutrition': {
                    'Calories': '420',
                    'Protein': '14g',
                    'Carbs': '52g',
                    'Fat': '16g',
                    'Fiber': '8g'
                }
            },
            {
                'id': '8',
                'title': 'Green Power Bowl',
                'image': 'https://images.unsplash.com/photo-1512621776951-a57141f2eefd',
                'time': 30,
                'calories': 380,
                'tags': ['lunch', 'vegetarian', 'healthy'],
                'ingredients': [
                    '1 cup quinoa',
                    '2 cups mixed greens',
                    '1 avocado',
                    '1 cup edamame',
                    '2 tbsp tahini dressing',
                    'Mixed seeds',
                    'Lemon juice'
                ],
                'instructions': [
                    'Cook quinoa according to package instructions',
                    'Steam edamame',
                    'Assemble bowl with quinoa base',
                    'Add mixed greens and edamame',
                    'Top with sliced avocado',
                    'Drizzle with tahini dressing and lemon juice',
                    'Sprinkle with seeds'
                ],
                'nutrition': {
                    'Calories': '380',
                    'Protein': '16g',
                    'Carbs': '45g',
                    'Fat': '18g',
                    'Fiber': '12g'
                }
            },
            {
                'id': '9',
                'title': 'Berry Protein Pancakes',
                'image': 'https://images.unsplash.com/photo-1567620905732-2d1ec7ab7445',
                'time': 20,
                'calories': 320,
                'tags': ['breakfast', 'protein', 'quick'],
                'ingredients': [
                    '1 cup protein pancake mix',
                    '1 egg',
                    '1 cup almond milk',
                    '1 cup mixed berries',
                    '1 tbsp maple syrup',
                    '1 tbsp butter',
                    'Vanilla extract'
                ],
                'instructions': [
                    'Mix pancake mix, egg, and almond milk',
                    'Add vanilla extract',
                    'Cook pancakes on griddle',
                    'Top with berries and maple syrup',
                    'Serve with butter'
                ],
                'nutrition': {
                    'Calories': '320',
                    'Protein': '24g',
                    'Carbs': '35g',
                    'Fat': '12g',
                    'Fiber': '6g'
                }
            },
            {
                'id': '10',
                'title': 'Mexican Quinoa Bowl',
                'image': 'https://images.unsplash.com/photo-1512058564366-18510be2db19',
                'time': 35,
                'calories': 450,
                'tags': ['lunch', 'mexican', 'vegetarian'],
                'ingredients': [
                    '1 cup quinoa',
                    '1 can black beans',
                    '1 cup corn',
                    '1 avocado',
                    '1 cup salsa',
                    '2 tbsp lime juice',
                    'Cilantro'
                ],
                'instructions': [
                    'Cook quinoa according to package instructions',
                    'Drain and rinse black beans',
                    'Mix quinoa with beans and corn',
                    'Top with sliced avocado',
                    'Add salsa and lime juice',
                    'Garnish with cilantro'
                ],
                'nutrition': {
                    'Calories': '450',
                    'Protein': '18g',
                    'Carbs': '65g',
                    'Fat': '16g',
                    'Fiber': '15g'
                }
            },
            {
                'id': '11',
                'title': 'Salmon Power Bowl',
                'image': 'https://images.unsplash.com/photo-1512058564366-18510be2db19',
                'time': 30,
                'calories': 520,
                'tags': ['dinner', 'protein', 'healthy'],
                'ingredients': [
                    '6 oz salmon fillet',
                    '1 cup quinoa',
                    '2 cups mixed vegetables',
                    '1 avocado',
                    '2 tbsp olive oil',
                    'Lemon juice',
                    'Fresh herbs'
                ],
                'instructions': [
                    'Cook quinoa according to package instructions',
                    'Season salmon with herbs',
                    'Bake salmon at 400°F for 15 minutes',
                    'Steam mixed vegetables',
                    'Assemble bowl with quinoa base',
                    'Add salmon and vegetables',
                    'Top with avocado and lemon juice'
                ],
                'nutrition': {
                    'Calories': '520',
                    'Protein': '38g',
                    'Carbs': '45g',
                    'Fat': '22g',
                    'Fiber': '10g'
                }
            },
            {
                'id': '12',
                'title': 'Vegan Buddha Bowl',
                'image': 'https://images.unsplash.com/photo-1512621776951-a57141f2eefd',
                'time': 40,
                'calories': 480,
                'tags': ['lunch', 'vegan', 'healthy'],
                'ingredients': [
                    '1 cup quinoa',
                    '1 sweet potato',
                    '1 cup chickpeas',
                    '2 cups kale',
                    '1 avocado',
                    '2 tbsp tahini dressing',
                    'Mixed seeds'
                ],
                'instructions': [
                    'Cook quinoa according to package instructions',
                    'Roast sweet potato cubes',
                    'Drain and rinse chickpeas',
                    'Massage kale with olive oil',
                    'Assemble bowl with quinoa base',
                    'Add roasted sweet potato and chickpeas',
                    'Top with kale and avocado'
                ],
                'nutrition': {
                    'Calories': '480',
                    'Protein': '16g',
                    'Carbs': '68g',
                    'Fat': '20g',
                    'Fiber': '14g'
                }
            },
            {
                'id': '13',
                'title': 'Greek Yogurt Parfait',
                'image': 'https://images.unsplash.com/photo-1490474418585-ba9bad8fd0ea',
                'time': 10,
                'calories': 280,
                'tags': ['breakfast', 'protein', 'quick'],
                'ingredients': [
                    '1 cup Greek yogurt',
                    '1/4 cup granola',
                    '1/4 cup mixed berries',
                    '1 tbsp honey',
                    '1 tbsp chia seeds',
                    'Vanilla extract',
                    'Cinnamon'
                ],
                'instructions': [
                    'Layer Greek yogurt in a glass',
                    'Add granola layer',
                    'Add berries layer',
                    'Repeat layers',
                    'Top with honey and chia seeds',
                    'Sprinkle with cinnamon'
                ],
                'nutrition': {
                    'Calories': '280',
                    'Protein': '20g',
                    'Carbs': '32g',
                    'Fat': '8g',
                    'Fiber': '6g'
                }
            },
            {
                'id': '14',
                'title': 'Tofu Stir-Fry',
                'image': 'https://images.unsplash.com/photo-1512058564366-18510be2db19',
                'time': 25,
                'calories': 380,
                'tags': ['dinner', 'vegetarian', 'asian'],
                'ingredients': [
                    '1 block firm tofu',
                    '2 cups mixed vegetables',
                    '2 tbsp soy sauce',
                    '1 tbsp ginger',
                    '2 cloves garlic',
                    '1 tbsp sesame oil',
                    'Brown rice'
                ],
                'instructions': [
                    'Press and cube tofu',
                    'Cook rice according to package instructions',
                    'Heat sesame oil in wok',
                    'Add ginger and garlic',
                    'Add tofu and vegetables',
                    'Stir-fry until vegetables are tender',
                    'Add soy sauce and serve with rice'
                ],
                'nutrition': {
                    'Calories': '380',
                    'Protein': '22g',
                    'Carbs': '42g',
                    'Fat': '16g',
                    'Fiber': '8g'
                }
            },
            {
                'id': '15',
                'title': 'Mediterranean Wrap',
                'image': 'https://images.unsplash.com/photo-1512058564366-18510be2db19',
                'time': 20,
                'calories': 420,
                'tags': ['lunch', 'mediterranean', 'quick'],
                'ingredients': [
                    '1 whole grain wrap',
                    '1 cup hummus',
                    '1 cup mixed vegetables',
                    '1/4 cup feta cheese',
                    '2 tbsp olive oil',
                    'Mixed herbs',
                    'Lemon juice'
                ],
                'instructions': [
                    'Spread hummus on wrap',
                    'Add mixed vegetables',
                    'Sprinkle feta cheese',
                    'Drizzle with olive oil',
                    'Add herbs and lemon juice',
                    'Roll wrap tightly',
                    'Cut in half and serve'
                ],
                'nutrition': {
                    'Calories': '420',
                    'Protein': '16g',
                    'Carbs': '48g',
                    'Fat': '22g',
                    'Fiber': '10g'
                }
            },
            {
                'id': '16',
                'title': 'Protein Power Bowl',
                'image': 'https://images.unsplash.com/photo-1512621776951-a57141f2eefd',
                'time': 30,
                'calories': 550,
                'tags': ['dinner', 'protein', 'healthy'],
                'ingredients': [
                    '1 cup quinoa',
                    '6 oz grilled chicken',
                    '1 cup black beans',
                    '1 avocado',
                    '1 cup mixed vegetables',
                    '2 tbsp olive oil',
                    'Lime juice'
                ],
                'instructions': [
                    'Cook quinoa according to package instructions',
                    'Grill chicken until cooked through',
                    'Heat black beans in saucepan',
                    'Assemble bowl with quinoa base',
                    'Add grilled chicken and black beans',
                    'Top with mixed vegetables and avocado',
                    'Drizzle with olive oil and lime juice'
                ],
                'nutrition': {
                    'Calories': '550',
                    'Protein': '42g',
                    'Carbs': '45g',
                    'Fat': '22g',
                    'Fiber': '12g'
                }
            },
            {
                'id': '17',
                'title': 'Berry Protein Smoothie',
                'image': 'https://images.unsplash.com/photo-1502741224143-90386d7f8c82',
                'time': 10,
                'calories': 320,
                'tags': ['breakfast', 'protein', 'quick'],
                'ingredients': [
                    '1 cup mixed berries',
                    '1 banana',
                    '1 scoop protein powder',
                    '1 cup almond milk',
                    '1 tbsp chia seeds',
                    '1 tbsp honey',
                    'Ice'
                ],
                'instructions': [
                    'Blend berries, banana, and protein powder',
                    'Add almond milk and ice',
                    'Blend until smooth',
                    'Add chia seeds and honey',
                    'Blend briefly',
                    'Pour into glass',
                    'Serve immediately'
                ],
                'nutrition': {
                    'Calories': '320',
                    'Protein': '24g',
                    'Carbs': '38g',
                    'Fat': '8g',
                    'Fiber': '8g'
                }
            },
            {
                'id': '18',
                'title': 'Veggie Pasta Bowl',
                'image': 'https://images.unsplash.com/photo-1473093226795-af9932fe5856',
                'time': 25,
                'calories': 420,
                'tags': ['dinner', 'vegetarian', 'pasta'],
                'ingredients': [
                    '8 oz whole grain pasta',
                    '2 cups mixed vegetables',
                    '2 cloves garlic',
                    '2 tbsp olive oil',
                    '1/4 cup parmesan',
                    'Fresh basil',
                    'Red pepper flakes'
                ],
                'instructions': [
                    'Cook pasta according to package instructions',
                    'Sauté garlic in olive oil',
                    'Add mixed vegetables',
                    'Cook until vegetables are tender',
                    'Toss with pasta',
                    'Top with parmesan and basil',
                    'Add red pepper flakes to taste'
                ],
                'nutrition': {
                    'Calories': '420',
                    'Protein': '14g',
                    'Carbs': '52g',
                    'Fat': '16g',
                    'Fiber': '8g'
                }
            },
            {
                'id': '19',
                'title': 'Tuna Power Bowl',
                'image': 'https://images.unsplash.com/photo-1512058564366-18510be2db19',
                'time': 20,
                'calories': 450,
                'tags': ['lunch', 'protein', 'healthy'],
                'ingredients': [
                    '1 can tuna',
                    '1 cup quinoa',
                    '2 cups mixed vegetables',
                    '1 avocado',
                    '2 tbsp olive oil',
                    'Lemon juice',
                    'Mixed herbs'
                ],
                'instructions': [
                    'Cook quinoa according to package instructions',
                    'Drain tuna',
                    'Steam mixed vegetables',
                    'Assemble bowl with quinoa base',
                    'Add tuna and vegetables',
                    'Top with sliced avocado',
                    'Drizzle with olive oil and lemon juice'
                ],
                'nutrition': {
                    'Calories': '450',
                    'Protein': '32g',
                    'Carbs': '42g',
                    'Fat': '18g',
                    'Fiber': '8g'
                }
            },
            {
                'id': '20',
                'title': 'Chocolate Protein Overnight Oats',
                'image': 'https://images.unsplash.com/photo-1490645935967-10de6ba17061',
                'time': 5,
                'calories': 380,
                'tags': ['breakfast', 'protein', 'quick'],
                'ingredients': [
                    '1 cup rolled oats',
                    '1 scoop chocolate protein powder',
                    '1 cup almond milk',
                    '1 tbsp chia seeds',
                    '1 tbsp cocoa powder',
                    '1 tbsp honey',
                    '1/4 cup mixed berries'
                ],
                'instructions': [
                    'Mix oats, protein powder, and cocoa powder',
                    'Add almond milk and chia seeds',
                    'Stir in honey',
                    'Refrigerate overnight',
                    'Top with mixed berries',
                    'Serve cold'
                ],
                'nutrition': {
                    'Calories': '380',
                    'Protein': '24g',
                    'Carbs': '48g',
                    'Fat': '12g',
                    'Fiber': '10g'
                }
            },
            {
                'id': '21',
                'title': 'Shrimp Scampi Pasta',
                'image': 'https://images.unsplash.com/photo-1473093226795-af9932fe5856',
                'time': 30,
                'calories': 480,
                'tags': ['dinner', 'seafood', 'pasta'],
                'ingredients': [
                    '8 oz whole grain pasta',
                    '1 lb shrimp',
                    '4 cloves garlic',
                    '2 tbsp olive oil',
                    '1/4 cup white wine',
                    'Fresh parsley',
                    'Red pepper flakes'
                ],
                'instructions': [
                    'Cook pasta according to package instructions',
                    'Sauté garlic in olive oil',
                    'Add shrimp and cook until pink',
                    'Add white wine and reduce',
                    'Toss with pasta',
                    'Garnish with parsley',
                    'Add red pepper flakes to taste'
                ],
                'nutrition': {
                    'Calories': '480',
                    'Protein': '36g',
                    'Carbs': '42g',
                    'Fat': '16g',
                    'Fiber': '6g'
                }
            },
            {
                'id': '22',
                'title': 'Veggie Power Bowl',
                'image': 'https://images.unsplash.com/photo-1512621776951-a57141f2eefd',
                'time': 35,
                'calories': 420,
                'tags': ['lunch', 'vegetarian', 'healthy'],
                'ingredients': [
                    '1 cup quinoa',
                    '2 cups mixed vegetables',
                    '1 cup chickpeas',
                    '1 avocado',
                    '2 tbsp tahini dressing',
                    'Mixed seeds',
                    'Lemon juice'
                ],
                'instructions': [
                    'Cook quinoa according to package instructions',
                    'Roast mixed vegetables',
                    'Drain and rinse chickpeas',
                    'Assemble bowl with quinoa base',
                    'Add roasted vegetables and chickpeas',
                    'Top with sliced avocado',
                    'Drizzle with tahini dressing'
                ],
                'nutrition': {
                    'Calories': '420',
                    'Protein': '16g',
                    'Carbs': '58g',
                    'Fat': '18g',
                    'Fiber': '12g'
                }
            },
            {
                'id': '23',
                'title': 'Breakfast Burrito',
                'image': 'https://images.unsplash.com/photo-1512058564366-18510be2db19',
                'time': 25,
                'calories': 450,
                'tags': ['breakfast', 'protein', 'mexican'],
                'ingredients': [
                    '1 whole grain tortilla',
                    '3 eggs',
                    '1 cup black beans',
                    '1/4 cup cheese',
                    '1 avocado',
                    'Salsa',
                    'Cilantro'
                ],
                'instructions': [
                    'Scramble eggs',
                    'Heat black beans',
                    'Warm tortilla',
                    'Layer eggs and beans',
                    'Add cheese and avocado',
                    'Top with salsa',
                    'Roll and serve'
                ],
                'nutrition': {
                    'Calories': '450',
                    'Protein': '24g',
                    'Carbs': '42g',
                    'Fat': '22g',
                    'Fiber': '10g'
                }
            },
            {
                'id': '24',
                'title': 'Mediterranean Salmon',
                'image': 'https://images.unsplash.com/photo-1512058564366-18510be2db19',
                'time': 30,
                'calories': 480,
                'tags': ['dinner', 'seafood', 'mediterranean'],
                'ingredients': [
                    '6 oz salmon fillet',
                    '2 cups mixed vegetables',
                    '2 tbsp olive oil',
                    'Lemon juice',
                    'Fresh herbs',
                    'Garlic',
                    'Brown rice'
                ],
                'instructions': [
                    'Cook rice according to package instructions',
                    'Season salmon with herbs and garlic',
                    'Bake salmon at 400°F for 15 minutes',
                    'Roast mixed vegetables',
                    'Serve salmon with vegetables',
                    'Drizzle with olive oil and lemon juice'
                ],
                'nutrition': {
                    'Calories': '480',
                    'Protein': '36g',
                    'Carbs': '38g',
                    'Fat': '22g',
                    'Fiber': '8g'
                }
            }
        ]

        if not os.path.exists('recipes.json'):
            save_recipes(default_recipes)
            return default_recipes
            
        with open('recipes.json', 'r', encoding='utf-8') as f:
            recipes = json.load(f)
            if not recipes:
                save_recipes(default_recipes)
                return default_recipes
            return recipes
    except FileNotFoundError:
        save_recipes(default_recipes)
        return default_recipes
    except json.JSONDecodeError:
        print("Error: Invalid JSON in recipes.json")
        save_recipes(default_recipes)
        return default_recipes
    except Exception as e:
        print(f"Error loading recipes: {str(e)}")
        return default_recipes

def save_recipes(recipes):
    try:
        with open('recipes.json', 'w', encoding='utf-8') as f:
            json.dump(recipes, f, indent=4, ensure_ascii=False)
    except Exception as e:
        print(f"Error saving recipes: {str(e)}")

@app.route('/recipes')
def get_recipes():
    try:
        recipes = load_recipes()
        return jsonify(recipes)
    except Exception as e:
        print(f"Error in get_recipes route: {str(e)}")
        return jsonify({'error': 'Internal server error'}), 500

@app.route('/api/recipes', methods=['POST'])
def add_recipe():
    try:
        data = request.get_json()
        if not data:
            return jsonify({'error': 'No data provided'}), 400
            
        required_fields = ['title', 'image', 'time', 'calories', 'tags', 'ingredients', 'instructions', 'nutrition']
        if not all(field in data for field in required_fields):
            return jsonify({'error': 'Missing required fields'}), 400
            
        recipes = load_recipes()
        data['id'] = str(len(recipes) + 1)
        recipes.append(data)
        save_recipes(recipes)
        return jsonify({'message': 'Recipe added successfully', 'recipe': data})
    except Exception as e:
        print(f"Error in add_recipe route: {str(e)}")
        return jsonify({'error': 'Internal server error'}), 500

@app.route('/api/recipes/<int:recipe_id>', methods=['PUT'])
def update_recipe(recipe_id):
    try:
        data = request.get_json()
        if not data:
            return jsonify({'error': 'No data provided'}), 400
            
        recipes = load_recipes()
        if 0 <= recipe_id < len(recipes):
            data['id'] = str(recipe_id + 1)
            recipes[recipe_id] = data
            save_recipes(recipes)
            return jsonify({'message': 'Recipe updated successfully', 'recipe': data})
        return jsonify({'error': 'Recipe not found'}), 404
    except Exception as e:
        print(f"Error in update_recipe route: {str(e)}")
        return jsonify({'error': 'Internal server error'}), 500

@app.route('/api/recipes/<int:recipe_id>', methods=['DELETE'])
def delete_recipe(recipe_id):
    try:
        recipes = load_recipes()
        if 0 <= recipe_id < len(recipes):
            deleted_recipe = recipes.pop(recipe_id)
            save_recipes(recipes)
            return jsonify({'message': 'Recipe deleted successfully', 'recipe': deleted_recipe})
        return jsonify({'error': 'Recipe not found'}), 404
    except Exception as e:
        print(f"Error in delete_recipe route: {str(e)}")
        return jsonify({'error': 'Internal server error'}), 500

if __name__ == '__main__':
    app.run(debug=True) 