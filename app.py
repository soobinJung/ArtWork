import streamlit as st
import requests

# 🔍 MET API를 이용한 검색 함수
def search_artworks(query):
    url = "https://collectionapi.metmuseum.org/public/collection/v1/search"
    params = {"q": query}
    response = requests.get(url, params=params)
    data = response.json()  # ✅ JSON 응답 저장

    object_ids = data.get("objectIDs")
    if not object_ids:
        return []
    return object_ids[:10]

# 📄 작품 ID를 이용한 상세정보 요청 함수
def get_artwork_details(object_id):
    url = f"https://collectionapi.metmuseum.org/public/collection/v1/objects/{object_id}"
    return requests.get(url).json()

# 🎨 Streamlit 웹앱 시작
st.set_page_config(page_title="MET Art Explorer", page_icon="🎨", layout="centered")
st.title("🎨 Explore Artworks with MET Museum API")
st.markdown("Search and view artworks from the Metropolitan Museum of Art collection.")

# 🔎 사용자 입력 받기
query = st.text_input("Enter a keyword to search artworks (e.g., Monet, sculpture, Japan):")

# 🔄 검색어가 있을 때만 동작
if query:
    with st.spinner("Searching artworks..."):
        ids = search_artworks(query)

    if not ids:
        st.warning("No artworks found. Try a different keyword.")
    else:
        for object_id in ids:
            data = get_artwork_details(object_id)

            # 🎨 작품 제목
            st.subheader(data.get("title", "Untitled"))

            # 🖼️ 썸네일 이미지
            image_url = data.get("primaryImageSmall")
            if image_url:
                st.image(image_url, width=300)
            else:
                st.text("No image available.")

            # 👨‍🎨 작가 및 정보
            st.markdown(f"**Artist:** {data.get('artistDisplayName', 'Unknown')}")
            st.markdown(f"**Date:** {data.get('objectDate', 'N/A')}")
            st.markdown(f"**Medium:** {data.get('medium', 'N/A')}")
            st.markdown(f"[🔗 View on MET website]({data.get('objectURL', '#')})")

            st.markdown("---")
