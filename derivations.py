# TESTING - DONT RUN IT IN PRODUCTION


import pprint

def calculate_secondary_traits(emotion_scores):
    # Define the weights for each secondary emotion based on specific primary emotions
    weights = {
        "Hunger to Achieve": {"Determination": 0.5, "Excitement": 0.3, "Joy": 0.2},
        "Passion for Work": {"Enthusiasm": 0.4, "Interest": 0.4, "Love": 0.2},
        "Positivity": {"Joy": 0.5, "Gratitude": 0.3, "Contentment": 0.2},
        "Resilience": {"Determination": 0.5, "Anxiety": 0.3, "Courage": 0.2},
        "Humility": {"Empathic Pain": 0.4, "Sympathy": 0.4, "Distress": 0.2},
        "Adaptability": {"Excitement": 0.4, "Calmness": 0.3, "Confusion": 0.3},
        "Accountability": {"Trust": 0.4, "Integrity": 0.4, "Guilt": 0.2},
        "Gratitude": {"Joy": 0.5, "Contentment": 0.3, "Admiration": 0.2},
        "Integrity": {"Trust": 0.4, "Accountability": 0.4, "Calmness": 0.2},
        "Courage": {"Determination": 0.5, "Fear": 0.3, "Anxiety": 0.2},
        "Trust": {"Gratitude": 0.4, "Admiration": 0.4, "Calmness": 0.2},
        "Commitment": {"Determination": 0.5, "Satisfaction": 0.5},
        "Innovation": {"Interest": 0.5, "Excitement": 0.5},
        "Inclusivity": {"Sympathy": 0.5, "Joy": 0.5},
        "Excellence": {"Satisfaction": 0.6, "Pride": 0.4},
        # Using only specified emotions
        "Sustainability ": {"Guilt": 0.5, "Awe": 0.5}, 
        'Collaborative ': {'Sympathy': .5, 'Joy': .5},
        'Effectively manages ambiguity': {'Calmness': .6,
                                             'Concentration': .4},
        'Able to lead and take charge': {'Excitement': .6,
                                           'Determination': .4},
        'Comfortable working in hyper-growth environment':
            {'Excitement': .6,
             'Adaptability': .4},
        'Proactive': {'Enthusiasm': .6,
                      'Determination': .4},
        'Detail-oriented': {'Concentration': .6,
                             'Awareness': .4}, 
        'Communicative': {'Joy': .5,
                          'Enthusiasm': .5},
        'Analytical': {'Concentration': .6,
                       'Interest': .4},
        'Resourceful': {'Interest': .5,
                        'Determination': .5}
    }

    # Initialize a dictionary to hold the presence counts
    presence_counts = {trait: 0 for trait in weights.keys()}

    # Calculate the weighted presence for each secondary trait
    for trait, emotion_weights in weights.items():
        for emotion, weight in emotion_weights.items():
            if emotion in emotion_scores:
                presence_counts[trait] += emotion_scores[emotion] * weight

    # Calculate total score
    total_score = sum(presence_counts.values())

    # Calculate percentage presence of each secondary trait
    percentage_presence = {trait: (score / total_score * 100) if total_score > 0 else 0 
                           for trait, score in presence_counts.items()}

    return percentage_presence

# Example usage with provided scores
emotion_scores_input = {
    'Calmness': 7104650028049946,
    'Interest': 5199310481548309,
    'Confusion': 45544262230396,
    'Boredom': 115827962756157,
    'Annoyance': 448085855692625,
    'Enthusiasm': 211018346250057,
    'Contentment': 56078803539276,
    'Awkwardness': 271374724805355,
    'Satisfaction': 908108070492744,
    'Surprise (positive)': 514429308474064,
    'Determination': 476231765002012,
    'Realization': 158466272056103,
    'Concentration': 124630227684975,
    'Contempt': 188349407166243,
    'Excitement': 138930870220065,
    'Joy': 99351099692285,
    'Sarcasm': 72828596457839,
    'Contemplation': 566108137369156,
    'Surprise (negative)': 650459814816713,
    'Amusement': 90411219745874,
    'Disapproval': 413393026217818,
    'Tiredness': 324090600013733,
    'Doubt': 966475304216146,
    'Aesthetic Appreciation': 7526798918843,
    'Disappointment': 772448423318565,
    'Triumph': 6863964293152094,
    'Admiration': 580142371356487,
    'Sympathy': 5048176534473896,
    'Relief': 41551001742482,
    'Pride': 4420739114285,
    'Entrancement': 6881288271397352,
    'Adoration':2448427747003734,
    'Love':4770378395915,
    'Gratitude':2545244777575135,
    'Distress':894338079728186,
    'Awe':891698152758181,
    'Empathic Pain' :178406136110425,
    'Anxiety':7719839932397008,
    'Desire':261445593089,
    'Sadness':610097475349903,
    'Pain':58192937634885,
    'Anger':5256412560120225,
    'Embarrassment':1451218209695071,
    'Shame':18540163710713,
    'Romance':179345598211512,
    'Nostalgia':1048079439206049,
    'Disgust':9749885532073677,
    'Envy':9486284398008138,
    'Ecstasy':8500829280819744,
    'Craving':7609984721057117,
    'Fear':6241430848604068,
    'Guilt':4910387448035181,
    'Horror':29455902040353976
}

result = calculate_secondary_traits(emotion_scores_input)
pprint.pprint(result)
