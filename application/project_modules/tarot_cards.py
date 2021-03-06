import random

from bs4 import BeautifulSoup
from requests_cache import CachedSession

# ---- Get The Names Of The Tarot Cards Online ---- #
session = CachedSession()
website = "https://labyrinthos.co/blogs/tarot-card-meanings-list"
website_data = session.get(website).text

soup = BeautifulSoup(website_data, 'html.parser')

tarot_data = soup.find_all('h3')
tarot_names = [card.get_text().replace(" Meaning", "") for card in tarot_data]

# ---- Get the Pictures for Each Card ---- #
# picture_names = os.listdir("../static/images/tarot_cards")
picture_names = ['0 - The World - tiffany-chan-_SAVhxRL2U8-unsplash.jpg',
                 '01 - Judgement - gabriela-gutierrez-I2HZhYDEDN0-unsplash.jpg',
                 '02 - The Sun - matthias-oberholzer-gM5msl7rP2k-unsplash.jpg',
                 '03 - The Moon - annie-spratt-kDo57E2qOE4-unsplash.jpg',
                 '04 - The Star - vanessa-serpas-e6lWMBIgNso-unsplash.jpg',
                 '05- The Tower - sebastian-pichler-JNCkUF-QwOI-unsplash.jpg',
                 '06- The Devil - joshua-harris--rkW0aKhOMA-unsplash.jpg',
                 '07 - Temperance - todd-trapani-a-AqoJXVYVY-unsplash.jpg',
                 '08 - Death - javardh-YWY8q9G3jY8-unsplash.jpg',
                 '09 - The Hanged Man - bankim-desai-XShUaqahkZM-unsplash.jpg',
                 '10 - Justice - yehor-tulinov-xPtmUu-9VDU-unsplash.jpg',
                 '11 - The Wheel of Fortune - annie-spratt-kXqTlz4Ejhw-unsplash.jpg',
                 '12 - The Hermit - timothy-dykes-Z66JM_4wleU-unsplash.jpg',
                 '13 - Strength - salman-hossain-saif-RvWpwfzSjbQ-unsplash.jpg',
                 '14 - The Chariot - jorge-zapata-6FgbPqag3h8-unsplash.jpg',
                 '15 - The Lovers - zdenek-machacek-ekV_axnZRUA-unsplash.jpg',
                 '16 - The Heirophant - mamun-srizon-qyZAmc-8M1s-unsplash.jpg',
                 '17 - The Emperor - savitri-wendt-0SMM_mRFpYc-unsplash.jpg',
                 '18 - The Empress - daniel-monteiro-4w79vITaWK4-unsplash.jpg',
                 '19 - High Priestess - wang-xi-DVbYj04Y124-unsplash.jpg',
                 '20 - The Magician - carol-petri-ssPyq97lxVY-unsplash.jpg',
                 '21 - The Fool - jamie-street-Lw9STRb-D6o-unsplash.jpg',
                 '22 - The Programmer - imdadul-hussain-CqHFJ3_Zlss-unsplash.jpg',
                 '23 - Seven of Wands - nelson-flores-y_yKkAYsQRQ-unsplash.jpg',
                 '24 - Four of Wands - james-wainscoat-is8f7sBcfzY-unsplash.jpg',
                 '25 - Ace of Wands - james-wainscoat-is8f7sBcfzY-unsplash.jpg',
                 '26 - Ten of Wands - rotekirsche20-q-mqF5F31CU-unsplash.jpg',
                 '27 - Nine of Wands - agata-create-0sA6WQIaizg-unsplash.jpg',
                 '28 - Eight of Wands - sun-studio-creative-Ix6io6HYiDg-unsplash.jpg',
                 '29 - Six of Wands - nelson-flores-y_yKkAYsQRQ-unsplash.jpg',
                 '30 - Five of Wands - kalineri-T8beRu40qh0-unsplash.jpg',
                 '31 - Three of Wands - reed-geiger-EFpKh3mXpRc-unsplash.jpg',
                 '32 - Two of Wands - photo-1635408113209-c360a418619d.jpg',
                 '33 - Page of Wands - maria-lupan-paojjhmfDTk-unsplash.jpg',
                 '34 - Queen of Wands - hedy-yin-H7Bl5S3wP4k-unsplash.jpg',
                 '35 - King of Wands - cut-collective-60gguflK7Gc-unsplash.jpg',
                 '36 - Knight of Wands - andrew-ling-ORVwlyk9y3U-unsplash.jpg',
                 '37 - The Artist - nathan-bingle-Rn49SU03cqk-unsplash.jpg',
                 '38 - King of Cups - atik-sulianami-xwiO6w6XEiM-unsplash.jpg',
                 '39 - Queen of Cups - atik-sulianami-xwiO6w6XEiM-unsplash.jpg', '40 - Knight of Cups.jpg',
                 '41 - Page of Cups - timothy-dykes-8wvuKdZuz8Q-unsplash.jpg',
                 '42 - Ten of Cups - timothy-dykes-8wvuKdZuz8Q-unsplash.jpg',
                 '43 - Nine of Cups - timothy-dykes-8wvuKdZuz8Q-unsplash.jpg',
                 '44 - Eight of Cups - timothy-dykes-8wvuKdZuz8Q-unsplash.jpg',
                 '45 - Seven of Cups - jez-timms-4l3rr3gUYH4-unsplash.jpg',
                 '46 - Six of Cups - jez-timms-4l3rr3gUYH4-unsplash.jpg',
                 '47 - Five of Cups - jez-timms-4l3rr3gUYH4-unsplash.jpg',
                 '48 - Four of Cups - hans-veth--Vp8y5L2fKg-unsplash.jpg',
                 '49 - Three of Cups - hans-veth--Vp8y5L2fKg-unsplash.jpg',
                 '50 - Two of Cups - dorothea-oldani-zu-19OUH4rk-unsplash.jpg',
                 '51 - Ace of Cups - jay-pVdiv_8oY_s-unsplash.jpg',
                 '52 - king of swords - j-lee-uYGSizO3ZWY-unsplash.jpg',
                 '53 - knight of swords - tijana-drndarski-AoFp9qeFIss-unsplash.jpg',
                 '54 - queen of swords = aaron-burden-m1_A_0YDLAo-unsplash.jpg',
                 '55 - Page of Swords - omid-armin-khyHnsPO0pE-unsplash.jpg',
                 '56 - Ten of Swords - peter-zagar-bLgWa9b0ioY-unsplash.jpg',
                 '57 - Nine of Swords - linh-le-Ebwp2-6BG8E-unsplash.jpg',
                 '58 - Eight  of Swords - linh-le-Ebwp2-6BG8E-unsplash.jpg',
                 '59 - Seven of Swords - linh-le-Ebwp2-6BG8E-unsplash.jpg',
                 '60 - Six of Swords - linh-le-Ebwp2-6BG8E-unsplash.jpg',
                 '61 - Five of Swords - john-silliman-J8SIeEKo5rA-unsplash.jpg',
                 '62 - Three of Swords - linh-le-Ebwp2-6BG8E-unsplash.jpg',
                 '63 - Four of Swords - linh-le-Ebwp2-6BG8E-unsplash.jpg',
                 '64 - Two of Swords - matthew-sichkaruk-l40_qRmoHVY-unsplash.jpg',
                 '65 - Ace of Swords - montatip-lilitsanong-D4XNEB3ZXSI-unsplash.jpg',
                 '66 - King of Pentacles - thought-catalog-9aOswReDKPo-unsplash.jpg',
                 '67 - queen of pentacles - allec-gomes-ofRrymNhmvI-unsplash.jpg',
                 '68 - knight of pentacles - adam-sidaway-z_3lU9-H_Dk-unsplash.jpg',
                 '69 - Page of Pentacles - thought-catalog-9aOswReDKPo-unsplash.jpg',
                 '70 - 10 of pentacles - stephanie-harvey-Lgkf6AfZOEU-unsplash.jpg',
                 '71 - Nine of Pentacles - lauren-mancke-sil2Hx4iupI-unsplash.jpg',
                 '72 - eight of pentacles - alex-belogub-TPZtQOYcvUc-unsplash.jpg',
                 '73 - seven of pentacles - janine-joles--8nbY8W2YEE-unsplash.jpg',
                 '74 - Six of Pentacles- marek-studzinski-3D6yReT06p0-unsplash.jpg',
                 '75 - five of pentacles - cristy-zinn-KBlCdNY33Wc-unsplash.jpg',
                 '76 - four of pentacles - diane-helentjaris-Po1luGu2fmc-unsplash.jpg',
                 '77 - three of pentacles - quaritsch-photography-4LwWLbFRck4-unsplash.jpg',
                 '78 - two of pentacles - charlotte-harrison-RcDJZCVRrQ4-unsplash.jpg',
                 '79 -Ace of Pentacles - viktor-talashuk-m7VRDnn1IaM-unsplash.jpg']
pictures = ['/static/images/tarot_cards/' + picture_names[i] for i in range(len(picture_names))]

# ---- Finalize Deck ---- #
tarot_deck = {i: {'number': i, 'name': tarot_names[i], 'img': pictures[i]} for i in range(len(tarot_names))}
tarot_deck[22]['name'] = 'The Programmer'
tarot_deck[37]['name'] = 'The Artist'


# ---- Card Manager ---- #
class TarotManager:
    def __init__(self):
        # ---- Initialize Deck of Cards ---- #
        self.tarot_deck = tarot_deck

    def deal_cards(self):
        """
        Picks three cards at random from the tarot deck.
        :return: a list of three cards.
        """
        # ---- Make a Copy of Deck So It Resets ---- #
        avail_cards = self.tarot_deck.copy()
        selected_cards = []
        card_numbers = random.sample(range(0, len(avail_cards) - 1), 3)

        # ---- Pick Cards ---- #
        for i in card_numbers:
            selected_cards.append(tarot_deck[i])
            avail_cards.pop(i)

        return selected_cards


# ---- Message Manager ---- #
class MessageGenerator:
    def __init__(self, messages, user_messages):
        self.messages = messages
        self.user_messages = user_messages
        self.all_messages = self.messages + self.user_messages

    def deliver_message(self, total):
        """
        Delivers a random message based on the total sum of the selected cards' hidden numbers.
        :param total: sum of selected cards' hidden numbers.
        :return: a random string of from list of messages.
        """
        random.shuffle(self.all_messages)
        possible_messages = self.all_messages[:151]
        if total < 79:
            message_to_deliver = random.choice(possible_messages[:51])
        elif 79 <= total <= 158:
            message_to_deliver = random.choice(possible_messages[52:101])
        else:
            message_to_deliver = random.choice(possible_messages[102:151])

        return message_to_deliver


# ---- Messages ---- #
def get_custom_messages(table):
    """
    Gets custom messages from the table.
    :param table: custom message table
    :return: list of messages
    """
    custom_message_data = table.query.all()
    custom_messages = [row.message for row in custom_message_data]
    return custom_messages


tarot_messages = [
    "I am in the right place at the right time, doing the right thing. - LOUISE HAY",
    "Conscious breathing is my anchor. - THICH NHAT HANH",
    "I am loved just for being who I am, just for existing. - RAM DASS",
    "The chance to love and be loved exists no matter where you are. - OPRAH",
    "Courage starts with showing up and letting ourselves be seen. - BREN?? BROWN",
    "Make way for the unprecedented and watch your reality rearrange itself. - YRSA DALEY-WARD",
    "Open your heart and drink in the glorious day. - HEATHER HAVRILESKY",
    "Embrace the glorious mess that you are. - ELIZABETH GILBERT",
    "The perfect moment is this one. - JON KABAT-ZINN",
    "I deserve joy, happiness, and success.",
    "I am deliberate and afraid of nothing. - AUDRE LORD",
    "Who you are inside is what helps you make and do everything in life. - MISTER ROGERS",
    "Your perspective is unique. It's important and it counts. - GLENN CLOSE",
    "Every day above earth is a good day. - ERNEST HEMINGWAY",
    "Nothing can dim the light that shines from within. - MAYA ANGELOU",
    "I will not be my own bully.",
    "You must do things you think you cannot do. - ELEANOR ROOSEVELT",
    "I am calm and courageous.",
    "I am growing into greater versions of myself.",
    "I trust my intuitions.",
    "I am intentional about my happiness.",
    "I am not afraid of change.",
    "I wake up feeling grateful for life.",
    "I am loved and appreciated.",
    "I enjoy the present moment.",
    "I feel strong today.",
    "I love who I am becoming.",
    "I am better than I used to be. But hopefully not as good as I'll be tomorrow. - MARIANNE WILLIAMSON",
    "I have control over my life.",
    "I am excited to discover fresh paths.",
    "I am bold and brave.",
    "I have people who love and inspire me.",
    "What I desire will become a reality.",
    "I am more than enough.",
    "I attract only the best of things.",
    "I am energized for the entire day.",
    "Failure is just another way to learn how to do something right. - MARIAN WRIGHT EDELMAN",
    "If I keep trying, I will get there.",
    "It is okay to depend on others.",
    "I am confident in my abilities.",
    "I can create a positive change in my world.",
    "I believe I can be successful at whatever I do.",
    "I have what it takes to succeed.",
    "I can learn from my failures.",
    "I can celebrate the small wins.",
    "I was always worthy.",
    "It is not selfish to prioritize myself.",
    "I can let myself rest. I don't need an excuse.",
    "I can take up challenges and new opportunities.",
    "I am living to my fullest potential.",
    "I can stretch myself beyond my comfort zone.",
    "I won???t let my failures define me.",
    "I am capable of so much more.",
    "Almost everything will work again if you unplug it for a few minutes, including you. - ANNE LAMOTT",
    "I value myself by giving value to my time.",
    "Grab a coffee. Journal your intentions. Get to work. Create miracles. - ELYSE SANTILLI",
    "Loving yourself isn???t vanity. It???s sanity. - KATRINA MEYER",
    "We cannot direct the wind, but we can adjust the sails. - DOLLY PARTON",
    "I can give myself permission to hit pause.",
    "I am a beautiful person, inside and out.",
    "I want to feel my life while I'm in it. - MERYL STREEP",
    "Always make decisions that prioritize your inner peace - IZEY VICTORIA ODIASE",
    "I can accept change gracefully.",
    "I know where I'm going and how to get there.",
    "I can maintain a home that is clean and organized.",
    "If you try to numb the vulnerability, you also numb joy, happiness, and connection. - JONATHAN VAN NESS",
    "Saying 'no' can be the best form of self care.",
    "I can take time to do what makes me happy.",
    "When you say 'yes' to others, make sure you are not saying 'no' to yourself. - PAULO COEHLO",
    "I owe myself the love I freely give to others.",
    "You can't get anywhere on an empty tank. Take time to refuel.",
    "Be so completely yourself that everyone feels safe to be themselves, too.",
    "I can be independent.",
    "I can let others love me for being me.",
    "I will forever appreciate myself.",
    "When I look in the mirror, I see someone to be grateful for.",
    "I would rather make mistakes than make nothing at all.",
    "The darker the night, the brighter the stars.",
    "I am what I have overcome.",
    "I am Groot. - GROOT",
    "I will struggle. I will fail, but to surrender is a privilege I do not have.",
    "If the situation changes, I can decide what it becomes.",
    "Opportunity awards those who wait.",
    "Sometimes, you just gotta do it yourself.",
    "Compromise where you can. Where you can't, don't.",
    "I can hold myself accountable for my commitments.",
    "I am willing to surprise myself.",
    "I will embrace the best version of myself.",
    "What makes something beautiful is not that it lasts, but that it is.",
    "Yesterday is history, tomorrow is a mystery, but today is a gift.",
    "The steps I take don't need to be big; they only need to take me in the right direction.",
    "I have the tools to help me stay productive.",
    "I can ask for help when I???m stuck.",
    "I will not let my fears control my actions.",
    "Power comes in response to a need, not a desire. You have to create that need.",
    "I can always make a different choice.",
    "It's okay for me to change my mind.",
    "Keep your face always towards the sunshine, and shadows will fall behind you. - WALT WHITMAN",
    "You are never too old to set another goal or to dream a new dream. - MALALA YOUSAFZAI",
    "Believe you can and you're halfway there. - THEODORE ROOSEVELT",
    "I am not a drop in the ocean, but the ocean in a drop.",
    "Don???t try to lessen yourself for the world; let the world catch up to you. - BEYONC??",
    "I am open to new opportunities.",
    "We are not our best intentions. We are what we do. - Amy Dickinson",
    "I will not belittle my progress.",
    "I will not give up.",
    "I can make mistakes and learn from them.",
    "It is not my responsibility to accept an apology.",
    "I am not late to being myself.",
    "I am not confined by my environment.",
    "I will not be scared of my full potential.",
    "Allow yourself some time in the sun.",
    "I can create something new.",
    "'Impossible' is only an opinion.",
    "I am becoming more efficient.",
    "It's not the load that breaks you down, but the way you carry it. - LOU HOLTZ",
    "Work hard in silence, let your success be the noise. - FRANK OCEAN",
    "You can dance all by yourself.",
    "It's okay to cry.",
    "Be happy about the success of others so you can see how yours arrives.",
    "I have the space and liberty to create.",
    "Simple goes a long way. - BAD BUNNY",
    "In times of crisis, the wise build bridges, while the foolish build barriers. - T'CHALLA",
    "I have nothing to prove to anyone but myself.",
    "I am strong, I am worthy, and I am not going to be silent about it.",
    "Today gives me a chance for something new.",
    "It's more important to master the cards you're holding, than to complain about the ones someone else was dealt.",
    "A delayed game is eventually good, but a rushed game is forever bad. - SHIGERU MIYAMOTO",
    "Just keep swimming. - DORY",
    "I can give time to what is important to me.",
    "There's no one I rather be than me.",
    "If speaking is silver, then listening is gold.",
    "Peace cannot be kept by force; it can only be achieved by understanding. - ALBERT EINSTEIN",
    "I can be a safe space for others.",
    "I can block out things that distract me from my goals.",
    "Best to be hated for what you are, than loved for what you're not.",
    "Time you enjoy wasting is not wasted time.",
    "When you can't find someone to follow, there's your chance to lead by example.",
    "I will be strong, I will be weak, and both will be okay.",
    "I will not doubt myself.",
    "A friend may be waiting behind a stranger's face. - MAYA ANGELOU",
    "Being good to people is a wonderful legacy to leave behind.",
    "I will not let others dictate who I am.",
    "I will not be afraid to be weird.",
    "One good thing about music: when it hits you, you feel no pain. - BOB MARLEY",
    "I am moved by faith and not fears.",
    "There is grace in forgiveness.",
    "Be kind; to others, and to yourself.",
    "Carry out a random act of kindness, with no expectation of a reward.",
    "My efforts will one day translate to success.",
]
