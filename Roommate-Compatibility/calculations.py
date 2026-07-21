import pandas as pd


# =========================================================
# DIFFERENCE FEATURES
# =========================================================

def cleanliness_diff(a, b):

    return abs(a - b) / 9


def social_energy_diff(a, b):

    return abs(a - b) / 9


def noise_tolerance_diff(a, b):

    return abs(a - b) / 9


# =========================================================
# SIMILARITY FEATURES
# =========================================================

def academic_goal_similarity(a, b):

    return int(a == b)


def study_style_similarity(a, b):

    return int(a == b)


def communication_style_similarity(a, b):

    return int(a == b)


def organization_similarity(a, b):

    return int(abs(a - b) <= 2)


def food_preference_similarity(a, b):

    return int(a == b)


def hobby_similarity(a, b):

    a = set(a)
    b = set(b)

    return int(len(a.intersection(b)) > 0)


def weekend_activity_similarity(a, b):

    return int(a == b)


# =========================================================
# INTERACTION FEATURES
# =========================================================

def messy_vs_clean_conflict(clean_a, clean_b):

    return int(
        (clean_a <= 3 and clean_b >= 8)
        or
        (clean_b <= 3 and clean_a >= 8)
    )


def nightowl_vs_earlybird_conflict(sleep_a, sleep_b):

    return int(abs(sleep_a - sleep_b) >= 5)


def gamer_vs_light_sleeper(gaming_a, noise_b):

    return int(
        gaming_a >= 6 and noise_b <= 3
    )


def loud_music_vs_noise_sensitive(music_a, noise_b):

    return int(
        music_a >= 7 and noise_b <= 3
    )


def guest_heavy_vs_private_person(guest_a, social_b):

    return int(
        guest_a >= 5 and social_b <= 3
    )


def extrovert_vs_introvert_conflict(social_a, social_b):

    return int(abs(social_a - social_b) >= 6)


def group_study_vs_solo_study(a, b):

    return int(a != b)


def emotional_expressive_vs_reserved(a, b):

    return int(a != b)


def high_spender_vs_budget_person(a, b):

    return int(
        (a >= 8 and b <= 3)
        or
        (b >= 8 and a <= 3)
    )


def fitness_focused_vs_irregular(a, b):

    return int(a != b)


# =========================================================
# MAIN FEATURE GENERATION
# =========================================================

def generate_features(student1, student2):

    features = {

        # =====================================
        # DIFFERENCE FEATURES
        # =====================================

        "cleanliness_diff": cleanliness_diff(
            student1["cleanliness"],
            student2["cleanliness"]
        ),

        "social_energy_diff": social_energy_diff(
            student1["social_energy"],
            student2["social_energy"]
        ),

        "noise_tolerance_diff": noise_tolerance_diff(
            student1["noise_tolerance"],
            student2["noise_tolerance"]
        ),

        # =====================================
        # SIMILARITY FEATURES
        # =====================================

        "academic_goal_similarity": academic_goal_similarity(
            student1["academic_goal"],
            student2["academic_goal"]
        ),

        "study_style_similarity": study_style_similarity(
            student1["study_style"],
            student2["study_style"]
        ),

        "communication_style_similarity":
        communication_style_similarity(
            student1["communication_style"],
            student2["communication_style"]
        ),

        "organization_similarity": organization_similarity(
            student1["cleanliness"],
            student2["cleanliness"]
        ),

        "food_preference_similarity":
        food_preference_similarity(
            student1["food_preference"],
            student2["food_preference"]
        ),

        "hobby_similarity": hobby_similarity(
            student1["hobbies"],
            student2["hobbies"]
        ),

        "weekend_activity_similarity":
        weekend_activity_similarity(
            student1["weekend_activity"],
            student2["weekend_activity"]
        ),

        # =====================================
        # INTERACTION FEATURES
        # =====================================

        "messy_vs_clean_conflict":
        messy_vs_clean_conflict(
            student1["cleanliness"],
            student2["cleanliness"]
        ),

        "nightowl_vs_earlybird_conflict":
        nightowl_vs_earlybird_conflict(
            student1["sleep_time"],
            student2["sleep_time"]
        ),

        "gamer_vs_light_sleeper":
        gamer_vs_light_sleeper(
            student1["gaming_hours"],
            student2["noise_tolerance"]
        ),

        "loud_music_vs_noise_sensitive":
        loud_music_vs_noise_sensitive(
            student1["music_volume"],
            student2["noise_tolerance"]
        ),

        "guest_heavy_vs_private_person":
        guest_heavy_vs_private_person(
            student1["guest_frequency"],
            student2["social_energy"]
        ),

        "extrovert_vs_introvert_conflict":
        extrovert_vs_introvert_conflict(
            student1["social_energy"],
            student2["social_energy"]
        ),

        "group_study_vs_solo_study":
        group_study_vs_solo_study(
            student1["study_style"],
            student2["study_style"]
        ),

        "emotional_expressive_vs_reserved":
        emotional_expressive_vs_reserved(
            student1["communication_style"],
            student2["communication_style"]
        ),

        "high_spender_vs_budget_person":
        high_spender_vs_budget_person(
            student1["spending_habit"],
            student2["spending_habit"]
        ),

        "fitness_focused_vs_irregular":
        fitness_focused_vs_irregular(
            student1["fitness_routine"],
            student2["fitness_routine"]
        )
    }

    return pd.DataFrame([features])