"""SAP API Client - handles all SAP API requests"""
import requests
from typing import List, Dict, Optional


class SAPClient:
    def __init__(self, api_key: str, base_url: str):
        self.api_key = api_key
        self.base_url = base_url
        self.headers = {
            "APIKey": api_key,
            "Accept": "application/json"
        }
    
    def get_business_partners(self, limit: int = 10) -> List[Dict]:
        """Get list of business partners from SAP"""
        url = f"{self.base_url}/A_BusinessPartner?$top={limit}"
        
        try:
            response = requests.get(url, headers=self.headers, timeout=10)
            response.raise_for_status()
            
            data = response.json()
            partners = data.get('d', {}).get('results', [])
            
            # Format response
            return [{
                'id': p.get('BusinessPartner'),
                'name': p.get('BusinessPartnerFullName', 'N/A'),
                'category': p.get('BusinessPartnerCategory', 'N/A')
            } for p in partners]
            
        except requests.exceptions.RequestException as e:
            return {'error': str(e)}
    
    def search_partner(self, partner_id: str) -> Optional[Dict]:
        """Search for specific business partner by ID"""
        url = f"{self.base_url}/A_BusinessPartner('{partner_id}')"
        
        try:
            response = requests.get(url, headers=self.headers, timeout=10)
            response.raise_for_status()
            
            data = response.json()
            partner = data.get('d', {})
            
            return {
                'id': partner.get('BusinessPartner'),
                'name': partner.get('BusinessPartnerFullName', 'N/A'),
                'category': partner.get('BusinessPartnerCategory', 'N/A'),
                'search_term': partner.get('SearchTerm1', 'N/A')
            }
            
        except requests.exceptions.RequestException as e:
            return {'error': str(e)}
        