import streamlit as st
from azure.ai.textanalytics import TextAnalyticsClient
from azure.core.credentials import AzureKeyCredential

# Azureのキーとエンドポイント
key = "AZURE_API_KEY"
endpoint = "AZURE_ENDPOINT"

# クライアント作成
client = TextAnalyticsClient(
    endpoint=endpoint,
    credential=AzureKeyCredential(key)
)

# 初期状態
if "result" not in st.session_state:
    st.session_state.result = {
        "sentiment": "未判定",
        "positive": 0.0,
        "neutral": 0.0,
        "negative": 0.0
    }

st.title("🫧 相談文トーン判定アプリ 🫧")
st.markdown(
    "<div style='margin-top:10px; margin-bottom:25px; color:gray;'>"
    "入力された文章の感情トーンを判定します"
    "</div>",
    unsafe_allow_html=True
)

text = st.text_area("📝 相談文を入力してください👇", height=150)

if st.button("判定する"):
    if text.strip():
        response = client.analyze_sentiment(documents=[text])[0]

        st.session_state.result = {
            "sentiment": response.sentiment,
            "positive": response.confidence_scores.positive,
            "neutral": response.confidence_scores.neutral,
            "negative": response.confidence_scores.negative
        }
    else:
        st.warning("文章を入力してください")

# 表示部分
sentiment_info = {
    "positive": {"label": "ポジティブ", "color": "green"},
    "neutral": {"label": "中立", "color": "orange"},
    "negative": {"label": "ネガティブ", "color": "red"},
    "未判定": {"label": "未判定", "color": "gray"}
}

result = st.session_state.result
info = sentiment_info.get(result["sentiment"], sentiment_info["未判定"])
sentiment_jp = info["label"]
color = info["color"]

st.markdown("---")
st.subheader("📌 全体の判定")
st.markdown(
    f"<h2 style='color:{color}; margin-top:0px;'>{sentiment_jp}</h2>",
    unsafe_allow_html=True
)

st.markdown(
    "<div style='margin-top:20px; margin-bottom:10px; font-size:20px;'>📊 感情スコア</div>",
    unsafe_allow_html=True
)

st.write("😊 ポジティブ")
st.progress(int(result["positive"] * 100))
st.write(f"{result['positive']:.2f}")

st.write("😐 中立")
st.progress(int(result["neutral"] * 100))
st.write(f"{result['neutral']:.2f}")

st.write("😟 ネガティブ")
st.progress(int(result["negative"] * 100))
st.write(f"{result['negative']:.2f}")

if result["sentiment"] == "negative":
    st.warning("不安や困りごとが強い可能性があります。早めの確認が必要かもしれません。")