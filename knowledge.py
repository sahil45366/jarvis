knowledge = {

    "what is java":
    "Java is a high level programming language used for software development, Android applications and enterprise systems.",


    "what is python":
    "Python is a programming language used for automation, artificial intelligence, web development and data science.",


    "what is c++":
    "C plus plus is a programming language used for system software, games and competitive programming.",


    "what is machine learning":
    "Machine learning is a branch of artificial intelligence where computers learn from data."

}



conversation = {

    "hello":
    "Hello Sahil, kaise ho?",


    "hi":
    "Hi Sahil, batao kya help chahiye?",


    "kaise ho":
    "Main bilkul theek hu Sahil.",


    "kya haal hai":
    "Main badhiya hu Sahil, tum batao.",


    "tum kaun ho":
    "Main Jarvis hu, tumhara personal AI assistant.",


    "what are you":
    "I am Jarvis, your personal AI assistant.",


    "tum kya kar sakte ho":
    "Main apps open kar sakta hu, search kar sakta hu, calculation kar sakta hu aur tumhari help kar sakta hu.",


    "thank you":
    "Welcome Sahil, hamesha help ke liye ready hu."
    ,

    "kaun ho tum":
    "Main Jarvis hu Sahil.",


"samjhao":
"Bilkul Sahil, main explain karta hu.",


"mujhe nahi samajh aaya":
"Koi baat nahi Sahil, main simple language me samjhata hu."

}



def get_answer(command):

    command = command.lower().strip()


    # Conversation check

    for key, value in conversation.items():

        if key in command:

            return value



    # Knowledge check

    for key, value in knowledge.items():

        if key in command:

            return value



    return None