import json
import requests

courses_container = []

headers = {
    "user_agent": 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.149 Safari/537.36',
    "referer":"https://www.udemy.com/courses/search/?src=ukw&q=web+scraping"
}
for i in range(1,2):
    url_api = """https://www.udemy.com/api-2.0/search-courses/?p="""+ str(i) +"""&q=web%20scraping%3Fp%3D2&src=ukw&skip_price=true"""

    response = requests.get(url_api, headers=headers)

    data = response.json()

    courses = data["courses"]

    for course in courses:
        courses_container.append({
            "title": course["title"],
            "rating": course["rating"],
            "reviews": course["num_reviews"],
            "students": course["num_subscribers"],
            "hours of content": course["hrs_of_content_f"],
            "url": "https://www.udemy.com" + course["url"]
        })

out_file = open("courses.json", "w")
json.dump(courses_container, out_file)
out_file.close()

print('Courses saved in reviews.json ;)')
