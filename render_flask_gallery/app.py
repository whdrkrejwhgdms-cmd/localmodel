from flask import Flask, render_template, abort, request
import math

app = Flask(__name__)

# 예제 이미지 데이터입니다. 나중에 외부 API 데이터로 교체할 수 있습니다.
PHOTOS = [
    {
        "id": 1,
        "title": "푸른 바다",
        "category": "자연",
        "description": "맑고 푸른 바다와 잔잔한 파도를 담은 사진입니다.",
        "image": "https://images.unsplash.com/photo-1507525428034-b723cf961d3e?auto=format&fit=crop&w=1200&q=80",
    },
    {
        "id": 2,
        "title": "산속의 호수",
        "category": "자연",
        "description": "산과 호수가 어우러진 평화로운 풍경입니다.",
        "image": "https://images.unsplash.com/photo-1472396961693-142e6e269027?auto=format&fit=crop&w=1200&q=80",
    },
    {
        "id": 3,
        "title": "도시의 야경",
        "category": "도시",
        "description": "해가 진 뒤 빛나는 도시의 풍경입니다.",
        "image": "https://images.unsplash.com/photo-1519501025264-65ba15a82390?auto=format&fit=crop&w=1200&q=80",
    },
    {
        "id": 4,
        "title": "숲속 산책길",
        "category": "자연",
        "description": "초록빛 나무가 둘러싼 숲길을 따라 걸어 보세요.",
        "image": "https://images.unsplash.com/photo-1441974231531-c6227db76b6e?auto=format&fit=crop&w=1200&q=80",
    },
    {
        "id": 5,
        "title": "따뜻한 커피",
        "category": "일상",
        "description": "여유로운 시간을 위한 커피 한 잔입니다.",
        "image": "https://images.unsplash.com/photo-1495474472287-4d71bcdd2085?auto=format&fit=crop&w=1200&q=80",
    },
    {
        "id": 6,
        "title": "바다 위의 절벽",
        "category": "여행",
        "description": "바다와 절벽이 만드는 웅장한 풍경입니다.",
        "image": "https://images.unsplash.com/photo-1464822759023-fed622ff2c3b?auto=format&fit=crop&w=1200&q=80",
    },
    {
        "id": 7,
        "title": "꽃과 정원",
        "category": "자연",
        "description": "다채로운 색상의 꽃이 피어 있는 정원입니다.",
        "image": "https://images.unsplash.com/photo-1490730141103-6cac27aaab94?auto=format&fit=crop&w=1200&q=80",
    },
    {
        "id": 8,
        "title": "거리의 풍경",
        "category": "도시",
        "description": "여행 중 만나는 활기찬 거리의 모습입니다.",
        "image": "https://images.unsplash.com/photo-1519608487953-e999c86e7455?auto=format&fit=crop&w=1200&q=80",
    },
    {
        "id": 9,
        "title": "눈 덮인 산",
        "category": "여행",
        "description": "하얀 눈으로 덮인 산의 시원한 풍경입니다.",
        "image": "https://images.unsplash.com/photo-1519681393784-d120267933ba?auto=format&fit=crop&w=1200&q=80",
    },
    {
        "id": 10,
        "title": "푸른 들판",
        "category": "자연",
        "description": "넓게 펼쳐진 초록 들판을 바라보는 순간입니다.",
        "image": "https://images.unsplash.com/photo-1500382017468-9049fed747ef?auto=format&fit=crop&w=1200&q=80",
    },
    {
        "id": 11,
        "title": "해변의 노을",
        "category": "여행",
        "description": "해 질 무렵 해변에 내려앉은 따뜻한 빛입니다.",
        "image": "https://images.unsplash.com/photo-1473116763249-2faaef81ccda?auto=format&fit=crop&w=1200&q=80",
    },
    {
        "id": 12,
        "title": "건축과 하늘",
        "category": "도시",
        "description": "도시 건축물과 하늘이 어우러진 장면입니다.",
        "image": "https://images.unsplash.com/photo-1480714378408-67cf0d13bc1b?auto=format&fit=crop&w=1200&q=80",
    },
    {
        "id": 13,
        "title": "작은 폭포",
        "category": "자연",
        "description": "숲속에서 시원하게 흐르는 물을 담았습니다.",
        "image": "https://images.unsplash.com/photo-1432405972618-c60b0225b8f9?auto=format&fit=crop&w=1200&q=80",
    },
    {
        "id": 14,
        "title": "여행 가방",
        "category": "여행",
        "description": "새로운 장소로 떠날 준비를 하는 순간입니다.",
        "image": "https://images.unsplash.com/photo-1553062407-98eeb64c6a62?auto=format&fit=crop&w=1200&q=80",
    },
    {
        "id": 15,
        "title": "책과 휴식",
        "category": "일상",
        "description": "책 한 권과 함께하는 조용한 휴식 시간입니다.",
        "image": "https://images.unsplash.com/photo-1507842217343-583bb7270b66?auto=format&fit=crop&w=1200&q=80",
    },
    {
        "id": 16,
        "title": "호숫가 풍경",
        "category": "자연",
        "description": "호수에 주변 풍경이 잔잔하게 비칩니다.",
        "image": "https://images.unsplash.com/photo-1433086966358-54859d0ed716?auto=format&fit=crop&w=1200&q=80",
    },
    {
        "id": 17,
        "title": "밤의 거리",
        "category": "도시",
        "description": "밤이 찾아온 도시의 불빛을 감상해 보세요.",
        "image": "https://images.unsplash.com/photo-1519608487953-e999c86e7455?auto=format&fit=crop&w=1200&q=80",
    },
    {
        "id": 18,
        "title": "아침의 산",
        "category": "여행",
        "description": "아침 햇살이 산 능선을 부드럽게 비춥니다.",
        "image": "https://images.unsplash.com/photo-1464278533981-50106e6176b1?auto=format&fit=crop&w=1200&q=80",
    },
    {
        "id": 19,
        "title": "식물과 햇살",
        "category": "일상",
        "description": "햇살이 비치는 실내 식물의 싱그러운 모습입니다.",
        "image": "https://images.unsplash.com/photo-1485955900006-10f4d324d411?auto=format&fit=crop&w=1200&q=80",
    },
    {
        "id": 20,
        "title": "잔잔한 파도",
        "category": "자연",
        "description": "해안가에 부드럽게 밀려오는 파도입니다.",
        "image": "https://images.unsplash.com/photo-1505142468610-359e7d316be0?auto=format&fit=crop&w=1200&q=80",
    },
    {
        "id": 21,
        "title": "넓은 사막",
        "category": "여행",
        "description": "모래 언덕이 끝없이 이어지는 사막 풍경입니다.",
        "image": "https://images.unsplash.com/photo-1509316785289-025f5b846b35?auto=format&fit=crop&w=1200&q=80",
    },
    {
        "id": 22,
        "title": "창가의 빛",
        "category": "일상",
        "description": "창문을 통해 들어오는 부드러운 빛을 담았습니다.",
        "image": "https://images.unsplash.com/photo-1449247709967-d4461a6a6103?auto=format&fit=crop&w=1200&q=80",
    },
]

PER_PAGE = 20


@app.route("/")
def home():
    return render_template("about.html", page_title="홈")


@app.route("/gallery")
def gallery():
    page = request.args.get("page", 1, type=int)
    page = max(page, 1)
    total_pages = max(1, math.ceil(len(PHOTOS) / PER_PAGE))
    page = min(page, total_pages)

    start = (page - 1) * PER_PAGE
    photos = PHOTOS[start:start + PER_PAGE]

    return render_template(
        "index.html",
        photos=photos,
        page=page,
        total_pages=total_pages,
        page_title="갤러리",
    )


@app.route("/photo/<int:photo_id>")
def photo_detail(photo_id):
    photo = next((item for item in PHOTOS if item["id"] == photo_id), None)
    if photo is None:
        abort(404)
    return render_template("detail.html", photo=photo, page_title=photo["title"])


@app.route("/about")
def about():
    return render_template("about.html", page_title="소개")


@app.errorhandler(404)
def not_found(error):
    return render_template("404.html", page_title="페이지를 찾을 수 없습니다"), 404


if __name__ == "__main__":
    import os
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)), debug=True)
