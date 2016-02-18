#!/usr/bin/env python3

import random

vowels = list("aeiou")
consonants = list("pbtdkg")

# for each preceding consonant, give the proper assimilated nasal
nasals = {
        "k": "ng",
        "g": "ng",
        "p": "m",
        "b": "m",
        "otherwise": "n",
}

# don't use 3rd person singular (would need additional verb agreement)
pronoun_pairs = {
        "I": "me",
        "we": "us",
        "they": "them",
        "you": "you",
        "you all": "you all",
}

actor_glosses = "cat dog fox bird man woman elder friend enemy".split(" ")
action_glosses = "like hate love bite see hurt hear".split(" ")

def cv_syllable():
    return random.choice(consonants) + random.choice(vowels)

def coin_noun():
    word = random.choice(vowels)
    for i in range(random.randrange(1, 4)):
        word += cv_syllable()
    return word

def append_nasal(word):
    return word + nasals.get(word[-2], nasals["otherwise"])

def coin_verb():
    return append_nasal(coin_noun())

def indefinite_article_for(word):
    return "an" if word[0] in vowels else "a"

class GlossedLanguage:
    def __init__(self, nouns, pronouns, verbs, pronoun_pairs):
        self.nouns = nouns
        self.pronouns = pronouns
        self.actors = dict(**nouns, **pronouns)

        self.pronoun_pairs = pronoun_pairs

        self.verbs = verbs

        self.words = dict(**verbs, **self.actors)

    def actor(self):
        return random.choice(list(self.actors.items()))

    def action(self):
        return random.choice(list(self.verbs.items()))

    def sentence(self):
        agent, agent_gloss = self.actor()
        patient, patient_gloss = self.actor()
        action, action_gloss = self.action()

        # verb agreement
        if agent_gloss not in self.pronoun_pairs:
            action_gloss += "s"

        patient_gloss = self.pronoun_pairs.get(patient_gloss, patient_gloss)
        new_sentence = "{} {} {}.".format(agent, patient, action).capitalize()
        gloss = "{} {} {}.".format(agent_gloss, action_gloss, patient_gloss).capitalize()
        return (new_sentence, gloss)

if __name__ == "__main__":
    nom_pronoun_glosses = list(pronoun_pairs.keys())
    random.shuffle(nom_pronoun_glosses)

    language = GlossedLanguage(
        nouns={ coin_noun() : indefinite_article_for(gloss) + " " + gloss for gloss in actor_glosses },
        pronouns={ vowels[i] : gloss for i, gloss in enumerate(nom_pronoun_glosses) },
        verbs={ coin_verb() : action_gloss for action_gloss in action_glosses },
        pronoun_pairs=pronoun_pairs,
    )

    print("lexicon\n".upper())
    for word, gloss in language.words.items():
        print("  - %-10s %s" % (word + ":", gloss))

    print("\n\nexample sentences".upper())
    for i in range(20):
        sentence, gloss = language.sentence()
        print()
        print("  -", sentence)
        print("   ", gloss)

    #print("\n\nungrammatical examples".upper()) #TODO
