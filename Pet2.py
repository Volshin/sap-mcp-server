import requests
from anthropic import Anthropic

# Конфигурация

sap_headers = {
    "APIKey": SAP_API_KEY,
    "Accept": "application/json"
}

client = Anthropic(api_key=CLAUDE_API_KEY)

def get_business_partners(top=10):
    """Получить список бизнес-партнеров из SAP"""
    url = f"{SAP_BASE_URL}/A_BusinessPartner?$top={top}"
    response = requests.get(url, headers=sap_headers)
    
    if response.status_code == 200:
        data = response.json()
        return data['d']['results']
    return []

def ask_claude_about_sap_data(question, sap_data):
    """Отправить вопрос Claude с данными SAP"""
    
    # Форматируем SAP данные для Claude
    context = "SAP Business Partners data:\n"
    for bp in sap_data:
        context += f"- ID: {bp['BusinessPartner']}, Name: {bp.get('BusinessPartnerFullName', 'N/A')}\n"
    
    # Запрос к Claude
    message = client.messages.create(
        model="claude-sonnet-4-20250514",
        max_tokens=1024,
        messages=[{
            "role": "user",
            "content": f"{context}\n\nQuestion: {question}"
        }]
    )
    
    return message.content[0].text

# Главная функция
def main():
    print("🤖 SAP AI Assistant\n")
    
    # Получаем данные из SAP
    print("📊 Fetching data from SAP...")
    partners = get_business_partners(top=5)
    print(f"✅ Retrieved {len(partners)} business partners\n")
    
    # Задаем вопрос Claude
    question = "How many business partners are there? List their names."
    print(f"❓ Question: {question}\n")
    
    print("🤔 Claude is thinking...\n")
    answer = ask_claude_about_sap_data(question, partners)
    
    print("💡 Answer:")
    print(answer)

if __name__ == "__main__":
    main()