#!/usr/bin/python
#-*- coding: utf-8 -*-

import webapp
import urllib


class shortenApp (webapp.webApp):

    dic_real_url = {}
    dic_url_num = {}
    num = 0

    def parse(self, request):

        verb = request.split(' ', 2)[0]
        res = request.split(' ', 2)[1]
        if verb == "POST":
            body = request.split('\r\n\r\n', 1)[1]
            body = body.split('=')[1].replace('+', ' ')
        else:
            body = ""
        return (verb, res, body)

    def process(self, resourceName):

        (verb, res, body) = resourceName

        form = '<form action="" method="POST">'
        form += 'URL a acortar: <input type="text" name="valor">'
        form += '<input type="submit" value="Enviar">'
        form += '</form>'

        if verb == "GET":
            if res == '/':
                httpCode = "200 OK"
                htmlBody = ("<html><body>" + form + "URL buscadas: "
                            + str(self.dic_real_url.keys()) + "<br>"
                            + "URL acortadas en uso: "
                            + str(self.dic_url_num.keys()) + "</body></html>")
            else:
                try:
                    res = int(res[1:])
                    if res not in self.dic_url_num:
                        httpCode = "404 Not found"
                        htmlBody = ("<html><body>"
                                    + "HTTP Error: Recurso no disponible"
                                    + "</body></html>")
                    else:
                        httpCode = ('301 Redirect\nLocation: '
                                    + "http://localhost:1234"
                                    + str(self.dic_url_num[res]))
                        htmlBody = ("<html><body>" + "<a href="
                                    + "http://localhost:1234"
                                    + str(self.dic_url_num[res]) +
                                    + "</href></br>" + "</body></html>")
                except ValueError:
                    httpCode = "404 Not Found"
                    htmlBody = ("<html><body>" + "Error 404: Not found"
                                + "</body></html>")
        elif verb == "POST":
            url = urllib.unquote(body)
            if not url.startswith("http://") and \
                    not url.startswith("https://"):
                url = "http://" + url
            else:
                url = url.split("%3A%2F%2F")[0]
            if url in self.dic_real_url:
                self.num = self.dic_real_url[url]
            else:
                self.num = len(self.dic_real_url)
                self.dic_real_url[url] = self.num
                self.dic_url_num[self.num] = url

            httpCode = "200 OK"
            htmlBody = ("<html><body>" + "URL buscada: "
                        + "<a href=" + url + ">" + url + "</href></br>"
                        + "URL acortada: " + "<a href=" + str(self.num) + ">"
                        + str(self.num) + "</href></br>" + "</boy></html>")
        return (httpCode, htmlBody)


if __name__ == "__main__":
    testWebApp = shortenApp("localhost", 1234)
