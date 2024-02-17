css ="""
    <style>
        /* User Chat Message */

        .st-emotion-cache-janbn0 {
            background-color: #2b313e;
        }

        /* AI Chat Message */
    
        .st-emotion-cache-4oy321 {
            background-color: #475063;
        }

        section[data-testid="stSidebar"] {
            width: 380px !important;
        }
    </style>
    """

def get_avatar(sender_type):
    if sender_type == "human":
        return "chat_icons/user_image.png"
    else:
       return "chat_icons/bot_image.png"