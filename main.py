from time import sleep
from ulauncher.api.client.Extension import Extension
from ulauncher.api.client.EventListener import EventListener
from ulauncher.api.shared.event import KeywordQueryEvent, ItemEnterEvent
from ulauncher.api.shared.item.ExtensionResultItem import ExtensionResultItem
from ulauncher.api.shared.action.RenderResultListAction import RenderResultListAction
from ulauncher.api.shared.action.ExtensionCustomAction import ExtensionCustomAction
from ulauncher.api.shared.action.HideWindowAction import HideWindowAction

import webbrowser

class UrlOpener:
    def open(self, url):
        url = self.complete_url(url)
        webbrowser.open(url)
            
    def complete_url(self, url):
        if url == None:
            return "www.google.com"
        if "https://www." in url:
            pass
        elif "www." in url:
            url = "https://" + url
        else:
            url = "https://www." + url
            
        if len(url.split('.')) == 2: url += '.com'
            
        return url
        
        
url_opener = UrlOpener()


class DemoExtension(Extension):
    def __init__(self):
        super(DemoExtension, self).__init__()
        self.subscribe(KeywordQueryEvent, KeywordQueryEventListener())
        self.subscribe(ItemEnterEvent, ItemEnterEventListener())


class KeywordQueryEventListener(EventListener):
    def on_event(self, event, extension):
        url = [
            ExtensionResultItem(
                icon='images/icon.png',
                name= f"Open in browser",
                description= f"Open url {url_opener.complete_url(event.get_argument())} in {webbrowser.get().name}",
                on_enter=ExtensionCustomAction({"url":event.get_argument()}, keep_app_open=False))
        ]

        return RenderResultListAction(url)


class ItemEnterEventListener(EventListener):
    def on_event(self, event, extension):
        data = event.get_data()
        return RenderResultListAction([ExtensionResultItem(icon='images/icon.png',
                                                           name=data["url"],
                                                           on_enter=url_opener.open(data["url"])
)])


if __name__ == '__main__':
    DemoExtension().run()
