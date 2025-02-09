from requests_html import HTML
from requests_html import HTMLSession
import random
import requests
from bs4 import BeautifulSoup
from bs4.element import Comment

class HtmlScrapper:
    def __init__(self):
        pass
        
    def _get_source(self, url):
        user_agent_list = [
                'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/93.0.4577.82 Safari/537.36',
                'Mozilla/5.0 (iPhone; CPU iPhone OS 14_4_2 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0.3 Mobile/15E148 Safari/604.1',                
                'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.141 Safari/537.36 Edg/87.0.664.75',
                'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.102 Safari/537.36 Edge/18.18363',
            ]
        headers={"User-Agent": random.choice(user_agent_list)}

        try:            
            with HTMLSession() as session:                
                response = session.get(url, headers=headers)            
                return response

        except requests.exceptions.RequestException as e:
            print(e)
            return None
    
    def text_from_html(self, url):
        body = self._get_source(url)
        if body and body.html:
            visible_text =  self._text_from_html(body.html.html,  self._tag_visible)
            return u" ".join(t.strip() for t in visible_text)
        return ""

    
    def links_from_html(self, url):
        body =  self._get_source(url)
        if body and body.html:
            links =  self._text_from_html(body.html.html,  self._tag_a_link)
            return list(links)
        return []

    def _text_from_html(self, body, function):
        soup = BeautifulSoup(body, 'html.parser')
        texts = soup.find_all(string=True)        
        return filter(function, texts)

    def _tag_visible(self, element):
        if element.parent.name in ['style','script','title','meta','[document]'] or isinstance(element, Comment):
            return False
        
        return True
    
    def _tag_a_link(self, element):
        if element.parent.name in ['a']:
            return True
        return False