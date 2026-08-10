from __future__ import annotations

import copy
import random
from dataclasses import dataclass, field

from app.models.food import Food


# ============================================================
# Data Transfer Objects
# ============================================================

@dataclass
class FoodItem:
    id: int
    name: str
    category: str

    calories: float
    protein: float
    carbs: float
    fat: float

    suitable_meals: list[str] = field(default_factory=list)

    # role مستقیماً از دیتابیس می‌آید.
    # category هیچ دخالتی در تعیین role ندارد.
    role: str | None = None

    score_base: float = 1.0

    @classmethod
    def from_orm(cls, food: Food) -> "FoodItem":

        suitable_meals = []

        if food.suitable_meals:
            suitable_meals = [
                meal.strip()
                for meal in food.suitable_meals.split(",")
                if meal.strip()
            ]

        return cls(
            id=food.id,
            name=food.name_en,
            category=food.category,

            calories=food.calories,
            protein=food.protein,
            carbs=food.carbs,
            fat=food.fat,

            suitable_meals=suitable_meals,

            # فقط role واقعی دیتابیس
            role=food.role,

            score_base=food.score_base or 1.0,
        )


@dataclass
class MealTarget:
    calories: float
    protein: float
    carbs: float
    fat: float


@dataclass
class Gene:
    food: FoodItem
    quantity: float  # grams

    @property
    def calories(self) -> float:
        return self.food.calories * self.quantity / 100

    @property
    def protein(self) -> float:
        return self.food.protein * self.quantity / 100

    @property
    def carbs(self) -> float:
        return self.food.carbs * self.quantity / 100

    @property
    def fat(self) -> float:
        return self.food.fat * self.quantity / 100


# ============================================================
# Chromosome
# ============================================================

Chromosome = dict[str, list[Gene]]


# ============================================================
# Configuration
# ============================================================

MEAL_TYPES = [
    "breakfast",
    "morning_snack",
    "lunch",
    "afternoon_snack",
    "dinner",
]


# سهم کالری هر وعده از کل کالری روز
MEAL_CALORIE_RATIO = {
    "breakfast": 0.25,
    "morning_snack": 0.10,
    "lunch": 0.35,
    "afternoon_snack": 0.10,
    "dinner": 0.20,
}


# ============================================================
# Meal Role Rules
# ============================================================

# نکته مهم:
#
# category و role کاملاً جدا هستند.
#
# مثال:
#
# fast_food + main
# shirini + dessert
# drink + drink
#
# GA فقط role را برای قوانین وعده بررسی می‌کند.
#
# category فقط در Fitness برای جریمه fast_food استفاده می‌شود.

MEAL_ROLE_RULES = {

    "breakfast": {
        "required": ["easy_main"],
        "optional": [
            "main_side",
            "hot_drink",
        ],
        "max_optional": 2,
    },

    "morning_snack": {
        "required": ["snack"],
        "optional": [
            "dessert",
            "hot_drink",
            "cold_drink",
        ],
        "max_optional": 2,
    },

    "lunch": {
        "required": ["heavy_main"],
        "optional": [
            "side_side",
            "cold_drink",
            "dessert",
        ],
        "max_optional": 2,
    },

    "afternoon_snack": {
        "required": ["snack"],
        "optional": [
            "dessert",
            "hot_drink",
            "cold_drink",
        ],
        "max_optional": 2,
    },

    "dinner": {
        "required": ["heavy_main"],
        "optional": [
            "side_side",
            "cold_drink",
            "dessert",
        ],
        "max_optional": 2,
    },
}

# ============================================================
# Role Groups
# ============================================================

ROLE_GROUPS = {
    "drink": {
        "hot_drink",
        "cold_drink",
    },
}

def _role_group(role: str | None) -> str | None:

    if role is None:
        return None

    for group_name, roles in ROLE_GROUPS.items():

        if role in roles:
            return group_name

    return None

# ============================================================
# Fast Food Penalty
# ============================================================

# هرچه این مقدار بیشتر باشد،
# GA بیشتر از fast_food دوری می‌کند.
#
# مقدار 1.5 یک جریمه متوسط است.
# اگر هنوز KFC زیاد انتخاب شد می‌توانیم آن را به 2.0 یا 3.0 افزایش دهیم.

FAST_FOOD_PENALTY = 1.5


# ============================================================
# Quantity
# ============================================================

HEAVY_MAIN_QUANTITY_RANGE = (150, 300)

EASY_MAIN_QUANTITY_RANGE = (100, 250)

MAIN_SIDE_QUANTITY_RANGE = (30, 120)

SIDE_SIDE_QUANTITY_RANGE = (30, 100)

HOT_DRINK_QUANTITY_RANGE = (100, 300)

COLD_DRINK_QUANTITY_RANGE = (100, 300)

SNACK_QUANTITY_RANGE = (50, 200)

DESSERT_QUANTITY_RANGE = (30, 100)


# ============================================================
# GA Configuration
# ============================================================

POPULATION_SIZE = 50

GENERATIONS = 100

MUTATION_RATE = 0.15

ELITE_COUNT = 5


# ============================================================
# Utility Functions
# ============================================================

def _quantity_range_for_role(
    role: str,
) -> tuple[float, float]:

    if role == "heavy_main":
        return HEAVY_MAIN_QUANTITY_RANGE

    if role == "easy_main":
        return EASY_MAIN_QUANTITY_RANGE

    if role == "main_side":
        return MAIN_SIDE_QUANTITY_RANGE

    if role == "side_side":
        return SIDE_SIDE_QUANTITY_RANGE

    if role == "hot_drink":
        return HOT_DRINK_QUANTITY_RANGE

    if role == "cold_drink":
        return COLD_DRINK_QUANTITY_RANGE

    if role == "snack":
        return SNACK_QUANTITY_RANGE

    if role == "dessert":
        return DESSERT_QUANTITY_RANGE

    raise ValueError(
        f"Unknown food role: {role}"
    )

def _random_quantity(
    role: str | None,
) -> float:

    low, high = _quantity_range_for_role(role)

    return random.uniform(low, high)


# ============================================================
# Foods By Role
# ============================================================

def _foods_by_role(
    pool: list[FoodItem],
) -> dict[str, list[FoodItem]]:

    result = {
        "heavy_main": [],
        "easy_main": [],

        "main_side": [],
        "side_side": [],

        "hot_drink": [],
        "cold_drink": [],

        "snack": [],
        "dessert": [],
    }

    for food in pool:

        role = food.role

        if role in result:
            result[role].append(food)

    return result

# ============================================================
# Choose Food
# ============================================================

def _choose_food(
    foods: list[FoodItem],
    used_ids: set[int] | None = None,
) -> FoodItem | None:

    if not foods:
        return None

    used_ids = used_ids or set()

    available = [
        food
        for food in foods
        if food.id not in used_ids
    ]

    if available:
        return random.choice(available)

    # اگر همه استفاده شده بودند،
    # اجازه تکرار می‌دهیم.
    return random.choice(foods)


# ============================================================
# Create Gene
# ============================================================

def _create_gene(
    food: FoodItem,
) -> Gene:

    return Gene(
        food=food,
        quantity=_random_quantity(
            food.role
        ),
    )


# ============================================================
# Meal Construction
# ============================================================

def _build_meal(
    meal: str,
    pool: list[FoodItem],
) -> list[Gene]:

    chromosome_meal: list[Gene] = []

    if not pool:
        return chromosome_meal

    by_role = _foods_by_role(pool)

    rules = MEAL_ROLE_RULES[meal]

    used_ids: set[int] = set()

    # ========================================================
    # 1. Required role
    # ========================================================

    required_food = None

    for role in rules["required"]:

        candidates = by_role.get(
            role,
            [],
        )

        if not candidates:
            continue

        required_food = _choose_food(
            candidates,
            used_ids,
        )

        if required_food:
            break

    # ========================================================
    # 2. Required food
    #
    # اگر وجود نداشت:
    # هیچ fallback نامرتبطی انجام نمی‌دهیم.
    # ========================================================

    if required_food is not None:

        chromosome_meal.append(
            _create_gene(required_food)
        )

        used_ids.add(
            required_food.id
        )

    # ========================================================
    # 3. Optional roles
    # ========================================================

    optional_roles = rules["optional"][:]

    random.shuffle(optional_roles)

    selected_optional_roles = []

    selected_groups = set()

    for role in optional_roles:

        # ----------------------------------------------------
        # Role Group
        # ----------------------------------------------------

        group = _role_group(role)

        # ----------------------------------------------------
        # اگر این role عضو یک group است،
        # فقط یکی از اعضای آن group مجاز است.
        # ----------------------------------------------------

        if group is not None:

            if group in selected_groups:
                continue

            selected_groups.add(group)

        selected_optional_roles.append(role)

        # ----------------------------------------------------
        # حداکثر تعداد optional
        # ----------------------------------------------------

        if len(selected_optional_roles) >= rules["max_optional"]:
            break

    # ========================================================
    # 4. Add optional foods
    # ========================================================

    for role in selected_optional_roles:

        candidates = by_role.get(
            role,
            [],
        )

        if not candidates:
            continue

        food = _choose_food(
            candidates,
            used_ids,
        )

        if food is None:
            continue

        chromosome_meal.append(
            _create_gene(food)
        )

        used_ids.add(
            food.id
        )

    return chromosome_meal
# ============================================================
# Chromosome Initialization
# ============================================================

def _init_chromosome(
    food_pools: dict[str, list[FoodItem]],
) -> Chromosome:

    chromosome: Chromosome = {}

    for meal in MEAL_TYPES:

        pool = food_pools.get(
            meal,
            [],
        )

        chromosome[meal] = _build_meal(
            meal,
            pool,
        )

    return chromosome


# ============================================================
# Nutrition Calculation
# ============================================================

def _meal_totals(
    genes: list[Gene],
) -> tuple[float, float, float, float]:

    calories = sum(
        gene.calories
        for gene in genes
    )

    protein = sum(
        gene.protein
        for gene in genes
    )

    carbs = sum(
        gene.carbs
        for gene in genes
    )

    fat = sum(
        gene.fat
        for gene in genes
    )

    return (
        calories,
        protein,
        carbs,
        fat,
    )


def _daily_totals(
    chromosome: Chromosome,
) -> tuple[float, float, float, float]:

    calories = 0.0
    protein = 0.0
    carbs = 0.0
    fat = 0.0

    for genes in chromosome.values():

        meal_cal, meal_pro, meal_carb, meal_fat = (
            _meal_totals(genes)
        )

        calories += meal_cal
        protein += meal_pro
        carbs += meal_carb
        fat += meal_fat

    return (
        calories,
        protein,
        carbs,
        fat,
    )


# ============================================================
# Relative Error
# ============================================================

def _rel_err(
    actual: float,
    target: float,
) -> float:

    if target <= 0:
        return 0.0

    return abs(actual - target) / target


# ============================================================
# Fast Food Penalty Calculation
# ============================================================

def _fast_food_penalty(
    chromosome: Chromosome,
) -> float:

    penalty = 0.0

    for genes in chromosome.values():

        for gene in genes:

            if gene.food.category == "fast_food":

                penalty += FAST_FOOD_PENALTY

    return penalty


# ============================================================
# Fitness
# ============================================================

def _fitness(
    chromosome: Chromosome,
    daily_target: MealTarget,
) -> float:
    """
    Fitness شامل:

    1. نزدیکی کالری کل روز
    2. نزدیکی پروتئین کل روز
    3. نزدیکی کربوهیدرات کل روز
    4. نزدیکی چربی کل روز
    5. نزدیکی کالری هر وعده به target خودش
    6. جریمه برای وعده‌های خالی
    7. جریمه برای role نامناسب
    8. جریمه برای تعداد optional بیشتر از حد مجاز
    """

    # ========================================================
    # Daily totals
    # ========================================================

    total_cal, total_pro, total_carb, total_fat = (
        _daily_totals(chromosome)
    )

    calorie_error = _rel_err(
        total_cal,
        daily_target.calories,
    )

    protein_error = _rel_err(
        total_pro,
        daily_target.protein,
    )

    carb_error = _rel_err(
        total_carb,
        daily_target.carbs,
    )

    fat_error = _rel_err(
        total_fat,
        daily_target.fat,
    )

    # ========================================================
    # Daily nutrition error
    # ========================================================

    daily_error = (
        calorie_error * 5.0
        + protein_error * 2.5
        + carb_error * 3
        + fat_error * 1.5
    )

    # ========================================================
    # Meal calorie error
    # ========================================================

    meal_error = 0.0

    for meal in MEAL_TYPES:

        genes = chromosome.get(
            meal,
            [],
        )

        target_calories = (
            daily_target.calories
            * MEAL_CALORIE_RATIO[meal]
        )

        actual_calories = sum(
            gene.calories
            for gene in genes
        )

        meal_error += _rel_err(
            actual_calories,
            target_calories,
        )

    # ========================================================
    # Empty meal penalty
    # ========================================================

    empty_meal_penalty = 0.0

    for meal in MEAL_TYPES:

        if not chromosome.get(meal):

            empty_meal_penalty += 5.0

    # ========================================================
    # Role penalty
    # ========================================================

    role_penalty = 0.0

    for meal in MEAL_TYPES:

        genes = chromosome.get(
            meal,
            [],
        )

        rules = MEAL_ROLE_RULES[meal]

        roles = [
            gene.food.role
            for gene in genes
        ]

        role_set = set(roles)

        # ----------------------------------------------------
        # Required role
        # ----------------------------------------------------

        required_ok = any(
            role in role_set
            for role in rules["required"]
        )

        if not required_ok:

            role_penalty += 4.0

        # ----------------------------------------------------
        # Invalid roles
        # ----------------------------------------------------

        allowed_roles = set(
            rules["required"]
            + rules["optional"]
        )

        for role in roles:

            if role not in allowed_roles:

                role_penalty += 5.0

        # ----------------------------------------------------
        # Optional count
        # ----------------------------------------------------

        # ----------------------------------------------------
        # Optional count by role groups
        # ----------------------------------------------------

        optional_roles = [
            role
            for role in roles
            if role in rules["optional"]
        ]

        optional_groups = set()

        for role in optional_roles:

            group = _role_group(role)

            if group is not None:
                optional_groups.add(group)
            else:
                optional_groups.add(role)

        optional_count = len(optional_groups)

        if optional_count > rules["max_optional"]:
            role_penalty += (
                                    optional_count
                                    - rules["max_optional"]
                            ) * 3.0
        # ----------------------------------------------------
        # Drink group constraint
        # ----------------------------------------------------

        drink_roles = {
            role
            for role in roles
            if role in ROLE_GROUPS["drink"]
        }

        if len(drink_roles) > 1:
            # hot_drink + cold_drink
            # نباید همزمان وجود داشته باشند.

            role_penalty += 5.0

    # ========================================================
    # Final error
    # ========================================================

    error = (
        daily_error
        + meal_error * 2.0
        + empty_meal_penalty
        + role_penalty
    )

    return 1.0 / (1.0 + error)

# ============================================================
# Crossover
# ============================================================

def _crossover(
    parent1: Chromosome,
    parent2: Chromosome,
) -> Chromosome:

    cut = random.randint(
        1,
        len(MEAL_TYPES) - 1,
    )

    child: Chromosome = {}

    for i, meal in enumerate(MEAL_TYPES):

        source = (
            parent1
            if i < cut
            else parent2
        )

        child[meal] = copy.deepcopy(
            source.get(
                meal,
                [],
            )
        )

    return child


# ============================================================
# Mutation
# ============================================================

def _mutate(
    chromosome: Chromosome,
    food_pools: dict[str, list[FoodItem]],
) -> Chromosome:

    for meal in MEAL_TYPES:

        pool = food_pools.get(
            meal,
            [],
        )

        if not pool:
            continue

        genes = chromosome.get(
            meal,
            [],
        )

        # ----------------------------------------------------
        # اگر وعده somehow خالی شد،
        # دوباره بر اساس قوانین جدید بساز
        # ----------------------------------------------------

        if not genes:

            chromosome[meal] = _build_meal(
                meal,
                pool,
            )

            continue

        # ----------------------------------------------------
        # Mutation روی Geneهای موجود
        # ----------------------------------------------------

        for index, gene in enumerate(
            chromosome[meal]
        ):

            if random.random() >= MUTATION_RATE:
                continue

            action = random.choice([
                "replace",
                "quantity",
            ])

            # =================================================
            # Replace food
            # =================================================

            if action == "replace":

                used_ids = {
                    g.food.id
                    for j, g in enumerate(
                        chromosome[meal]
                    )
                    if j != index
                }

                # ---------------------------------------------
                # فقط غذاهایی که همان role را دارند
                # ---------------------------------------------
                same_role_foods = [
                    food
                    for food in pool
                    if (
                        food.role == gene.food.role
                        and food.id not in used_ids
                    )
                ]

                if same_role_foods:

                    new_food = random.choice(
                        same_role_foods
                    )

                    chromosome[meal][index] = Gene(
                        food=new_food,
                        quantity=_random_quantity(
                            new_food.role
                        ),
                    )

                # ---------------------------------------------
                # اگر غذای دیگری با همان role نبود،
                # اصلاً role را عوض نکن
                # ---------------------------------------------
                continue

            # =================================================
            # Change quantity
            # =================================================

            else:

                chromosome[meal][index].quantity = (
                    _random_quantity(
                        gene.food.role
                    )
                )

        # ====================================================
        # احتمال اضافه کردن یک optional item
        # ====================================================

        if random.random() < MUTATION_RATE:

            rules = MEAL_ROLE_RULES[meal]

            current_roles = {
                gene.food.role
                for gene in chromosome[meal]
            }

            # ------------------------------------------------
            # roleهای optional که هنوز در وعده نیستند
            # ------------------------------------------------

            available_roles = []

            current_groups = {
                _role_group(role)
                for role in current_roles
                if _role_group(role) is not None
            }

            for role in rules["optional"]:

                # ---------------------------------------------
                # role خودش قبلاً استفاده شده
                # ---------------------------------------------

                if role in current_roles:
                    continue

                # ---------------------------------------------
                # اگر role عضو یک group است
                # و آن group قبلاً استفاده شده،
                # role جدید مجاز نیست.
                # ---------------------------------------------

                group = _role_group(role)

                if group is not None and group in current_groups:
                    continue

                available_roles.append(role)

            # ------------------------------------------------
            # تعداد optionalهای فعلی
            # ------------------------------------------------

            current_optional_roles = [
                gene.food.role
                for gene in chromosome[meal]
                if gene.food.role in rules["optional"]
            ]

            current_optional_groups = set()

            for role in current_optional_roles:

                group = _role_group(role)

                if group is not None:
                    current_optional_groups.add(group)
                else:
                    current_optional_groups.add(role)

            current_optional_count = len(
                current_optional_groups
            )

            # ------------------------------------------------
            # فقط اگر هنوز ظرفیت optional داریم
            # ------------------------------------------------

            if (
                    available_roles
                    and current_optional_count
                    < rules["max_optional"]
            ):

                role = random.choice(
                    available_roles
                )

                candidates = [
                    food
                    for food in pool
                    if food.role == role
                ]

                if candidates:

                    used_ids = {
                        gene.food.id
                        for gene in chromosome[meal]
                    }

                    candidates = [
                        food
                        for food in candidates
                        if food.id not in used_ids
                    ]

                    if candidates:
                        food = random.choice(
                            candidates
                        )

                        chromosome[meal].append(
                            _create_gene(food)
                        )
    return chromosome

# ============================================================
# Parent Selection
# ============================================================

def _select_parents(
    population: list[Chromosome],
    fitnesses: list[float],
) -> tuple[Chromosome, Chromosome]:

    def tournament() -> Chromosome:

        k = min(
            3,
            len(population),
        )

        candidates = random.sample(
            range(len(population)),
            k=k,
        )

        best = max(
            candidates,
            key=lambda i: fitnesses[i],
        )

        return population[best]

    return (
        tournament(),
        tournament(),
    )


# ============================================================
# Public API
# ============================================================

def run_ga(
    food_pools: dict[str, list[FoodItem]],
    daily_target: MealTarget,
    days: int = 7,
) -> list[Chromosome]:
    """
    تولید برنامه غذایی چندروزه.

    هر روز یک GA مستقل اجرا می‌شود.

    قوانین:

    - هر ۵ وعده در chromosome وجود دارند.
    - breakfast/lunch/dinner ترجیحاً main دارند.
    - morning_snack/afternoon_snack ترجیحاً snack دارند.
    - dessert فقط در وعده‌هایی که در MEAL_ROLE_RULES
      اجازه داده شده باشد.
    - drink فقط طبق role دیتابیس انتخاب می‌شود.
    - fast_food مجاز است، اما در Fitness جریمه می‌شود.
    - category هرگز به role تبدیل نمی‌شود.
    """

    best_per_day: list[Chromosome] = []

    for _ in range(days):

        # ====================================================
        # Initial population
        # ====================================================

        population = [
            _init_chromosome(food_pools)
            for _ in range(POPULATION_SIZE)
        ]

        # ====================================================
        # Evolution
        # ====================================================

        for _ in range(GENERATIONS):

            fitnesses = [
                _fitness(
                    chromosome,
                    daily_target,
                )
                for chromosome in population
            ]

            # ------------------------------------------------
            # Elite
            # ------------------------------------------------

            elite_indices = sorted(
                range(len(population)),
                key=lambda i: fitnesses[i],
                reverse=True,
            )[:ELITE_COUNT]

            new_population = [
                copy.deepcopy(
                    population[i]
                )
                for i in elite_indices
            ]

            # ------------------------------------------------
            # Children
            # ------------------------------------------------

            while len(new_population) < POPULATION_SIZE:

                parent1, parent2 = _select_parents(
                    population,
                    fitnesses,
                )

                child = _crossover(
                    parent1,
                    parent2,
                )

                child = _mutate(
                    child,
                    food_pools,
                )

                new_population.append(
                    child
                )

            population = new_population

        # ====================================================
        # Best chromosome
        # ====================================================

        fitnesses = [
            _fitness(
                chromosome,
                daily_target,
            )
            for chromosome in population
        ]

        best_index = max(
            range(len(population)),
            key=lambda i: fitnesses[i],
        )

        best_per_day.append(
            copy.deepcopy(
                population[best_index]
            )
        )

    return best_per_day