from speak import speak
from apps import open_app, close_app
from intent import detect_intent
from entity import extract_query
from task_manager import process_task

import browser
import media
import utility
import filemanager
import system
import memory
import calculator
import webbrowser
import urllib.parse
import website
import context
import learning
import conversation_memory

import ai_brain
import weather
import news

def brain(command):

    command = command.lower().strip()
    print(f"Brain received: {command}")

    intent = detect_intent(command)
    print("Detected Intent:", intent)

   # ---------------- MEMORY SYSTEM ---------------- #

    if "my name is" in command:

        name = command.replace("my name is", "").strip()

        if name:
            memory.remember("name", name)
            speak(f"Okay, I will remember your name as {name}")

        else:
            speak("Please tell me your name")


    elif "what is my name" in command or "what's my name" in command:

        name = memory.recall("name")

        if name:
            speak(f"Your name is {name}")

        else:
            speak("I don't know your name yet")
            
            
    # ---------------- LEARNING SYSTEM ---------------- #

    elif "learn" in command:

        data = command.replace("learn", "").strip()

        if "to" in data:

            cmd, action = data.split("to", 1)

            cmd = cmd.strip()
            action = action.strip()

            learning.save_command(
                cmd,
                action
            )

            speak(
                f"I learned {cmd}"
            )

        else:

            speak(
                "Say: learn command to action"
            )
   

    elif "what do i like" in command:

        like = conversation_memory.recall("like")

        if like:
            speak(f"You like {like}")
        else:
            speak("I don't know yet")
    
    elif "i like" in command:

        thing = command.replace(
            "i like",
             ""
            ).strip()
        if thing:

            conversation_memory.remember(
                "like",
                thing
            )

            speak(
                f"I will remember that you like {thing}"
            )
        else:
            speak("Please tell me what you like")


            
    # ----------- FAVOURITE BROWSER MEMORY ----------- #

    elif "my favourite browser is" in command:

        browser_name = command.replace(
            "my favourite browser is",
            ""
        ).strip()

        if browser_name:

            memory.remember(
                "favourite_browser",
                browser_name
            )

            speak(
                f"Okay, I will remember your favourite browser as {browser_name}"
            )

        else:

            speak("Please tell me your favourite browser")



    elif "what is my favourite browser" in command:

        browser_name = memory.recall(
            "favourite_browser"
        )

        if browser_name:

            speak(
                f"Your favourite browser is {browser_name}"
            )

        else:

            speak(
                "I don't know your favourite browser yet"
            )



    # ---------------- OPEN APPS ---------------- #

    elif intent == "open_chrome":

       speak("Opening Chrome")
       open_app("chrome")
       return True
    elif intent == "open_youtube":

        speak("Opening YouTube")

        browser.open_youtube()

        context.set_context("website", "youtube")

        print("Context Saved:", context.get_context("website"))
        return True

    
    elif intent == "open_google":

        speak("Opening Google")
        browser.open_google()
        return True
        
   
        
    elif intent == "open_github":

        speak("Opening GitHub")
        website.open_website("github")
        return True
        
    elif intent == "open_spotify":
        speak("Opening Spotify")
        open_app("spotify")
        return True
        
    elif intent == "open_whatsapp":

       speak("Opening WhatsApp")

       open_app("whatsapp")
       return True



    elif intent == "open_instagram":

        speak("Opening Instagram")

        open_app("instagram") 
        return True
    elif intent == "open_microsoft_store":

         speak("Opening Microsoft Store")

         open_app("microsoft store") 
         return True
    elif intent == "open_cap_cut":

         speak("Opening Cap Cut")

         open_app("cap cut")
         return True
    elif intent == "open_word":

         speak("Opening Word")

         open_app(" word")
         return True
    elif intent == "open_excel":

         speak("Opening  Excel")

         open_app("excel")
         return True
    elif intent == "open_powerpoint":

         speak("Opening PowerPoint")

         open_app("powerpoint") 
         return True  
    elif intent == "open_vs_code":

         speak("Opening VS Code")

         open_app("vs code")
         return True
    elif intent == "open_microsoft_edge":
        
         speak("Opening Microsoft Edge")

         open_app("microsoft edge")
         return True
    elif intent == "open_gmail":

         speak("Opening Gmail")

         website.open_website("gmail")   
         return True    
  # ================= CLOSE APPS ================= #

    elif intent == "close_chrome":

       speak("Closing Chrome")
       close_app("chrome")
       return True


    elif intent == "close_spotify":

        speak("Closing Spotify")
        close_app("spotify")
        return True

    elif intent == "close_whatsapp":

        speak("Closing WhatsApp")
        close_app("whatsapp")
        return True


    elif intent == "close_instagram":

        speak("Closing Instagram")
        close_app("instagram")
        return True


    elif intent == "close_capcut":

         speak("Closing CapCut")
         close_app("capcut")
         return True
         


    elif intent == "close_word":

        speak("Closing Word")
        close_app("word")
        return True


    elif intent == "close_excel":

        speak("Closing Excel")
        close_app("excel")
        return True


    elif intent == "close_powerpoint":

       speak("Closing PowerPoint")
       close_app("powerpoint")
       return True
    elif intent == "close_vs_code": 
           
        speak("Closing VS Code")
        close_app("vs code") 
        return True
    elif intent == "close_microsoft_edge":
        speak("Closing Microsoft Edge")
        close_app("microsoft edge")
        return True
    elif intent == "close_gmail":
        speak("Closing Gmail")
        close_app("gmail")  
        return True
    elif intent ==   "close_microsoft_store":
        speak("Closing Microsoft Store")
        close_app("microsoft store")
        return True
    elif intent == "close_downloads":

         speak("Closing Downloads")

           # optional: downloads folder close
         close_app("downloads")
         return True
        
       
    # ---------------- WEBSITE ---------------- #

    

    elif "open youtube" in command or "youtube kholo" in command:
        speak("Opening YouTube")
        website.open_website("youtube")
        return True

    elif "open github" in command:
        speak("Opening GitHub")
        website.open_website("github")
        return True
        
        
    # ---------------- BROWSER ---------------- #

    elif intent == "new_tab":

        browser.new_tab()
        return True


    elif intent == "close_tab":

        browser.close_tab()
        return True


    elif intent == "refresh":

        browser.refresh_page()
        return True

    elif intent == "back":

        browser.go_back()
        return True


    elif intent == "forward":

        browser.go_forward()
        return True



    # ---------------- MEDIA ---------------- #

    elif intent == "volume_up":

        speak("Volume up")
        media.volume_up()
        return True


    elif intent == "volume_down":

        speak("Volume down")
        media.volume_down()
        return True


    elif intent == "mute":

        speak("Muting volume")

        media.mute()
        return True



    elif intent == "play_pause":

        media.play_pause()
        return True



    elif intent == "next_song":

        media.next_song()
        return True


    elif intent == "previous_song":

        media.previous_song()
        return True


    # ---------------- FILE MANAGER ---------------- #

    elif intent == "open_downloads":

        filemanager.open_downloads()
        return True



    elif intent == "open_desktop":

        filemanager.open_desktop()
        return True



    elif intent == "open_documents":

        filemanager.open_documents()
        return True



    elif intent == "open_pictures":

        filemanager.open_pictures()
        return True



    elif intent == "open_music":

        filemanager.open_music()
        return True



    elif intent == "open_videos":

        filemanager.open_videos()
        return True



    elif intent == "open_recycle_bin":

        filemanager.open_recycle_bin()
        return True
    



    # ---------------- UTILITY ---------------- #

    elif "screenshot" in command:

        utility.take_screenshot()
        return True



    elif "copy" in command:

        utility.copy()
        return True


    elif "paste" in command:

        utility.paste()
        return True



    elif "undo" in command:

        utility.undo()
        return True


    elif "redo" in command:

        utility.redo()
        return True



            # ---------------- WINDOWS LOCATIONS ---------------- #

    elif "open this pc" in command:
        speak("Opening This PC")
        filemanager.open_this_pc()
        return True

    elif "open recycle bin" in command:
        speak("Opening Recycle Bin")
        filemanager.open_recycle_bin()
        return True

    elif "open settings" in command:
        speak("Opening Settings")
        filemanager.open_settings()
        return True

    elif "open control panel" in command:
        speak("Opening Control Panel")
        filemanager.open_control_panel()
        return True

    elif "open task manager" in command:
        speak("Opening Task Manager")
        filemanager.open_task_manager()
        return True

    elif "open temp" in command:
        speak("Opening Temp Folder")
        filemanager.open_temp()
        return True

    elif "open run" in command:
        speak("Opening Run")
        filemanager.open_run()
        return True


    
    # ---------------- SYSTEM ---------------- #
       # -------- CLOSE APPS -------- #

    elif command.startswith("close "):

        app_name = command.replace("close ", "", 1).strip()

        success = close_app(app_name)

        if success:
            speak(f"Closing {app_name}")
        else:
            speak(f"Could not close {app_name}")

        return True



    elif "time" in command:

        speak(system.get_time())
        return True



    elif "date" in command:

        speak(system.get_date())
        return True



    elif "battery" in command:

        battery = system.battery_percentage()
        speak(f"Battery is {battery} percent")
        return True



    elif "calculator" in command:

        system.open_calculator()
        speak("Opening Calculator")
        return True
    


    elif "notepad" in command:

          speak("Opening Notepad")
          system.open_notepad()
          return True

# -------- WEATHER -------- #

    elif "weather" in command:

        city = ""


        if "in " in command:

            city = command.split("in ")[1].strip()


        elif command.startswith("weather "):

            city = command.replace(
                "weather",
                ""
            ).strip()


        result = weather.get_weather(city)

        speak(result)
        return True
    # -------- NEWS -------- #

    elif "news" in command or "khabar" in command:

        query = "India"

        if "news" in command:

            query = command.replace(
                "latest news",
                ""
            ).strip()

        if query == "":

            query = "India"



            
        result = news.get_news(query)


        speak(result)
        return True
      

    # ---------------- SEARCH ---------------- #
    
    
    
    elif intent == "youtube_search":

        query = extract_query(command)

        if query:
            speak(f"Searching YouTube for {query}")
            browser.youtube_search(query)

        else:
            speak("What should I search on YouTube?")
            


    elif intent == "search":

        query = extract_query(command)
        
        print("Search Query:", query)
        print("Current Context:", context.get_context("website"))
        
        if query:

            current_site = context.get_context("website")

            print("Current Context:", current_site)


            if current_site == "youtube":

                speak(f"Searching YouTube for {query}")
                browser.youtube_search(query)

            else:

                speak(f"Searching Google for {query}")
                browser.google_search(query)

        else:
            speak("What should I search?")
    # ---------------- GREETING ---------------- #
    elif "hello" in command.split() or "hi" in command.split():

        name = memory.recall("name")

        if name:
            speak(f"Hello {name}, how can I help you")

        else:
            speak("Hello Sahil, how can I help you")
        
    # ---------------- AI QUESTION ---------------- #

    elif command == "close":

        speak("Which app should I close?")
        return True
        # ---------------- TASK MANAGER ---------------- #

    elif intent == "task_request":

        speak("I am preparing your task.")

        result = process_task(command)

        status = result.get("status", "UNKNOWN")

        if status == "VERIFIED":
            speak("Task completed and verified.")

        elif status == "NEEDS_VERIFICATION":
            speak("Task actions were requested. Please check the screen.")

        elif status == "CANCELLED":
            speak("Task cancelled.")

        elif status == "BLOCKED":
            speak("This task was blocked by safety checks.")

        else:
            speak("I could not complete the task.")

        return True
    
    elif intent == "ai_question":

          print("Sending to AI Brain:", command)

          handled = ai_brain.ai_answer(command)

          if not handled:

           speak("I don't know this yet")

          return

  # ---------------- CALCULATOR ---------------- #

    elif (
    command.startswith("calculate")
    or command.startswith("what is")
    or any(word in command for word in [
        "plus",
        "minus",
        "multiply",
        "times",
        "divide",
        "square"
    ])
    and any(char.isdigit() for char in command)
):
        result = calculator.calculate(command)

        if result is not None:
            speak(f"Answer is {result}")
        else:
            speak("I cannot calculate this")



    # ---------------- EXIT ---------------- #

    elif "exit" in command or "stop" in command:

        speak("Goodbye Sahil")
        exit()



    else:

    # Second chance intent check
      retry_intent = detect_intent(command)

      if retry_intent:

        print("Retry Intent:", retry_intent)

        intent = retry_intent


    learned_action = learning.get_command(command)

    if learned_action:

        speak("Executing learned command")

        if "open spotify" in learned_action:
            open_app("spotify")

        elif "open chrome" in learned_action:
            open_app("chrome")

        elif "open whatsapp" in learned_action:
            open_app("whatsapp")

        elif "open instagram" in learned_action:
            open_app("instagram")

        else:
            speak(
                "I learned it but action is not available yet"
            )

    else:

        handled = ai_brain.ai_answer(command)

        if not handled:

            speak("Searching Google")
            browser.google_search(command)