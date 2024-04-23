package com.ctf.ezjava;

import com.ctf.ezjava.tools.CookieManager;
import com.ctf.ezjava.tools.UserCredentials;

import javax.servlet.annotation.WebServlet;
import javax.servlet.http.Cookie;
import javax.servlet.http.HttpServlet;
import javax.servlet.http.HttpServletRequest;
import javax.servlet.http.HttpServletResponse;
import java.io.IOException;

@WebServlet(name="CheckServlet", urlPatterns="/check")
public class CheckServlet extends HttpServlet {
    @Override
    public void doGet(HttpServletRequest request, HttpServletResponse response) throws IOException {
        request.setCharacterEncoding("UTF-8");
        response.setCharacterEncoding("UTF-8");
        response.setContentType("text/html");

        Cookie[] cookies = request.getCookies();
        if (cookies != null) {
            for (Cookie cookie : cookies) {
                if ("token".equals(cookie.getName())) {
                    String token = cookie.getValue();
                    if (token != null) {
                        try {
                            UserCredentials userCredentials = CookieManager.parseCookie(token);
                            if (userCredentials != null) {
                                response.getWriter().write("<html><head><title>Check</title></head><body>");
                                response.getWriter().write("<h1>Check</h1>");
                                response.getWriter().write("<p>Hi " + userCredentials.username + ", you are logged in!</p>");
                                response.getWriter().write("</body></html>");
                                return;
                            }
                        } catch (Exception e) {
                            e.printStackTrace();
                        }
                    }
                }
            }
        }
        response.getWriter().write("<html><head><title>Check</title></head><body>");
        response.getWriter().write("<h1>Check</h1>");
        response.getWriter().write("<p>You are not logged in!</p>");
        response.getWriter().write("<a href=\"/login\">Login</a>");
        response.getWriter().write("</body></html>");
    }

    @Override
    public void doPost(HttpServletRequest request, HttpServletResponse response) throws IOException {
        doGet(request, response);
    }
}
