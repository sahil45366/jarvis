import difflib


def detect_intent(command):

    command = command.lower().strip()
    command = command.replace("jarvis", "").strip()
    command = " ".join(command.split())
    
    
     # ================= TASK REQUEST ================= #
    
    task_phrases = [
            "do this task",
            "perform this task",
            "complete this task",
            "execute this task",
            "do these steps",
            "perform these steps",
            "task karo",
            "ye task karo",
            "ye kaam karo",
            "mere liye ye karo"
        ]
    
    multi_step_markers = [
            " and search ",
            " then search ",
            " aur search ",
            " phir search "
        ]
    
    if any(phrase in command for phrase in task_phrases):
            return "task_request"
    
    if command.startswith(("open ", "kholo ")) and any(
            marker in f" {command} " for marker in multi_step_markers
        ):
            return "task_request"

    # ================= CLOSE =================

    if command.startswith(("close ", "band ")):
        if "chrome" in command:
            return "close_chrome"
        if "spotify" in command:
            return "close_spotify"
        if "youtube" in command:
            return "close_youtube"
        if "whatsapp" in command:
            return "close_whatsapp"
        if "instagram" in command:
            return "close_instagram"
        if "capcut" in command or "cap cut" in command:
            return "close_capcut"
        if "word" in command:
            return "close_word"
        if "excel" in command:
            return "close_excel"
        if "powerpoint" in command or "power point" in command:
            return "close_powerpoint"
        if "vs code" in command:
            return "close_vs_code"
        if "gmail" in command:
            return "close_gmail"
        if "microsoft store" in command or "store" in command:
            return "close_microsoft_store"
        if "tab" in command:
            return "close_tab"

        return None

    # ================= OPEN =================

    if command.startswith(("open ", "kholo ")):
        if "chrome" in command:
            return "open_chrome"
        if "spotify" in command:
            return "open_spotify"
        if "youtube" in command:
            return "open_youtube"
        if "google" in command:
            return "open_google"
        if "whatsapp" in command:
            return "open_whatsapp"
        if "instagram" in command:
            return "open_instagram"
        if "capcut" in command or "cap cut" in command:
            return "open_capcut"
        if "word" in command:
            return "open_word"
        if "excel" in command:
            return "open_excel"
        if "powerpoint" in command or "power point" in command:
            return "open_powerpoint"
        if "vs code" in command:
            return "open_vs_code"
        if "edge" in command:
            return "open_edge"
        if "gmail" in command:
            return "open_gmail"
        if "microsoft store" in command or command == "open store":
            return "open_microsoft_store"

        return None
    # Remove Jarvis word
    command = command.replace("jarvis", "").strip()

    # Remove extra spaces
    command = " ".join(command.split())


    intents = {


        # ================= APPS ================= #

        "open_chrome": [
            "open chrome",
            "chrome kholo",
            "chrome open karo",
            "chrome chalao",
            "browser kholo",
            "internet kholo"
        ],


        "open_youtube": [
            "open youtube",
            "youtube kholo",
            "youtube chalao"
        ],


        "open_google": [
            "open google",
            "google kholo"
        ],


        "open_spotify": [
            "open spotify",
            "spotify kholo",
            "spotify open karo",
            "spotify chala do",
            "music chalao",
            "gaane chalao",
            "song chalao",
            "mujhe music sunna hai"
        ],


        "open_whatsapp": [
            "open whatsapp",
            "whatsapp kholo",
            "whatsapp open karo"
        ],


        "open_instagram": [
            "open instagram",
            "instagram kholo",
            "instagram open karo"
        ],


        "open_capcut": [
            "open capcut",
            "open cap cut",
            "capcut kholo",
            "cap cut kholo",
            "video editor kholo"
        ],


        "open_word": [
            "open word",
            "word kholo",
            "microsoft word kholo"
        ],


        "open_excel": [
            "open excel",
            "excel kholo",
            "microsoft excel kholo"
        ],


        "open_powerpoint": [
            "open powerpoint",
            "open power point",
            "powerpoint kholo"
        ],


        "open_vs_code": [
            "open vs code",
            "vs code kholo",
            "code kholo"
        ],


        "open_edge": [
    "open microsoft edge",
    "edge kholo",
    "edge open karo"
],

        "open_gmail": [
            "open gmail",
            "gmail kholo"
        ],
        "open_microsoft_store": [
            "open microsoft store",
            "microsoft store kholo",
            "open store",
            "store kholo"
        ],
        
      
         "close_chrome": [
         "close chrome",
         "chrome band karo",
          "chrome close karo"
        ],

"close_spotify": [
    "close spotify",
    "spotify band karo",
    "spotify close karo"
],

"close_whatsapp": [
    "close whatsapp",
    "whatsapp band karo",
    "whatsapp close karo"
],

"close_instagram": [
    "close instagram",
    "instagram band karo"
],

"close_capcut": [
    "close capcut",
    "capcut band karo",
    "cap cut close karo"
],

"close_word": [
    "close word",
    "word band karo"
],

"close_excel": [
    "close excel",
    "excel band karo"
],

"close_powerpoint": [
    "close powerpoint",
    "powerpoint band karo"
],
"close_vs_code": [
    "close vs code",
    "vs code band karo"
],
"close_gmail": [
    "close gmail",
    "gmail band karo"
],
      "close_microsoft_store": [
       "close microsoft store",
      "close store",
       "microsoft store close",
         "microsoft store band karo",
        "store band karo"
        ],


        # ================= BROWSER ================= #

        "new_tab": [
            "new tab",
            "naya tab kholo"
        ],


        "close_tab": [
            "close tab",
            "tab band karo"
        ],


        "refresh": [
            "refresh",
            "page refresh karo"
        ],


        "back": [
            "back",
            "peeche jao"
        ],



        # ================= MEDIA ================= #


        "volume_up": [
            "volume up",
            "increase volume",
            "volume badhao",
            "awaaz badhao",
            "awaaz tej karo",
            "sound badhao"
        ],


        "volume_down": [
            "volume down",
            "decrease volume",
            "volume kam karo",
            "awaaz kam karo",
            "awaaz dheemi karo"
        ],


        "mute": [
            "mute",
            "volume mute",
            "sound mute"
        ],


        "play_pause": [
            "play",
            "pause",
            "play pause"
        ],


        "next_song": [
            "next song",
            "agla gana"
        ],


        "previous_song": [
            "previous song",
            "pichla gana"
        ],



        # ================= FILE ================= #

        "open_downloads": [
            "open downloads",
            "downloads kholo"
        ],


        "open_desktop": [
            "open desktop",
            "desktop kholo"
        ],


        "open_documents": [
            "open documents",
            "documents kholo"
        ],



        # ================= SYSTEM ================= #


        "battery": [
            "battery",
            "battery percentage"
        ],


        "time": [
            "time",
            "samay kya hua"
        ],


        "date": [
            "date",
            "aaj ki date"
        ],



        # ================= MEMORY ================= #


        "save_name": [
            "my name is",
            "mera naam hai"
        ],


        "get_name": [
            "what is my name",
            "mera naam kya hai"
        ],



        # ================= SEARCH ================= #
        "ai_question": [

    # English
    "what is",
    "what are",
    "who is",
    "who was",
    "tell me about",
    "explain",
    "how does",
    "how do",
    "why",
    "define",

    # Hindi
    "kaun hai",
    "kaun tha",
    "kya hai",
    "kya tha",
    "batao",
    "samjhao",
    "ke bare me",
    "ke baare mein",
    "kisne",
    "kyun",
    "kaise"

],
        "youtube_search": [
            "search youtube",
            "youtube search",
            "youtube par",
            "youtube pe"
        ],


        "search": [
              "search for",
              "search google",
             "google search",
             "dhundo",
             "find karo"
             ],


        
    }
         
    # ================= AI QUESTION SMART CHECK ================= #
    
    ai_words = [
        "kaun",
        "kya",
        "kyun",
        "kaise",
        "batao",
        "tha",
        "hai",
        "who",
        "what",
        "why",
        "how",
        "explain"
    ]


    if any(word in command.split() for word in ai_words):

        return "ai_question"




    # ================= MATCHING SYSTEM ================= #

    # 1) Exact Match (sabse pehle)
    for intent, phrases in intents.items():

        for phrase in phrases:

            if command == phrase:
                return intent



    # 2) Longest Phrase Contains Match
    # bada phrase pehle check hoga

    all_phrases = []

    for intent, phrases in intents.items():

        for phrase in phrases:

            all_phrases.append(
                (phrase, intent)
            )


    all_phrases.sort(
        key=lambda x: len(x[0]),
        reverse=True
    )


    for phrase, intent in all_phrases:

        if phrase in command:

            return intent



       # ================= FUZZY MATCH ================= #

    # Bahut chhote command ko fuzzy se match mat karo
    if len(command.split()) < 2:
        return None


    best_intent = None
    best_score = 0


    for intent, phrases in intents.items():

        for phrase in phrases:

            score = difflib.SequenceMatcher(
                None,
                command,
                phrase
            ).ratio()


            if score > best_score:

                best_score = score
                best_intent = intent



    # Confidence check

    if best_score >= 0.75:

        print(
            "Fuzzy Match:",
            best_intent,
            best_score
        )

        return best_intent



    return None
