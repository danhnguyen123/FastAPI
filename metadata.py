app_description = """
Chimichang App API helps you do awesome stuff. 🚀
Root Domain:
* **Dev** http://122.248.233.230:8001
* **Prod** https://api-bi.finan.me
"""
contact_metadata={
    "name": "Danh Nguyen",
    "email": "nguyenthedanh34@gmail.com",
}

tags_metadata = [
    {
        "name": "public-webhook",
        "description": "Operations with users. The **login** logic is also here.",
    },
    {
        "name": "Internal-traffic",
        "description": "Manage items. So _fancy_ they have their own docs.",
        "externalDocs": {
            "description": "Items external docs",
            "url": "https://fastapi.tiangolo.com/",
        },
    },
    {
        "name": "Internal-chat",
        "description": "Chat bot base on Botpress",
        "externalDocs": {
            "description": "Items external docs",
            "url": "https://bi.finan.me",
        },
    },
    {
        "name": "root",
        "description": "Root",
    },

]
