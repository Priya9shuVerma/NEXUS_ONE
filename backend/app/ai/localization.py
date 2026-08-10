def localized_document_text(
    user_language: str,
    key: str,
    value: str = ""
) -> str:

    templates = {

        # =========================
        # CGPA
        # =========================
        "cgpa": {
            "English":
                f"Your CGPA is **{value} / 10**.",

            "Hinglish":
                f"Aapka CGPA **{value} / 10** hai.",

            "Roman Bhojpuri":
                f"Tohar CGPA **{value} / 10** ba.",

            "Hindi":
                f"आपका CGPA **{value} / 10** है।",

            "Sanskrit":
                f"भवतः CGPA **{value} / 10** अस्ति।",

            "Tamil":
                f"உங்கள் CGPA **{value} / 10** ஆகும்.",

            "Telugu":
                f"మీ CGPA **{value} / 10**.",

            "Kannada":
                f"ನಿಮ್ಮ CGPA **{value} / 10** ಆಗಿದೆ.",

            "Malayalam":
                f"നിങ്ങളുടെ CGPA **{value} / 10** ആണ്.",

            "Bengali":
                f"আপনার CGPA **{value} / 10**।",

            "Marathi":
                f"तुमचा CGPA **{value} / 10** आहे.",

            "Gujarati":
                f"તમારો CGPA **{value} / 10** છે.",

            "Punjabi":
                f"ਤੁਹਾਡਾ CGPA **{value} / 10** ਹੈ।",

            "Japanese":
                f"あなたのCGPAは **{value} / 10** です。",

            "French":
                f"Votre CGPA est de **{value} / 10**.",

            "Spanish":
                f"Tu CGPA es **{value} / 10**.",
        },

        # =========================
        # DSA
        # =========================
        "dsa": {
            "English":
                f"You have solved **{value}+ DSA problems** on LeetCode.",

            "Hinglish":
                f"Aapne LeetCode par **{value}+ DSA problems** solve kiye hain.",

            "Roman Bhojpuri":
                f"Tohar LeetCode par **{value}+ DSA problems** solve bhail ba.",

            "Hindi":
                f"आपने LeetCode पर **{value}+ DSA समस्याएँ** हल की हैं।",

            "Sanskrit":
                f"भवता LeetCode इत्यत्र **{value}+ DSA समस्याः** समाधानिताः।",

            "Tamil":
                f"நீங்கள் LeetCode-ல் **{value}+ DSA பிரச்சினைகளை** தீர்த்துள்ளீர்கள்.",

            "Telugu":
                f"మీరు LeetCodeలో **{value}+ DSA సమస్యలను** పరిష్కరించారు.",

            "Kannada":
                f"ನೀವು LeetCode ನಲ್ಲಿ **{value}+ DSA ಸಮಸ್ಯೆಗಳನ್ನು** ಪರಿಹರಿಸಿದ್ದೀರಿ.",

            "Malayalam":
                f"നിങ്ങൾ LeetCode-ൽ **{value}+ DSA പ്രശ്നങ്ങൾ** പരിഹരിച്ചിട്ടുണ്ട്.",

            "Bengali":
                f"আপনি LeetCode-এ **{value}+ DSA সমস্যা** সমাধান করেছেন।",

            "Marathi":
                f"तुम्ही LeetCode वर **{value}+ DSA समस्या** सोडवल्या आहेत.",

            "Gujarati":
                f"તમે LeetCode પર **{value}+ DSA સમસ્યાઓ** ઉકેલી છે.",

            "Punjabi":
                f"ਤੁਸੀਂ LeetCode ਉੱਤੇ **{value}+ DSA ਸਮੱਸਿਆਵਾਂ** ਹੱਲ ਕੀਤੀਆਂ ਹਨ।",

            "Japanese":
                f"あなたはLeetCodeで **{value}+ 問のDSA問題** を解きました。",

            "French":
                f"Vous avez résolu **{value}+ problèmes de DSA** sur LeetCode.",

            "Spanish":
                f"Has resuelto **{value}+ problemas de DSA** en LeetCode.",
        },

        # =========================
        # UNKNOWN
        # =========================
        # =========================
    # PROJECTS
    # =========================
    "projects": {
        "English":
            "Based on your uploaded document, your projects are:\n\n{value}",

        "Hinglish":
            "Aapke uploaded document ke according, aapke projects hain:\n\n{value}",

        "Roman Bhojpuri":
            "Tohar uploaded document ke hisaab se, tohar projects ee ba:\n\n{value}",

        "Hindi":
            "???? ????? ??? ?? ????????? ?? ??????, ???? ????????? ???:\n\n{value}",

        "Sanskrit":
            "???? ???????-??????????? ??????? ???? ????????? ?????:\n\n{value}",

        "Tamil":
            "??????? ?????????? ????????????, ?????? ??????????:\n\n{value}",

        "Telugu":
            "???? ???????? ????? ????? ???????, ?? ?????????????:\n\n{value}",

        "Kannada":
            "???? ???????? ????? ????? ??????, ????? ??????????????:\n\n{value}",

        "Malayalam":
            "?????? ???????? ????? ??? ???????, ????????? ?????????????:\n\n{value}",

        "Bengali":
            "????? ????? ??? ??? ????????, ????? ??????????? ??:\n\n{value}",

        "Marathi":
            "?????? ????? ???????? ?????????????, ????? ??????? ????:\n\n{value}",

        "Gujarati":
            "??? ????? ????? ???????? ??????, ????? ??????????? ??:\n\n{value}",

        "Punjabi":
            "?????? ????? ???? ???????? ?? ??????, ?????? ???????? ??:\n\n{value}",

        "Japanese":
            "???????????????????????????????????????\n\n{value}",

        "French":
            "D?apr?s votre document t?l?charg?, vos projets sont :\n\n{value}",

        "Spanish":
            "Seg?n el documento que has subido, tus proyectos son:\n\n{value}",
    },

    "unknown": {
            "English":
                "I don't know based on the uploaded document.",

            "Hinglish":
                "Uploaded document mein iski information nahi hai.",

            "Roman Bhojpuri":
                "Uploaded document mein ee jankari na ba.",

            "Hindi":
                "अपलोड किए गए दस्तावेज़ में इसकी जानकारी नहीं है।",

            "Sanskrit":
                "अपलोडिते दस्तावेजे अस्य विषयस्य सूचना नास्ति।",

            "Tamil":
                "பதிவேற்றப்பட்ட ஆவணத்தில் இதற்கான தகவல் இல்லை.",

            "Telugu":
                "అప్‌లోడ్ చేసిన పత్రంలో దీనికి సంబంధించిన సమాచారం లేదు.",

            "Kannada":
                "ಅಪ್‌ಲೋಡ್ ಮಾಡಿದ ದಾಖಲೆಗಳಲ್ಲಿ இதಕ್ಕೆ ಸಂಬಂಧಿಸಿದ ಮಾಹಿತಿ ಇಲ್ಲ.",

            "Malayalam":
                "അപ്‌ലോഡ് ചെയ്ത രേഖയിൽ ഇതിനെക്കുറിച്ചുള്ള വിവരമില്ല.",

            "Bengali":
                "আপলোড করা নথিতে এই বিষয়ে কোনো তথ্য নেই।",

            "Marathi":
                "अपलोड केलेल्या दस्तऐवजात याबद्दल माहिती नाही.",

            "Gujarati":
                "અપલોડ કરેલા દસ્તાવેજમાં આ અંગેની માહિતી નથી.",

            "Punjabi":
                "ਅਪਲੋਡ ਕੀਤੇ ਦਸਤਾਵੇਜ਼ ਵਿੱਚ ਇਸ ਬਾਰੇ ਜਾਣਕਾਰੀ ਨਹੀਂ ਹੈ।",

            "Japanese":
                "アップロードされたドキュメントには、この情報がありません。",

            "French":
                "Cette information n'existe pas dans le document téléchargé.",

            "Spanish":
                "Esta información no aparece en el documento cargado.",
        },
    }

    language_table = templates.get(key, {})

    return language_table.get(
        user_language,
        language_table.get("English", value)
    )
