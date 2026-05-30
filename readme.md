People circulate fake circulars pretending to be from government, Others generate fake certification/marksheet to get a job, but Uphold eliminates this, the document is signed and hashed so employers or citizens know that the document given to them was fake/tempered or it was from a real authority.

How it works
government/company/user can upload the document which is then hashed and signed with a private key, it stores that proof and then anyone else can upload the document again to check its authenticity to check if it was the same document which was meant to be shared.

-----------------------
---------------
HOW to run
1. go to [https://uphold-navy.vercel.app/admin.html](https://uphold-navy.vercel.app/admin.html)

2. upload the document

3. then you can go to verify page at    [https://uphold-navy.vercel.app/verify.html](https://uphold-navy.vercel.app/verify.html)

4. in the certify page[https://uphold-navy.vercel.app/admin.html] there is also a new AI summerizer that uses qwen-32b model through HACKCLUB AI API

5. new feature!! using which you can verify using the hash in url only example: http://https://uphold-navy.vercel.app/verify.html?hash={your-hash}
----------
Video Demo: https://drive.google.com/file/d/1qWGsIpyeYP5Vk9YtRFhw7CCVt7XC2oUY/view?usp=sharing

----------
----------
HOW To run locally
1. clone the repo
2. run `.\venv\Scripts\activate`
3. install requirements `pip install -r requirements.txt`
4. run `python generate_keys.py`
5. run `python -m uvicorn main:app --reload --port 8000`
6. go to [http://[IP_ADDRESS]/admin.html]

-----
-----
AI Usage
ai was used to deploy to vercel, because code was working locally and it was also used to fix some small problems while learning the concept

Submission for Hackclub The game :)